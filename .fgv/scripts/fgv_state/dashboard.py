from __future__ import annotations

from datetime import date, timedelta
from pathlib import PurePosixPath
import re

from .config import Settings


PRIORITY_RANK = {"highest": 5, "high": 4, "medium": 3, "normal": 2, "low": 1, "lowest": 0}
GAP_RANK = {"gap": 0, "nao_sabe": 0, "parcial": 1, "nao_testado": 2, "certo": 3}
CLASS_RE = re.compile(r"^(\d{2})\.(\d{2})$")


def _escape(value: object) -> str:
    return (str(value).replace("\\", "\\\\").replace("\n", " ").replace("\r", " ")
            .replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
            .replace("<", "&lt;").replace(">", "&gt;"))


def _wikilink(path: str, label: object) -> str:
    target = path[:-3] if path.endswith(".md") else path
    return f"[[{target}|{_escape(label)}]]"


def _append(lines: list[str], heading: str, items: list[str]) -> None:
    lines.extend((heading, "", *(items or ["Nenhuma."]), ""))


def _classes(records: tuple[dict[str, object], ...], settings: Settings, as_of: str) -> list[dict[str, object]]:
    today = date.fromisoformat(as_of)
    grouped: dict[tuple[str, str], dict[str, object]] = {}
    for record in records:
        if record.get("record_type") != "file" or record.get("scope") != "active":
            continue
        path = str(record["path"])
        for subject in settings.subjects:
            prefix = subject.path + "/Aulas/"
            if not path.startswith(prefix):
                continue
            folder = path[len(prefix):].split("/", 1)[0]
            match = CLASS_RE.fullmatch(folder)
            if not match:
                continue
            try:
                class_date = date.fromisoformat(f"{settings.semester[:4]}-{match.group(1)}-{match.group(2)}")
            except ValueError:
                continue
            if class_date > today:
                continue
            grouped.setdefault((subject.id, folder), {"subject_id": subject.id, "folder": folder, "date": class_date.isoformat(), "files": []})["files"].append(record)
    return sorted(grouped.values(), key=lambda item: (-date.fromisoformat(str(item["date"])).toordinal(), str(item["subject_id"]), str(item["folder"])))


def _class_link(state: dict[str, object], name: str) -> str:
    notes = sorted((record for record in state["files"] if record.get("kind") == "note"),
                   key=lambda record: (0 if PurePosixPath(str(record["path"])).name.casefold().startswith("resumo") else 1, str(record["path"])))
    label = f"{name} {state['folder']}"
    return _wikilink(str(notes[0]["path"]), label) if notes else f"`{_escape(label)}`"


def render_dashboard(records: tuple[dict[str, object], ...], settings: Settings, as_of: str,
                     build_fingerprint: str, catalog_sha256: str) -> str:
    today = date.fromisoformat(as_of)
    subject_by_id = settings.subject_by_id
    tasks = [record for record in records if record.get("record_type") == "task"
             and record.get("status") in {"todo", "in_progress"} and record.get("subject_ids")]
    def task_sort(record: dict[str, object]) -> tuple[object, ...]:
        return (str(record.get("due") or "9999-12-31"), -PRIORITY_RANK.get(str(record.get("priority")), 0),
                str(record["subject_ids"][0]), str(record.get("description", "")).casefold())
    def task_line(record: dict[str, object]) -> str:
        names = ", ".join(subject_by_id[item].name for item in record["subject_ids"] if item in subject_by_id)
        return f"- {_escape(record.get('due') or 'sem prazo')}, {_escape(record['description'])} ({_escape(names)}, [[00 Home/Tasks|Tasks]])"
    overdue = sorted([record for record in tasks if record.get("due") and date.fromisoformat(str(record["due"])) < today], key=task_sort)
    due_today = sorted([record for record in tasks if record.get("due") == as_of], key=task_sort)
    horizon = today + timedelta(days=7)
    upcoming = sorted([record for record in tasks if record.get("due") and today < date.fromisoformat(str(record["due"])) <= horizon], key=task_sort)

    classes = _classes(records, settings, as_of)
    today_pending: list[str] = []
    missing_transcript: list[str] = []
    material_without_summary: list[str] = []
    latest: dict[str, dict[str, object]] = {}
    for state in classes:
        subject = subject_by_id[str(state["subject_id"])]
        files = list(state["files"])
        names = [PurePosixPath(str(record["path"])).name.casefold() for record in files if record.get("kind") == "note"]
        has_transcript = any(name.startswith("transcrito") for name in names)
        has_summary = any(name.startswith("resumo") for name in names)
        has_material = any(record.get("kind") != "note" or "/Materiais/" in str(record["path"]) for record in files)
        link = _class_link(state, subject.name)
        if str(state["date"]) == as_of:
            pending = []
            if not has_transcript:
                pending.append("sem transcrito")
            if has_material and not has_summary:
                pending.append("com material e sem resumo")
            if pending:
                today_pending.append(f"- {link}: {'; '.join(pending)}")
        else:
            if not has_transcript:
                missing_transcript.append(f"- {link}: sem transcrito")
            if has_material and not has_summary:
                material_without_summary.append(f"- {link}: com material e sem resumo")
        current = latest.get(subject.id)
        if current is None or str(state["date"]) > str(current["date"]):
            latest[subject.id] = state

    reviews = sorted([record for record in records if record.get("record_type") == "file" and record.get("scope") == "active"
                      and record.get("kind") == "note" and record.get("review_due")
                      and date.fromisoformat(str(record["review_due"])) <= today and record.get("mastery") != 3],
                     key=lambda record: (str(record["review_due"]), str(record["path"])))
    learning = [record for record in records if record.get("record_type") == "learning_state"]
    def learning_lines(scope: str, statuses: set[str], limit: int | None = None) -> list[str]:
        selected = sorted([record for record in learning if record.get("scope") == scope and record.get("last_status") in statuses],
                          key=lambda record: (GAP_RANK[str(record["last_status"])], str(record.get("last_probed") or "0000-00-00"), str(record["concept"])))
        if limit is not None:
            selected = selected[:limit]
        output: list[str] = []
        for record in selected:
            concept = _wikilink(str(record["concept_path"]), record["concept"]) if record.get("concept_path") else _escape(record["concept"])
            output.append(f"- {concept}: {_escape(record['last_status'])}, última sondagem {_escape(record.get('last_probed') or 'sem data')}")
        return output

    lines = ["---", "tipo: dashboard_snapshot", "schema_version: 1", f"as_of: {as_of}",
             f'build_fingerprint: "{build_fingerprint}"', f'catalog_sha256: "{catalog_sha256}"', "---", "",
             "<!-- GENERATED FILE. Edite as fontes e regenere. -->", "# Painel", "", "## Agora", ""]
    _append(lines, "### Atrasadas", [task_line(record) for record in overdue])
    _append(lines, "### Hoje", [task_line(record) for record in due_today])
    _append(lines, "### Próximos 7 dias", [task_line(record) for record in upcoming])
    lines.extend(("## Processamento", ""))
    _append(lines, "### Aulas de hoje, processamento pendente", today_pending)
    _append(lines, "### Aulas sem transcrito", missing_transcript)
    _append(lines, "### Aulas com material e sem resumo", material_without_summary)
    _append(lines, "## Revisões vencidas", [f"- {_escape(record['review_due'])}, {_wikilink(str(record['path']), record['title'])}" for record in reviews])
    lines.extend(("## Aprendizagem ativa", ""))
    _append(lines, "### Gaps abertos", learning_lines("active", {"gap", "nao_sabe", "parcial"}))
    _append(lines, "### Não testados", learning_lines("active", {"nao_testado"}, 10))
    lines.extend(("## Aprendizagem arquivada", ""))
    _append(lines, "### Gaps do arquivo", learning_lines("archive", {"gap", "nao_sabe", "parcial"}))
    lines.extend(("## Matérias", "", "| Matéria | Pendentes | Atrasadas | Última aula | Gaps |", "|---|---:|---:|---|---:|"))
    for subject in sorted(settings.subjects, key=lambda item: item.name):
        pending_count = sum(subject.id in record["subject_ids"] for record in tasks)
        overdue_count = sum(subject.id in record["subject_ids"] for record in overdue)
        gap_count = sum(subject.id in record.get("subject_ids", []) and record.get("last_status") in {"gap", "nao_sabe", "parcial"} for record in learning)
        current = latest.get(subject.id)
        latest_text = _class_link(current, subject.name) if current else "Nenhuma"
        lines.append(f"| {_escape(subject.name)} | {pending_count} | {overdue_count} | {latest_text} | {gap_count} |")
    warnings = sum(len(record.get("warnings", [])) for record in records)
    lines.extend(("", "## Integridade", "", "Nenhum aviso." if warnings == 0 else f"- {warnings} aviso(s) de metadata no catálogo."))
    return "\n".join(lines).rstrip() + "\n"
