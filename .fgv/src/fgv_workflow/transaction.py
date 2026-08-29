import hashlib
import json
import os
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import unicodedata
from typing import Callable

from . import CONTRACT_VERSION
from .calendar import build_calendar_intent
from .concepts import ConceptCandidate, should_promote
from .locking import vault_lock
from .naming import clean_topic, lesson_dir
from .plaud import render_artifact, validate_analysis
from .source_store import make_transaction_id, sha256_file
from .subjects import SubjectRegistry
from .tasks import make_task_id


PLAN_KEYS = {
    "schema_version",
    "contract_version",
    "runtime",
    "transaction_id",
    "subject_id",
    "class_date",
    "source_name",
    "source_sha256",
    "analysis_sha256",
    "raw_relpath",
    "manifest_relpath",
    "artifacts",
    "concept_actions",
    "task_actions",
    "calendar_intents",
    "requires_confirmation",
}
RECEIPT_KEYS = {
    "schema_version",
    "contract_version",
    "transaction_id",
    "plan_sha256",
    "plan",
    "started_at",
    "as_of",
    "state",
    "progress",
    "file_hashes",
    "actions",
    "validations",
}
ARTIFACT_KINDS = ("transcrito", "resumo")
SOURCE_SUFFIXES = {".txt", ".md", ".vtt", ".srt"}
TRANSACTION_ROOT = Path("30 Sistema/Estado/workflow-transactions")
CONCEPT_QUEUE = Path("30 Sistema/Estado/concept-candidates.jsonl")
CALENDAR_QUEUE = Path("30 Sistema/Estado/calendar-intents.jsonl")
TASKS_PATH = Path("00 Home/Tasks.md")
CATALOG_PATH = Path("30 Sistema/Estado/catalog.jsonl")
SNAPSHOT_PATH = Path("30 Sistema/Estado/dashboard-snapshot.md")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(payload: object) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def plan_sha256(plan: dict) -> str:
    return sha256_bytes(canonical_json(plan))


def _relative(value: str) -> Path:
    if not isinstance(value, str) or not value or unicodedata.normalize("NFC", value) != value:
        raise ValueError("workflow path must be non-empty NFC text")
    parsed = PurePosixPath(value)
    if parsed.is_absolute() or ".." in parsed.parts or "." in parsed.parts:
        raise ValueError(f"unsafe workflow path: {value}")
    return Path(*parsed.parts)


def _vault_path(vault_root: Path, value: str | Path) -> Path:
    relative = _relative(value.as_posix() if isinstance(value, Path) else value)
    current = vault_root.resolve()
    if not current.is_dir():
        raise ValueError(f"vault root must be a regular directory: {current}")
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise ValueError(f"workflow path contains a symlink: {current}")
    return current


def _planning_path(vault_root: Path, value: str | Path) -> Path:
    if vault_root.exists():
        return _vault_path(vault_root, value)
    return vault_root / _relative(value.as_posix() if isinstance(value, Path) else value)


def _safe_concept_title(value: str) -> str:
    title = " ".join(value.split()).strip(" .")
    if (
        not title
        or len(title) > 100
        or "\n" in title
        or "\r" in title
        or any(character in title for character in '/\\:*?"<>|')
    ):
        raise ValueError(f"unsafe concept title: {value}")
    return title


def _task_id(description: str, due: str, tag: str) -> str:
    return make_task_id(description, due, tag)


def _concept_content(
    title: str,
    subject_id: str,
    transaction_id: str,
) -> bytes:
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    text = (
        "---\n"
        'tipo: "conceito"\n'
        f"materias: [{quote(subject_id)}]\n"
        'status: "inicial"\n'
        "contract_version: 1\n"
        f"transaction_id: {quote(transaction_id)}\n"
        "---\n\n"
        f"# {title}\n\n"
        "## Definição\n\n"
        "// preencher a partir de evidência confirmada\n\n"
        "## Aplicação\n\n"
        "// preencher\n\n"
        "## Pergunta de recuperação\n\n"
        "// preencher\n\n"
        "## Aulas relacionadas\n\n"
        f"- transaction_id: {transaction_id}\n"
    )
    return text.encode("utf-8")


def _existing_receipt(vault_root: Path, transaction_id: str) -> dict | None:
    path = _vault_path(vault_root, TRANSACTION_ROOT / f"{transaction_id}.json")
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"transaction receipt is not a regular file: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != 1
        or payload.get("transaction_id") != transaction_id
        or not isinstance(payload.get("plan"), dict)
        or payload.get("plan_sha256") != plan_sha256(payload["plan"])
    ):
        raise ValueError(f"invalid transaction receipt: {path}")
    validate_plan(payload["plan"])
    validate_receipt(payload)
    return payload


def build_plan(
    *,
    runtime: str,
    vault_root: Path,
    source: Path,
    analysis_path: Path,
    class_date: str,
) -> dict:
    vault_root = vault_root.resolve()
    if runtime not in {"codex", "claude"}:
        raise ValueError(f"unsupported local runtime: {runtime}")
    parsed_date = date.fromisoformat(class_date)
    if parsed_date.isoformat() != class_date:
        raise ValueError("class_date must be canonical YYYY-MM-DD")
    if (
        not source.is_file()
        or source.is_symlink()
        or not analysis_path.is_file()
        or analysis_path.is_symlink()
    ):
        raise ValueError("source and analysis must be regular non-symlink files")
    if source.name != Path(source.name).name or unicodedata.normalize("NFC", source.name) != source.name:
        raise ValueError("source name must be a basename in NFC")
    suffix = source.suffix.lower() or ".txt"
    if suffix not in SOURCE_SUFFIXES:
        raise ValueError(f"unsupported transcript extension: {suffix}")
    analysis_bytes = analysis_path.read_bytes()
    analysis = json.loads(analysis_bytes.decode("utf-8"))
    validate_analysis(analysis)
    registry = SubjectRegistry.load_default()
    subject = registry.resolve(analysis["subject_id"])
    source_sha256 = sha256_file(source)
    transaction_id = make_transaction_id(source_sha256, subject.id, class_date)
    if vault_root.exists() and not vault_root.is_dir():
        raise ValueError(f"vault root is not a directory: {vault_root}")
    prior = _existing_receipt(vault_root, transaction_id) if vault_root.exists() else None
    if prior is not None:
        plan = prior["plan"]
        if (
            plan["source_sha256"] != source_sha256
            or plan["analysis_sha256"] != sha256_bytes(analysis_bytes)
            or plan["runtime"] != runtime
        ):
            raise ValueError("existing transaction uses different authenticated inputs")
        return plan

    lesson = lesson_dir(vault_root, subject, parsed_date)
    lesson_relative = lesson.relative_to(vault_root)
    topic = clean_topic(analysis["topic"])
    raw_relpath = (
        lesson_relative / "Fontes" / f"Plaud - {transaction_id}{suffix}"
    ).as_posix()
    manifest_relpath = (
        lesson_relative / "Fontes" / f"Manifest - {transaction_id}.json"
    ).as_posix()
    artifacts = {
        kind: (
            lesson_relative
            / f"{'Transcrito' if kind == 'transcrito' else 'Resumo'} - {topic}.md"
        ).as_posix()
        for kind in ARTIFACT_KINDS
    }
    for relative in (raw_relpath, manifest_relpath, *artifacts.values()):
        path = _planning_path(vault_root, relative)
        if path.exists():
            raise FileExistsError(f"planned destination already exists: {relative}")

    concept_actions = []
    for raw_candidate in analysis["concept_candidates"]:
        candidate = ConceptCandidate(**raw_candidate)
        title = _safe_concept_title(candidate.title)
        relative = Path("20 Conhecimento/Conceitos") / f"{title}.md"
        path = _planning_path(vault_root, relative)
        if path.exists():
            action = {
                "title": title,
                "action": "link_existing",
                "relpath": relative.as_posix(),
                "expected_sha256": sha256_file(path),
            }
        elif should_promote(candidate):
            content = _concept_content(title, subject.id, transaction_id)
            action = {
                "title": title,
                "action": "create",
                "relpath": relative.as_posix(),
                "content_sha256": sha256_bytes(content),
            }
        else:
            action = {
                "title": title,
                "action": "queue",
                "relpath": CONCEPT_QUEUE.as_posix(),
                "queue_id": hashlib.sha256(
                    f"{transaction_id}\0{title.casefold()}".encode("utf-8")
                ).hexdigest()[:20],
            }
        concept_actions.append(action)

    task_actions = []
    planned_task_ids: set[str] = set()
    for mention in analysis["task_mentions"]:
        task_id = _task_id(mention["description"], mention["due"], subject.task_tag)
        if task_id in planned_task_ids:
            continue
        planned_task_ids.add(task_id)
        task_actions.append(
            {
                "task_id": task_id,
                "description": mention["description"].strip(),
                "due": mention["due"],
                "priority": mention["priority"],
                "tag": subject.task_tag,
                "relpath": TASKS_PATH.as_posix(),
            }
        )
    calendar_intents = []
    planned_calendar_ids: set[str] = set()
    for mention in analysis["calendar_mentions"]:
        intent = asdict(
            build_calendar_intent(
                transaction_id=transaction_id,
                action=mention["action"],
                calendar_alias=mention["calendar_alias"],
                payload=mention["payload"],
            )
        )
        if intent["action_id"] in planned_calendar_ids:
            continue
        planned_calendar_ids.add(intent["action_id"])
        calendar_intents.append(intent)
    plan = {
        "schema_version": 1,
        "contract_version": CONTRACT_VERSION,
        "runtime": runtime,
        "transaction_id": transaction_id,
        "subject_id": subject.id,
        "class_date": class_date,
        "source_name": source.name,
        "source_sha256": source_sha256,
        "analysis_sha256": sha256_bytes(analysis_bytes),
        "raw_relpath": raw_relpath,
        "manifest_relpath": manifest_relpath,
        "artifacts": artifacts,
        "concept_actions": concept_actions,
        "task_actions": task_actions,
        "calendar_intents": calendar_intents,
        "requires_confirmation": any(
            intent["requires_confirmation"] for intent in calendar_intents
        ),
    }
    validate_plan(plan)
    return plan


def validate_plan(plan: dict) -> None:
    if not isinstance(plan, dict) or set(plan) != PLAN_KEYS:
        raise ValueError("ingest plan has a closed-schema mismatch")
    if type(plan["schema_version"]) is not int or plan["schema_version"] != 1:
        raise ValueError("ingest plan schema_version must be integer 1")
    if type(plan["contract_version"]) is not int or plan["contract_version"] != 1:
        raise ValueError("ingest plan contract_version must be integer 1")
    if plan["runtime"] not in {"codex", "claude"}:
        raise ValueError("ingest plan runtime is invalid")
    if not re.fullmatch(r"[0-9a-f]{20}", plan["transaction_id"]):
        raise ValueError("ingest plan transaction_id is invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", plan["source_sha256"]):
        raise ValueError("ingest plan source hash is invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", plan["analysis_sha256"]):
        raise ValueError("ingest plan analysis hash is invalid")
    parsed = date.fromisoformat(plan["class_date"])
    if parsed.isoformat() != plan["class_date"]:
        raise ValueError("ingest plan date is not canonical")
    if Path(plan["source_name"]).name != plan["source_name"]:
        raise ValueError("ingest plan source_name is not a basename")
    if (
        not isinstance(plan["source_name"], str)
        or "\n" in plan["source_name"]
        or "\r" in plan["source_name"]
        or unicodedata.normalize("NFC", plan["source_name"]) != plan["source_name"]
    ):
        raise ValueError("ingest plan source_name is invalid")
    for value in (plan["raw_relpath"], plan["manifest_relpath"], *plan["artifacts"].values()):
        _relative(value)
    if set(plan["artifacts"]) != set(ARTIFACT_KINDS):
        raise ValueError("ingest plan artifact set is invalid")
    suffix = Path(plan["source_name"]).suffix.lower() or ".txt"
    if suffix not in SOURCE_SUFFIXES:
        raise ValueError(f"unsupported transcript extension: {suffix}")
    if Path(plan["raw_relpath"]).name != f"Plaud - {plan['transaction_id']}{suffix}":
        raise ValueError("raw path is not deterministic for transaction_id")
    if Path(plan["manifest_relpath"]).name != f"Manifest - {plan['transaction_id']}.json":
        raise ValueError("manifest path is not deterministic for transaction_id")
    if type(plan["requires_confirmation"]) is not bool:
        raise ValueError("requires_confirmation must be a strict boolean")
    for collection in ("concept_actions", "task_actions", "calendar_intents"):
        if not isinstance(plan[collection], list):
            raise ValueError(f"{collection} must be a list")
    for action in plan["concept_actions"]:
        if action.get("action") not in {"link_existing", "create", "queue"}:
            raise ValueError("concept action is invalid")
        expected_keys = {
            "link_existing": {"title", "action", "relpath", "expected_sha256"},
            "create": {"title", "action", "relpath", "content_sha256"},
            "queue": {"title", "action", "relpath", "queue_id"},
        }[action["action"]]
        if set(action) != expected_keys:
            raise ValueError("concept action schema mismatch")
        _relative(action.get("relpath", ""))
        hash_key = "expected_sha256" if action["action"] == "link_existing" else "content_sha256"
        if action["action"] != "queue" and not re.fullmatch(r"[0-9a-f]{64}", action[hash_key]):
            raise ValueError("concept action hash is invalid")
        if action["action"] == "queue" and not re.fullmatch(r"[0-9a-f]{20}", action["queue_id"]):
            raise ValueError("concept queue id is invalid")
    for action in plan["task_actions"]:
        if set(action) != {"task_id", "description", "due", "priority", "tag", "relpath"}:
            raise ValueError("task action schema mismatch")
        if "\n" in action["description"] or "\r" in action["description"]:
            raise ValueError("task description must be single-line")
        _relative(action["relpath"])
    for intent in plan["calendar_intents"]:
        if set(intent) != {
            "schema_version",
            "action_id",
            "transaction_id",
            "action",
            "calendar_alias",
            "payload",
            "requires_confirmation",
            "status",
        }:
            raise ValueError("calendar intent schema mismatch")
        if type(intent.get("requires_confirmation")) is not bool:
            raise ValueError("calendar confirmation must be a strict boolean")
        rebuilt = build_calendar_intent(
            transaction_id=intent["transaction_id"],
            action=intent["action"],
            calendar_alias=intent["calendar_alias"],
            payload=intent["payload"],
        )
        if asdict(rebuilt) != intent:
            raise ValueError("calendar intent identity mismatch")
    if plan["requires_confirmation"] != any(
        intent["requires_confirmation"] for intent in plan["calendar_intents"]
    ):
        raise ValueError("plan confirmation aggregate mismatch")
    for value in _walk_strings(plan):
        if unicodedata.normalize("NFC", value) != value:
            raise ValueError("all plan strings must be NFC")


def _walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _walk_strings(key)
            yield from _walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)


def validate_receipt(receipt: dict) -> None:
    if not isinstance(receipt, dict) or set(receipt) != RECEIPT_KEYS:
        raise ValueError("transaction receipt has a closed-schema mismatch")
    if type(receipt["schema_version"]) is not int or receipt["schema_version"] != 1:
        raise ValueError("receipt schema_version must be integer 1")
    if type(receipt["contract_version"]) is not int or receipt["contract_version"] != 1:
        raise ValueError("receipt contract_version must be integer 1")
    if receipt["transaction_id"] != receipt["plan"]["transaction_id"]:
        raise ValueError("receipt transaction_id mismatch")
    if receipt["plan_sha256"] != plan_sha256(receipt["plan"]):
        raise ValueError("receipt plan hash mismatch")
    try:
        datetime.fromisoformat(receipt["started_at"])
    except (TypeError, ValueError) as error:
        raise ValueError("receipt started_at is invalid") from error
    try:
        parsed_as_of = date.fromisoformat(receipt["as_of"])
    except (TypeError, ValueError) as error:
        raise ValueError("receipt as_of is invalid") from error
    if parsed_as_of.isoformat() != receipt["as_of"]:
        raise ValueError("receipt as_of is not canonical")
    if receipt["state"] not in {
        "planned",
        "raw",
        "manifest",
        "transcrito",
        "resumo",
        "concepts",
        "tasks",
        "state_pending",
        "complete",
    }:
        raise ValueError("receipt state is invalid")
    progress = receipt["progress"]
    if not isinstance(progress, dict) or set(progress) != {
        "raw",
        "manifest",
        "artifacts",
        "concepts",
        "tasks",
        "calendar",
        "state",
    }:
        raise ValueError("receipt progress schema mismatch")
    if set(progress["artifacts"]) != set(ARTIFACT_KINDS):
        raise ValueError("receipt artifact progress mismatch")
    progress_bools = [
        progress["raw"],
        progress["manifest"],
        progress["concepts"],
        progress["tasks"],
        progress["calendar"],
        progress["state"],
        *progress["artifacts"].values(),
    ]
    if any(type(value) is not bool for value in progress_bools):
        raise ValueError("receipt progress values must be strict booleans")
    if not isinstance(receipt["file_hashes"], dict) or any(
        not isinstance(key, str) or not re.fullmatch(r"[0-9a-f]{64}", value)
        for key, value in receipt["file_hashes"].items()
    ):
        raise ValueError("receipt file hashes are invalid")
    if not isinstance(receipt["actions"], dict) or set(receipt["actions"]) != {
        "concepts",
        "tasks",
        "calendar",
    }:
        raise ValueError("receipt actions schema mismatch")
    if not all(isinstance(value, list) for value in receipt["actions"].values()):
        raise ValueError("receipt action values must be lists")
    if not isinstance(receipt["validations"], list) or not all(
        isinstance(value, str) for value in receipt["validations"]
    ):
        raise ValueError("receipt validations must be text list")


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _mkdir_parents_durable(directory: Path) -> None:
    missing = []
    current = directory
    while not current.exists():
        missing.append(current)
        if current.parent == current:
            raise IOError(f"cannot find existing parent for directory: {directory}")
        current = current.parent
    if not current.is_dir() or current.is_symlink():
        raise IOError(f"directory parent is not a regular directory: {current}")
    for item in reversed(missing):
        try:
            os.mkdir(item, 0o755)
        except FileExistsError:
            if not item.is_dir() or item.is_symlink():
                raise IOError(f"directory path changed concurrently: {item}")
        _fsync_directory(item.parent)


def _write_all(handle, data: bytes) -> None:
    view = memoryview(data)
    while view:
        written = handle.write(view)
        if written is None or written <= 0:
            raise IOError("short write while persisting workflow data")
        view = view[written:]


def _write_exclusive(path: Path, data: bytes) -> None:
    _mkdir_parents_durable(path.parent)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            _write_all(handle, data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as error:
            raise FileExistsError(f"destination appeared concurrently: {path}") from error
        _fsync_directory(path.parent)
    finally:
        if temporary.exists():
            temporary.unlink()


def _atomic_write(path: Path, data: bytes) -> None:
    _mkdir_parents_durable(path.parent)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            _write_all(handle, data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        if temporary.exists():
            temporary.unlink()


def _checkpoint(path: Path, receipt: dict) -> None:
    validate_receipt(receipt)
    _atomic_write(path, canonical_json(receipt))


def _append_shared_bytes(path: Path, data: bytes) -> None:
    _mkdir_parents_durable(path.parent)
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o644)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise IOError(f"append target is not a regular file: {path}")
        written = os.write(descriptor, data)
        if written != len(data):
            raise IOError(
                f"short append while persisting workflow data: {written}/{len(data)}"
            )
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    _fsync_directory(path.parent)


def _ensure_exact(path: Path, data: bytes, label: str) -> str:
    expected = sha256_bytes(data)
    if path.exists():
        if not path.is_file() or path.is_symlink() or sha256_file(path) != expected:
            raise IOError(f"{label} hash mismatch: {path}")
        return expected
    try:
        _write_exclusive(path, data)
    except FileExistsError:
        if not path.is_file() or path.is_symlink() or sha256_file(path) != expected:
            raise FileExistsError(f"{label} destination belongs to another owner: {path}")
    return expected


def _ensure_source_copy(path: Path, source: Path, expected_hash: str) -> str:
    if path.exists():
        if not path.is_file() or path.is_symlink() or sha256_file(path) != expected_hash:
            raise IOError(f"raw hash mismatch: {path}")
        return expected_hash
    data = source.read_bytes()
    if sha256_bytes(data) != expected_hash or sha256_file(source) != expected_hash:
        raise IOError("source changed during authenticated copy")
    return _ensure_exact(path, data, "raw")


def _authenticate_jsonl_exact(
    path: Path,
    key: str,
    expected: dict,
    *,
    required: bool,
) -> str | None:
    encoded = json.dumps(expected, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if not path.exists():
        if required:
            raise IOError(f"JSONL action missing for {key}")
        return None
    if not path.is_file() or path.is_symlink():
        raise IOError(f"JSONL queue is not a regular file: {path}")
    matches = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise IOError(f"invalid JSONL row at {path}:{line_number}") from error
        if not isinstance(row, dict):
            raise IOError(f"invalid JSONL object at {path}:{line_number}")
        if row.get("action_id") == key or row.get("queue_id") == key:
            matches.append(row)
    if len(matches) > 1:
        raise IOError(f"duplicate JSONL identity for {key}")
    if not matches:
        if required:
            raise IOError(f"JSONL action missing for {key}")
        return None
    actual = json.dumps(
        matches[0], ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    if actual != encoded:
        raise IOError(f"JSONL action mismatch for {key}")
    return sha256_bytes(encoded.encode("utf-8"))


def _append_jsonl_exact(path: Path, key: str, expected: dict) -> str:
    existing_hash = _authenticate_jsonl_exact(
        path,
        key,
        expected,
        required=False,
    )
    if existing_hash is not None:
        return existing_hash
    encoded = json.dumps(expected, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    _append_shared_bytes(path, (encoded + "\n").encode("utf-8"))
    authenticated = _authenticate_jsonl_exact(
        path,
        key,
        expected,
        required=True,
    )
    if authenticated is None:
        raise IOError(f"JSONL action missing after append for {key}")
    return authenticated


def _ensure_task(path: Path, action: dict, transaction_id: str) -> dict:
    marker, expected_core, action_hash = _task_material(action, transaction_id)
    observed = _inspect_task(path, action, transaction_id)
    if observed is not None:
        return {
            **action,
            "outcome": observed,
            "marker": marker if observed == "existing" else None,
            "action_sha256": action_hash,
        }
    prefix = ""
    if not path.exists():
        prefix = "# Tasks\n\n## Adicionadas pela skill /fgv\n\n"
    elif "## Adicionadas pela skill /fgv" not in path.read_text(encoding="utf-8"):
        prefix = "\n## Adicionadas pela skill /fgv\n\n"
    line = f"- [ ] {expected_core} {marker}\n"
    _append_shared_bytes(path, (prefix + line).encode("utf-8"))
    if _inspect_task(path, action, transaction_id) != "existing":
        raise IOError(f"task marker missing after append: {action['task_id']}")
    return {
        **action,
        "outcome": "appended",
        "marker": marker,
        "action_sha256": action_hash,
    }


def _task_material(action: dict, transaction_id: str) -> tuple[str, str, str]:
    marker = f"<!-- fgv-task:{action['task_id']} source:{transaction_id} -->"
    priority = f" {action['priority']}" if action["priority"] else ""
    expected_core = (
        f"{action['description']} {action['tag']} 📅 {action['due']}{priority}"
    )
    action_hash = sha256_bytes(
        f"{action['task_id']}\0{expected_core}".encode("utf-8")
    )
    return marker, expected_core, action_hash


def _inspect_task(path: Path, action: dict, transaction_id: str) -> str | None:
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise IOError(f"task path is not a regular file: {path}")
    marker, expected_core, _action_hash = _task_material(action, transaction_id)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeError as error:
        raise IOError(f"task file is not valid UTF-8: {path}") from error
    exact_marker = re.compile(
        r"^- \[[ xX]\] " + re.escape(f"{expected_core} {marker}") + r"$"
    )
    marker_lines = [line for line in lines if marker in line]
    if marker_lines and (
        len(marker_lines) != 1 or exact_marker.fullmatch(marker_lines[0]) is None
    ):
        raise IOError(f"task marker content mismatch: {action['task_id']}")
    semantic_core = " ".join(
        f"{action['description']} {action['tag']} 📅 {action['due']}".casefold().split()
    )
    semantic_with_priority = " ".join(expected_core.casefold().split())
    semantic_lines = []
    for line in lines:
        match = re.fullmatch(r"- \[[ xX]\] (.*)", line)
        if match is None:
            continue
        body = " ".join(match.group(1).casefold().split())
        if body in {semantic_core, semantic_with_priority}:
            semantic_lines.append(line)
    identity_count = len(marker_lines) + len(semantic_lines)
    if identity_count > 1:
        raise IOError(f"task identity must occur exactly once: {action['task_id']}")
    if marker_lines:
        return "existing"
    if semantic_lines:
        return "semantic_existing"
    return None


def _authenticate_file(path: Path, expected_hash: str, label: str) -> str:
    if not path.is_file() or path.is_symlink() or sha256_file(path) != expected_hash:
        raise IOError(f"{label} hash mismatch: {path}")
    return expected_hash


def _require_receipt_hash(receipt: dict, key: str, expected_hash: str) -> None:
    if receipt["file_hashes"].get(key) != expected_hash:
        raise IOError(f"receipt {key} hash mismatch")


def _authenticate_task_outcome(
    path: Path,
    action: dict,
    recorded: dict,
    transaction_id: str,
) -> None:
    marker, expected_core, action_hash = _task_material(action, transaction_id)
    outcome = recorded.get("outcome")
    if outcome not in {"appended", "existing", "semantic_existing"}:
        raise IOError(f"receipt task outcome is invalid: {action['task_id']}")
    expected_record = {
        **action,
        "outcome": outcome,
        "marker": None if outcome == "semantic_existing" else marker,
        "action_sha256": action_hash,
    }
    if recorded != expected_record:
        raise IOError(f"receipt task action mismatch: {action['task_id']}")
    observed = _inspect_task(path, action, transaction_id)
    if observed is None:
        raise IOError(f"task identity is missing: {action['task_id']}")
    if outcome == "semantic_existing" and observed != "semantic_existing":
        raise IOError(f"semantic task unexpectedly gained marker: {action['task_id']}")
    if outcome in {"appended", "existing"} and observed != "existing":
        raise IOError(f"task marker content mismatch: {action['task_id']}")


def _manifest_bytes(plan: dict, raw_path: Path, started_at: str) -> bytes:
    return canonical_json(
        {
            "schema_version": 1,
            "contract_version": CONTRACT_VERSION,
            "transaction_id": plan["transaction_id"],
            "subject_id": plan["subject_id"],
            "class_date": plan["class_date"],
            "source_name": plan["source_name"],
            "source_sha256": plan["source_sha256"],
            "raw_relpath": plan["raw_relpath"],
            "size_bytes": raw_path.stat().st_size,
            "ingested_at": started_at,
        }
    )


def _artifact_bytes(
    kind: str,
    plan: dict,
    context: dict,
    processor: str,
    started_at: str,
) -> bytes:
    return render_artifact(
        kind=kind,
        subject_id=plan["subject_id"],
        semester=context["registry"].semester,
        class_date=date.fromisoformat(plan["class_date"]),
        analysis=context["analysis"],
        processor=processor,
        updated_at=datetime.fromisoformat(started_at),
        source_sha256=plan["source_sha256"],
        transaction_id=plan["transaction_id"],
        raw_relpath=plan["raw_relpath"],
    ).encode("utf-8")


def _authenticate_local_outputs(
    plan: dict,
    receipt: dict,
    context: dict,
    vault_root: Path,
    processor: str,
) -> None:
    progress = receipt["progress"]
    local_progress = [
        progress["raw"],
        progress["manifest"],
        progress["concepts"],
        progress["tasks"],
        progress["calendar"],
        *progress["artifacts"].values(),
    ]
    if not all(local_progress):
        raise IOError("state receipt is missing completed local stages")

    expected_file_keys = {"raw", "manifest", *ARTIFACT_KINDS}
    raw_path = _vault_path(vault_root, plan["raw_relpath"])
    raw_hash = _authenticate_file(raw_path, plan["source_sha256"], "raw")
    _require_receipt_hash(receipt, "raw", raw_hash)

    manifest_data = _manifest_bytes(plan, raw_path, receipt["started_at"])
    manifest_hash = sha256_bytes(manifest_data)
    _authenticate_file(
        _vault_path(vault_root, plan["manifest_relpath"]),
        manifest_hash,
        "manifest",
    )
    _require_receipt_hash(receipt, "manifest", manifest_hash)

    for kind in ARTIFACT_KINDS:
        artifact_hash = sha256_bytes(
            _artifact_bytes(kind, plan, context, processor, receipt["started_at"])
        )
        _authenticate_file(
            _vault_path(vault_root, plan["artifacts"][kind]),
            artifact_hash,
            "artifact",
        )
        _require_receipt_hash(receipt, kind, artifact_hash)

    candidates = {
        _safe_concept_title(item["title"]): ConceptCandidate(**item)
        for item in context["analysis"]["concept_candidates"]
    }
    concept_outcomes = receipt["actions"]["concepts"]
    if len(concept_outcomes) != len(plan["concept_actions"]):
        raise IOError("receipt concept action count mismatch")
    for action, recorded in zip(plan["concept_actions"], concept_outcomes, strict=True):
        path = _vault_path(vault_root, action["relpath"])
        if action["action"] == "link_existing":
            expected_hash = _authenticate_file(
                path, action["expected_sha256"], "linked concept"
            )
            _require_receipt_hash(receipt, f"concept:{action['title']}", expected_hash)
            expected_record = {**action, "outcome": "linked"}
            expected_file_keys.add(f"concept:{action['title']}")
        elif action["action"] == "create":
            content = _concept_content(
                action["title"], plan["subject_id"], plan["transaction_id"]
            )
            expected_hash = sha256_bytes(content)
            if expected_hash != action["content_sha256"]:
                raise IOError(f"planned concept hash mismatch: {action['title']}")
            _authenticate_file(path, expected_hash, "concept")
            _require_receipt_hash(receipt, f"concept:{action['title']}", expected_hash)
            expected_record = {**action, "outcome": "created_or_authenticated"}
            expected_file_keys.add(f"concept:{action['title']}")
        else:
            candidate = candidates[action["title"]]
            row = _concept_queue_row(plan, action, candidate)
            row_hash = _authenticate_jsonl_exact(
                path, action["queue_id"], row, required=True
            )
            expected_record = {
                **action,
                "outcome": "queued_or_authenticated",
                "row_sha256": row_hash,
            }
        if recorded != expected_record:
            raise IOError(f"receipt concept action mismatch: {action['title']}")

    task_outcomes = receipt["actions"]["tasks"]
    if len(task_outcomes) != len(plan["task_actions"]):
        raise IOError("receipt task action count mismatch")
    for action, recorded in zip(plan["task_actions"], task_outcomes, strict=True):
        _authenticate_task_outcome(
            _vault_path(vault_root, action["relpath"]),
            action,
            recorded,
            plan["transaction_id"],
        )

    calendar_outcomes = receipt["actions"]["calendar"]
    if len(calendar_outcomes) != len(plan["calendar_intents"]):
        raise IOError("receipt calendar action count mismatch")
    for intent, recorded in zip(
        plan["calendar_intents"], calendar_outcomes, strict=True
    ):
        row_hash = _authenticate_jsonl_exact(
            _vault_path(vault_root, CALENDAR_QUEUE),
            intent["action_id"],
            intent,
            required=True,
        )
        if recorded != {
            **intent,
            "relpath": CALENDAR_QUEUE.as_posix(),
            "row_sha256": row_hash,
        }:
            raise IOError(f"receipt calendar action mismatch: {intent['action_id']}")

    allowed_file_keys = expected_file_keys | {"catalog", "snapshot"}
    if not expected_file_keys.issubset(receipt["file_hashes"]):
        raise IOError("receipt is missing local output hashes")
    if set(receipt["file_hashes"]).difference(allowed_file_keys):
        raise IOError("receipt contains unknown output hashes")
    required_validations = {
        "plan_schema",
        "source_hash",
        "analysis_hash",
        "state_preflight",
        "raw_hash",
        "manifest_hash",
        "transcrito_metadata_and_hash",
        "resumo_metadata_and_hash",
        "concept_actions",
        "task_actions",
        "calendar_actions",
    }
    if not required_validations.issubset(receipt["validations"]):
        raise IOError("receipt is missing local validations")


def _concept_queue_row(plan: dict, action: dict, candidate: ConceptCandidate) -> dict:
    return {
        "schema_version": 1,
        "queue_id": action["queue_id"],
        "transaction_id": plan["transaction_id"],
        "subject_id": plan["subject_id"],
        "title": action["title"],
        "criteria": asdict(candidate),
        "status": "pending",
    }


def _preflight_new_transaction(
    plan: dict,
    context: dict,
    vault_root: Path,
) -> None:
    candidates = {
        _safe_concept_title(item["title"]): ConceptCandidate(**item)
        for item in context["analysis"]["concept_candidates"]
    }
    for action in plan["concept_actions"]:
        candidate = candidates[action["title"]]
        concept_relative = (
            Path("20 Conhecimento/Conceitos") / f"{action['title']}.md"
        )
        concept_path = _vault_path(vault_root, concept_relative)
        if concept_path.exists():
            expected_action = "link_existing"
        elif should_promote(candidate):
            expected_action = "create"
        else:
            expected_action = "queue"
        if action["action"] != expected_action:
            raise ValueError(
                f"concept action selection changed for {action['title']}"
            )
        if expected_action == "link_existing":
            if (
                not concept_path.is_file()
                or concept_path.is_symlink()
                or sha256_file(concept_path) != action["expected_sha256"]
            ):
                raise IOError(f"linked concept changed after plan: {concept_path}")
        elif expected_action == "create":
            if concept_path.exists():
                raise FileExistsError(
                    f"concept destination appeared after plan: {concept_path}"
                )
        else:
            row = _concept_queue_row(plan, action, candidate)
            _authenticate_jsonl_exact(
                _vault_path(vault_root, CONCEPT_QUEUE),
                action["queue_id"],
                row,
                required=False,
            )
    for action in plan["task_actions"]:
        _inspect_task(
            _vault_path(vault_root, action["relpath"]),
            action,
            plan["transaction_id"],
        )
    for intent in plan["calendar_intents"]:
        _authenticate_jsonl_exact(
            _vault_path(vault_root, CALENDAR_QUEUE),
            intent["action_id"],
            intent,
            required=False,
        )


def state_command(vault_root: Path, as_of: str, *, check: bool) -> list[str]:
    vault_root = vault_root.resolve()
    generator = vault_root / ".fgv" / "scripts" / "generate_state.py"
    if not generator.is_file() or generator.is_symlink():
        raise FileNotFoundError(f"canonical state generator not found: {generator}")
    command = [
        sys.executable,
        generator.as_posix(),
        "--vault",
        vault_root.resolve().as_posix(),
        "--as-of",
        as_of,
    ]
    if check:
        command.append("--check")
    return command


def run_state(
    vault_root: Path,
    as_of: str,
    *,
    check: bool,
    runner: Callable[[list[str]], int] | None,
) -> int:
    command = state_command(vault_root, as_of, check=check)
    if runner is not None:
        return runner(command)
    return subprocess.run(command, check=False).returncode


def _validate_inputs(plan: dict, source: Path, analysis_path: Path) -> dict:
    validate_plan(plan)
    if (
        not source.is_file()
        or source.is_symlink()
        or not analysis_path.is_file()
        or analysis_path.is_symlink()
    ):
        raise ValueError("source and analysis must remain regular non-symlink files")
    if source.name != plan["source_name"] or sha256_file(source) != plan["source_sha256"]:
        raise ValueError("source hash or name does not match ingest plan")
    analysis_bytes = analysis_path.read_bytes()
    if sha256_bytes(analysis_bytes) != plan["analysis_sha256"]:
        raise ValueError("analysis hash does not match ingest plan")
    analysis = json.loads(analysis_bytes.decode("utf-8"))
    validate_analysis(analysis)
    registry = SubjectRegistry.load_default()
    subject = registry.resolve(analysis["subject_id"])
    if subject.id != plan["subject_id"]:
        raise ValueError("analysis subject does not match ingest plan")
    expected_tx = make_transaction_id(
        plan["source_sha256"], subject.id, plan["class_date"]
    )
    if expected_tx != plan["transaction_id"]:
        raise ValueError("transaction_id does not match authenticated inputs")
    lesson = lesson_dir(Path("."), subject, date.fromisoformat(plan["class_date"]))
    topic = clean_topic(analysis["topic"])
    suffix = Path(plan["source_name"]).suffix.lower() or ".txt"
    expected_raw = (
        lesson / "Fontes" / f"Plaud - {plan['transaction_id']}{suffix}"
    ).as_posix()
    expected_manifest = (
        lesson / "Fontes" / f"Manifest - {plan['transaction_id']}.json"
    ).as_posix()
    if (
        plan["raw_relpath"] != expected_raw
        or plan["manifest_relpath"] != expected_manifest
    ):
        raise ValueError("raw or manifest path does not match authenticated inputs")
    expected_artifacts = {
        "transcrito": (lesson / f"Transcrito - {topic}.md").as_posix(),
        "resumo": (lesson / f"Resumo - {topic}.md").as_posix(),
    }
    if plan["artifacts"] != expected_artifacts:
        raise ValueError("artifact paths do not match authenticated analysis")
    expected_tasks = []
    expected_task_ids: set[str] = set()
    for item in analysis["task_mentions"]:
        task_id = _task_id(item["description"], item["due"], subject.task_tag)
        if task_id in expected_task_ids:
            continue
        expected_task_ids.add(task_id)
        expected_tasks.append({
            "task_id": task_id,
            "description": item["description"].strip(),
            "due": item["due"],
            "priority": item["priority"],
            "tag": subject.task_tag,
            "relpath": TASKS_PATH.as_posix(),
        })
    if plan["task_actions"] != expected_tasks:
        raise ValueError("task actions do not match authenticated analysis")
    expected_calendar = []
    expected_calendar_ids: set[str] = set()
    for item in analysis["calendar_mentions"]:
        intent = asdict(
            build_calendar_intent(
                transaction_id=plan["transaction_id"],
                action=item["action"],
                calendar_alias=item["calendar_alias"],
                payload=item["payload"],
            )
        )
        if intent["action_id"] in expected_calendar_ids:
            continue
        expected_calendar_ids.add(intent["action_id"])
        expected_calendar.append(intent)
    if plan["calendar_intents"] != expected_calendar:
        raise ValueError("calendar intents do not match authenticated analysis")
    candidates = {
        _safe_concept_title(item["title"]): ConceptCandidate(**item)
        for item in analysis["concept_candidates"]
    }
    if [action["title"] for action in plan["concept_actions"]] != list(candidates):
        raise ValueError("concept actions do not match authenticated analysis")
    for action in plan["concept_actions"]:
        candidate = candidates[action["title"]]
        expected_relpath = (
            CONCEPT_QUEUE
            if action["action"] == "queue"
            else Path("20 Conhecimento/Conceitos") / f"{action['title']}.md"
        ).as_posix()
        if action["relpath"] != expected_relpath:
            raise ValueError("concept action path is invalid")
        if action["action"] == "queue" and should_promote(candidate):
            raise ValueError("promoted concept cannot be queued")
        if action["action"] == "queue":
            expected_queue_id = hashlib.sha256(
                f"{plan['transaction_id']}\0{action['title'].casefold()}".encode(
                    "utf-8"
                )
            ).hexdigest()[:20]
            if action["queue_id"] != expected_queue_id:
                raise ValueError("concept queue identity does not match analysis")
        if action["action"] == "create":
            if not should_promote(candidate):
                raise ValueError("concept create does not pass the promotion gate")
            expected_content = _concept_content(
                action["title"], subject.id, plan["transaction_id"]
            )
            if action["content_sha256"] != sha256_bytes(expected_content):
                raise ValueError("concept content hash does not match analysis")
    return {"analysis": analysis, "registry": registry, "subject": subject}


def _new_receipt(plan: dict, as_of: str) -> dict:
    return {
        "schema_version": 1,
        "contract_version": CONTRACT_VERSION,
        "transaction_id": plan["transaction_id"],
        "plan_sha256": plan_sha256(plan),
        "plan": plan,
        "started_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "as_of": as_of,
        "state": "planned",
        "progress": {
            "raw": False,
            "manifest": False,
            "artifacts": {kind: False for kind in ARTIFACT_KINDS},
            "concepts": False,
            "tasks": False,
            "calendar": False,
            "state": False,
        },
        "file_hashes": {},
        "actions": {"concepts": [], "tasks": [], "calendar": []},
        "validations": [
            "plan_schema",
            "source_hash",
            "analysis_hash",
            "state_preflight",
        ],
    }


def _mark_state_pending(receipt_path: Path, receipt: dict) -> None:
    receipt["progress"]["state"] = False
    receipt["file_hashes"].pop("catalog", None)
    receipt["file_hashes"].pop("snapshot", None)
    receipt["validations"] = [
        validation
        for validation in receipt["validations"]
        if validation == "state_preflight" or not validation.startswith("state_")
    ]
    receipt["state"] = "state_pending"
    _checkpoint(receipt_path, receipt)


def _refresh_state(
    vault_root: Path,
    receipt_path: Path,
    receipt: dict,
    *,
    state_runner: Callable[[list[str]], int] | None,
    fault_hook: Callable[[str], None] | None,
    initial_check: int | None,
) -> dict:
    state_check = initial_check
    if state_check is None:
        state_check = run_state(
            vault_root,
            receipt["as_of"],
            check=True,
            runner=state_runner,
        )
    if state_check == 1:
        state_build = run_state(
            vault_root,
            receipt["as_of"],
            check=False,
            runner=state_runner,
        )
        if state_build != 0:
            receipt["validations"].append(f"state_build_exit:{state_build}")
            receipt["validations"] = list(dict.fromkeys(receipt["validations"]))
            _checkpoint(receipt_path, receipt)
            return receipt
        if fault_hook is not None:
            fault_hook("state_build")
        state_check = run_state(
            vault_root,
            receipt["as_of"],
            check=True,
            runner=state_runner,
        )
    if state_check == 0 and fault_hook is not None:
        fault_hook("state_check")
    if state_check != 0:
        receipt["validations"].append(f"state_check_exit:{state_check}")
        receipt["validations"] = list(dict.fromkeys(receipt["validations"]))
        _checkpoint(receipt_path, receipt)
        return receipt
    catalog = _vault_path(vault_root, CATALOG_PATH)
    snapshot = _vault_path(vault_root, SNAPSHOT_PATH)
    if (
        not catalog.is_file()
        or catalog.is_symlink()
        or not snapshot.is_file()
        or snapshot.is_symlink()
    ):
        raise IOError("state generator reported fresh without canonical outputs")
    receipt["file_hashes"]["catalog"] = sha256_file(catalog)
    receipt["file_hashes"]["snapshot"] = sha256_file(snapshot)
    receipt["progress"]["state"] = True
    receipt["state"] = "complete"
    receipt["validations"].append("state_fresh")
    receipt["validations"] = list(dict.fromkeys(receipt["validations"]))
    _checkpoint(receipt_path, receipt)
    return receipt


def _refresh_complete_state_readonly(
    vault_root: Path,
    receipt: dict,
    *,
    fault_hook: Callable[[str], None] | None,
    initial_check: int,
) -> dict:
    if initial_check == 1:
        raise RuntimeError(
            "state is stale; run build-state with the current operational --as-of"
        )
    if initial_check != 0:
        raise RuntimeError(f"state check failed with exit {initial_check}")
    if fault_hook is not None:
        fault_hook("state_check")
    catalog = _vault_path(vault_root, CATALOG_PATH)
    snapshot = _vault_path(vault_root, SNAPSHOT_PATH)
    if (
        not catalog.is_file()
        or catalog.is_symlink()
        or not snapshot.is_file()
        or snapshot.is_symlink()
    ):
        raise IOError("state generator reported fresh without canonical outputs")
    return receipt


def apply_transaction(
    plan: dict,
    *,
    vault_root: Path,
    source: Path,
    analysis_path: Path,
    processor: str,
    as_of: str,
    state_runner: Callable[[list[str]], int] | None = None,
    fault_hook: Callable[[str], None] | None = None,
) -> dict:
    vault_root = vault_root.resolve()
    try:
        parsed_as_of = date.fromisoformat(as_of)
    except (TypeError, ValueError) as error:
        raise ValueError("as_of must use canonical YYYY-MM-DD") from error
    if parsed_as_of.isoformat() != as_of:
        raise ValueError("as_of must use canonical YYYY-MM-DD")
    if processor not in {"codex", "claude"} or processor != plan.get("runtime"):
        raise ValueError("processor must match the planned runtime")
    with vault_lock(vault_root):
        context = _validate_inputs(plan, source, analysis_path)
        receipt_path = _vault_path(
            vault_root,
            TRANSACTION_ROOT / f"{plan['transaction_id']}.json",
        )
        receipt = _existing_receipt(vault_root, plan["transaction_id"])
        if receipt is None:
            artifact_paths = set(plan["artifacts"].values())
            for relative in (
                plan["raw_relpath"],
                plan["manifest_relpath"],
                *artifact_paths,
            ):
                if _vault_path(vault_root, relative).exists():
                    label = "artifact destination" if relative in artifact_paths else "destination"
                    raise FileExistsError(f"{label} appeared after plan: {relative}")
            _preflight_new_transaction(plan, context, vault_root)
            preflight = run_state(
                vault_root,
                as_of,
                check=True,
                runner=state_runner,
            )
            if preflight not in {0, 1}:
                raise RuntimeError(f"state preflight failed with exit {preflight}")
            receipt = _new_receipt(plan, as_of)
            validate_receipt(receipt)
            _write_exclusive(receipt_path, canonical_json(receipt))
        elif receipt["plan"] != plan:
            raise ValueError("receipt plan differs from requested plan")
        elif receipt["state"] != "complete" and receipt["as_of"] != as_of:
            raise ValueError("as_of differs from the durable transaction receipt")
        if receipt["state"] in {"state_pending", "complete"}:
            _authenticate_local_outputs(
                plan,
                receipt,
                context,
                vault_root,
                processor,
            )
            if receipt["state"] == "complete":
                if not receipt["progress"]["state"]:
                    raise IOError("complete receipt has pending state progress")
                if not {"catalog", "snapshot"}.issubset(receipt["file_hashes"]):
                    raise IOError("complete receipt is missing state hashes")
                if "state_fresh" not in receipt["validations"]:
                    raise IOError("complete receipt is missing state validation")
                state_check = run_state(
                    vault_root,
                    as_of,
                    check=True,
                    runner=state_runner,
                )
                return _refresh_complete_state_readonly(
                    vault_root,
                    receipt,
                    fault_hook=fault_hook,
                    initial_check=state_check,
                )
            if receipt["progress"]["state"]:
                raise IOError("state_pending receipt has complete state progress")
            return _refresh_state(
                vault_root,
                receipt_path,
                receipt,
                state_runner=state_runner,
                fault_hook=fault_hook,
                initial_check=None,
            )

        raw_path = _vault_path(vault_root, plan["raw_relpath"])
        raw_hash = _ensure_source_copy(raw_path, source, plan["source_sha256"])
        if fault_hook is not None:
            fault_hook("raw")
        receipt["file_hashes"]["raw"] = raw_hash
        receipt["validations"].append("raw_hash")
        receipt["progress"]["raw"] = True
        receipt["state"] = "raw"
        _checkpoint(receipt_path, receipt)

        manifest_path = _vault_path(vault_root, plan["manifest_relpath"])
        manifest_hash = _ensure_exact(
            manifest_path,
            _manifest_bytes(plan, raw_path, receipt["started_at"]),
            "manifest",
        )
        if fault_hook is not None:
            fault_hook("manifest")
        receipt["file_hashes"]["manifest"] = manifest_hash
        receipt["validations"].append("manifest_hash")
        receipt["progress"]["manifest"] = True
        receipt["state"] = "manifest"
        _checkpoint(receipt_path, receipt)

        for kind in ARTIFACT_KINDS:
            rendered = _artifact_bytes(
                kind,
                plan,
                context,
                processor,
                receipt["started_at"],
            )
            path = _vault_path(vault_root, plan["artifacts"][kind])
            artifact_hash = _ensure_exact(path, rendered, "artifact")
            if fault_hook is not None:
                fault_hook(f"artifact:{kind}")
            receipt["file_hashes"][kind] = artifact_hash
            receipt["validations"].append(f"{kind}_metadata_and_hash")
            receipt["progress"]["artifacts"][kind] = True
            receipt["state"] = kind
            _checkpoint(receipt_path, receipt)

        concept_outcomes = []
        candidates_by_title = {
            _safe_concept_title(item["title"]): ConceptCandidate(**item)
            for item in context["analysis"]["concept_candidates"]
        }
        for action in plan["concept_actions"]:
            path = _vault_path(vault_root, action["relpath"])
            if action["action"] == "link_existing":
                if not path.is_file() or sha256_file(path) != action["expected_sha256"]:
                    raise IOError(f"linked concept hash mismatch: {path}")
                outcome = {**action, "outcome": "linked"}
                receipt["file_hashes"][f"concept:{action['title']}"] = action[
                    "expected_sha256"
                ]
            elif action["action"] == "create":
                candidate = candidates_by_title[action["title"]]
                if not should_promote(candidate):
                    raise ValueError("concept promotion no longer passes gate")
                content = _concept_content(
                    action["title"], plan["subject_id"], plan["transaction_id"]
                )
                if sha256_bytes(content) != action["content_sha256"]:
                    raise ValueError("concept content hash differs from plan")
                _ensure_exact(path, content, "concept")
                outcome = {**action, "outcome": "created_or_authenticated"}
                receipt["file_hashes"][f"concept:{action['title']}"] = action[
                    "content_sha256"
                ]
            else:
                candidate = candidates_by_title[action["title"]]
                row = _concept_queue_row(plan, action, candidate)
                row_hash = _append_jsonl_exact(path, action["queue_id"], row)
                outcome = {**action, "outcome": "queued_or_authenticated", "row_sha256": row_hash}
            concept_outcomes.append(outcome)
        if fault_hook is not None:
            fault_hook("concepts")
        receipt["actions"]["concepts"] = concept_outcomes
        receipt["validations"].append("concept_actions")
        receipt["progress"]["concepts"] = True
        receipt["state"] = "concepts"
        _checkpoint(receipt_path, receipt)

        task_outcomes = [
            _ensure_task(
                _vault_path(vault_root, action["relpath"]),
                action,
                plan["transaction_id"],
            )
            for action in plan["task_actions"]
        ]
        if fault_hook is not None:
            fault_hook("tasks")
        receipt["actions"]["tasks"] = task_outcomes
        receipt["validations"].append("task_actions")
        receipt["progress"]["tasks"] = True
        receipt["state"] = "tasks"
        _checkpoint(receipt_path, receipt)

        calendar_outcomes = []
        for intent in plan["calendar_intents"]:
            row_hash = _append_jsonl_exact(
                _vault_path(vault_root, CALENDAR_QUEUE),
                intent["action_id"],
                intent,
            )
            calendar_outcomes.append(
                {
                    **intent,
                    "relpath": CALENDAR_QUEUE.as_posix(),
                    "row_sha256": row_hash,
                }
            )
        if fault_hook is not None:
            fault_hook("calendar")
        receipt["actions"]["calendar"] = calendar_outcomes
        receipt["validations"].append("calendar_actions")
        receipt["progress"]["calendar"] = True
        _authenticate_local_outputs(
            plan,
            receipt,
            context,
            vault_root,
            processor,
        )
        _mark_state_pending(receipt_path, receipt)
        return _refresh_state(
            vault_root,
            receipt_path,
            receipt,
            state_runner=state_runner,
            fault_hook=fault_hook,
            initial_check=1,
        )
