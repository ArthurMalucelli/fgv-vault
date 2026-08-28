# FGV Workflow Unification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Unificar o workflow FGV em um core canônico oculto e versionado, com ingestão Plaud idempotente, raw imutável, adapters finos para Codex e Claude, pacote seguro para Hermes e comportamento verificável por testes de conformance.

**Architecture:** O diretório oculto `.fgv/` será a única fonte das regras, schemas, templates, configuração e código determinístico. Codex, Claude e Hermes apenas traduzirão ferramentas do runtime para o mesmo plano transacional, enquanto artefatos humanos continuarão em `00 Home/`, `10 Matérias/`, `20 Conhecimento/` e `30 Sistema/`. Git e Google Calendar serão efeitos externos explícitos, idempotentes e auditáveis, nunca lógica escondida dentro das skills.

**Tech Stack:** Python 3.12, pytest, Hypothesis, jsonschema, PyYAML, Markdown, JSON, JSONL, Git CLI, Obsidian, Google Calendar adapters.

---

## Decisões fixas

- O core canônico fica somente em `.fgv/`. `30 Sistema/` contém documentação, estado materializado e pacotes de distribuição, não uma segunda cópia editável das regras.
- A pasta de aula permanece `Aulas/MM.DD/`, com dois dígitos.
- A data não aparece no nome visível do arquivo dentro da pasta da aula.
- Os nomes processados são `Transcrito - <tema curto>.md`, `Resumo - <tema curto>.md` e `Revisao - <tema curto>.md`.
- O ano completo permanece no YAML, no `id`, no manifest e no `transaction_id`.
- O raw Plaud é imutável. O pipeline copia bytes para `Fontes/`, valida o hash e nunca apaga a origem externa.
- `transaction_id` é determinístico a partir de versão do contrato, hash raw, matéria e data resolvida.
- Conceitos novos são gated. Extração de cinco a quinze conceitos por aula deixa de ser uma regra.
- Tasks são alterações locais no vault. Google Calendar é uma fila de intents aplicada por adapters com connector.
- Cancelamento e mudança de data ou horário no Calendar exigem confirmação explícita.
- No Mac, Obsidian Git é o único processo autorizado a sincronizar, commitar e enviar. Codex e Claude não executam Git de rede.
- No VPS, um único wrapper `fgv-sync` possui Git. Hermes, Eclass e WhatsApp não executam comandos Git diretamente.
- O instalador desta fase apenas produz bundles em staging. Ele deve rejeitar `~/.agents/`, `~/.claude/` e `/root/.hermes/` como destinos.
- Nenhuma instalação live, merge em `main`, alteração no VPS ou migração do vault vivo faz parte da implementação desta branch.

## Mapa de arquivos

### Core canônico

- Create: `.fgv/VERSION`, versão textual do contrato.
- Create: `.fgv/CORE.md`, invariantes e máquina de estados do workflow.
- Create: `.fgv/pyproject.toml`, pacote Python e dependências de teste.
- Create: `.fgv/config/subjects.json`, registry canônico de matérias, aliases, pastas e tags.
- Create: `.fgv/config/sync-ownership.json`, ownership Git por runtime.
- Create: `.fgv/schemas/source-manifest.schema.json`, contrato do raw preservado.
- Create: `.fgv/schemas/ingest-plan.schema.json`, contrato do plano transacional.
- Create: `.fgv/schemas/calendar-intent.schema.json`, contrato de efeitos Calendar.
- Create: `.fgv/schemas/catalog-record.schema.json`, contrato do catálogo materializado.

### Biblioteca determinística

- Create: `.fgv/src/fgv_workflow/models.py`, dataclasses e enums compartilhados.
- Create: `.fgv/src/fgv_workflow/schema.py`, carregamento e validação de JSON Schema.
- Create: `.fgv/src/fgv_workflow/subjects.py`, resolução de matéria e aliases.
- Create: `.fgv/src/fgv_workflow/naming.py`, caminhos `MM.DD` e nomes sem data.
- Create: `.fgv/src/fgv_workflow/source_store.py`, hash, cópia atômica, manifest e idempotência.
- Create: `.fgv/src/fgv_workflow/date_resolution.py`, resolução da data por evidência.
- Create: `.fgv/src/fgv_workflow/plaud.py`, planejamento e renderização dos derivados.
- Create: `.fgv/src/fgv_workflow/concepts.py`, promoção gated e fila de candidatos.
- Create: `.fgv/src/fgv_workflow/tasks.py`, criação e deduplicação de tasks.
- Create: `.fgv/src/fgv_workflow/calendar.py`, intents e idempotência do Calendar.
- Create: `.fgv/src/fgv_workflow/catalog.py`, catálogo e dashboard snapshot.
- Create: `.fgv/src/fgv_workflow/sync.py`, política de ownership e wrapper Git do Hermes.
- Create: `.fgv/src/fgv_workflow/adapters.py`, geração dos adapters finos.
- Create: `.fgv/src/fgv_workflow/hermes_package.py`, bundle do Hermes sem instalação.
- Create: `.fgv/src/fgv_workflow/migration.py`, inventário e migração dry-run por manifest.
- Create: `.fgv/src/fgv_workflow/cli.py`, comandos públicos usados por todos os runtimes.

### Templates, adapters e distribuição

- Create: `.fgv/templates/transcrito.md`.
- Create: `.fgv/templates/resumo.md`.
- Create: `.fgv/templates/revisao.md`.
- Create: `.fgv/templates/conceito.md`.
- Create: `.fgv/adapters/codex/SKILL.md.tmpl`.
- Create: `.fgv/adapters/claude/SKILL.md.tmpl`.
- Create: `.fgv/adapters/hermes/SKILL.md.tmpl`.
- Create: `.fgv/prompts/hermes.md`.
- Create: `.fgv/scripts/stage_adapters.py`.
- Create: `.fgv/scripts/build_hermes_package.py`.
- Create: `.fgv/scripts/validate_vault.py`.
- Create: `30 Sistema/Hermes/README.md`.
- Create: `30 Sistema/Hermes/eclass-path-migration.json`.
- Create: `30 Sistema/Estado/adapter-staging/.gitkeep`.

### Testes e fixtures

- Create: `.fgv/tests/test_contract_files.py`.
- Create: `.fgv/tests/test_schemas.py`.
- Create: `.fgv/tests/test_subjects_and_naming.py`.
- Create: `.fgv/tests/test_source_store.py`.
- Create: `.fgv/tests/test_date_resolution.py`.
- Create: `.fgv/tests/test_plaud_pipeline.py`.
- Create: `.fgv/tests/test_concepts.py`.
- Create: `.fgv/tests/test_tasks_and_calendar.py`.
- Create: `.fgv/tests/test_catalog.py`.
- Create: `.fgv/tests/test_sync.py`.
- Create: `.fgv/tests/test_adapter_staging.py`.
- Create: `.fgv/tests/test_hermes_package.py`.
- Create: `.fgv/tests/test_migration.py`.
- Create: `.fgv/tests/test_conformance.py`.
- Create: `.fgv/tests/fixtures/plaud/contabilidade-2026-08-28.txt`.
- Create: `.fgv/tests/fixtures/plaud/contabilidade-analysis.json`.
- Create: `.fgv/tests/fixtures/calendar/events.json`.
- Create: `.fgv/tests/fixtures/expected/ingest-plan.json`.

## Preparação da execução

- [ ] **Step 1: Confirmar que a implementação ocorre na worktree isolada**

Run:

```bash
pwd
git branch --show-current
git status --short
```

Expected:

```text
/Users/arthurmalucelli/Documents/Codex/2026-08-27/new-chat/work/fgv-vault-plan-b
codex/vault-plan-b
 M "30 Sistema/Specs/2026-08-28-vault-plan-b-design.md"
```

O arquivo de design já modificado não pertence à implementação deste plano. Não o reverta, não o inclua em commits e não o edite.

- [ ] **Step 2: Criar ambiente de teste isolado**

Run:

```bash
python3 -m venv .fgv-venv
.fgv-venv/bin/python -m pip install --upgrade pip
```

Expected: os dois comandos terminam com exit code `0`. Não adicionar `.fgv-venv/` ao Git.

### Task 1: Bootstrap do core canônico e registry de matérias

**Files:**

- Create: `.fgv/VERSION`
- Create: `.fgv/CORE.md`
- Create: `.fgv/pyproject.toml`
- Create: `.fgv/config/subjects.json`
- Create: `.fgv/src/fgv_workflow/__init__.py`
- Test: `.fgv/tests/test_contract_files.py`

- [ ] **Step 1: Escrever o teste que exige um único core oculto**

Create `.fgv/tests/test_contract_files.py`:

```python
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / ".fgv"


def test_core_version_and_invariants_exist() -> None:
    assert (CORE / "VERSION").read_text(encoding="utf-8") == "1\n"
    text = (CORE / "CORE.md").read_text(encoding="utf-8")
    assert "raw é imutável" in text
    assert "transaction_id" in text
    assert "CalendarIntent" in text
    assert "Codex e Claude não executam Git de rede" in text


def test_subject_registry_has_only_current_subjects() -> None:
    payload = json.loads(
        (CORE / "config" / "subjects.json").read_text(encoding="utf-8")
    )
    assert payload["schema_version"] == 1
    assert {item["id"] for item in payload["subjects"]} == {
        "contabilidade-financeira",
        "direito-empresarial",
        "estatistica-2",
        "estudos-organizacionais",
        "matematica-aplicada",
        "psicologia",
        "tecnologia-dados-negocios",
    }
    assert all(item["folder"] for item in payload["subjects"])
    assert all(item["task_tag"].startswith("#") for item in payload["subjects"])


def test_no_second_editable_core_is_declared() -> None:
    assert not (ROOT / "30 Sistema" / "Skills" / "fgv-core").exists()
```

- [ ] **Step 2: Rodar o teste e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_contract_files.py -q
```

Expected: FAIL com `FileNotFoundError` para `.fgv/VERSION`.

- [ ] **Step 3: Criar o pacote, a versão, o contrato e o registry mínimos**

Create `.fgv/pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"

[project]
name = "fgv-workflow"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = [
  "jsonschema>=4.23,<5",
  "PyYAML>=6.0,<7",
]

[project.optional-dependencies]
test = [
  "pytest>=8.3,<9",
  "hypothesis>=6.112,<7",
]

[project.scripts]
fgv-workflow = "fgv_workflow.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
```

Create `.fgv/VERSION` with exactly:

```text
1
```

Create `.fgv/src/fgv_workflow/__init__.py`:

```python
"""Deterministic core for the FGV academic workflow."""

CONTRACT_VERSION = 1
```

Create `.fgv/config/subjects.json`:

```json
{
  "schema_version": 1,
  "subjects": [
    {
      "id": "contabilidade-financeira",
      "display_name": "Contabilidade Financeira",
      "folder": "ContabilidadeFinanceira",
      "task_tag": "#cont",
      "aliases": ["contabilidade", "cont", "contabilidadefinanceira"]
    },
    {
      "id": "direito-empresarial",
      "display_name": "Direito Empresarial",
      "folder": "DireitoEmpresarial",
      "task_tag": "#dir",
      "aliases": ["direito empresarial", "dir", "direitoempresarial"]
    },
    {
      "id": "estatistica-2",
      "display_name": "Estatística II",
      "folder": "Estatistica2",
      "task_tag": "#est2",
      "aliases": ["estatística ii", "estatistica ii", "estatistica2", "est2"]
    },
    {
      "id": "estudos-organizacionais",
      "display_name": "Estudos Organizacionais",
      "folder": "EstudosOrganizacionais",
      "task_tag": "#eo",
      "aliases": ["estudos organizacionais", "eo", "estudosorganizacionais"]
    },
    {
      "id": "matematica-aplicada",
      "display_name": "Matemática Aplicada I",
      "folder": "MatemáticaAplicada",
      "task_tag": "#ma1",
      "aliases": ["matemática aplicada", "matematica aplicada", "ma1"]
    },
    {
      "id": "psicologia",
      "display_name": "Psicologia",
      "folder": "Psicologia",
      "task_tag": "#psi",
      "aliases": ["psicologia", "psi"]
    },
    {
      "id": "tecnologia-dados-negocios",
      "display_name": "Tecnologia, Dados e Negócios",
      "folder": "TecnologiaDadosNegocios",
      "task_tag": "#tdn",
      "aliases": ["tecnologia dados negócios", "tecnologia dados negocios", "tdn"]
    }
  ]
}
```

Create `.fgv/CORE.md` with these normative sections:

```markdown
# FGV Workflow Contract v1

## Invariantes

- O raw é imutável, preservado byte a byte e nunca apagado pelo workflow.
- Toda derivação aponta para `source_sha256` e `transaction_id`.
- Matéria ou data ambígua interrompe a escrita e exige confirmação.
- Rerun com os mesmos inputs produz no-op ou o mesmo plano.
- Arquivo existente nunca é sobrescrito quando pertence a outra transação.
- Calendar é representado primeiro como `CalendarIntent` idempotente.
- Conceitos novos exigem critério explícito de promoção.
- Codex e Claude não executam Git de rede.
- Hermes usa somente o wrapper `fgv-sync` para Git.

## Estados

`preflight -> planned -> staged -> validated -> published -> side_effects_pending -> complete`

Qualquer falha antes de `published` preserva os arquivos canônicos anteriores. Falha de Calendar mantém a intent pendente e repetível.

## Identidade

`transaction_id = sha256("fgv:v1\\0" + source_sha256 + "\\0" + subject_id + "\\0" + class_date)[:20]`

## Naming

- Pasta: `10 Matérias/<folder>/Aulas/MM.DD/`.
- Transcrito: `Transcrito - <tema curto>.md`.
- Resumo: `Resumo - <tema curto>.md`.
- Revisão: `Revisao - <tema curto>.md`.
- Raw Plaud: `Fontes/Plaud - original.<ext>`, com sufixo numérico apenas em colisão real.
```

- [ ] **Step 4: Instalar o pacote em modo editável e rodar o teste**

Run:

```bash
.fgv-venv/bin/python -m pip install -e '.fgv[test]'
.fgv-venv/bin/python -m pytest .fgv/tests/test_contract_files.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 5: Fazer commit pequeno**

Run:

```bash
git add .fgv/VERSION .fgv/CORE.md .fgv/pyproject.toml .fgv/config/subjects.json .fgv/src/fgv_workflow/__init__.py .fgv/tests/test_contract_files.py
git commit -m "feat(fgv): add canonical workflow core"
```

Expected: commit criado sem incluir `30 Sistema/Specs/2026-08-28-vault-plan-b-design.md`.

### Task 2: Models tipados e schemas de fronteira

**Files:**

- Create: `.fgv/src/fgv_workflow/models.py`
- Create: `.fgv/src/fgv_workflow/schema.py`
- Create: `.fgv/schemas/source-manifest.schema.json`
- Create: `.fgv/schemas/ingest-plan.schema.json`
- Create: `.fgv/schemas/calendar-intent.schema.json`
- Create: `.fgv/schemas/catalog-record.schema.json`
- Test: `.fgv/tests/test_schemas.py`

- [ ] **Step 1: Escrever testes de payload válido e inválido**

Create `.fgv/tests/test_schemas.py`:

```python
from dataclasses import asdict

import pytest
from jsonschema import ValidationError

from fgv_workflow.models import SourceManifest
from fgv_workflow.schema import validate_payload


def valid_manifest() -> SourceManifest:
    return SourceManifest(
        schema_version=1,
        transaction_id="8d9f83f21788cc90e1d2",
        subject_id="contabilidade-financeira",
        class_date="2026-08-28",
        original_name="PLAUID_export.txt",
        raw_relpath=(
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/"
            "Fontes/Plaud - original.txt"
        ),
        source_sha256="sha256:" + "a" * 64,
        size_bytes=42,
        ingested_at="2026-08-28T10:30:00-03:00",
    )


def test_source_manifest_matches_schema() -> None:
    validate_payload("source-manifest", asdict(valid_manifest()))


def test_source_manifest_rejects_missing_hash() -> None:
    payload = asdict(valid_manifest())
    del payload["source_sha256"]
    with pytest.raises(ValidationError):
        validate_payload("source-manifest", payload)


def test_calendar_intent_requires_confirmation_flag() -> None:
    with pytest.raises(ValidationError):
        validate_payload(
            "calendar-intent",
            {
                "schema_version": 1,
                "action_id": "cal-123",
                "transaction_id": "tx-123",
                "action": "reschedule",
                "calendar_alias": "classes",
                "payload": {"event_id": "event-1"},
                "status": "pending"
            },
        )
```

- [ ] **Step 2: Rodar os testes e confirmar import failure**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_schemas.py -q
```

Expected: collection FAIL com `ModuleNotFoundError: No module named 'fgv_workflow.models'`.

- [ ] **Step 3: Criar models e validador com nomes estáveis**

Create `.fgv/src/fgv_workflow/models.py`:

```python
from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class SourceManifest:
    schema_version: int
    transaction_id: str
    subject_id: str
    class_date: str
    original_name: str
    raw_relpath: str
    source_sha256: str
    size_bytes: int
    ingested_at: str


@dataclass(frozen=True)
class DateEvidence:
    kind: Literal["explicit", "plaud", "transcript", "calendar", "mtime"]
    value: str
    confidence: float
    source: str


@dataclass(frozen=True)
class DateResolution:
    status: Literal["resolved", "ambiguous"]
    value: str | None
    confidence: float
    evidence: tuple[DateEvidence, ...]


@dataclass(frozen=True)
class CalendarIntent:
    schema_version: int
    action_id: str
    transaction_id: str
    action: Literal[
        "append_description",
        "update_location",
        "create_assessment",
        "mark_cancelled",
        "reschedule",
    ]
    calendar_alias: Literal["classes", "assessments"]
    payload: dict[str, Any]
    requires_confirmation: bool
    status: Literal["pending", "confirmed", "applied", "failed"]


@dataclass(frozen=True)
class IngestPlan:
    schema_version: int
    transaction_id: str
    contract_version: int
    subject_id: str
    class_date: str
    lesson_relpath: str
    source_sha256: str
    raw_relpath: str
    artifact_relpaths: tuple[str, ...]
    task_intents: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    calendar_intents: tuple[CalendarIntent, ...] = field(default_factory=tuple)
    concept_actions: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    requires_confirmation: bool = False
```

Create `.fgv/src/fgv_workflow/schema.py`:

```python
import json
from pathlib import Path
from typing import Any

from jsonschema import validate


SCHEMA_DIR = Path(__file__).resolve().parents[2] / "schemas"


def validate_payload(schema_name: str, payload: dict[str, Any]) -> None:
    schema_path = SCHEMA_DIR / f"{schema_name}.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(instance=payload, schema=schema)
```

Create the four schema files with draft 2020-12, `additionalProperties: false` and these required fields:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SourceManifest",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "transaction_id",
    "subject_id",
    "class_date",
    "original_name",
    "raw_relpath",
    "source_sha256",
    "size_bytes",
    "ingested_at"
  ],
  "properties": {
    "schema_version": {"const": 1},
    "transaction_id": {"type": "string", "minLength": 20},
    "subject_id": {"type": "string", "minLength": 1},
    "class_date": {"type": "string", "format": "date"},
    "original_name": {"type": "string", "minLength": 1},
    "raw_relpath": {"type": "string", "minLength": 1},
    "source_sha256": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"},
    "size_bytes": {"type": "integer", "minimum": 0},
    "ingested_at": {"type": "string", "format": "date-time"}
  }
}
```

Use the same strict shape for `ingest-plan.schema.json` and `calendar-intent.schema.json`. The Calendar schema must require `requires_confirmation` and constrain destructive actions with:

```json
{
  "if": {
    "properties": {
      "action": {"enum": ["mark_cancelled", "reschedule"]}
    }
  },
  "then": {
    "properties": {
      "requires_confirmation": {"const": true}
    }
  }
}
```

`catalog-record.schema.json` must require `id`, `tipo`, `materias`, `data`, `path`, `canonical_for_search` and `source_sha256`.

- [ ] **Step 4: Rodar os testes de schema**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_schemas.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 5: Commitar models e schemas**

Run:

```bash
git add .fgv/src/fgv_workflow/models.py .fgv/src/fgv_workflow/schema.py .fgv/schemas .fgv/tests/test_schemas.py
git commit -m "feat(fgv): define workflow boundary schemas"
```

Expected: um commit contendo somente models, schemas e seus testes.

### Task 3: Registry, pasta `MM.DD` e naming sem data no filename

**Files:**

- Create: `.fgv/src/fgv_workflow/subjects.py`
- Create: `.fgv/src/fgv_workflow/naming.py`
- Test: `.fgv/tests/test_subjects_and_naming.py`

- [ ] **Step 1: Escrever testes para aliases, caminhos e colisões**

Create `.fgv/tests/test_subjects_and_naming.py`:

```python
from datetime import date
from pathlib import Path

from fgv_workflow.naming import artifact_path, lesson_dir
from fgv_workflow.subjects import SubjectRegistry


def registry() -> SubjectRegistry:
    return SubjectRegistry.load_default()


def test_alias_resolves_to_canonical_subject() -> None:
    subject = registry().resolve("Contabilidade")
    assert subject.id == "contabilidade-financeira"
    assert subject.folder == "ContabilidadeFinanceira"


def test_lesson_path_uses_mm_dd_but_file_has_no_date(tmp_path: Path) -> None:
    subject = registry().resolve("cont")
    folder = lesson_dir(tmp_path, subject, date(2026, 8, 28))
    path = artifact_path(folder, "resumo", "DRE, provisões e arrendamentos")
    assert folder.relative_to(tmp_path).as_posix() == (
        "10 Matérias/ContabilidadeFinanceira/Aulas/08.28"
    )
    assert path.name == "Resumo - DRE, provisões e arrendamentos.md"
    assert "2026" not in path.name
    assert "08.28" not in path.name


def test_collision_gets_numeric_suffix_without_overwrite(tmp_path: Path) -> None:
    folder = tmp_path / "Aulas" / "08.28"
    folder.mkdir(parents=True)
    first = folder / "Resumo - DRE.md"
    first.write_text("existing", encoding="utf-8")
    assert artifact_path(folder, "resumo", "DRE").name == "Resumo - DRE - 02.md"
```

- [ ] **Step 2: Rodar o teste e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_subjects_and_naming.py -q
```

Expected: collection FAIL por ausência de `fgv_workflow.naming`.

- [ ] **Step 3: Implementar registry e naming**

Create `.fgv/src/fgv_workflow/subjects.py`:

```python
import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path


def normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


@dataclass(frozen=True)
class Subject:
    id: str
    display_name: str
    folder: str
    task_tag: str
    aliases: tuple[str, ...]


class SubjectRegistry:
    def __init__(self, subjects: tuple[Subject, ...]) -> None:
        self.subjects = subjects
        self._aliases = {
            normalize(alias): subject
            for subject in subjects
            for alias in (subject.id, subject.display_name, subject.folder, *subject.aliases)
        }

    @classmethod
    def load_default(cls) -> "SubjectRegistry":
        path = Path(__file__).resolve().parents[2] / "config" / "subjects.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            tuple(
                Subject(
                    id=item["id"],
                    display_name=item["display_name"],
                    folder=item["folder"],
                    task_tag=item["task_tag"],
                    aliases=tuple(item["aliases"]),
                )
                for item in payload["subjects"]
            )
        )

    def resolve(self, value: str) -> Subject:
        key = normalize(value)
        if key not in self._aliases:
            raise KeyError(f"unknown subject: {value}")
        return self._aliases[key]
```

Create `.fgv/src/fgv_workflow/naming.py`:

```python
import re
from datetime import date
from pathlib import Path

from .subjects import Subject


PREFIX = {
    "transcrito": "Transcrito",
    "resumo": "Resumo",
    "revisao": "Revisao",
}


def lesson_dir(vault_root: Path, subject: Subject, class_date: date) -> Path:
    return (
        vault_root
        / "10 Matérias"
        / subject.folder
        / "Aulas"
        / class_date.strftime("%m.%d")
    )


def clean_topic(topic: str) -> str:
    cleaned = re.sub(r"[/\\\\:*?\"<>|]", ",", topic)
    cleaned = re.sub(r"\\s+", " ", cleaned).strip(" .,-")
    if not 3 <= len(cleaned) <= 90:
        raise ValueError("topic must contain between 3 and 90 characters")
    return cleaned


def artifact_path(folder: Path, kind: str, topic: str) -> Path:
    base = f"{PREFIX[kind]} - {clean_topic(topic)}"
    candidate = folder / f"{base}.md"
    sequence = 2
    while candidate.exists():
        candidate = folder / f"{base} - {sequence:02d}.md"
        sequence += 1
    return candidate
```

- [ ] **Step 4: Rodar os testes de naming**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_subjects_and_naming.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 5: Commitar naming**

Run:

```bash
git add .fgv/src/fgv_workflow/subjects.py .fgv/src/fgv_workflow/naming.py .fgv/tests/test_subjects_and_naming.py
git commit -m "feat(fgv): add canonical subject and naming rules"
```

Expected: commit pequeno, sem renomear nenhuma nota real.

### Task 4: Raw imutável, hash, manifest e `transaction_id`

**Files:**

- Create: `.fgv/src/fgv_workflow/source_store.py`
- Test: `.fgv/tests/test_source_store.py`

- [ ] **Step 1: Escrever testes de preservação e idempotência**

Create `.fgv/tests/test_source_store.py`:

```python
from datetime import date, datetime, timezone
from pathlib import Path

from fgv_workflow.source_store import (
    ingest_source,
    make_transaction_id,
    sha256_file,
)


def test_raw_is_copied_byte_for_byte_and_source_survives(tmp_path: Path) -> None:
    source = tmp_path / "download" / "Plaud export.txt"
    source.parent.mkdir()
    source.write_bytes(b"speaker 1\\nconteudo original\\n")
    lesson = tmp_path / "vault" / "Aulas" / "08.28"

    result = ingest_source(
        vault_root=tmp_path / "vault",
        source=source,
        lesson_dir=lesson,
        subject_id="contabilidade-financeira",
        class_date=date(2026, 8, 28),
        ingested_at=datetime(2026, 8, 28, 13, 0, tzinfo=timezone.utc),
    )

    assert source.exists()
    assert result.raw_path.read_bytes() == source.read_bytes()
    assert result.raw_path.name == "Plaud - original.txt"
    assert result.manifest_path.name == "manifest.json"
    assert sha256_file(result.raw_path) == sha256_file(source)


def test_same_hash_is_a_no_op(tmp_path: Path) -> None:
    source = tmp_path / "Plaud.txt"
    source.write_text("same", encoding="utf-8")
    lesson = tmp_path / "Aulas" / "08.28"
    kwargs = {
        "vault_root": tmp_path,
        "source": source,
        "lesson_dir": lesson,
        "subject_id": "contabilidade-financeira",
        "class_date": date(2026, 8, 28),
        "ingested_at": datetime(2026, 8, 28, 13, 0, tzinfo=timezone.utc),
    }
    first = ingest_source(**kwargs)
    second = ingest_source(**kwargs)
    assert second.created is False
    assert second.transaction_id == first.transaction_id
    assert list((lesson / "Fontes").glob("Plaud - original*.txt")) == [first.raw_path]


def test_transaction_id_changes_with_date_or_subject() -> None:
    digest = "sha256:" + "f" * 64
    first = make_transaction_id(digest, "contabilidade-financeira", "2026-08-28")
    assert first == make_transaction_id(
        digest, "contabilidade-financeira", "2026-08-28"
    )
    assert first != make_transaction_id(
        digest, "contabilidade-financeira", "2026-08-29"
    )
```

- [ ] **Step 2: Rodar os testes e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_source_store.py -q
```

Expected: collection FAIL por ausência de `fgv_workflow.source_store`.

- [ ] **Step 3: Implementar o source store sem delete nem overwrite**

Create `.fgv/src/fgv_workflow/source_store.py` com esta API:

```python
import hashlib
import json
import os
import shutil
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path

from .models import SourceManifest
from .schema import validate_payload


@dataclass(frozen=True)
class IngestedSource:
    transaction_id: str
    raw_path: Path
    manifest_path: Path
    created: bool


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def make_transaction_id(
    source_sha256: str,
    subject_id: str,
    class_date: str,
) -> str:
    material = (
        "fgv:v1\\0" + source_sha256 + "\\0" + subject_id + "\\0" + class_date
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()[:20]


def _load_manifest(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": 1, "sources": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _atomic_write(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def ingest_source(
    vault_root: Path,
    source: Path,
    lesson_dir: Path,
    subject_id: str,
    class_date: date,
    ingested_at: datetime,
) -> IngestedSource:
    source_hash = sha256_file(source)
    tx = make_transaction_id(source_hash, subject_id, class_date.isoformat())
    sources_dir = lesson_dir / "Fontes"
    sources_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = sources_dir / "manifest.json"
    payload = _load_manifest(manifest_path)
    for item in payload["sources"]:
        if item["transaction_id"] == tx:
            return IngestedSource(
                transaction_id=tx,
                raw_path=vault_root / item["raw_relpath"],
                manifest_path=manifest_path,
                created=False,
            )

    suffix = source.suffix.lower() or ".txt"
    raw_path = sources_dir / f"Plaud - original{suffix}"
    sequence = 2
    while raw_path.exists():
        raw_path = sources_dir / f"Plaud - original - {sequence:02d}{suffix}"
        sequence += 1
    temporary = raw_path.with_suffix(raw_path.suffix + ".tmp")
    shutil.copyfile(source, temporary)
    if sha256_file(temporary) != source_hash:
        raise IOError("raw hash mismatch after copy")
    os.replace(temporary, raw_path)

    manifest = SourceManifest(
        schema_version=1,
        transaction_id=tx,
        subject_id=subject_id,
        class_date=class_date.isoformat(),
        original_name=source.name,
        raw_relpath=raw_path.relative_to(vault_root).as_posix(),
        source_sha256=source_hash,
        size_bytes=source.stat().st_size,
        ingested_at=ingested_at.isoformat(),
    )
    validate_payload("source-manifest", asdict(manifest))
    payload["sources"].append(asdict(manifest))
    _atomic_write(
        manifest_path,
        json.dumps(payload, ensure_ascii=False, indent=2) + "\\n",
    )
    return IngestedSource(tx, raw_path, manifest_path, True)
```

O argumento `vault_root` é obrigatório. A implementação não conta níveis de `parents`, porque layouts aninhados tornam essa inferência frágil.

- [ ] **Step 4: Rodar testes, incluindo um teste de propriedade**

Add to `.fgv/tests/test_source_store.py`:

```python
from hypothesis import given, strategies as st


@given(
    digest=st.text(
        alphabet="0123456789abcdef",
        min_size=64,
        max_size=64,
    )
)
def test_transaction_id_is_stable_for_any_hex_digest(digest: str) -> None:
    source_hash = "sha256:" + digest
    assert make_transaction_id(
        source_hash, "psicologia", "2026-08-20"
    ) == make_transaction_id(source_hash, "psicologia", "2026-08-20")
```

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_source_store.py -q
```

Expected:

```text
4 passed
```

- [ ] **Step 5: Commitar a camada de raw**

Run:

```bash
git add .fgv/src/fgv_workflow/source_store.py .fgv/tests/test_source_store.py
git commit -m "feat(fgv): preserve Plaud raw with manifests"
```

Expected: nenhuma remoção ou movimentação de arquivo existente no diff.

### Task 5: Resolver data por evidência, não pelo relógio

**Files:**

- Create: `.fgv/src/fgv_workflow/date_resolution.py`
- Test: `.fgv/tests/test_date_resolution.py`

- [ ] **Step 1: Escrever casos de resolução, conflito e evidência fraca**

Create `.fgv/tests/test_date_resolution.py`:

```python
from fgv_workflow.date_resolution import resolve_class_date
from fgv_workflow.models import DateEvidence


def evidence(kind: str, value: str, confidence: float) -> DateEvidence:
    return DateEvidence(
        kind=kind,
        value=value,
        confidence=confidence,
        source=f"fixture:{kind}",
    )


def test_explicit_date_beats_file_mtime() -> None:
    result = resolve_class_date(
        (
            evidence("explicit", "2026-08-28", 1.0),
            evidence("mtime", "2026-08-29", 0.4),
        )
    )
    assert result.status == "resolved"
    assert result.value == "2026-08-28"


def test_conflicting_high_confidence_dates_are_ambiguous() -> None:
    result = resolve_class_date(
        (
            evidence("plaud", "2026-08-27", 0.95),
            evidence("calendar", "2026-08-28", 0.95),
        )
    )
    assert result.status == "ambiguous"
    assert result.value is None


def test_mtime_alone_never_authorizes_write() -> None:
    result = resolve_class_date((evidence("mtime", "2026-08-28", 0.4),))
    assert result.status == "ambiguous"
    assert result.value is None
```

- [ ] **Step 2: Rodar e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_date_resolution.py -q
```

Expected: FAIL por módulo ausente.

- [ ] **Step 3: Implementar a política de evidência**

Create `.fgv/src/fgv_workflow/date_resolution.py`:

```python
from collections import defaultdict

from .models import DateEvidence, DateResolution


MIN_AUTO_CONFIDENCE = 0.90


def resolve_class_date(
    evidence: tuple[DateEvidence, ...],
) -> DateResolution:
    by_value: dict[str, list[DateEvidence]] = defaultdict(list)
    for item in evidence:
        by_value[item.value].append(item)
    strong = {
        value: items
        for value, items in by_value.items()
        if max(item.confidence for item in items) >= MIN_AUTO_CONFIDENCE
    }
    if len(strong) != 1:
        return DateResolution(
            status="ambiguous",
            value=None,
            confidence=max(
                (item.confidence for item in evidence),
                default=0.0,
            ),
            evidence=evidence,
        )
    value, items = next(iter(strong.items()))
    confidence = max(item.confidence for item in items)
    return DateResolution(
        status="resolved",
        value=value,
        confidence=confidence,
        evidence=evidence,
    )
```

Adapters devem fornecer evidências nesta ordem de preferência: data confirmada pelo usuário, metadata Plaud, data dita no transcript, match único no Calendar, mtime. O core não consulta o relógio para inventar a data da aula.

- [ ] **Step 4: Rodar os testes**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_date_resolution.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 5: Commitar a resolução de data**

Run:

```bash
git add .fgv/src/fgv_workflow/date_resolution.py .fgv/tests/test_date_resolution.py
git commit -m "feat(fgv): resolve class date from evidence"
```

Expected: commit sem referência a `date.today()` ou `datetime.now()` como decisão de data da aula.

### Task 6: Pipeline Plaud e templates de aprendizagem

**Files:**

- Create: `.fgv/src/fgv_workflow/plaud.py`
- Create: `.fgv/templates/transcrito.md`
- Create: `.fgv/templates/resumo.md`
- Create: `.fgv/templates/revisao.md`
- Create: `.fgv/tests/fixtures/plaud/contabilidade-2026-08-28.txt`
- Create: `.fgv/tests/fixtures/plaud/contabilidade-analysis.json`
- Test: `.fgv/tests/test_plaud_pipeline.py`

- [ ] **Step 1: Criar fixture raw e analysis estruturado**

`contabilidade-2026-08-28.txt` deve conter exatamente:

```text
Speaker 1: Hoje vamos fechar DRE e provisões.
Speaker 2: Professor, provisão sempre tira caixa?
Speaker 1: Não. Provisão afeta competência agora e caixa apenas quando houver pagamento.
Speaker 1: Isso cai na prova. Comparem DRE, balanço e fluxo de caixa.
Speaker 1: Na próxima aula teremos exercício no laboratório.
```

`contabilidade-analysis.json` deve conter um objeto com `subject_id`, `topic`, `cleaned_transcript`, `lesson_map`, `essential_concepts`, `formulas`, `examples`, `pitfalls`, `review_questions`, `applications`, `open_questions`, `concept_candidates`, `task_mentions` e `calendar_mentions`. Inclua seis perguntas de revisão e preserve a pergunta substantiva do aluno.

- [ ] **Step 2: Escrever o teste do plano e dos derivados**

Create `.fgv/tests/test_plaud_pipeline.py`:

```python
import json
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

from fgv_workflow.plaud import AnalysisError, process_plaud


FIXTURES = Path(__file__).parent / "fixtures" / "plaud"


def test_pipeline_preserves_raw_and_writes_three_unique_artifacts(
    tmp_path: Path,
) -> None:
    source = FIXTURES / "contabilidade-2026-08-28.txt"
    analysis = json.loads(
        (FIXTURES / "contabilidade-analysis.json").read_text(encoding="utf-8")
    )
    result = process_plaud(
        vault_root=tmp_path,
        source=source,
        class_date=date(2026, 8, 28),
        analysis=analysis,
        processor="test-adapter",
        ingested_at=datetime(2026, 8, 28, 13, 0, tzinfo=timezone.utc),
    )
    lesson = (
        tmp_path
        / "10 Matérias"
        / "ContabilidadeFinanceira"
        / "Aulas"
        / "08.28"
    )
    assert (lesson / "Fontes" / "Plaud - original.txt").read_bytes() == (
        source.read_bytes()
    )
    assert {path.name for path in result.artifacts} == {
        "Transcrito - DRE e provisões.md",
        "Resumo - DRE e provisões.md",
        "Revisao - DRE e provisões.md",
    }
    assert all("2026-08-28" not in path.name for path in result.artifacts)
    assert source.exists()


def test_pipeline_rejects_fewer_than_five_recall_questions(
    tmp_path: Path,
) -> None:
    analysis = json.loads(
        (FIXTURES / "contabilidade-analysis.json").read_text(encoding="utf-8")
    )
    analysis["review_questions"] = analysis["review_questions"][:4]
    with pytest.raises(AnalysisError, match="5 to 10"):
        process_plaud(
            vault_root=tmp_path,
            source=FIXTURES / "contabilidade-2026-08-28.txt",
            class_date=date(2026, 8, 28),
            analysis=analysis,
            processor="test-adapter",
            ingested_at=datetime(2026, 8, 28, 13, 0, tzinfo=timezone.utc),
        )
```

- [ ] **Step 3: Rodar e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_plaud_pipeline.py -q
```

Expected: collection FAIL por ausência de `fgv_workflow.plaud`.

- [ ] **Step 4: Implementar análise validada, renderização e publicação atômica**

Create templates com YAML canônico. O início de `.fgv/templates/resumo.md` deve ser:

```markdown
---
id: $artifact_id
tipo: resumo
materias: [$subject_id]
semestre: $semester
data: $class_date
tema: $topic
topicos: $topics
status: completo
origens: [plaud]
atualizado_por: fgv
atualizado_em: $updated_at
contract_version: $contract_version
source_sha256: $source_sha256
transaction_id: $transaction_id
dominio: 0
ultima_revisao:
proxima_revisao: $next_review
---

# $topic

## Mapa da aula

$lesson_map

## Conceitos essenciais

$essential_concepts

## Fórmulas e mecanismos

$formulas

## Exemplos do professor

$examples

## Pegadinhas

$pitfalls

## Recuperação ativa

$review_questions

## Aplicações

$applications

## Dúvidas abertas

$open_questions
```

`transcrito.md` deve conter o mapa da aula antes da fala limpa e campos `source_sha256` e `transaction_id`. `revisao.md` deve conter perguntas sem respostas inline, uma seção `Erros e retestes` vazia e links para resumo, transcrito e materiais.

Implement `process_plaud` com o seguinte fluxo completo:

```python
@dataclass(frozen=True)
class PlaudResult:
    transaction_id: str
    raw_path: Path
    manifest_path: Path
    artifacts: tuple[Path, ...]
    created: bool


def process_plaud(
    vault_root: Path,
    source: Path,
    class_date: date,
    analysis: dict,
    processor: str,
    ingested_at: datetime,
) -> PlaudResult:
    required = {
        "subject_id",
        "topic",
        "cleaned_transcript",
        "lesson_map",
        "essential_concepts",
        "formulas",
        "examples",
        "pitfalls",
        "review_questions",
        "applications",
        "open_questions",
        "concept_candidates",
        "task_mentions",
        "calendar_mentions",
    }
    missing = sorted(required.difference(analysis))
    if missing:
        raise AnalysisError("missing analysis keys: " + ", ".join(missing))
    question_count = len(analysis["review_questions"])
    if not 5 <= question_count <= 10:
        raise AnalysisError("review_questions must contain 5 to 10 items")

    registry = SubjectRegistry.load_default()
    subject = registry.resolve(analysis["subject_id"])
    lesson = lesson_dir(vault_root, subject, class_date)
    ingested = ingest_source(
        vault_root=vault_root,
        source=source,
        lesson_dir=lesson,
        subject_id=subject.id,
        class_date=class_date,
        ingested_at=ingested_at,
    )
    existing = tuple(
        path
        for path in lesson.glob("*.md")
        if f"transaction_id: {ingested.transaction_id}"
        in path.read_text(encoding="utf-8")
    )
    if not ingested.created and len(existing) == 3:
        return PlaudResult(
            transaction_id=ingested.transaction_id,
            raw_path=ingested.raw_path,
            manifest_path=ingested.manifest_path,
            artifacts=existing,
            created=False,
        )

    context = build_template_context(
        subject=subject,
        class_date=class_date,
        analysis=analysis,
        processor=processor,
        ingested_at=ingested_at,
        source_sha256=sha256_file(source),
        transaction_id=ingested.transaction_id,
    )
    published: list[Path] = []
    for kind in ("transcrito", "resumo", "revisao"):
        destination = artifact_path(lesson, kind, analysis["topic"])
        rendered = render_template(kind, context)
        validate_rendered_artifact(rendered, kind, ingested.transaction_id)
        temporary = destination.with_suffix(".md.tmp")
        temporary.write_text(rendered, encoding="utf-8")
        os.replace(temporary, destination)
        published.append(destination)
    return PlaudResult(
        transaction_id=ingested.transaction_id,
        raw_path=ingested.raw_path,
        manifest_path=ingested.manifest_path,
        artifacts=tuple(published),
        created=True,
    )
```

No mesmo arquivo, defina `build_template_context`, `render_template` e `validate_rendered_artifact` antes de `process_plaud`. `render_template` usa `string.Template.substitute`, portanto falha quando um campo obrigatório está ausente. `validate_rendered_artifact` parseia o YAML, confirma `tipo`, `source_sha256`, `transaction_id`, `contract_version=1` e rejeita qualquer path já pertencente a outra transação.

O código acima executa, nesta ordem:

- validar todas as chaves do analysis;
- exigir entre cinco e dez perguntas;
- resolver matéria exclusivamente pelo registry;
- criar `lesson_dir` em `MM.DD`;
- chamar `ingest_source` com `vault_root` explícito;
- calcular IDs estáveis `<sigla>-<YYYY-MM-DD>-<tipo>-<tx8>`;
- renderizar em diretório temporário dentro da pasta da aula;
- validar frontmatter antes de publicar;
- recusar overwrite de artefato de outra transação;
- usar `os.replace` para publicar;
- retornar no-op no rerun da mesma transação.

- [ ] **Step 5: Rodar testes Plaud**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_plaud_pipeline.py .fgv/tests/test_source_store.py -q
```

Expected:

```text
6 passed
```

- [ ] **Step 6: Commitar o pipeline Plaud**

Run:

```bash
git add .fgv/src/fgv_workflow/plaud.py .fgv/templates .fgv/tests/test_plaud_pipeline.py .fgv/tests/fixtures/plaud
git commit -m "feat(fgv): add idempotent Plaud pipeline"
```

Expected: nenhum arquivo fora de `.fgv/` alterado.

### Task 7: Promoção gated de conceitos

**Files:**

- Create: `.fgv/src/fgv_workflow/concepts.py`
- Create: `.fgv/templates/conceito.md`
- Test: `.fgv/tests/test_concepts.py`

- [ ] **Step 1: Escrever testes das regras de promoção**

Create `.fgv/tests/test_concepts.py`:

```python
from pathlib import Path

from fgv_workflow.concepts import ConceptCandidate, plan_concept_actions


def candidate(**overrides) -> ConceptCandidate:
    values = {
        "title": "Provisão",
        "centrality_explicit": False,
        "used_in_assessment": False,
        "occurrence_count": 1,
        "cross_subject": False,
        "needs_own_explanation": False,
    }
    values.update(overrides)
    return ConceptCandidate(**values)


def test_single_incidental_term_stays_candidate(tmp_path: Path) -> None:
    actions = plan_concept_actions(
        (candidate(),),
        concepts_dir=tmp_path / "20 Conhecimento" / "Conceitos",
    )
    assert actions[0].action == "queue"


def test_assessed_or_recurring_term_is_promoted(tmp_path: Path) -> None:
    actions = plan_concept_actions(
        (
            candidate(used_in_assessment=True),
            candidate(title="DRE", occurrence_count=2),
        ),
        concepts_dir=tmp_path / "20 Conhecimento" / "Conceitos",
    )
    assert [action.action for action in actions] == ["create", "create"]


def test_existing_note_is_linked_not_rewritten(tmp_path: Path) -> None:
    concepts = tmp_path / "20 Conhecimento" / "Conceitos"
    concepts.mkdir(parents=True)
    note = concepts / "DRE.md"
    note.write_text("human content", encoding="utf-8")
    actions = plan_concept_actions(
        (candidate(title="DRE", centrality_explicit=True),),
        concepts_dir=concepts,
    )
    assert actions[0].action == "link_existing"
    assert note.read_text(encoding="utf-8") == "human content"
```

- [ ] **Step 2: Rodar e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_concepts.py -q
```

Expected: collection FAIL por módulo ausente.

- [ ] **Step 3: Implementar critério gated e queue append-only**

Create `.fgv/src/fgv_workflow/concepts.py`:

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class ConceptCandidate:
    title: str
    centrality_explicit: bool
    used_in_assessment: bool
    occurrence_count: int
    cross_subject: bool
    needs_own_explanation: bool


@dataclass(frozen=True)
class ConceptAction:
    title: str
    action: Literal["queue", "create", "link_existing"]
    path: Path | None


def should_promote(item: ConceptCandidate) -> bool:
    return any(
        (
            item.centrality_explicit,
            item.used_in_assessment,
            item.occurrence_count >= 2,
            item.cross_subject,
            item.needs_own_explanation,
        )
    )


def plan_concept_actions(
    candidates: tuple[ConceptCandidate, ...],
    concepts_dir: Path,
) -> tuple[ConceptAction, ...]:
    actions: list[ConceptAction] = []
    for item in candidates:
        path = concepts_dir / f"{item.title}.md"
        if path.exists():
            action = "link_existing"
        elif should_promote(item):
            action = "create"
        else:
            action = "queue"
        actions.append(
            ConceptAction(
                title=item.title,
                action=action,
                path=path if action != "queue" else None,
            )
        )
    return tuple(actions)
```

A fila deve ser materializada em `30 Sistema/Estado/concept-candidates.jsonl` com `transaction_id`, critérios e status `pending`. Um rerun com a mesma combinação de `transaction_id` e título não adiciona outra linha.

Create `.fgv/templates/conceito.md` com `materias` sempre como lista, aliases, definição, aplicação, pergunta de recuperação, erros comuns, aulas relacionadas e conceitos relacionados.

- [ ] **Step 4: Rodar os testes**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_concepts.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 5: Commitar concept gate**

Run:

```bash
git add .fgv/src/fgv_workflow/concepts.py .fgv/templates/conceito.md .fgv/tests/test_concepts.py
git commit -m "feat(fgv): gate concept note creation"
```

Expected: nenhuma criação em massa dentro de `Vault/Conceitos/` ou `20 Conhecimento/Conceitos/`.

### Task 8: Tasks deduplicadas e Calendar intents

**Files:**

- Create: `.fgv/src/fgv_workflow/tasks.py`
- Create: `.fgv/src/fgv_workflow/calendar.py`
- Create: `.fgv/tests/fixtures/calendar/events.json`
- Test: `.fgv/tests/test_tasks_and_calendar.py`

- [ ] **Step 1: Escrever testes de dedupe e confirmação**

Create `.fgv/tests/test_tasks_and_calendar.py`:

```python
from pathlib import Path

from fgv_workflow.calendar import build_calendar_intent, queue_intent
from fgv_workflow.tasks import TaskMention, append_tasks


def test_task_requires_concrete_date_and_deduplicates(tmp_path: Path) -> None:
    tasks = tmp_path / "00 Home" / "Tasks.md"
    mentions = (
        TaskMention(
            description="Prova parcial de Contabilidade",
            due="2026-09-04",
            tag="#cont",
            priority="🔺",
        ),
        TaskMention(
            description="Prova parcial de Contabilidade",
            due="2026-09-04",
            tag="#cont",
            priority="🔺",
        ),
    )
    appended = append_tasks(tasks, mentions, transaction_id="tx-1")
    assert appended == 1
    assert tasks.read_text(encoding="utf-8").count("Prova parcial") == 1


def test_reschedule_always_requires_confirmation() -> None:
    intent = build_calendar_intent(
        transaction_id="tx-1",
        action="reschedule",
        calendar_alias="classes",
        payload={
            "event_id": "event-1",
            "start": "2026-09-05T11:00:00-03:00",
        },
    )
    assert intent.requires_confirmation is True
    assert intent.status == "pending"


def test_calendar_queue_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "30 Sistema" / "Estado" / "calendar-intents.jsonl"
    intent = build_calendar_intent(
        transaction_id="tx-1",
        action="append_description",
        calendar_alias="classes",
        payload={"event_id": "event-1", "text": "Leitura: capítulo 4"},
    )
    assert queue_intent(path, intent) is True
    assert queue_intent(path, intent) is False
    assert len(path.read_text(encoding="utf-8").splitlines()) == 1
```

- [ ] **Step 2: Rodar os testes e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_tasks_and_calendar.py -q
```

Expected: collection FAIL por ausência dos módulos.

- [ ] **Step 3: Implementar TaskIntent local**

`tasks.py` deve:

- rejeitar `due` ausente ou fora de `YYYY-MM-DD`;
- gerar chave de dedupe por descrição normalizada, data e tag;
- escrever somente em `00 Home/Tasks.md`;
- incluir marcador HTML `<!-- fgv-task:<hash> source:<transaction_id> -->`;
- criar a seção `## Adicionadas por /fgv` quando ausente;
- nunca alterar tasks existentes.

Public API:

```python
@dataclass(frozen=True)
class TaskMention:
    description: str
    due: str
    tag: str
    priority: str


def append_tasks(
    path: Path,
    mentions: tuple[TaskMention, ...],
    transaction_id: str,
) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text(encoding="utf-8") if path.exists() else "# Tasks\n"
    heading = "\n## Adicionadas por /fgv\n"
    if heading.strip() not in current:
        current = current.rstrip() + heading
    additions: list[str] = []
    for mention in mentions:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", mention.due):
            raise ValueError("task due date must use YYYY-MM-DD")
        normalized = " ".join(mention.description.casefold().split())
        material = f"{normalized}\0{mention.due}\0{mention.tag}"
        task_id = hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]
        marker = f"<!-- fgv-task:{task_id} source:{transaction_id} -->"
        if f"fgv-task:{task_id}" in current or any(
            f"fgv-task:{task_id}" in line for line in additions
        ):
            continue
        priority = f" {mention.priority}" if mention.priority else ""
        additions.append(
            f"- [ ] {mention.description} {mention.tag} "
            f"📅 {mention.due}{priority} {marker}"
        )
    if additions:
        updated = current.rstrip() + "\n\n" + "\n".join(additions) + "\n"
        temporary = path.with_suffix(".md.tmp")
        temporary.write_text(updated, encoding="utf-8")
        os.replace(temporary, path)
    return len(additions)
```

Inclua `import hashlib`, `import os` e `import re` no topo de `tasks.py`.

- [ ] **Step 4: Implementar CalendarIntent sem connector**

`calendar.py` deve calcular:

```python
def make_action_id(
    transaction_id: str,
    action: str,
    calendar_alias: str,
    payload: dict,
) -> str:
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    material = f"{transaction_id}\\0{action}\\0{calendar_alias}\\0{canonical}"
    return "cal-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:20]
```

`build_calendar_intent` força `requires_confirmation=True` para `mark_cancelled` e `reschedule`. `queue_intent` escreve JSONL append-only e deduplica por `action_id`. IDs reais de calendário não entram no repo; o core usa aliases `classes` e `assessments`.

- [ ] **Step 5: Rodar os testes**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_tasks_and_calendar.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 6: Commitar tasks e intents**

Run:

```bash
git add .fgv/src/fgv_workflow/tasks.py .fgv/src/fgv_workflow/calendar.py .fgv/tests/test_tasks_and_calendar.py .fgv/tests/fixtures/calendar/events.json
git commit -m "feat(fgv): add task and calendar intents"
```

Expected: nenhum evento real criado e nenhum Calendar ID secreto commitado.

### Task 9: Catálogo e dashboard materializados

**Files:**

- Create: `.fgv/src/fgv_workflow/catalog.py`
- Create: `.fgv/scripts/validate_vault.py`
- Test: `.fgv/tests/test_catalog.py`

- [ ] **Step 1: Escrever teste de catálogo determinístico**

Create `.fgv/tests/test_catalog.py`:

```python
import json
from pathlib import Path

from fgv_workflow.catalog import build_catalog


NOTE = """---
id: cont-2026-08-28-resumo
tipo: resumo
materias: [contabilidade-financeira]
data: 2026-08-28
status: completo
source_sha256: sha256:{digest}
canonical_for_search: true
---
# DRE
"""


def test_catalog_is_sorted_and_does_not_double_count_source(tmp_path: Path) -> None:
    lesson = (
        tmp_path
        / "10 Matérias"
        / "ContabilidadeFinanceira"
        / "Aulas"
        / "08.28"
    )
    lesson.mkdir(parents=True)
    (lesson / "Resumo - DRE.md").write_text(
        NOTE.format(digest="a" * 64),
        encoding="utf-8",
    )
    state = tmp_path / "30 Sistema" / "Estado"
    result = build_catalog(tmp_path, state)
    records = [
        json.loads(line)
        for line in result.catalog.read_text(encoding="utf-8").splitlines()
    ]
    assert [record["id"] for record in records] == [
        "cont-2026-08-28-resumo"
    ]
    assert "Última aula processada" in result.dashboard.read_text(encoding="utf-8")
```

- [ ] **Step 2: Rodar e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_catalog.py -q
```

Expected: collection FAIL por ausência de `fgv_workflow.catalog`.

- [ ] **Step 3: Implementar scanner e writer único**

`build_catalog(vault_root, state_dir)` deve:

- escanear Markdown sob `00 Home/`, `10 Matérias/`, `20 Conhecimento/` e `90 Arquivo/`;
- ignorar `.fgv/`, `30 Sistema/Plans/`, `30 Sistema/Specs/` e outputs temporários;
- parsear YAML com `yaml.safe_load`;
- validar cada record com `catalog-record.schema.json`;
- ordenar por `data`, `materias`, `tipo` e `path`;
- gravar atomicamente `catalog.jsonl`, `dashboard-snapshot.md` e `sync-status.json`;
- marcar originals com `canonical_for_search=false` quando existe extração textual com o mesmo `source_hash`;
- nunca usar Dataview ou Tasks renderizados como input.

Return type:

```python
@dataclass(frozen=True)
class CatalogResult:
    catalog: Path
    dashboard: Path
    sync_status: Path
    record_count: int
```

- [ ] **Step 4: Criar o CLI de validação**

`.fgv/scripts/validate_vault.py` deve chamar `build_catalog` em `--check`, comparar o conteúdo esperado com o existente sem escrevê-lo e retornar:

- exit `0` e `vault validation: ok` quando igual;
- exit `1` e uma lista de paths divergentes quando desatualizado;
- exit `2` quando metadata ou schema forem inválidos.

- [ ] **Step 5: Rodar os testes**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_catalog.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 6: Commitar catálogo**

Run:

```bash
git add .fgv/src/fgv_workflow/catalog.py .fgv/scripts/validate_vault.py .fgv/tests/test_catalog.py .fgv/schemas/catalog-record.schema.json
git commit -m "feat(fgv): materialize catalog and dashboard"
```

Expected: somente código, schema e testes; nenhum snapshot do vault real nesta task.

### Task 10: Ownership Git e wrapper `fgv-sync`

**Files:**

- Create: `.fgv/config/sync-ownership.json`
- Create: `.fgv/src/fgv_workflow/sync.py`
- Create: `.fgv/scripts/fgv_sync.py`
- Test: `.fgv/tests/test_sync.py`

- [ ] **Step 1: Escrever testes com Git runner falso**

Create `.fgv/tests/test_sync.py`:

```python
from pathlib import Path

import pytest

from fgv_workflow.sync import (
    DirtyWorkingTree,
    GitCommandDenied,
    SyncCoordinator,
)


class FakeGit:
    def __init__(self, status: str = "", behind: bool = False) -> None:
        self.status = status
        self.behind = behind
        self.calls: list[tuple[str, ...]] = []

    def run(self, *args: str) -> str:
        self.calls.append(args)
        if args == ("status", "--porcelain"):
            return self.status
        if args == ("rev-list", "--count", "HEAD..origin/main"):
            return "1" if self.behind else "0"
        return ""


def test_mac_agent_cannot_run_network_git(tmp_path: Path) -> None:
    git = FakeGit()
    coordinator = SyncCoordinator(tmp_path, role="mac-agent", git=git)
    with pytest.raises(GitCommandDenied):
        coordinator.prepare_write()
    assert git.calls == [("status", "--porcelain")]


def test_hermes_refuses_dirty_tree(tmp_path: Path) -> None:
    git = FakeGit(status=" M Tasks.md")
    coordinator = SyncCoordinator(tmp_path, role="hermes-sync", git=git)
    with pytest.raises(DirtyWorkingTree):
        coordinator.prepare_write()


def test_hermes_fetches_and_fast_forwards_when_clean(tmp_path: Path) -> None:
    git = FakeGit(behind=True)
    coordinator = SyncCoordinator(tmp_path, role="hermes-sync", git=git)
    coordinator.prepare_write()
    assert ("fetch", "origin", "main") in git.calls
    assert ("merge", "--ff-only", "origin/main") in git.calls
```

- [ ] **Step 2: Rodar e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_sync.py -q
```

Expected: collection FAIL por módulo ausente.

- [ ] **Step 3: Criar configuração de ownership**

Create `.fgv/config/sync-ownership.json`:

```json
{
  "schema_version": 1,
  "roles": {
    "mac-agent": {
      "git_owner": "obsidian-git",
      "allowed": ["status"],
      "denied": ["fetch", "pull", "merge", "rebase", "commit", "push"]
    },
    "hermes-sync": {
      "git_owner": "fgv-sync",
      "allowed": ["status", "fetch", "merge-ff-only", "commit-scoped", "push"],
      "retry_push_rejection": 1,
      "force_push": false
    }
  }
}
```

- [ ] **Step 4: Implementar coordinator, lock e commits scoped**

`sync.py` deve:

- receber um `GitRunner` injetável;
- adquirir `fcntl.flock` em `.git/fgv-sync.lock` no Hermes;
- executar `status --porcelain` antes de qualquer fetch;
- negar qualquer Git de rede para `mac-agent`;
- no Hermes, exigir árvore limpa, executar `fetch origin main` e `merge --ff-only origin/main`;
- adicionar somente a lista de paths do `transaction_id`, nunca `git add -A`;
- tentar push uma vez;
- em push rejeitado, fazer um único fetch e rebase não conflitivo;
- abortar e reportar conflito sem force push;
- retornar `as_of_commit` em toda leitura acadêmica.

Public API:

```python
class GitRunner(Protocol):
    def run(self, *args: str) -> str:
        raise NotImplementedError("GitRunner.run is supplied by the runtime")


class SyncCoordinator:
    def __init__(
        self,
        repo: Path,
        role: Literal["mac-agent", "hermes-sync"],
        git: GitRunner,
    ) -> None:
        self.repo = repo
        self.role = role
        self.git = git

    def prepare_read(self, require_latest: bool) -> str:
        status = self.git.run("status", "--porcelain")
        if require_latest and self.role == "hermes-sync":
            if status:
                raise DirtyWorkingTree(status)
            self.git.run("fetch", "origin", "main")
            behind = self.git.run(
                "rev-list", "--count", "HEAD..origin/main"
            ).strip()
            if behind != "0":
                self.git.run("merge", "--ff-only", "origin/main")
        return self.git.run("rev-parse", "HEAD").strip()

    def prepare_write(self) -> None:
        status = self.git.run("status", "--porcelain")
        if status:
            raise DirtyWorkingTree(status)
        if self.role == "mac-agent":
            raise GitCommandDenied("Obsidian Git owns network Git on Mac")
        self.git.run("fetch", "origin", "main")
        behind = self.git.run(
            "rev-list", "--count", "HEAD..origin/main"
        ).strip()
        if behind != "0":
            self.git.run("merge", "--ff-only", "origin/main")

    def publish(self, paths: tuple[Path, ...], message: str) -> str:
        if self.role != "hermes-sync":
            raise GitCommandDenied("only hermes-sync may publish")
        for path in paths:
            relative = path.resolve().relative_to(self.repo.resolve())
            self.git.run("add", "--", relative.as_posix())
        self.git.run("commit", "-m", message)
        try:
            self.git.run("push", "origin", "main")
        except GitPushRejected:
            self.git.run("fetch", "origin", "main")
            self.git.run("rebase", "origin/main")
            self.git.run("push", "origin", "main")
        return self.git.run("rev-parse", "HEAD").strip()
```

Defina `GitCommandDenied`, `DirtyWorkingTree` e `GitPushRejected` como subclasses de `RuntimeError`. O runner concreto converte exit code não zero de push em `GitPushRejected` e qualquer conflito de rebase em erro terminal, sem segunda tentativa e sem force push.

- [ ] **Step 5: Rodar testes de ownership**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_sync.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 6: Commitar sync policy**

Run:

```bash
git add .fgv/config/sync-ownership.json .fgv/src/fgv_workflow/sync.py .fgv/scripts/fgv_sync.py .fgv/tests/test_sync.py
git commit -m "feat(fgv): enforce sync ownership"
```

Expected: nenhuma operação Git real executada pelos testes.

### Task 11: Adapters finos Codex e Claude, com staging seguro

**Files:**

- Create: `.fgv/adapters/codex/SKILL.md.tmpl`
- Create: `.fgv/adapters/claude/SKILL.md.tmpl`
- Create: `.fgv/src/fgv_workflow/adapters.py`
- Create: `.fgv/scripts/stage_adapters.py`
- Create: `30 Sistema/Estado/adapter-staging/.gitkeep`
- Test: `.fgv/tests/test_adapter_staging.py`

- [ ] **Step 1: Escrever teste que proíbe drift e instalação live**

Create `.fgv/tests/test_adapter_staging.py`:

```python
from pathlib import Path

import pytest

from fgv_workflow.adapters import LiveInstallDenied, stage_adapters


def normalized_semantics(text: str) -> list[str]:
    return [
        line
        for line in text.splitlines()
        if line.startswith("CORE:")
        or line.startswith("CLI:")
        or line.startswith("GIT_ROLE:")
    ]


def test_codex_and_claude_share_the_same_semantic_contract(
    tmp_path: Path,
) -> None:
    result = stage_adapters(tmp_path)
    codex = result.codex.read_text(encoding="utf-8")
    claude = result.claude.read_text(encoding="utf-8")
    assert normalized_semantics(codex) == normalized_semantics(claude)
    assert "subjects" not in codex.casefold()
    assert "subjects" not in claude.casefold()


@pytest.mark.parametrize(
    "destination",
    [
        Path.home() / ".agents" / "skills",
        Path.home() / ".claude" / "skills",
        Path("/root/.hermes/skills"),
    ],
)
def test_stager_refuses_live_installations(destination: Path) -> None:
    with pytest.raises(LiveInstallDenied):
        stage_adapters(destination)
```

- [ ] **Step 2: Rodar e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_adapter_staging.py -q
```

Expected: collection FAIL por módulo ausente.

- [ ] **Step 3: Criar templates pequenos e sem listas duplicadas**

O corpo normativo de ambos os templates deve ter menos de 80 linhas e conter:

```markdown
# FGV runtime adapter

CORE: `<vault>/.fgv/CORE.md`
CLI: `<vault>/.fgv-venv/bin/fgv-workflow`
GIT_ROLE: `mac-agent`

1. Carregue `.fgv/VERSION`, `.fgv/CORE.md` e `.fgv/config/subjects.json`.
2. Gere primeiro um `IngestPlan`. Não escreva se matéria ou data estiver ambígua.
3. Use o CLI compartilhado para naming, raw, manifest, tasks, catálogo e validação.
4. Nunca mova ou apague a origem Plaud.
5. Nunca execute fetch, pull, merge, rebase, commit ou push.
6. Traduza `CalendarIntent` somente se o runtime tiver connector disponível.
7. Cancelamento e reschedule exigem confirmação explícita.
8. Retorne receipt com transaction_id, paths, hashes, intents e validações.
```

A única diferença permitida é a seção de ferramentas:

- Codex usa aprovações e ferramentas locais do Codex.
- Claude usa ferramentas locais e Google Calendar MCP quando disponível.

- [ ] **Step 4: Implementar stager que escreve somente no destino informado**

`stage_adapters(destination)` deve:

- resolver o path real;
- rejeitar qualquer path igual ou contido em instalações live;
- criar `codex/fgv/SKILL.md` e `claude/fgv/SKILL.md` sob staging;
- não criar backup porque não toca a instalação existente;
- emitir `manifest.json` com hash dos templates e `contract_version`;
- nunca chamar subprocess, Git ou connector.

- [ ] **Step 5: Rodar testes e gerar staging dentro da worktree**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_adapter_staging.py -q
.fgv-venv/bin/python .fgv/scripts/stage_adapters.py \
  --output '30 Sistema/Estado/adapter-staging'
```

Expected:

```text
4 passed
staged adapters: codex, claude
live installations modified: 0
```

- [ ] **Step 6: Commitar templates e stager, não os outputs gerados**

Run:

```bash
git add .fgv/adapters/codex/SKILL.md.tmpl .fgv/adapters/claude/SKILL.md.tmpl .fgv/src/fgv_workflow/adapters.py .fgv/scripts/stage_adapters.py .fgv/tests/test_adapter_staging.py '30 Sistema/Estado/adapter-staging/.gitkeep'
git commit -m "feat(fgv): stage thin local adapters"
```

Expected: `git status --short` mostra os bundles de staging como untracked ou ignorados, nunca paths em `~/.agents` ou `~/.claude`.

### Task 12: Pacote e prompt Hermes sem alterar o VPS

**Files:**

- Create: `.fgv/adapters/hermes/SKILL.md.tmpl`
- Create: `.fgv/prompts/hermes.md`
- Create: `.fgv/src/fgv_workflow/hermes_package.py`
- Create: `.fgv/scripts/build_hermes_package.py`
- Create: `30 Sistema/Hermes/README.md`
- Create: `30 Sistema/Hermes/eclass-path-migration.json`
- Test: `.fgv/tests/test_hermes_package.py`

- [ ] **Step 1: Escrever teste do bundle autocontido**

Create `.fgv/tests/test_hermes_package.py`:

```python
import json
from pathlib import Path

from fgv_workflow.hermes_package import build_hermes_package


def test_bundle_is_pinned_and_does_not_touch_live_runtime(
    tmp_path: Path,
) -> None:
    output = tmp_path / "dist"
    result = build_hermes_package(output)
    assert (result / "VERSION").read_text(encoding="utf-8") == "1\n"
    assert (result / "CORE.md").exists()
    assert (result / "prompts" / "hermes.md").exists()
    manifest = json.loads(
        (result / "package-manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["contract_version"] == 1
    assert manifest["install_performed"] is False
    assert not Path("/root/.hermes/skills/fgv").exists()


def test_prompt_requires_fresh_commit_and_catalog_first(tmp_path: Path) -> None:
    result = build_hermes_package(tmp_path / "dist")
    prompt = (result / "prompts" / "hermes.md").read_text(encoding="utf-8")
    assert "as_of_commit" in prompt
    assert "catalog.jsonl" in prompt
    assert "CalendarIntent" in prompt
    assert "raw é imutável" in prompt
```

O primeiro teste não deve depender da inexistência real de `/root/.hermes/skills/fgv`. Injete uma lista de roots proibidos no builder e afirme que nenhuma chamada de escrita usa esses roots.

- [ ] **Step 2: Rodar e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_hermes_package.py -q
```

Expected: collection FAIL por módulo ausente.

- [ ] **Step 3: Criar prompt operacional do Hermes**

Create `.fgv/prompts/hermes.md`:

```markdown
# Hermes adapter for FGV Workflow v1

Antes de agir, carregue `VERSION`, `CORE.md` e `config/subjects.json` do pacote.

Para leitura acadêmica:

- Use `fgv-sync prepare-read --latest`.
- Se não puder atualizar o clone, declare `as_of_commit` e `stale: true`.
- Consulte `30 Sistema/Estado/catalog.jsonl` antes de explorar o filesystem.
- Resolva aula recente pelo campo YAML `data`, não apenas por `MM.DD`.
- Não trate original, extração, transcrito e resumo como evidências independentes.

Para escrita:

- Produza primeiro `IngestPlan`.
- Raw é imutável e nunca é apagado.
- Só `fgv-sync` opera Git.
- Arquivo de outra transação não pode ser sobrescrito.
- Calendar recebe `CalendarIntent`; cancelamento e reschedule exigem confirmação.
- Após validação, retorne receipt com `transaction_id`, hashes, paths, intents e `as_of_commit`.

Nunca escreva em caminhos live durante instalação deste pacote. O pacote apenas fornece arquivos para staging e um plano de cutover.
```

- [ ] **Step 4: Criar mapeamento de paths do Eclass**

Create `30 Sistema/Hermes/eclass-path-migration.json`:

```json
{
  "schema_version": 1,
  "old_vault_root": "/root/vault",
  "new_subject_root": "/root/vault/10 Matérias",
  "tasks_path": "/root/vault/00 Home/Tasks.md",
  "state_path": "/root/vault/30 Sistema/Estado",
  "lesson_pattern": "<subject_folder>/Aulas/MM.DD",
  "forbidden_destinations": [
    "/root/vault/Vault/<subject_folder>",
    "<lesson>/Slides",
    "<lesson>/Material"
  ],
  "install_automatically": false
}
```

`30 Sistema/Hermes/README.md` deve listar todos os caminhos hardcoded identificados na auditoria que o cutover posterior precisa atualizar: memória, `eclass-scan.py`, skills `eclass`, `fgv-eclass-api`, `fgv-briefing`, cronjobs, `Tasks.md`, branch e remote.

- [ ] **Step 5: Implementar builder por cópia allowlist**

`build_hermes_package(output)` deve copiar somente:

- `VERSION`;
- `CORE.md`;
- `config/subjects.json`;
- `config/sync-ownership.json`;
- `schemas/`;
- adapter Hermes renderizado;
- prompt Hermes;
- scripts necessários;
- `package-manifest.json` com hashes.

O builder rejeita roots live e não chama `git`, `ssh`, `scp` ou ferramentas MCP.

- [ ] **Step 6: Rodar testes e construir bundle em staging**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_hermes_package.py -q
HERMES_STAGE="$(mktemp -d)"
.fgv-venv/bin/python .fgv/scripts/build_hermes_package.py \
  --output "$HERMES_STAGE"
find "$HERMES_STAGE" -maxdepth 3 -type f | sort
```

Expected:

```text
2 passed
Hermes package built
install_performed=false
```

O `find` lista VERSION, CORE, config, schemas, skill, prompt, scripts e manifest. Não lista arquivos fora do diretório temporário.

- [ ] **Step 7: Commitar pacote fonte e documentação**

Run:

```bash
git add .fgv/adapters/hermes/SKILL.md.tmpl .fgv/prompts/hermes.md .fgv/src/fgv_workflow/hermes_package.py .fgv/scripts/build_hermes_package.py .fgv/tests/test_hermes_package.py '30 Sistema/Hermes/README.md' '30 Sistema/Hermes/eclass-path-migration.json'
git commit -m "feat(fgv): add staged Hermes package"
```

Expected: nenhuma modificação em `/root/.hermes` e nenhum bundle temporário commitado.

### Task 13: Migração determinística, idempotente e dry-run por padrão

**Files:**

- Create: `.fgv/src/fgv_workflow/migration.py`
- Create: `.fgv/scripts/plan_migration.py`
- Test: `.fgv/tests/test_migration.py`

- [ ] **Step 1: Escrever teste em vault temporário**

Create `.fgv/tests/test_migration.py`:

```python
from pathlib import Path

from fgv_workflow.migration import build_migration_plan, execute_migration


def test_dry_run_plans_without_writing(tmp_path: Path) -> None:
    old = tmp_path / "ContabilidadeFinanceira" / "Aulas" / "08.28"
    old.mkdir(parents=True)
    source = old / "Resumo.md"
    source.write_text(
        "---\\nmateria: ContabilidadeFinanceira\\n"
        "data: 2026-08-28\\ntema: DRE e provisões\\n---\\n",
        encoding="utf-8",
    )
    plan = build_migration_plan(tmp_path)
    assert plan.operations[0].destination.as_posix().endswith(
        "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/"
        "Resumo - DRE e provisões.md"
    )
    assert source.exists()
    assert not (tmp_path / "10 Matérias").exists()


def test_apply_preserves_count_and_hashes(tmp_path: Path) -> None:
    old = tmp_path / "Psicologia" / "Aulas" / "08.20"
    old.mkdir(parents=True)
    raw = old / "plaud.txt"
    raw.write_bytes(b"raw bytes")
    plan = build_migration_plan(tmp_path)
    receipt = execute_migration(plan, expected_head="fixture-head")
    assert receipt.before_count == receipt.after_count
    assert receipt.binary_hash_mismatches == ()
    assert receipt.deleted_paths == ()
```

- [ ] **Step 2: Rodar e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_migration.py -q
```

Expected: collection FAIL por módulo ausente.

- [ ] **Step 3: Implementar inventário e plano sem heurística destrutiva**

`build_migration_plan` deve:

- inventariar todo arquivo e hash antes de propor operação;
- mapear matérias ativas para `10 Matérias/`;
- mapear `Vault/Conceitos` para `20 Conhecimento/Conceitos`;
- mapear templates, automation e Tutor para `30 Sistema/`;
- mapear `Vault/S1` para `90 Arquivo/2026.1`;
- mapear `Tasks.md` para `00 Home/Tasks.md`;
- transformar `Resumo.md` e `Transcrito.md` pelo tema YAML;
- manter `MM.DD` na pasta e não colocar data no filename;
- enviar arquivo sem classificação segura para `00 Home/Inbox/Legado/`;
- detectar colisões antes de qualquer escrita;
- escrever `migration-manifest.json` com source, destination, hash e reason.

`execute_migration` deve exigir `expected_head`, recusar plano com colisão e usar cópia verificada antes de remover o path antigo dentro da worktree. Nenhuma operação deve excluir conteúdo sem destino e hash confirmados.

- [ ] **Step 4: Adicionar teste de idempotência**

Add:

```python
def test_second_plan_after_apply_has_no_operations(tmp_path: Path) -> None:
    old = tmp_path / "Tasks.md"
    old.write_text("# Tasks\\n", encoding="utf-8")
    first = build_migration_plan(tmp_path)
    execute_migration(first, expected_head="fixture-head")
    second = build_migration_plan(tmp_path)
    assert second.operations == ()
```

- [ ] **Step 5: Rodar testes e dry-run real**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_migration.py -q
.fgv-venv/bin/python .fgv/scripts/plan_migration.py \
  --vault-root . \
  --output '30 Sistema/Estado/migration-dry-run.json'
```

Expected:

```text
3 passed
mode=dry-run
files_written=0
collisions=<number>
unsafe_operations=0
```

O comando não aceita `--apply` nesta task. A execução real da migração requer uma tarefa de cutover separada após validação de Hermes.

- [ ] **Step 6: Commitar somente planner e testes**

Run:

```bash
git add .fgv/src/fgv_workflow/migration.py .fgv/scripts/plan_migration.py .fgv/tests/test_migration.py
git commit -m "feat(fgv): add migration dry run planner"
```

Expected: não commitar `migration-dry-run.json` nem qualquer movimento real do vault.

### Task 14: CLI único e conformance Codex, Claude e Hermes

**Files:**

- Create: `.fgv/src/fgv_workflow/cli.py`
- Create: `.fgv/tests/fixtures/expected/ingest-plan.json`
- Create: `.fgv/tests/test_conformance.py`

- [ ] **Step 1: Escrever teste de planos normalizados idênticos**

Create `.fgv/tests/test_conformance.py`:

```python
import json
from pathlib import Path

from fgv_workflow.cli import plan_for_runtime


FIXTURES = Path(__file__).parent / "fixtures"


def normalize(plan: dict) -> dict:
    copy = dict(plan)
    copy.pop("processor", None)
    copy.pop("generated_at", None)
    return copy


def test_all_runtimes_emit_same_contract(tmp_path: Path) -> None:
    source = FIXTURES / "plaud" / "contabilidade-2026-08-28.txt"
    analysis = FIXTURES / "plaud" / "contabilidade-analysis.json"
    plans = [
        plan_for_runtime(
            runtime=runtime,
            vault_root=tmp_path / runtime,
            source=source,
            analysis_path=analysis,
            class_date="2026-08-28",
            plan_only=True,
        )
        for runtime in ("codex", "claude", "hermes")
    ]
    assert normalize(plans[0]) == normalize(plans[1]) == normalize(plans[2])


def test_rerun_is_identical_and_calendar_remains_pending(tmp_path: Path) -> None:
    source = FIXTURES / "plaud" / "contabilidade-2026-08-28.txt"
    analysis = FIXTURES / "plaud" / "contabilidade-analysis.json"
    kwargs = {
        "runtime": "codex",
        "vault_root": tmp_path,
        "source": source,
        "analysis_path": analysis,
        "class_date": "2026-08-28",
        "plan_only": True,
    }
    first = plan_for_runtime(**kwargs)
    second = plan_for_runtime(**kwargs)
    assert normalize(first) == normalize(second)
    assert all(item["status"] == "pending" for item in first["calendar_intents"])
```

- [ ] **Step 2: Rodar e confirmar a falha**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_conformance.py -q
```

Expected: collection FAIL porque `plan_for_runtime` ainda não existe.

- [ ] **Step 3: Implementar CLI como a única entrada pública**

`cli.py` deve expor:

```text
fgv-workflow plan-plaud --vault-root PATH --source FILE --analysis FILE --class-date YYYY-MM-DD --runtime codex|claude|hermes
fgv-workflow apply-plaud --plan FILE
fgv-workflow build-state --vault-root PATH
fgv-workflow queue-calendar --plan FILE
fgv-workflow validate --vault-root PATH
fgv-workflow sync-guard --role mac-agent|hermes-sync
fgv-workflow migration-plan --vault-root PATH --output FILE
fgv-workflow stage-adapters --output PATH
fgv-workflow build-hermes-package --output PATH
```

`plan-plaud` não escreve. `apply-plaud` valida `transaction_id` e schemas novamente antes de publicar. `runtime` pode alterar apenas capabilities, connector Calendar e receipt, nunca naming, metadata ou conteúdo canônico.

- [ ] **Step 4: Criar golden plan**

Run:

```bash
GOLDEN_ROOT="$(mktemp -d)"
.fgv-venv/bin/fgv-workflow plan-plaud \
  --vault-root "$GOLDEN_ROOT" \
  --source '.fgv/tests/fixtures/plaud/contabilidade-2026-08-28.txt' \
  --analysis '.fgv/tests/fixtures/plaud/contabilidade-analysis.json' \
  --class-date 2026-08-28 \
  --runtime codex \
  > '.fgv/tests/fixtures/expected/ingest-plan.json'
```

Expected: JSON válido, zero arquivos acadêmicos criados sob `$GOLDEN_ROOT` e `requires_confirmation=false` para o plano base.

- [ ] **Step 5: Rodar testes de conformance e golden**

Add a test that compares normalized output to `fixtures/expected/ingest-plan.json`, then run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests/test_conformance.py -q
```

Expected:

```text
3 passed
```

- [ ] **Step 6: Commitar CLI e conformance**

Run:

```bash
git add .fgv/src/fgv_workflow/cli.py .fgv/tests/test_conformance.py .fgv/tests/fixtures/expected/ingest-plan.json
git commit -m "feat(fgv): unify runtime contract through one CLI"
```

Expected: Codex, Claude e Hermes não possuem forks de lógica.

### Task 15: Validação integrada e documentação de cutover

**Files:**

- Modify: `.fgv/CORE.md`
- Modify: `30 Sistema/Hermes/README.md`
- Create: `30 Sistema/Hermes/CUTOVER-CHECKLIST.md`
- Test: all `.fgv/tests/`

- [ ] **Step 1: Adicionar checklist de cutover sem executar instalação**

Create `30 Sistema/Hermes/CUTOVER-CHECKLIST.md` com gates verificáveis:

- branch `codex/vault-plan-b` publicada;
- suite completa verde;
- migration dry-run com zero operações inseguras;
- bundles Codex, Claude e Hermes gerados somente em staging;
- backup do VPS feito pelo operador;
- Hermes testado contra a branch sem trocar `main`;
- Eclass escrevendo em `10 Matérias/<Materia>/Aulas/MM.DD/`;
- pergunta “aula mais recente” respondida com `as_of_commit`;
- Calendar intents aplicadas sem duplicata;
- raw fixture preservado por hash;
- aprovação explícita do Arthur antes de instalar adapters ou alterar `main`.

- [ ] **Step 2: Rodar scan de marcadores incompletos e corrigir o que aparecer**

Run:

```bash
rg -n 'TB[D]|TO[D]O|implement lat[e]r|fill in detail[s]|Similar to Tas[k]|Add appropriat[e]' \
  .fgv '30 Sistema/Hermes'
```

Expected: nenhum resultado.

- [ ] **Step 3: Rodar checks de naming e live-install**

Run:

```bash
rg -n 'Aulas/(DD\\.MM\\.AA|YYYY-MM-DD)|Vault/Tasks\\.md' .fgv
rg -n 'shutil\\.(copy|move).*\\.agents|shutil\\.(copy|move).*\\.claude|/root/\\.hermes' \
  .fgv/src .fgv/scripts
```

Expected: nenhum resultado. Menções de paths proibidos são permitidas somente em testes de recusa e documentação, nunca em código de escrita.

- [ ] **Step 4: Rodar a suite completa**

Run:

```bash
.fgv-venv/bin/python -m pytest .fgv/tests -q
```

Expected: todos os testes passam, sem skipped, xfailed ou warnings.

- [ ] **Step 5: Rodar conformance três vezes para detectar não determinismo**

Run:

```bash
for run in 1 2 3; do
  .fgv-venv/bin/python -m pytest \
    .fgv/tests/test_conformance.py::test_all_runtimes_emit_same_contract -q
done
```

Expected:

```text
1 passed
1 passed
1 passed
```

- [ ] **Step 6: Verificar que instalações live e vault real continuam intactos**

Run:

```bash
git status --short
git diff --name-status origin/main...HEAD
```

Expected:

- mudanças apenas na branch e worktree;
- nenhuma escrita em `/Users/arthurmalucelli/.agents/skills/fgv/`;
- nenhuma escrita em `/Users/arthurmalucelli/.claude/skills/fgv/`;
- nenhuma escrita em `/root/.hermes/`;
- o arquivo de design modificado preexistente continua fora dos commits deste plano.

- [ ] **Step 7: Fazer commit final de documentação**

Run:

```bash
git add .fgv/CORE.md '30 Sistema/Hermes/README.md' '30 Sistema/Hermes/CUTOVER-CHECKLIST.md'
git commit -m "docs(fgv): add workflow cutover gates"
```

Expected: commit apenas de contrato e documentação.

## Verificação final do implementador

- [ ] Cada requisito do design tem uma task correspondente.
- [ ] `.fgv/` é a única fonte editável do contrato.
- [ ] Nenhum filename processado dentro de `Aulas/MM.DD` repete a data.
- [ ] Raw Plaud permanece byte a byte igual e a origem externa continua existindo.
- [ ] `transaction_id` é estável e todos os efeitos são idempotentes.
- [ ] Data da aula depende de evidência com confiança suficiente.
- [ ] Conceitos incidentais ficam na fila, não viram notas automaticamente.
- [ ] Calendar destructive actions exigem confirmação.
- [ ] Codex e Claude produzem o mesmo plano normalizado.
- [ ] Installer produz apenas staging e rejeita instalações live.
- [ ] Hermes recebe bundle pinado e reporta `as_of_commit`.
- [ ] Apenas os sync owners executam Git.
- [ ] Migração real, instalação live, cutover do VPS e merge em `main` permanecem fora desta implementação.
