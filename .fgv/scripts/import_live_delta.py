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
FIRST_DELTA_COMMIT = "a81ff3df175c8d74d9523aaf83f0475fed6af94e"
REVISION_COMMIT = "a93c71f599f5d4fa9568946250f0958b2c28b64d"
FIRST_DELTA_TIP = "59c8c4407dd51b10c23695ddb4328ebf5372f0ea"
MATERIAL_COMMIT = "96e208f6e543fa69a7aba7ba74a068f8c4f2b6fe"
ROGERS_COMMIT = "d1d006b2991bc31b3a4c850ce78be2055bf33356"
FINAL_NOTES_COMMIT = "de77ca4378362451c552467ace03327e97ee15b3"
SOURCE_TIP = "cf8fe8c440a4dd442490afee62c0119a7db5ef9c"
SOURCE_COMMITS = (
    FIRST_DELTA_COMMIT,
    REVISION_COMMIT,
    FIRST_DELTA_TIP,
    MATERIAL_COMMIT,
    ROGERS_COMMIT,
    FINAL_NOTES_COMMIT,
    SOURCE_TIP,
)
DESTINATION_AUTHORITY = "c840413926da944254edb57b14564cf68c001e3b"
DESTINATION_AUTHORITY_TREE = "d91754bd4026d690d9fe7b115663eef28182c4e4"
MANIFEST = PurePosixPath("30 Sistema/Estado/live-delta-manifest.json")
REVISION_DESTINATION = PurePosixPath(
    "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/"
    "Revisao - Revisão de erros dos quizzes (Delícia Gelada, Sing's, "
    "Nosso Doce Amor, Lojas Paulistas).md"
)
PREVIOUS_OUTPUT_SHA256 = {
    REVISION_DESTINATION: "e224375bdaeadb677ef25104c92a3f806e9e1bb218e65dc03c2f7e5d85d69289",
    MANIFEST: "eae3d1819a67511e87d1192f46b43585214f172f7b81784cd23f2519cc8f605b",
}


RECORDS = (
    {
        "source": "ContabilidadeFinanceira/Aulas/08.28/RevisaoErrosQuizzes.md",
        "destination": (
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/"
            "Revisao - Revisão de erros dos quizzes (Delícia Gelada, Sing's, "
            "Nosso Doce Amor, Lojas Paulistas).md"
        ),
        "introduced_commit": SOURCE_COMMITS[0],
        "content_commit": FINAL_NOTES_COMMIT,
        "source_blob_oid": "8fd5f2f2af90d98b62bc96ba7a1e2d9dacc42567",
        "source_sha256": "86d47e270d77107f2b573a01c27cb217ad4b6ed2727a4bc941ef6ee9d3a55670",
        "source_size_bytes": 9635,
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
        "final_sha256": "ae100d5c6d57c4168c24539b7317cb8280fd89a1c4029d98639e7bfcc82f28d4",
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
        "introduced_commit": FIRST_DELTA_TIP,
        "content_commit": FIRST_DELTA_TIP,
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
        "introduced_commit": FIRST_DELTA_TIP,
        "content_commit": FIRST_DELTA_TIP,
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
    {
        "source": "ContabilidadeFinanceira/Aulas/08.26/Atividade_Cia_NaMeta_Resolvida.docx",
        "destination": (
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.26/Material/"
            "Atividade_Cia_NaMeta_Resolvida.docx"
        ),
        "introduced_commit": MATERIAL_COMMIT,
        "content_commit": MATERIAL_COMMIT,
        "source_blob_oid": "2c80ae6cfef981e97959890e00fa97176e32353d",
        "source_sha256": "5c154799e40c4b36f82eeb15d2f132deafa33513fd76810aa786203eac89e7cc",
        "source_size_bytes": 38356,
        "subject_id": "contabilidade-financeira",
        "class_date": "2026-08-26",
        "kind": "material",
        "topic": "Atividade Cia Na Meta resolvida",
        "frontmatter": None,
        "final_sha256": "5c154799e40c4b36f82eeb15d2f132deafa33513fd76810aa786203eac89e7cc",
    },
    {
        "source": "ContabilidadeFinanceira/Aulas/08.26/Atividade_Cia_NaMeta_Resolvida.pdf",
        "destination": (
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.26/Material/"
            "Atividade_Cia_NaMeta_Resolvida.pdf"
        ),
        "introduced_commit": MATERIAL_COMMIT,
        "content_commit": MATERIAL_COMMIT,
        "source_blob_oid": "02e6cf2050801829b9525cc36554dcf567fc17d3",
        "source_sha256": "cf49e682601f9abcdb2af505d753dc2dd3ba8b0b8af6593ee5f46cefee31aa79",
        "source_size_bytes": 27166,
        "subject_id": "contabilidade-financeira",
        "class_date": "2026-08-26",
        "kind": "material",
        "topic": "Atividade Cia Na Meta resolvida",
        "frontmatter": None,
        "final_sha256": "cf49e682601f9abcdb2af505d753dc2dd3ba8b0b8af6593ee5f46cefee31aa79",
    },
    {
        "source": "ContabilidadeFinanceira/Aulas/08.28/TreinoCorpoEmFoco_Enunciado.md",
        "destination": "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/TreinoCorpoEmFoco_Enunciado.md",
        "introduced_commit": FINAL_NOTES_COMMIT,
        "content_commit": FINAL_NOTES_COMMIT,
        "source_blob_oid": "4f00bc38bd24c3211dc1a0f5c909048220e22a23",
        "source_sha256": "402cc477f67083bbdee3634d064819f3d6b266b87aaf731565bd4d7f87f37c83",
        "source_size_bytes": 4089,
        "subject_id": "contabilidade-financeira",
        "class_date": "2026-08-28",
        "kind": "exercicio",
        "topic": "Treino 3 BP + DRE com estrutura nova (antecipadas do BP inicial, aporte, IR, dividendo escondido)",
        "frontmatter": """---
materias: [contabilidade-financeira]
semestre: 2026.2
data: 2026-08-28
tipo: exercicio
tema: Treino 3 BP + DRE com estrutura nova (antecipadas do BP inicial, aporte, IR, dividendo escondido)
status: completo
contract_version: 1
tags: [exercicio, treino]
---
""",
        "final_sha256": "dc6cfafe5ea89f6ebf7d7e6c0310f5c45bc222ac277ed2010ee069fbb9cda539",
    },
    {
        "source": "ContabilidadeFinanceira/Aulas/08.28/TreinoCorpoEmFoco_Gabarito.md",
        "destination": "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/TreinoCorpoEmFoco_Gabarito.md",
        "introduced_commit": FINAL_NOTES_COMMIT,
        "content_commit": FINAL_NOTES_COMMIT,
        "source_blob_oid": "9723e4df09e0f1658a0df3369f550a42ccebe1e9",
        "source_sha256": "49192710b2e23a04eb10b882b8323aeb1d2021430f14a353b61f64a0e8774abe",
        "source_size_bytes": 4632,
        "subject_id": "contabilidade-financeira",
        "class_date": "2026-08-28",
        "kind": "gabarito",
        "topic": "Gabarito comentado do treino Academia Corpo em Foco",
        "frontmatter": """---
materias: [contabilidade-financeira]
semestre: 2026.2
data: 2026-08-28
tipo: gabarito
tema: Gabarito comentado do treino Academia Corpo em Foco
status: completo
contract_version: 1
tags: [exercicio, gabarito]
---
""",
        "final_sha256": "b93b12f8f0189c57b50121bce6883627764f036c3f25cede987172aa836d8eed",
    },
    {
        "source": "ContabilidadeFinanceira/Aulas/08.28/TreinoNavalhaDeOuro_Enunciado.md",
        "destination": "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/TreinoNavalhaDeOuro_Enunciado.md",
        "introduced_commit": FINAL_NOTES_COMMIT,
        "content_commit": FINAL_NOTES_COMMIT,
        "source_blob_oid": "fd5c0d50f9ea1845c48b24ffa10174622482697b",
        "source_sha256": "d8f5d652ab763a067da485bb1521e3e318d59116ac91b346b44c6b02616ad17c",
        "source_size_bytes": 3572,
        "subject_id": "contabilidade-financeira",
        "class_date": "2026-08-28",
        "kind": "exercicio",
        "topic": "Treino 2 BP + DRE no estilo dos quizzes (variações novas das pegadinhas)",
        "frontmatter": """---
materias: [contabilidade-financeira]
semestre: 2026.2
data: 2026-08-28
tipo: exercicio
tema: Treino 2 BP + DRE no estilo dos quizzes (variações novas das pegadinhas)
status: completo
contract_version: 1
tags: [exercicio, treino]
---
""",
        "final_sha256": "6271d8baab7f61e6b5556b8fa7de7efdf2fd7e7dabff9979b2b5544eab8de6f9",
    },
    {
        "source": "ContabilidadeFinanceira/Aulas/08.28/TreinoNavalhaDeOuro_Gabarito.md",
        "destination": "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/TreinoNavalhaDeOuro_Gabarito.md",
        "introduced_commit": FINAL_NOTES_COMMIT,
        "content_commit": FINAL_NOTES_COMMIT,
        "source_blob_oid": "ce549b019c9040319b6c2d0ecb9ed7183e94b2b3",
        "source_sha256": "eda24340edef3419670f6515ebb0c6e1c4a889da98214a185d2b6c46ff004b00",
        "source_size_bytes": 3948,
        "subject_id": "contabilidade-financeira",
        "class_date": "2026-08-28",
        "kind": "gabarito",
        "topic": "Gabarito comentado do treino Barbearia Navalha de Ouro",
        "frontmatter": """---
materias: [contabilidade-financeira]
semestre: 2026.2
data: 2026-08-28
tipo: gabarito
tema: Gabarito comentado do treino Barbearia Navalha de Ouro
status: completo
contract_version: 1
tags: [exercicio, gabarito]
---
""",
        "final_sha256": "434567559161d6cd933c966405a90592a09dfd312796c2873d86beebfbc02866",
    },
    {
        "source": "TecnologiaDadosNegocios/Aulas/09.04/PPT 5_TD_Modelos Digitais.pdf",
        "destination": "10 Matérias/TecnologiaDadosNegocios/Aulas/09.04/Material/PPT 5_TD_Modelos Digitais.pdf",
        "introduced_commit": MATERIAL_COMMIT,
        "content_commit": MATERIAL_COMMIT,
        "source_blob_oid": "4e5a66260d38ff4bf212df918dd7e0710b43e1e8",
        "source_sha256": "1c09ce085ed3e53bf0e86036be6678fe165ddc6d5efa06dd5e6b3017da3ab882",
        "source_size_bytes": 1319768,
        "subject_id": "tecnologia-dados-negocios",
        "class_date": "2026-09-04",
        "kind": "material",
        "topic": "Modelos digitais",
        "frontmatter": None,
        "final_sha256": "1c09ce085ed3e53bf0e86036be6678fe165ddc6d5efa06dd5e6b3017da3ab882",
    },
    {
        "source": "TecnologiaDadosNegocios/Aulas/09.04/Rogers_2007.pdf",
        "destination": "10 Matérias/TecnologiaDadosNegocios/Aulas/09.04/Material/Rogers_2007.pdf",
        "introduced_commit": ROGERS_COMMIT,
        "content_commit": ROGERS_COMMIT,
        "source_blob_oid": "33cbcad58b08e26245ba76007afd7c7c138c2b83",
        "source_sha256": "fcdded54c476adeeede34c67f165648e2899641e336b64f9e4f327598d93c42e",
        "source_size_bytes": 21551974,
        "subject_id": "tecnologia-dados-negocios",
        "class_date": "2026-09-04",
        "kind": "material",
        "topic": "Rogers 2007",
        "frontmatter": None,
        "final_sha256": "fcdded54c476adeeede34c67f165648e2899641e336b64f9e4f327598d93c42e",
    },
)


class ImportError(RuntimeError):
    pass


def _git_environment() -> dict[str, str]:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


def _git(root: Path, *args: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        env=_git_environment(),
        check=True,
        capture_output=True,
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


def _assert_source_at_tip(root: Path, source: str, blob_oid: str) -> None:
    observed = bytes(
        _git(root, "ls-tree", "-z", SOURCE_TIP, "--", source, binary=True)
    )
    expected = f"100644 blob {blob_oid}\t{source}\0".encode("utf-8")
    if observed != expected:
        raise ImportError(f"source tip entry diverged: {source}")


def build_outputs(root: Path) -> tuple[dict[PurePosixPath, bytes], bytes]:
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", DESTINATION_AUTHORITY, "HEAD"],
        cwd=root,
        env=_git_environment(),
        check=False,
        capture_output=True,
    )
    if ancestry.returncode != 0:
        raise ImportError("destination authority is not an ancestor of HEAD")
    destination_tree = str(
        _git(root, "rev-parse", f"{DESTINATION_AUTHORITY}^{{tree}}")
    )
    if destination_tree != DESTINATION_AUTHORITY_TREE:
        raise ImportError("destination authority tree diverged")
    for commit in (SOURCE_BASE, *SOURCE_COMMITS):
        reachable = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, SOURCE_TIP],
            cwd=root,
            env=_git_environment(),
            check=False,
            capture_output=True,
        )
        if reachable.returncode != 0:
            raise ImportError(f"source authority is not reachable from tip: {commit}")
    delta_bytes = bytes(
        _git(
            root,
            "diff",
            "--name-only",
            "--no-renames",
            "-z",
            SOURCE_BASE,
            SOURCE_TIP,
            binary=True,
        )
    )
    changed_sources = {
        unicodedata.normalize("NFC", raw.decode("utf-8"))
        for raw in delta_bytes.split(b"\0")
        if raw
    }
    declared_sources = {str(spec["source"]) for spec in RECORDS}
    if len(declared_sources) != len(RECORDS) or changed_sources != declared_sources:
        missing = sorted(changed_sources - declared_sources)
        extra = sorted(declared_sources - changed_sources)
        raise ImportError(
            f"live delta source coverage diverged: missing={missing!r} extra={extra!r}"
        )
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
        _assert_source_at_tip(root, source, blob_oid)
        observed_oid = str(
            _git(root, "rev-parse", f"{spec['content_commit']}:{source}")
        )
        if observed_oid != blob_oid:
            raise ImportError(f"source blob authority diverged: {source}")
        original = bytes(_git(root, "cat-file", "blob", blob_oid, binary=True))
        if len(original) != spec["source_size_bytes"] or _sha256(original) != spec["source_sha256"]:
            raise ImportError(f"source bytes diverged: {source}")
        frontmatter = spec["frontmatter"]
        if frontmatter is None:
            original_body = original
            final = original
            content_class = "byte-identical"
        else:
            original_body = _body(original)
            final = str(frontmatter).encode("utf-8") + original_body
            content_class = "metadata_transform"
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
                "content_class": content_class,
                "transform_id": "none",
                "transform_occurrences": 0,
            }
        )

    manifest_records.sort(key=lambda item: str(item["destination"]).encode("utf-8"))
    authority: dict[str, object] = {
        "schema": SCHEMA,
        "schema_version": 1,
        "destination_authority_commit": DESTINATION_AUTHORITY,
        "destination_authority_tree": DESTINATION_AUTHORITY_TREE,
        "source_base_commit": SOURCE_BASE,
        "source_base_tree": source_base_tree,
        "source_tip_commit": SOURCE_TIP,
        "source_tip_tree": source_tip_tree,
        "source_commits": list(SOURCE_COMMITS),
        "record_count": len(manifest_records),
        "metadata_transform_count": sum(
            record["content_class"] == "metadata_transform"
            for record in manifest_records
        ),
        "byte_identical_count": sum(
            record["content_class"] == "byte-identical"
            for record in manifest_records
        ),
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


def _classify_existing(
    relative: PurePosixPath, observed: bytes | None, expected: bytes
) -> str:
    if observed is None:
        return "missing"
    if observed == expected:
        return "current"
    previous_sha256 = PREVIOUS_OUTPUT_SHA256.get(relative)
    if previous_sha256 is not None and _sha256(observed) == previous_sha256:
        return "upgrade"
    raise ImportError(f"existing live-delta output diverged: {relative}")


def _publish(target: Path, payload: bytes, *, replace: bool) -> None:
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
        if replace:
            os.replace(temporary, target)
        else:
            os.link(temporary, target)
            os.unlink(temporary)
        directory = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def apply(root: Path, *, check: bool) -> str:
    outputs, manifest = build_outputs(root)
    expected = {**outputs, MANIFEST: manifest}
    actions: dict[PurePosixPath, str] = {}
    for relative, payload in expected.items():
        target = root / relative
        try:
            metadata = target.lstat()
        except FileNotFoundError:
            observed = None
        else:
            if not stat.S_ISREG(metadata.st_mode):
                raise ImportError(f"output is not a regular file: {relative}")
            if stat.S_IMODE(metadata.st_mode) != 0o644:
                raise ImportError(f"output mode diverged: {relative}")
            observed = target.read_bytes()
        actions[relative] = _classify_existing(relative, observed, payload)

    if all(action == "current" for action in actions.values()):
        return "no_op"
    if check:
        return "planned"

    for relative, payload in expected.items():
        action = actions[relative]
        if action == "current":
            continue
        target = root / relative
        if action == "upgrade":
            current = target.read_bytes()
            if _classify_existing(relative, current, payload) != "upgrade":
                raise ImportError(f"output changed during upgrade: {relative}")
            _publish(target, payload, replace=True)
        elif action == "missing":
            _publish(target, payload, replace=False)
        else:
            raise AssertionError(f"unexpected action: {action}")
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
