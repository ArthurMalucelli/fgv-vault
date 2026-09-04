# Curvas de Kd, Ke e WACC Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gerar gráficos didáticos, numéricos e conceitualmente precisos para as curvas de Kd, Ke e WACC versus `D/V`.

**Architecture:** Um módulo Python concentra as fórmulas puras, a otimização contínua do WACC e a renderização Matplotlib. Testes com `unittest` validam pontos numéricos, formato das curvas, mínimo contínuo e dimensões dos arquivos. O comando do módulo gera PNG e SVG persistentes no vault.

**Tech Stack:** Python 3.14, NumPy 2.4, SciPy 1.17, Matplotlib 3.10, `unittest` da biblioteca padrão.

---

## Estrutura de arquivos

- Criar `tools/__init__.py`: transforma `tools` em pacote importável.
- Criar `tools/curvas_kd_ke_wacc.py`: contém premissas, cálculos, otimização, renderização e CLI.
- Criar `tests/test_curvas_kd_ke_wacc.py`: valida o modelo e os arquivos renderizados.
- Gerar `Vault/Attachments/CurvasKdKeWacc.png`: imagem de 2.400 por 960 pixels.
- Gerar `Vault/Attachments/CurvasKdKeWacc.svg`: versão vetorial do mesmo visual.

### Task 1: Implementar e testar o modelo financeiro

**Files:**

- Create: `tools/__init__.py`
- Create: `tools/curvas_kd_ke_wacc.py`
- Create: `tests/test_curvas_kd_ke_wacc.py`

- [ ] **Step 1: Escrever os testes que falham para fórmulas e mínimo do WACC**

Criar `tests/test_curvas_kd_ke_wacc.py` com este conteúdo:

```python
import unittest

import numpy as np

from tools.curvas_kd_ke_wacc import (
    CurveParameters,
    calculate_curves,
    find_wacc_minimum,
    kd_gross,
    ke,
    wacc,
)


class CurveModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.params = CurveParameters()

    def test_kd_endpoints_match_design(self) -> None:
        values = kd_gross(np.array([0.0, 0.8]), self.params)
        self.assertAlmostEqual(float(values[0]), 0.06, places=10)
        self.assertAlmostEqual(float(values[1]), 0.276, places=10)

    def test_ke_without_debt_starts_near_twelve_percent(self) -> None:
        value = float(ke(np.array([0.0]), self.params)[0])
        self.assertAlmostEqual(value, 0.12002, places=8)

    def test_wacc_uses_after_tax_kd(self) -> None:
        debt_ratio = 0.4
        kd_value = float(kd_gross(np.array([debt_ratio]), self.params)[0])
        ke_value = float(ke(np.array([debt_ratio]), self.params)[0])
        expected = (
            (1.0 - debt_ratio) * ke_value
            + debt_ratio * kd_value * (1.0 - self.params.tax_rate)
        )
        actual = float(wacc(np.array([debt_ratio]), self.params)[0])
        self.assertAlmostEqual(actual, expected, places=12)

    def test_continuous_minimum_matches_design(self) -> None:
        debt_ratio, minimum = find_wacc_minimum(self.params)
        self.assertAlmostEqual(debt_ratio, 0.412870635, places=7)
        self.assertAlmostEqual(minimum, 0.113349398, places=7)

    def test_curve_shapes_match_teaching_model(self) -> None:
        curves = calculate_curves(self.params, points=801)
        minimum_index = int(np.argmin(curves["wacc"]))

        self.assertTrue(np.all(np.diff(curves["kd_gross"]) >= 0.0))
        self.assertTrue(np.all(np.diff(curves["ke"]) > 0.0))
        self.assertLess(curves["wacc"][minimum_index], curves["wacc"][0])
        self.assertLess(curves["wacc"][minimum_index], curves["wacc"][-1])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Rodar os testes e confirmar a falha inicial**

Run:

```bash
python3 -m unittest tests/test_curvas_kd_ke_wacc.py -v
```

Expected: `ERROR` com `ModuleNotFoundError: No module named 'tools.curvas_kd_ke_wacc'`.

- [ ] **Step 3: Criar o pacote e a implementação mínima do modelo**

Criar `tools/__init__.py` vazio.

Criar `tools/curvas_kd_ke_wacc.py` com este conteúdo:

```python
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize_scalar


@dataclass(frozen=True)
class CurveParameters:
    tax_rate: float = 0.25
    risk_free_rate: float = 0.05
    market_risk_premium: float = 0.0778
    unlevered_beta: float = 0.90
    max_debt_ratio: float = 0.80


def kd_gross(
    debt_ratio: np.ndarray,
    params: CurveParameters,
) -> np.ndarray:
    debt_ratio = np.asarray(debt_ratio, dtype=float)
    high_leverage_premium = 0.20 * (
        np.maximum(0.0, debt_ratio - 0.40) / 0.40
    ) ** 2
    return 0.06 + 0.02 * debt_ratio + high_leverage_premium


def levered_beta(
    debt_ratio: np.ndarray,
    params: CurveParameters,
) -> np.ndarray:
    debt_ratio = np.asarray(debt_ratio, dtype=float)
    debt_to_equity = debt_ratio / (1.0 - debt_ratio)
    return params.unlevered_beta * (
        1.0 + (1.0 - params.tax_rate) * debt_to_equity
    )


def ke(
    debt_ratio: np.ndarray,
    params: CurveParameters,
) -> np.ndarray:
    return (
        params.risk_free_rate
        + levered_beta(debt_ratio, params) * params.market_risk_premium
    )


def wacc(
    debt_ratio: np.ndarray,
    params: CurveParameters,
) -> np.ndarray:
    debt_ratio = np.asarray(debt_ratio, dtype=float)
    equity_ratio = 1.0 - debt_ratio
    after_tax_kd = kd_gross(debt_ratio, params) * (1.0 - params.tax_rate)
    return equity_ratio * ke(debt_ratio, params) + debt_ratio * after_tax_kd


def calculate_curves(
    params: CurveParameters,
    points: int = 401,
) -> dict[str, np.ndarray]:
    if points < 2:
        raise ValueError("points deve ser pelo menos 2")

    debt_ratio = np.linspace(0.0, params.max_debt_ratio, points)
    gross_debt_cost = kd_gross(debt_ratio, params)
    return {
        "debt_ratio": debt_ratio,
        "kd_gross": gross_debt_cost,
        "kd_after_tax": gross_debt_cost * (1.0 - params.tax_rate),
        "ke": ke(debt_ratio, params),
        "wacc": wacc(debt_ratio, params),
    }


def find_wacc_minimum(
    params: CurveParameters,
) -> tuple[float, float]:
    result = minimize_scalar(
        lambda value: float(wacc(np.array([value]), params)[0]),
        bounds=(0.0, params.max_debt_ratio),
        method="bounded",
        options={"xatol": 1e-13},
    )
    if not result.success:
        raise RuntimeError(f"Falha ao minimizar WACC: {result.message}")
    return float(result.x), float(result.fun)
```

- [ ] **Step 4: Rodar os testes do modelo e confirmar sucesso**

Run:

```bash
python3 -m unittest tests/test_curvas_kd_ke_wacc.py -v
```

Expected: `Ran 5 tests` e `OK`.

- [ ] **Step 5: Commitar o modelo e seus testes**

```bash
git add tools/__init__.py tools/curvas_kd_ke_wacc.py tests/test_curvas_kd_ke_wacc.py
git commit -m "feat: modela curvas de Kd Ke e WACC"
```

### Task 2: Implementar e testar a renderização

**Files:**

- Modify: `tools/curvas_kd_ke_wacc.py`
- Modify: `tests/test_curvas_kd_ke_wacc.py`

- [ ] **Step 1: Expandir os testes com os requisitos dos arquivos renderizados**

Substituir `tests/test_curvas_kd_ke_wacc.py` por este conteúdo completo:

```python
import struct
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tools.curvas_kd_ke_wacc import (
    CurveParameters,
    calculate_curves,
    find_wacc_minimum,
    kd_gross,
    ke,
    render_figure,
    wacc,
)


class CurveModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.params = CurveParameters()

    def test_kd_endpoints_match_design(self) -> None:
        values = kd_gross(np.array([0.0, 0.8]), self.params)
        self.assertAlmostEqual(float(values[0]), 0.06, places=10)
        self.assertAlmostEqual(float(values[1]), 0.276, places=10)

    def test_ke_without_debt_starts_near_twelve_percent(self) -> None:
        value = float(ke(np.array([0.0]), self.params)[0])
        self.assertAlmostEqual(value, 0.12002, places=8)

    def test_wacc_uses_after_tax_kd(self) -> None:
        debt_ratio = 0.4
        kd_value = float(kd_gross(np.array([debt_ratio]), self.params)[0])
        ke_value = float(ke(np.array([debt_ratio]), self.params)[0])
        expected = (
            (1.0 - debt_ratio) * ke_value
            + debt_ratio * kd_value * (1.0 - self.params.tax_rate)
        )
        actual = float(wacc(np.array([debt_ratio]), self.params)[0])
        self.assertAlmostEqual(actual, expected, places=12)

    def test_continuous_minimum_matches_design(self) -> None:
        debt_ratio, minimum = find_wacc_minimum(self.params)
        self.assertAlmostEqual(debt_ratio, 0.412870635, places=7)
        self.assertAlmostEqual(minimum, 0.113349398, places=7)

    def test_curve_shapes_match_teaching_model(self) -> None:
        curves = calculate_curves(self.params, points=801)
        minimum_index = int(np.argmin(curves["wacc"]))

        self.assertTrue(np.all(np.diff(curves["kd_gross"]) >= 0.0))
        self.assertTrue(np.all(np.diff(curves["ke"]) > 0.0))
        self.assertLess(curves["wacc"][minimum_index], curves["wacc"][0])
        self.assertLess(curves["wacc"][minimum_index], curves["wacc"][-1])


class FigureRenderingTests(unittest.TestCase):
    def test_render_creates_expected_png_and_svg(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_directory = Path(temporary_directory)
            png_path, svg_path = render_figure(output_directory)

            self.assertTrue(png_path.is_file())
            self.assertTrue(svg_path.is_file())
            self.assertGreater(png_path.stat().st_size, 100_000)
            self.assertGreater(svg_path.stat().st_size, 10_000)

            with png_path.open("rb") as png_file:
                png_file.seek(16)
                width, height = struct.unpack(">II", png_file.read(8))
            self.assertEqual((width, height), (2400, 960))

            svg_text = svg_path.read_text(encoding="utf-8")
            self.assertIn("<svg", svg_text)
            self.assertIn("Custo da dívida", svg_text)
            self.assertIn("Custo do equity", svg_text)
            self.assertIn("WACC mínimo", svg_text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Rodar os testes e confirmar que a renderização ainda não existe**

Run:

```bash
python3 -m unittest tests/test_curvas_kd_ke_wacc.py -v
```

Expected: `ERROR` com `ImportError: cannot import name 'render_figure'`.

- [ ] **Step 3: Substituir o módulo pela implementação completa de cálculo e renderização**

Substituir `tools/curvas_kd_ke_wacc.py` por este conteúdo completo:

```python
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter
from scipy.optimize import minimize_scalar


@dataclass(frozen=True)
class CurveParameters:
    tax_rate: float = 0.25
    risk_free_rate: float = 0.05
    market_risk_premium: float = 0.0778
    unlevered_beta: float = 0.90
    max_debt_ratio: float = 0.80


def kd_gross(
    debt_ratio: np.ndarray,
    params: CurveParameters,
) -> np.ndarray:
    debt_ratio = np.asarray(debt_ratio, dtype=float)
    high_leverage_premium = 0.20 * (
        np.maximum(0.0, debt_ratio - 0.40) / 0.40
    ) ** 2
    return 0.06 + 0.02 * debt_ratio + high_leverage_premium


def levered_beta(
    debt_ratio: np.ndarray,
    params: CurveParameters,
) -> np.ndarray:
    debt_ratio = np.asarray(debt_ratio, dtype=float)
    debt_to_equity = debt_ratio / (1.0 - debt_ratio)
    return params.unlevered_beta * (
        1.0 + (1.0 - params.tax_rate) * debt_to_equity
    )


def ke(
    debt_ratio: np.ndarray,
    params: CurveParameters,
) -> np.ndarray:
    return (
        params.risk_free_rate
        + levered_beta(debt_ratio, params) * params.market_risk_premium
    )


def wacc(
    debt_ratio: np.ndarray,
    params: CurveParameters,
) -> np.ndarray:
    debt_ratio = np.asarray(debt_ratio, dtype=float)
    equity_ratio = 1.0 - debt_ratio
    after_tax_kd = kd_gross(debt_ratio, params) * (1.0 - params.tax_rate)
    return equity_ratio * ke(debt_ratio, params) + debt_ratio * after_tax_kd


def calculate_curves(
    params: CurveParameters,
    points: int = 401,
) -> dict[str, np.ndarray]:
    if points < 2:
        raise ValueError("points deve ser pelo menos 2")

    debt_ratio = np.linspace(0.0, params.max_debt_ratio, points)
    gross_debt_cost = kd_gross(debt_ratio, params)
    return {
        "debt_ratio": debt_ratio,
        "kd_gross": gross_debt_cost,
        "kd_after_tax": gross_debt_cost * (1.0 - params.tax_rate),
        "ke": ke(debt_ratio, params),
        "wacc": wacc(debt_ratio, params),
    }


def find_wacc_minimum(
    params: CurveParameters,
) -> tuple[float, float]:
    result = minimize_scalar(
        lambda value: float(wacc(np.array([value]), params)[0]),
        bounds=(0.0, params.max_debt_ratio),
        method="bounded",
        options={"xatol": 1e-13},
    )
    if not result.success:
        raise RuntimeError(f"Falha ao minimizar WACC: {result.message}")
    return float(result.x), float(result.fun)


def style_axis(axis: plt.Axes, y_min: float, y_max: float) -> None:
    axis.set_xlim(0.0, 80.0)
    axis.set_ylim(y_min, y_max)
    axis.set_xticks([0.0, 20.0, 40.0, 60.0, 80.0])
    axis.xaxis.set_major_formatter(PercentFormatter(xmax=100.0, decimals=0))
    axis.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
    axis.grid(axis="y", color="#D9DEE7", linewidth=0.8, linestyle=(0, (2, 4)))
    axis.spines[["top", "right"]].set_visible(False)
    axis.spines[["left", "bottom"]].set_color("#9AA3B2")
    axis.tick_params(colors="#596273", labelsize=8)
    axis.set_xlabel("Dívida / Valor total", fontsize=9, color="#374151")


def render_figure(output_directory: Path) -> tuple[Path, Path]:
    params = CurveParameters()
    curves = calculate_curves(params, points=801)
    optimal_debt_ratio, minimum_wacc = find_wacc_minimum(params)
    debt_percent = curves["debt_ratio"] * 100.0

    blue = "#2563EB"
    orange = "#EA580C"
    green = "#15803D"
    ink = "#172033"
    muted = "#596273"
    background = "#F5F7FA"

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.titlesize": 13,
            "svg.fonttype": "none",
        }
    )
    figure, axes = plt.subplots(1, 3, figsize=(12.0, 4.8), dpi=200)
    figure.patch.set_facecolor(background)
    for axis in axes:
        axis.set_facecolor("#FFFFFF")

    kd_axis, ke_axis, wacc_axis = axes

    kd_axis.plot(
        debt_percent,
        curves["kd_gross"],
        color=blue,
        linewidth=2.8,
        label="Kd bruto",
    )
    kd_axis.plot(
        debt_percent,
        curves["kd_after_tax"],
        color=blue,
        linewidth=2.0,
        linestyle=(0, (5, 4)),
        alpha=0.65,
        label="Kd líquido",
    )
    style_axis(kd_axis, 0.035, 0.295)
    kd_axis.set_title("Custo da dívida, Kd", color=ink, loc="left")
    kd_axis.set_ylabel("Custo anual", fontsize=9, color="#374151")
    kd_axis.legend(frameon=False, fontsize=8, loc="upper left")
    kd_axis.annotate(
        "Risco de crédito contido",
        xy=(20.0, float(kd_gross(np.array([0.20]), params)[0])),
        xytext=(5.0, 0.105),
        fontsize=7.5,
        color=muted,
        arrowprops={"arrowstyle": "->", "color": "#8B95A5", "lw": 0.8},
    )
    kd_axis.annotate(
        "Spread abre",
        xy=(68.0, float(kd_gross(np.array([0.68]), params)[0])),
        xytext=(48.0, 0.245),
        fontsize=7.5,
        color=blue,
        arrowprops={"arrowstyle": "->", "color": blue, "lw": 0.8},
    )

    ke_axis.plot(debt_percent, curves["ke"], color=orange, linewidth=2.8)
    style_axis(ke_axis, 0.10, 0.35)
    ke_axis.set_title("Custo do equity, Ke", color=ink, loc="left")
    ke_axis.annotate(
        "Risco residual se concentra\nnos acionistas",
        xy=(42.0, float(ke(np.array([0.42]), params)[0])),
        xytext=(7.0, 0.25),
        fontsize=7.5,
        color=muted,
        arrowprops={"arrowstyle": "->", "color": "#8B95A5", "lw": 0.8},
    )

    optimal_percent = optimal_debt_ratio * 100.0
    wacc_axis.axvspan(0.0, optimal_percent, color=green, alpha=0.06)
    wacc_axis.axvspan(optimal_percent, 80.0, color=orange, alpha=0.045)
    wacc_axis.plot(debt_percent, curves["wacc"], color=green, linewidth=3.0)
    wacc_axis.axvline(
        optimal_percent,
        color=green,
        linewidth=1.0,
        linestyle=(0, (3, 4)),
        alpha=0.75,
    )
    wacc_axis.scatter(
        [optimal_percent],
        [minimum_wacc],
        s=38,
        color=green,
        edgecolor="white",
        linewidth=1.2,
        zorder=5,
    )
    style_axis(wacc_axis, 0.105, 0.24)
    wacc_axis.set_title("Custo médio, WACC", color=ink, loc="left")
    wacc_axis.annotate(
        f"WACC mínimo: {minimum_wacc:.2%}\nD/V: {optimal_debt_ratio:.1%}",
        xy=(optimal_percent, minimum_wacc),
        xytext=(46.0, 0.125),
        fontsize=7.5,
        fontweight="bold",
        color=green,
        arrowprops={"arrowstyle": "->", "color": green, "lw": 0.8},
    )
    wacc_axis.text(
        4.0,
        0.226,
        "Benefício fiscal predomina",
        fontsize=7.2,
        color=green,
    )
    wacc_axis.text(
        48.0,
        0.226,
        "Risco financeiro predomina",
        fontsize=7.2,
        color=orange,
    )

    figure.suptitle(
        "Curvas de Kd, Ke e WACC versus endividamento",
        x=0.05,
        y=0.965,
        ha="left",
        fontsize=18,
        fontweight="bold",
        color=ink,
    )
    figure.text(
        0.05,
        0.905,
        "Simulação didática com premissas ilustrativas",
        ha="left",
        fontsize=10,
        color=muted,
    )
    figure.text(
        0.05,
        0.075,
        "Premissas: imposto 25%, Rf 5,0%, prêmio de mercado 7,78%, beta desalavancado 0,90. Eixos verticais independentes.",
        ha="left",
        fontsize=7.3,
        color=muted,
    )
    figure.text(
        0.05,
        0.035,
        "Curvas ilustrativas. Neste modelo, o U resulta do benefício fiscal e do aumento assumido em Kd e Ke com alta alavancagem.",
        ha="left",
        fontsize=7.3,
        color=muted,
    )
    figure.subplots_adjust(left=0.055, right=0.985, top=0.80, bottom=0.22, wspace=0.27)

    output_directory.mkdir(parents=True, exist_ok=True)
    png_path = output_directory / "CurvasKdKeWacc.png"
    svg_path = output_directory / "CurvasKdKeWacc.svg"
    figure.savefig(png_path, dpi=200, facecolor=background)
    figure.savefig(svg_path, facecolor=background)
    plt.close(figure)
    return png_path, svg_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera as curvas didáticas de Kd, Ke e WACC."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("Vault/Attachments"),
        help="Diretório dos arquivos PNG e SVG.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    png_path, svg_path = render_figure(args.output_dir)
    optimal_debt_ratio, minimum_wacc = find_wacc_minimum(CurveParameters())
    print(f"PNG: {png_path}")
    print(f"SVG: {svg_path}")
    print(f"Ótimo: D/V={optimal_debt_ratio:.2%}, WACC={minimum_wacc:.2%}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Rodar toda a suíte e confirmar sucesso**

Run:

```bash
python3 -m unittest tests/test_curvas_kd_ke_wacc.py -v
```

Expected: `Ran 6 tests` e `OK`.

- [ ] **Step 5: Commitar a renderização testada**

```bash
git add tools/curvas_kd_ke_wacc.py tests/test_curvas_kd_ke_wacc.py
git commit -m "feat: renderiza curvas didaticas de capital"
```

### Task 3: Gerar, validar e registrar os artefatos finais

**Files:**

- Create: `Vault/Attachments/CurvasKdKeWacc.png`
- Create: `Vault/Attachments/CurvasKdKeWacc.svg`

- [ ] **Step 1: Gerar os dois arquivos finais**

Run:

```bash
python3 -m tools.curvas_kd_ke_wacc --output-dir Vault/Attachments
```

Expected:

```text
PNG: Vault/Attachments/CurvasKdKeWacc.png
SVG: Vault/Attachments/CurvasKdKeWacc.svg
Ótimo: D/V=41.29%, WACC=11.33%
```

- [ ] **Step 2: Verificar dimensões, tamanho e estrutura dos arquivos**

Run:

```bash
python3 -m unittest tests/test_curvas_kd_ke_wacc.py -v
```

Expected: `Ran 6 tests` e `OK`.

Run:

```bash
python3 -c 'import struct; p="Vault/Attachments/CurvasKdKeWacc.png"; f=open(p,"rb"); f.seek(16); print(struct.unpack(">II",f.read(8))); f.close()'
```

Expected: `(2400, 960)`.

Run:

```bash
python3 -c 'import xml.etree.ElementTree as ET; ET.parse("Vault/Attachments/CurvasKdKeWacc.svg"); print("SVG válido")'
```

Expected: `SVG válido`.

- [ ] **Step 3: Inspecionar visualmente o PNG**

Abrir `Vault/Attachments/CurvasKdKeWacc.png` com a ferramenta de inspeção de imagem e confirmar:

- Os três painéis estão inteiros e alinhados.
- Nenhum título, rótulo ou rodapé está cortado.
- O Kd bruto e o Kd líquido são distinguíveis.
- O mínimo do WACC está marcado em 41,3%.
- As anotações não cobrem as curvas.
- O texto permanece legível na visualização padrão.

Se qualquer item falhar, ajustar apenas posições, tamanhos de fonte ou margens em `tools/curvas_kd_ke_wacc.py`, rodar novamente os seis testes e repetir a inspeção.

- [ ] **Step 4: Commitar os artefatos finais**

```bash
git add Vault/Attachments/CurvasKdKeWacc.png Vault/Attachments/CurvasKdKeWacc.svg
git commit -m "docs: adiciona graficos de Kd Ke e WACC"
```

- [ ] **Step 5: Confirmar estado final do repositório**

Run:

```bash
git status --short --branch
```

Expected: nenhuma alteração pendente; a branch aparece à frente apenas pelos commits produzidos durante este trabalho.
