"""Canonical path classification and collision-safe manifest construction."""

from dataclasses import dataclass
from pathlib import PurePosixPath
import unicodedata
from typing import Mapping, Sequence

from .inventory import InventoryEntry, normalize_relative_path


ACTIVE_SUBJECTS = (
    "ContabilidadeFinanceira",
    "DireitoEmpresarial",
    "Estatistica2",
    "EstudosOrganizacionais",
    "MatemáticaAplicada",
    "Psicologia",
    "TecnologiaDadosNegocios",
)


class RuleError(ValueError):
    """A migration rule cannot produce a safe manifest."""


class UnclassifiedError(RuleError):
    """One or more source paths have no explicit migration rule."""


class CollisionError(RuleError):
    """Two source paths resolve to the same destination."""


@dataclass(frozen=True)
class Classification:
    destination: str | None
    category: str
    phase: str
    reason: str


SPECIAL_MAPPINGS: Mapping[str, Classification] = {
    "Vault/Index.md": Classification(
        "00 Home/Home.md", "home", "structural", "canonical home index"
    ),
    "Tasks.md": Classification(
        "00 Home/Tasks.md", "home", "structural", "canonical task file"
    ),
    "Vault/Controle de Faltas 2026.2.md": Classification(
        "00 Home/Controle de Faltas 2026.2.md",
        "home",
        "structural",
        "canonical attendance control",
    ),
}

DEFAULT_INBOX_ALLOWLIST: Mapping[str, str] = {
    "Macro.md": "00 Home/Inbox/Legado/Macro.md",
    "Projeto 90 Dias.md": "00 Home/Inbox/Legado/Projeto 90 Dias.md",
    "Vault/FGV Finance/Prova - Tópicos cobrados.md": (
        "00 Home/Inbox/Legado/Prova - Tópicos cobrados.md"
    ),
    "Vault/Conceitos/Sem título.md": "00 Home/Inbox/Legado/Sem título.md",
}


def _prefix_mapping(
    source: str,
    source_root: str,
    destination_root: str,
    category: str,
    reason: str,
) -> Classification | None:
    prefix = f"{source_root}/"
    if not source.startswith(prefix):
        return None
    suffix = source[len(prefix) :]
    return Classification(
        f"{destination_root}/{suffix}", category, "structural", reason
    )


def _validated_allowlist(
    inbox_allowlist: Mapping[str, str] | None,
) -> dict[str, str]:
    combined = dict(DEFAULT_INBOX_ALLOWLIST)
    if inbox_allowlist is not None:
        combined.update(inbox_allowlist)

    validated: dict[str, str] = {}
    inbox_root = PurePosixPath("00 Home/Inbox/Legado")
    for source, destination in combined.items():
        normalized_source = normalize_relative_path(source)
        normalized_destination = normalize_relative_path(destination)
        destination_path = PurePosixPath(normalized_destination)
        if (
            destination_path == inbox_root
            or inbox_root not in destination_path.parents
        ):
            raise RuleError(
                f"Inbox allowlist destination is outside 00 Home/Inbox/Legado: {destination!r}"
            )
        validated[normalized_source] = destination
    return validated


def classify_path(
    source: str, *, inbox_allowlist: Mapping[str, str] | None = None
) -> Classification:
    normalized_source = normalize_relative_path(source)
    special = SPECIAL_MAPPINGS.get(normalized_source)
    if special is not None:
        return special

    allowlist = _validated_allowlist(inbox_allowlist)
    inbox_destination = allowlist.get(normalized_source)
    if inbox_destination is not None:
        return Classification(
            inbox_destination,
            "home",
            "structural",
            "explicit legacy Inbox allowlist",
        )

    for subject in ACTIVE_SUBJECTS:
        classification = _prefix_mapping(
            normalized_source,
            subject,
            f"10 Matérias/{subject}",
            "subject",
            "active subject folder",
        )
        if classification is not None:
            return classification

    prefix_rules = (
        (
            "Vault/Conceitos",
            "20 Conhecimento/Conceitos",
            "knowledge",
            "legacy concept library",
        ),
        ("Vault/Specs", "30 Sistema/Specs", "system", "system specification"),
        ("Vault/Templates", "30 Sistema/Templates", "system", "system template"),
        ("Vault/Tutor", "30 Sistema/Tutor", "system", "tutor system asset"),
        (
            "Vault/automation",
            "30 Sistema/Automacoes",
            "system",
            "automation system asset",
        ),
        ("Vault/S1", "90 Arquivo/2026.1", "archive", "semester 2026.1 archive"),
    )
    for source_root, destination_root, category, reason in prefix_rules:
        classification = _prefix_mapping(
            normalized_source, source_root, destination_root, category, reason
        )
        if classification is not None:
            return classification

    return Classification(None, "unclassified", "structural", "no migration rule")


def build_manifest(
    entries: Sequence[InventoryEntry],
    *,
    inbox_allowlist: Mapping[str, str] | None = None,
) -> tuple[dict[str, object], ...]:
    records: list[dict[str, object]] = []
    unclassified: list[str] = []
    exact_destinations: dict[str, str] = {}
    normalized_destinations: dict[str, tuple[str, str]] = {}

    for item in sorted(entries, key=lambda candidate: candidate.path.encode("utf-8")):
        classification = classify_path(
            item.path, inbox_allowlist=inbox_allowlist
        )
        raw_destination = classification.destination
        if raw_destination is None:
            unclassified.append(item.path)
            continue

        previous_exact = exact_destinations.get(raw_destination)
        if previous_exact is not None:
            raise CollisionError(
                f"exact destination collision: {previous_exact!r} and {item.path!r} -> {raw_destination!r}"
            )
        exact_destinations[raw_destination] = item.path

        normalized_destination = unicodedata.normalize("NFC", raw_destination)
        previous_normalized = normalized_destinations.get(normalized_destination)
        if previous_normalized is not None:
            previous_source, previous_raw = previous_normalized
            raise CollisionError(
                "destination collision after NFC: "
                f"{previous_source!r} -> {previous_raw!r}; "
                f"{item.path!r} -> {raw_destination!r}"
            )
        normalized_destinations[normalized_destination] = (item.path, raw_destination)

        records.append(
            {
                "schema_version": 1,
                "source": item.path,
                "destination": normalized_destination,
                "sha256": item.sha256,
                "size_bytes": item.size_bytes,
                "category": classification.category,
                "phase": classification.phase,
                "reason": classification.reason,
            }
        )

    if unclassified:
        joined = ", ".join(repr(path) for path in unclassified)
        raise UnclassifiedError(f"unclassified source paths: {joined}")
    return tuple(records)
