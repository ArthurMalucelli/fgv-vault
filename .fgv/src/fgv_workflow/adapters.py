import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from string import Template
import tempfile

from . import CONTRACT_VERSION


FGV_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = FGV_ROOT / "adapters"
LIVE_ROOTS = (
    Path.home() / ".agents" / "skills",
    Path.home() / ".claude" / "skills",
    Path("/root/.hermes/skills"),
)
RUNTIME_TOOLS = {
    "codex": "Use ferramentas locais do Codex e solicite aprovação no momento exato de qualquer efeito externo autorizado.",
    "claude": "Use ferramentas locais do Claude. Um connector Calendar disponível só pode traduzir intents já confirmadas.",
}


class LiveInstallDenied(PermissionError):
    pass


@dataclass(frozen=True)
class StagedAdapters:
    root: Path
    codex: Path
    claude: Path
    manifest: Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _assert_staging_destination(destination: Path) -> Path:
    resolved = destination.expanduser().resolve(strict=False)
    for live in LIVE_ROOTS:
        live_resolved = live.expanduser().resolve(strict=False)
        if resolved == live_resolved or live_resolved in resolved.parents:
            raise LiveInstallDenied(f"staging destination is a live installation: {resolved}")
    return resolved


def _normative_contract(text: str) -> str:
    marker = "\n## Ferramentas do runtime\n"
    if marker not in text:
        raise ValueError("adapter is missing runtime tools boundary")
    return text.split(marker, 1)[0].rstrip() + "\n"


def stage_adapters(destination: Path) -> StagedAdapters:
    destination = _assert_staging_destination(destination)
    outputs: dict[str, Path] = {}
    for runtime in ("codex", "claude"):
        template_path = TEMPLATE_ROOT / runtime / "SKILL.md.tmpl"
        rendered = Template(template_path.read_text(encoding="utf-8")).substitute(
            runtime_tools=RUNTIME_TOOLS[runtime]
        )
        output = destination / runtime / "fgv" / "SKILL.md"
        _atomic_write(output, (rendered.rstrip() + "\n").encode("utf-8"))
        outputs[runtime] = output
    codex_text = outputs["codex"].read_text(encoding="utf-8")
    claude_text = outputs["claude"].read_text(encoding="utf-8")
    semantic_hash = hashlib.sha256(
        _normative_contract(codex_text).encode("utf-8")
    ).hexdigest()
    manifest_payload = {
        "schema_version": 1,
        "contract_version": CONTRACT_VERSION,
        "install_performed": False,
        "parity": {
            "normative_contract_identical": _normative_contract(codex_text)
            == _normative_contract(claude_text),
            "semantic_sha256": semantic_hash,
        },
        "adapters": {
            runtime: {
                "path": outputs[runtime].relative_to(destination).as_posix(),
                "sha256": _sha256(outputs[runtime]),
                "template_sha256": _sha256(TEMPLATE_ROOT / runtime / "SKILL.md.tmpl"),
            }
            for runtime in ("codex", "claude")
        },
    }
    manifest = destination / "manifest.json"
    _atomic_write(
        manifest,
        (json.dumps(manifest_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    if not manifest_payload["parity"]["normative_contract_identical"]:
        raise ValueError("Codex and Claude normative contracts drifted")
    return StagedAdapters(destination, outputs["codex"], outputs["claude"], manifest)
