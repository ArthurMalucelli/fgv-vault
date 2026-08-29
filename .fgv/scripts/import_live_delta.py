#!/usr/bin/env python3
"""Import the authenticated 2026-08-28 live-vault delta into Plan B.

The importer reads only pinned Git blobs. It never reads the mutable working
tree of the live vault. All outputs are built and validated before publication.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import tempfile
import unicodedata


SCHEMA = "fgv.live-delta.v1"
SOURCE_BASE = "a7f7d58a5fcbbee86c90a046eb30e168217b5c78"
SOURCE_TIP = "59c8c4407dd51b10c23695ddb4328ebf5372f0ea"
SOURCE_COMMITS = (
    "a81ff3df175c8d74d9523aaf83f0475fed6af94e",
    "a93c71f599f5d4fa9568946250f0958b2c28b64d",
    SOURCE_TIP,
)
MANIFEST = PurePosixPath("30 Sistema/Estado/live-delta-manifest.json")


RECORDS = (
    {
        "source": "ContabilidadeFinanceira/Aulas/08.28/RevisaoErrosQuizzes.md",
        "destination": (
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/"
            "Revisao - Revisão de erros dos quizzes (Delícia Gelada, Sing's, "
            "Nosso Doce Amor, Lojas Paulistas).md"
        ),
        "introduced_commit": SOURCE_COMMITS[0],
        "content_commit": SOURCE_COMMITS[1],
        "source_blob_oid": "80e08e60da5e139f74963973d97417a45cb145be",
        "source_sha256": "bcefe329747c06892356e2067cbe68ec6fcc58d5e2fbe0e80fe2edc1e717a8ca",
        "source_size_bytes": 8484,
        "subject_id": "contabilidade-financeira",
        "class_date": "2026-08-28",
        "kind": "revisao",
        "topic": "Revisão de erros dos quizzes (Delícia Gelada, Sing's, Nosso Doce Amor, Lojas Paulistas)",
        "frontmatter": """---
materias: [contabilidade-financeira]
semestre: 2026.2
data: 2026-08-28
tipo: revisao
tema: Revisão de erros dos quizzes (Delícia Gelada, Sing's, Nosso Doce Amor, Lojas Paulistas)
status: completo
contract_version: 1
topicos: [regime de caixa, regime de competência, equação de saldo, contas antecipadas, CMV, dividendos]
tags: [resumo, revisao]
---
""",
        "final_sha256": "e224375bdaeadb677ef25104c92a3f806e9e1bb218e65dc03c2f7e5d85d69289",
    },
    {
        "source": "Vault/Conceitos/Equação de Saldo.md",
        "destination": "20 Conhecimento/Conceitos/Equação de Saldo.md",
        "introduced_commit": SOURCE_COMMITS[0],
        "content_commit": SOURCE_COMMITS[0],
        "source_blob_oid": "a36daf5a3a4adf9b967f19d0dc6528d1e05ea1f3",
        "source_sha256": "ce8383fff0475dea99d6fb65a8d8bf4633abc1be0e45d75333aecbde0ad7d446",
        "source_size_bytes": 1338,
        "subject_id": "contabilidade-financeira",
        "class_date": None,
        "kind": "conceito",
        "topic": "Equação de Saldo",
        "frontmatter": """---
tipo: conceito
materias: [contabilidade-financeira]
tags: [conceito]
---
""",
        "final_sha256": "37fae9ad1d32e8318a62c21fa6792dedbc16501bfeea85caf85c79db60dbd997",
    },
    {
        "source": "Vault/Conceitos/Fornecedores.md",
        "destination": "20 Conhecimento/Conceitos/Fornecedores.md",
        "introduced_commit": SOURCE_COMMITS[0],
        "content_commit": SOURCE_COMMITS[0],
        "source_blob_oid": "e8a3d466870a864c0d6085672ec7b33c8c8337e6",
        "source_sha256": "7d8782d14cb4378e9dd2f6b774b9476d4dbfbf0c87d91922d51bdf57753f21e8",
        "source_size_bytes": 952,
        "subject_id": "contabilidade-financeira",
        "class_date": None,
        "kind": "conceito",
        "topic": "Fornecedores",
        "frontmatter": """---
tipo: conceito
materias: [contabilidade-financeira]
tags: [conceito]
---
""",
        "final_sha256": "9e283c7ee8fe80d14d1d9163fa12e8ee48be7ba142b73d2d1d49dd99661f8fa4",
    },
    {
        "source": "ContabilidadeFinanceira/Aulas/08.28/TreinoBanhoEBicho_Enunciado.md",
        "destination": "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/TreinoBanhoEBicho_Enunciado.md",
        "introduced_commit": SOURCE_TIP,
        "content_commit": SOURCE_TIP,
        "source_blob_oid": "bceb9ebae53dc8e8b897f57ee1bec97ef8aad9fb",
        "source_sha256": "23e9b296f412a892b1428a10ce27acd3d0d4a3af66a3656e4225954684ba3406",
        "source_size_bytes": 3546,
        "subject_id": "contabilidade-financeira",
        "class_date": "2026-08-28",
        "kind": "exercicio",
        "topic": "Treino BP + DRE no estilo dos quizzes (gerado sob medida pros erros mapeados)",
        "frontmatter": """---
materias: [contabilidade-financeira]
semestre: 2026.2
data: 2026-08-28
tipo: exercicio
tema: Treino BP + DRE no estilo dos quizzes (gerado sob medida pros erros mapeados)
status: completo
contract_version: 1
tags: [exercicio, treino]
---
""",
        "final_sha256": "dcc486538df3ab26a7b38ca2929cb5b55157cbd339e0ad986cf0123c2e3f4578",
    },
    {
        "source": "ContabilidadeFinanceira/Aulas/08.28/TreinoBanhoEBicho_Gabarito.md",
        "destination": "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/TreinoBanhoEBicho_Gabarito.md",
        "introduced_commit": SOURCE_TIP,
        "content_commit": SOURCE_TIP,
        "source_blob_oid": "cee3a952af0273b57831292830341e33a1172802",
        "source_sha256": "a5aa305cc100d22dc1d9638b2921173e845cfddbae8dcb7b9d0c579b8a260f03",
        "source_size_bytes": 4269,
        "subject_id": "contabilidade-financeira",
        "class_date": "2026-08-28",
        "kind": "gabarito",
        "topic": "Gabarito comentado do treino Pet Shop Banho & Bicho",
        "frontmatter": """---
materias: [contabilidade-financeira]
semestre: 2026.2
data: 2026-08-28
tipo: gabarito
tema: Gabarito comentado do treino Pet Shop Banho & Bicho
status: completo
contract_version: 1
tags: [exercicio, gabarito]
---
""",
        "final_sha256": "d1cd6a427559f8b98226ea20960c38e3949caba679c7f4ff1ddf7a0c19c68f6c",
    },
)


class ImportError(RuntimeError):
    pass


def _git(root: Path, *args: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True
    )
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _body(payload: bytes) -> bytes:
    if not payload.startswith(b"---\n"):
        raise ImportError("source note has no frontmatter")
    closing = payload.find(b"\n---\n", 4)
    if closing < 0:
        raise ImportError("source note has unterminated frontmatter")
    return payload[closing + len(b"\n---\n") :]


def build_outputs(root: Path) -> tuple[dict[PurePosixPath, bytes], bytes]:
    authority_commit = str(_git(root, "rev-parse", "HEAD"))
    authority_tree = str(_git(root, "rev-parse", "HEAD^{tree}"))
    source_base_tree = str(_git(root, "rev-parse", f"{SOURCE_BASE}^{{tree}}"))
    source_tip_tree = str(_git(root, "rev-parse", f"{SOURCE_TIP}^{{tree}}"))
    outputs: dict[PurePosixPath, bytes] = {}
    manifest_records: list[dict[str, object]] = []

    for spec in RECORDS:
        source = str(spec["source"])
        destination = unicodedata.normalize("NFC", str(spec["destination"]))
        if PurePosixPath(destination).is_absolute() or ".." in PurePosixPath(destination).parts:
            raise ImportError(f"unsafe destination: {destination}")
        blob_oid = str(spec["source_blob_oid"])
        observed_oid = str(
            _git(root, "rev-parse", f"{spec['content_commit']}:{source}")
        )
        if observed_oid != blob_oid:
            raise ImportError(f"source blob authority diverged: {source}")
        original = bytes(_git(root, "cat-file", "blob", blob_oid, binary=True))
        if len(original) != spec["source_size_bytes"] or _sha256(original) != spec["source_sha256"]:
            raise ImportError(f"source bytes diverged: {source}")
        original_body = _body(original)
        final = str(spec["frontmatter"]).encode("utf-8") + original_body
        if _sha256(final) != spec["final_sha256"]:
            raise ImportError(f"final bytes diverged: {destination}")
        relative = PurePosixPath(destination)
        if relative in outputs:
            raise ImportError(f"duplicate destination: {destination}")
        outputs[relative] = final
        body_hash = _sha256(original_body)
        manifest_records.append(
            {
                "source": source,
                "destination": destination,
                "introduced_commit": spec["introduced_commit"],
                "content_commit": spec["content_commit"],
                "source_blob_oid": blob_oid,
                "source_sha256": spec["source_sha256"],
                "source_size_bytes": spec["source_size_bytes"],
                "source_mode": "100644",
                "subject_id": spec["subject_id"],
                "class_date": spec["class_date"],
                "kind": spec["kind"],
                "topic": spec["topic"],
                "original_body_sha256": body_hash,
                "final_body_sha256": body_hash,
                "final_sha256": _sha256(final),
                "final_size_bytes": len(final),
                "final_mode": "100644",
                "content_class": "metadata_transform",
                "transform_id": "none",
                "transform_occurrences": 0,
            }
        )

    manifest_records.sort(key=lambda item: str(item["destination"]).encode("utf-8"))
    authority: dict[str, object] = {
        "schema": SCHEMA,
        "schema_version": 1,
        "destination_authority_commit": authority_commit,
        "destination_authority_tree": authority_tree,
        "source_base_commit": SOURCE_BASE,
        "source_base_tree": source_base_tree,
        "source_tip_commit": SOURCE_TIP,
        "source_tip_tree": source_tip_tree,
        "source_commits": list(SOURCE_COMMITS),
        "record_count": len(manifest_records),
        "metadata_transform_count": len(manifest_records),
        "body_transform_count": 0,
        "records": manifest_records,
    }
    canonical = json.dumps(
        authority, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    authority["aggregate_sha256"] = _sha256(canonical)
    manifest_bytes = (
        json.dumps(authority, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")
    return outputs, manifest_bytes


def apply(root: Path, *, check: bool) -> str:
    outputs, manifest = build_outputs(root)
    expected = {**outputs, MANIFEST: manifest}
    observed: dict[PurePosixPath, tuple[bytes, int]] = {}
    for relative in expected:
        target = root / relative
        try:
            metadata = target.lstat()
        except FileNotFoundError:
            continue
        if not stat.S_ISREG(metadata.st_mode):
            raise ImportError(f"output is not a regular file: {relative}")
        observed[relative] = (target.read_bytes(), stat.S_IMODE(metadata.st_mode))
    if len(observed) == len(expected):
        authenticated = {
            relative: (payload, 0o644) for relative, payload in expected.items()
        }
        if observed != authenticated:
            raise ImportError("existing live-delta outputs diverged")
        return "no_op"
    if observed:
        raise ImportError("partial live-delta state")
    if check:
        return "planned"

    for relative, payload in expected.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(
            prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
        )
        try:
            os.fchmod(descriptor, 0o644)
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.link(temporary, target)
            os.unlink(temporary)
        except BaseException:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise
    return "applied"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    root = arguments.vault.resolve()
    status = apply(root, check=arguments.check)
    print(f"status={status} records={len(RECORDS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
