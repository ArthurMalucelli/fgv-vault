---
materia: Programacao
aula: 10
tema: Aula de exercícios — síntese de tipos básicos, strings, listas, iteração
quiz: 2026-05-05
---

# Aula 10: Exercícios (síntese)

NÃO temos o notebook teórico desta aula, só os dois cadernos de exercícios. Pelo conteúdo, dá pra inferir que foi uma aula de PRÁTICA combinando tipos básicos, manipulação de strings, listas, e introdução à iteração com `for ... in range(len())`.

Provavelmente os exercícios desta aula caem com peso no quiz, justamente porque foram feitos pra fixar o que veio antes.

## Tópicos cobertos pelos exercícios

### Bloco 1: TIPOS BÁSICOS

**Operações com inteiros (// e %):**

```python
n = 543
centenas = n // 100   # 5 (parte inteira da divisão por 100)
dezenas = (n // 10) % 10   # 4 (parte inteira da divisão por 10, módulo 10)
unidades = n - centenas * 100 - dezenas * 10   # 3
```
Output: `5`, `4`, `3`

A pegadinha aqui é montar a expressão correta de "dezenas". Alternativas comuns no multiple choice:
- `(n // 10) % 10` ✓ correto
- `n // 10` (errado, retorna 54)
- `n % 100 // 10` ✓ também correto
- `n % 10` (errado, retorna 3 que é unidades)

**Verificar tudo minúsculo:**
```python
texto = input(...)
if texto == texto.lower():
    print('o texto contém somente minusculas')
else:
    print('o texto contém minúsculas e maíusculas')
```

Note: `s.islower()` também funciona, mas a aula usou comparação direta.

**Substituir múltiplos caracteres (geração de senha):**
```python
senha = texto.replace('o', '0').replace('z', '2').replace('1', '!').replace('a', 'A')
```
Cada `replace` retorna NOVA string. Encadeia na sequência.

**Comparação CPF (string vs int):**
- CPF como int: `cpf = 71503115801` (sem zeros à esquerda)
- CPF digitado pelo user: `'715.031.158-01'`
- Pra comparar: limpar pontos e hífen, converter pra int, comparar
```python
cpf_user = input('CPF:').replace('.', '').replace('-', '')
cpf_user = int(cpf_user)
if cpf_user == cpf:
    print('CPF identificado')
else:
    print('CPF não identificado')
```

Pegadinha: CPF começando com 0. Se você converter pra int, perde os zeros. Daí precisa comparar com cuidado.

**Mascarar CPF (mostrar parcial):**
- Dado: `261.667.140-92`
- Mostrar: `***.667.140-**`
- Usa slicing: `'***' + cpf[3:11] + '**'` (ou similar)

### Bloco 2: LISTAS

**Predizer output sem rodar:**

| Código | Resposta |
|---|---|
| `a = [1,2,3,4,5]; len(a)` | `5` (NÃO 6 — pegadinha clássica) |
| `a = [1,2,3,4,5]; a[1]` | `2` (NÃO 1 — índice começa em 0) |
| `a = [1,2,3,4,5]; a[5]` | **IndexError** (índices vão de 0 a 4) |
| `a = [1,2,3,4,5]; a[-4]` | `2` (não 1!) |
| `a = ['Araçatuba']; len(a)` | `1` |
| `a = ['Araçatuba']; len(a[0])` | `9` (caracteres da string dentro) |

**Iteração: as duas formas mais usadas**

Forma 1 (iterar pelos elementos):
```python
a = ['Batman', 'Hulk', 'Thor', 'Aquaman']
for i in a:
    print(i)
```
Output:
```
Batman
Hulk
Thor
Aquaman
```

Forma 2 (iterar pelos índices):
```python
for i in range(len(a)):
    print(a[i])
```
Output igual ao anterior. Mas aqui `i` é 0, 1, 2, 3 e você usa `a[i]`.

**Diferença CRÍTICA:**
- Forma 1: `i` é o ELEMENTO (`'Batman'`, `'Hulk'`, ...)
- Forma 2: `i` é o ÍNDICE (`0`, `1`, `2`, `3`)
- Se você usa `i` como índice na Forma 1 (`a[i]`), erro.

**Iterar e calcular:**
```python
a = ['Batman', 'Hulk', 'Thor', 'Aquaman']
s = 0
for i in a:
    s = s + len(i)
print(s)   # 6 + 4 + 4 + 7 = 21
```

```python
for i in a:
    print(len(i))
```
Output:
```
6
4
4
7
```

**Concatenação de listas com `+` e `*`:**
```python
material_escritorio = ['caneta', 'lápis', 'caderno']
material_limpeza = ['sabão', 'detergente']

compras_totais = material_escritorio + material_limpeza
# ['caneta', 'lápis', 'caderno', 'sabão', 'detergente']

compras_totais = material_escritorio + material_limpeza * 2
# ['caneta', 'lápis', 'caderno', 'sabão', 'detergente', 'sabão', 'detergente']
# multiplica APENAS material_limpeza por 2 (precedência)
```

Pegadinha: `*` em lista REPETE os elementos. `material_limpeza * 2` = `['sabão', 'detergente', 'sabão', 'detergente']`. Não soma, não vira matriz.

**Ordenação:**
```python
compras_ordenada = sorted(compras_totais)   # nova lista
compras_totais.sort()   # modifica in-place, retorna None
```

## Pegadinhas pro quiz

**1. `a[len(a)]` é sempre IndexError**
- Lista de tamanho 5: `len(a)` = 5. Mas índices vão de 0 a 4. `a[5]` quebra.

**2. `a[-1]` é o ÚLTIMO, `a[-len(a)]` é o PRIMEIRO**
- `a = [1,2,3,4,5]`. `a[-1]` = 5, `a[-5]` = 1, `a[-6]` = IndexError.

**3. `for i in a` vs `for i in range(len(a))`**
- A primeira: `i` é o elemento.
- A segunda: `i` é o índice (0, 1, 2, ...).
- Se a alternativa mistura, errou.

**4. Lista vazia `len([]) = 0`, `[0]` tem `len = 1`**
- `[]` é lista vazia, len 0.
- `[0]` é lista com um elemento (zero), len 1.
- `[[]]` é lista com uma lista vazia dentro, len 1.

**5. `lista * n` repete; `lista + lista` concatena**
- `[1,2] * 3` = `[1, 2, 1, 2, 1, 2]`
- `[1,2] + [3,4]` = `[1, 2, 3, 4]`
- `[1,2] + 3` = TypeError (não pode somar lista com int)

**6. Modificar item por índice é OK**
- `a[0] = 'novo'` funciona em lista (mutável).
- Em string DÁ ERRO: `s[0] = 'X'` → TypeError, strings imutáveis.

## Aplicação financeira (BTC)

Exercício menciona dados de fechamento de Bitcoin. Padrão típico:
```python
# encontrar dia (índice) do menor preço
indice_min = 0
for i in range(len(prices)):
    if prices[i] < prices[indice_min]:
        indice_min = i

# retorno log diário: r_t = ln(preco_t / preco_{t-1})
import numpy as np
retornos = []
for i in range(1, len(prices)):
    r = np.log(prices[i] / prices[i-1])
    retornos.append(r)
```

## Pra fixar

- `//` divisão inteira, `%` resto, fundamentais pra extrair dígitos
- `replace()` retorna nova string, encadeia múltiplos
- `len(lista)` = nº elementos; índices válidos: `0` a `len-1`
- `for i in lista` → elemento; `for i in range(len(lista))` → índice
- `lista * 2` repete; `lista1 + lista2` concatena
- Lista é MUTÁVEL (modifica por índice OK), string IMUTÁVEL (não modifica por índice)
