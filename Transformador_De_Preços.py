"""
===============================================================
  TRANSFORMADOR DE PREÇO — PARADIGMA FUNCIONAL EM PYTHON
===============================================================
  Demonstra os princípios fundamentais da programação funcional:
    - Funções puras (sem efeitos colaterais)
    - Imutabilidade (uso de tuplas e frozenset)
    - Funções de alta ordem (map, filter, reduce)
    - Recursão (no lugar de loops)
    - Estilo declarativo (o QUÊ, não o COMO)
    - Transparência referencial
    - Composição de funções (pipe)
===============================================================
"""

from functools import reduce, partial
from typing import NamedTuple


# ---------------------------------------------------------------
# ESTRUTURAS DE DADOS IMUTÁVEIS
# NamedTuple é imutável por natureza — princípio fundamental do FP.
# Uma vez criado, o objeto não pode ser alterado; qualquer
# "modificação" gera um novo objeto.
# ---------------------------------------------------------------

class ReajusteHistorico(NamedTuple):
    ano: int            # Ano do reajuste
    percentual: float   # Ex: 0.10 = 10% de aumento
    motivo: str         # Descrição do motivo do reajuste


class Produto(NamedTuple):
    nome: str
    preco_base: float
    reajustes: tuple[ReajusteHistorico, ...]  # Tupla imutável de reajustes


class ResultadoFaturamento(NamedTuple):
    nome: str
    preco_original: float
    preco_reajustado: float
    variacao_percentual: float
    faturamento_estimado: float
    lucro_adicional: float


# ---------------------------------------------------------------
# DADOS HISTÓRICOS (imutáveis — definidos uma vez, nunca alterados)
# ---------------------------------------------------------------

HISTORICO_REAJUSTES: tuple[ReajusteHistorico, ...] = (
    ReajusteHistorico(2020, 0.05,  "Inflação IPCA 2020"),
    ReajusteHistorico(2021, 0.08,  "Alta de insumos pós-pandemia"),
    ReajusteHistorico(2022, 0.12,  "Crise energética + câmbio"),
    ReajusteHistorico(2023, 0.06,  "Reajuste salarial da equipe"),
    ReajusteHistorico(2024, 0.04,  "Melhora de margens operacionais"),
)

CATALOGO_PRODUTOS: tuple[Produto, ...] = (
    Produto("Notebook Pro",     3500.00, HISTORICO_REAJUSTES),
    Produto("Mouse Gamer",       250.00, HISTORICO_REAJUSTES[:3]),
    Produto("Teclado Mecânico",  420.00, HISTORICO_REAJUSTES[1:]),
    Produto("Monitor 4K",       1800.00, HISTORICO_REAJUSTES),
    Produto("Headset USB",       180.00, HISTORICO_REAJUSTES[:2]),
)

VOLUME_VENDAS: dict[str, int] = {
    "Notebook Pro":     120,
    "Mouse Gamer":      850,
    "Teclado Mecânico": 430,
    "Monitor 4K":       200,
    "Headset USB":      610,
}


# ---------------------------------------------------------------
# FUNÇÕES PURAS
# Sempre retornam o mesmo resultado para os mesmos argumentos.
# Não modificam nada fora do seu escopo.
# ---------------------------------------------------------------

def aplicar_reajuste(preco: float, reajuste: ReajusteHistorico) -> float:
    """Aplica um único reajuste percentual ao preço — função pura."""
    return preco * (1 + reajuste.percentual)


def calcular_preco_reajustado(produto: Produto) -> float:
    """
    Usa REDUCE para acumular todos os reajustes sobre o preço base.
    Equivale a: preco * (1+r1) * (1+r2) * ... * (1+rN)
    """
    return reduce(
        aplicar_reajuste,    # função binária pura
        produto.reajustes,   # coleção imutável
        produto.preco_base   # valor inicial (acumulador)
    )


def calcular_variacao(preco_original: float, preco_novo: float) -> float:
    """Calcula a variação percentual entre dois preços."""
    return ((preco_novo - preco_original) / preco_original) * 100


def calcular_faturamento(preco: float, volume: int) -> float:
    """Faturamento = preço × volume de vendas."""
    return preco * volume


def transformar_produto(volume_vendas: dict[str, int], produto: Produto) -> ResultadoFaturamento:
    """
    Transforma um Produto em ResultadoFaturamento.
    Não modifica nada — apenas transforma e retorna um novo objeto imutável.
    O volume_vendas é injetado via partial() (aplicação parcial).
    """
    preco_novo   = calcular_preco_reajustado(produto)
    variacao     = calcular_variacao(produto.preco_base, preco_novo)
    volume       = volume_vendas.get(produto.nome, 0)
    fat_original = calcular_faturamento(produto.preco_base, volume)
    fat_novo     = calcular_faturamento(preco_novo, volume)

    return ResultadoFaturamento(
        nome=produto.nome,
        preco_original=produto.preco_base,
        preco_reajustado=round(preco_novo, 2),
        variacao_percentual=round(variacao, 2),
        faturamento_estimado=round(fat_novo, 2),
        lucro_adicional=round(fat_novo - fat_original, 2),
    )


# ---------------------------------------------------------------
# PREDICADOS — funções booleanas puras usadas com filter()
# ---------------------------------------------------------------

def tem_reajuste_acima_de(limite: float, resultado: ResultadoFaturamento) -> bool:
    """Retorna True se a variação total superar o limite informado."""
    return resultado.variacao_percentual > limite


def tem_lucro_adicional_positivo(resultado: ResultadoFaturamento) -> bool:
    """Retorna True se o lucro adicional for positivo."""
    return resultado.lucro_adicional > 0


# ---------------------------------------------------------------
# COMPOSIÇÃO DE FUNÇÕES — pipe funcional
# Aplica uma sequência de funções ao mesmo valor.
# Equivale a: f3(f2(f1(valor)))
# ---------------------------------------------------------------

def pipe(valor, *funcoes):
    """Pipeline funcional: passa o valor por cada função em sequência."""
    return reduce(lambda v, f: f(v), funcoes, valor)


# ---------------------------------------------------------------
# RECURSÃO — alternativa funcional aos loops
# A função chama a si mesma com uma fatia menor da coleção
# até atingir o caso base (lista vazia).
# ---------------------------------------------------------------

def somar_faturamento_recursivo(resultados: tuple, acumulador: float = 0.0) -> float:
    """Soma o faturamento total via recursão — sem loop explícito."""
    if not resultados:               # Caso base — condição de parada
        return acumulador
    cabeca, *cauda = resultados      # Desestruturação: primeiro + resto
    return somar_faturamento_recursivo(
        tuple(cauda),
        acumulador + cabeca.faturamento_estimado
    )


def somar_lucro_recursivo(resultados: tuple, acumulador: float = 0.0) -> float:
    """Soma o lucro adicional total via recursão."""
    if not resultados:
        return acumulador
    cabeca, *cauda = resultados
    return somar_lucro_recursivo(tuple(cauda), acumulador + cabeca.lucro_adicional)


# ---------------------------------------------------------------
# APLICAÇÃO PARCIAL — partial() fixa argumentos antecipadamente,
# criando funções especializadas compatíveis com map() e filter()
# ---------------------------------------------------------------

# Especializa transformar_produto com o dicionário de volumes fixo
transformar_com_volume = partial(transformar_produto, VOLUME_VENDAS)

# Especializa o predicado com o limite de 30%
reajuste_alto = partial(tem_reajuste_acima_de, 30.0)


# ---------------------------------------------------------------
# PIPELINE PRINCIPAL — estilo declarativo puro
# Sem variáveis sendo reatribuídas, sem loops, sem estado mutável.
# Tudo é uma cadeia de transformações sobre dados imutáveis.
# ---------------------------------------------------------------

def executar_pipeline() -> dict:
    """Pipeline funcional: transforma, filtra e agrega os dados."""

    # MAP: transforma cada Produto → ResultadoFaturamento
    todos_resultados: tuple = tuple(
        map(transformar_com_volume, CATALOGO_PRODUTOS)
    )

    # FILTER: filtra produtos com reajuste acima de 30%
    produtos_alto_reajuste: tuple = tuple(
        filter(reajuste_alto, todos_resultados)
    )

    # FILTER: filtra produtos com lucro adicional positivo
    produtos_lucrativos: tuple = tuple(
        filter(tem_lucro_adicional_positivo, todos_resultados)
    )

    # RECURSÃO: agrega os totais sem loop
    faturamento_total = somar_faturamento_recursivo(todos_resultados)
    lucro_total       = somar_lucro_recursivo(todos_resultados)

    # sorted() retorna nova coleção — não muta a original
    ranking = tuple(
        sorted(todos_resultados, key=lambda r: r.faturamento_estimado, reverse=True)
    )

    return {
        "todos":               todos_resultados,
        "alto_reajuste":       produtos_alto_reajuste,
        "lucrativos":          produtos_lucrativos,
        "faturamento_total":   round(faturamento_total, 2),
        "lucro_total":         round(lucro_total, 2),
        "ranking_faturamento": ranking,
    }


# ---------------------------------------------------------------
# FORMATAÇÃO — funções puras de apresentação
# ---------------------------------------------------------------

def formatar_linha(resultado: ResultadoFaturamento) -> str:
    """Converte um ResultadoFaturamento em string legível — função pura."""
    return (
        f"  {'─' * 48}\n"
        f"  Produto          : {resultado.nome}\n"
        f"  Preço Original   : R$ {resultado.preco_original:>10.2f}\n"
        f"  Preço Reajustado : R$ {resultado.preco_reajustado:>10.2f}\n"
        f"  Variação Total   : {resultado.variacao_percentual:>+.2f}%\n"
        f"  Faturamento Est. : R$ {resultado.faturamento_estimado:>10,.2f}\n"
        f"  Lucro Adicional  : R$ {resultado.lucro_adicional:>10,.2f}\n"
    )


def imprimir_relatorio(relatorio: dict) -> None:
    """
    Única função com efeito colateral (print) — isolada propositalmente.
    Em FP, efeitos colaterais ficam nas bordas do sistema,
    mantendo o núcleo da lógica puro e testável.
    """
    sep = "═" * 52

    print(f"\n{sep}")
    print("  RELATÓRIO DE REAJUSTE DE PREÇOS")
    print(f"{sep}\n")

    print("📦 TODOS OS PRODUTOS:\n")
    print("\n".join(map(formatar_linha, relatorio["todos"])))

    print(f"\n{sep}")
    print("  🔺 PRODUTOS COM REAJUSTE ACIMA DE 30%:")
    print(f"{sep}\n")
    if relatorio["alto_reajuste"]:
        print("\n".join(map(formatar_linha, relatorio["alto_reajuste"])))
    else:
        print("  Nenhum produto nessa categoria.\n")

    print(f"\n{sep}")
    print("  🏆 RANKING POR FATURAMENTO ESTIMADO:")
    print(f"{sep}\n")
    for i, r in enumerate(relatorio["ranking_faturamento"], start=1):
        print(f"  {i}º {r.nome:<22} → R$ {r.faturamento_estimado:>12,.2f}")

    print(f"\n{sep}")
    print("  📊 TOTAIS CONSOLIDADOS:")
    print(f"{sep}")
    print(f"  Faturamento Total Estimado : R$ {relatorio['faturamento_total']:>12,.2f}")
    print(f"  Lucro Adicional Total      : R$ {relatorio['lucro_total']:>12,.2f}")
    print(f"{sep}\n")


# ---------------------------------------------------------------
# PONTO DE ENTRADA
# pipe() compõe o pipeline: executa → imprime
# ---------------------------------------------------------------

if __name__ == "__main__":
    pipe(
        executar_pipeline(),   # produz o relatório (puro)
        imprimir_relatorio     # consome o relatório (único efeito colateral)
    )