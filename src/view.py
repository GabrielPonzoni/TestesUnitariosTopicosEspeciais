import time

class ConsoleView:
    def imprimir_lento(self, linhas: list, delay: float = 0.08):
        """Imprime uma lista de linhas com atraso estilo terminal antigo."""
        for linha in linhas:
            print(linha, flush=True)
            time.sleep(delay)

    def exibir_relatorio_batalha(self, relatorio: dict, hp_maximo: int, ataque_atual: int):
        blocos_cheios = int((relatorio['hp_restante'] / hp_maximo) * 10)
        barra_hp = "#" * blocos_cheios + "-" * (10 - blocos_cheios)

        if relatorio["loot_recebido"]:
            linha_loot = f"| [!] LOOT ENCONTRADO: [{relatorio['loot_recebido'].upper()}]"
        else:
            linha_loot = "| [!] LOOT: NADA COLETADO (INVENTARIO CHEIO / SEM DROP)"

        linhas_relatorio = [
            "",
            "+------------------------------------------------------+",
            "| > LOG DE INCURSAO // RELATORIO DE COMBATE            |",
            "+------------------------------------------------------+",
            f"| [+] ALVOS ABATIDOS NA ZONA : {relatorio['inimigos_mortos_na_batalha']}",
            f"| [+] TOTAL DE ABATES        : {relatorio['total_abates']}",
            f"| [-] DANO SOFRIDO           : -{relatorio['dano_sofrido']} HP",
            f"| [*] INTEGRIDADE (HP)       : [{barra_hp}] {relatorio['hp_restante']}/{hp_maximo}",
            f"| [*] PODER DE FOGO ATUAL    : {ataque_atual} ATK",
            "+------------------------------------------------------+",
            linha_loot,
            "+------------------------------------------------------+"
        ]

        self.imprimir_lento(linhas_relatorio, delay=0.09)