class HeroiModel:
    """
    Classe pura (Model) que isola toda a lógica de Batalha, Status e Loot.
    Não depende de interface visual nem de sorteios aleatórios diretos.
    """
    def __init__(self, nome: str, hp_maximo: int, ataque_base: int, capacidade_inventario: int):
        if hp_maximo <= 0 or ataque_base <= 0 or capacidade_inventario <= 0:
            raise ValueError("HP, ataque e capacidade devem ser maiores que zero.")
        
        self.nome = nome
        self.hp_maximo = hp_maximo
        self.hp_atual = hp_maximo
        self.ataque_base = ataque_base
        self.bonus_dano = 0
        self.capacidade_inventario = capacidade_inventario
        self.inventario = []
        self.inimigos_derrotados = 0
        self.callbacks_status = []

    @property
    def ataque_total(self) -> int:
        return self.ataque_base + self.bonus_dano

    def registar_ouvinte(self, callback):
        self.callbacks_status.append(callback)

    def _notificar_mudanca(self, relatorio: dict):
        for callback in self.callbacks_status:
            callback(relatorio)

    # FUNCIONALIDADE 1: Ir para a Batalha (Calcula abates, vida restante e coleta de Loot)
    def ir_para_batalha(self, qtd_inimigos: int, dano_por_inimigo: int, loot_dropado: str = None) -> dict:
        if qtd_inimigos <= 0 or dano_por_inimigo < 0:
            raise ValueError("Quantidade de inimigos deve ser positiva e o dano não pode ser negativo.")
        if self.hp_atual == 0:
            raise ValueError("O herói derrotado não pode ir para a batalha.")

        # Quantos inimigos o herói consegue derrotar com base no seu Ataque Total (mínimo 1)
        capacidade_abate = max(1, self.ataque_total // 10)
        inimigos_mortos = min(qtd_inimigos, capacidade_abate)
        self.inimigos_derrotados += inimigos_mortos

        # Calcula o dano total sofrido na incursão (respeitando o limite mínimo de 0 HP)
        dano_total = qtd_inimigos * dano_por_inimigo
        self.hp_atual = max(0, self.hp_atual - dano_total)

        # Se sobreviveu e caiu loot, tenta guardar na mochila
        loot_coletado = False
        if self.hp_atual > 0 and loot_dropado:
            loot_coletado = self.adicionar_loot(loot_dropado)

        relatorio = {
            "inimigos_mortos_na_batalha": inimigos_mortos,
            "total_abates": self.inimigos_derrotados,
            "dano_sofrido": dano_total,
            "hp_restante": self.hp_atual,
            "loot_recebido": loot_dropado if loot_coletado else None
        }
        self._notificar_mudanca(relatorio)
        return relatorio

    # FUNCIONALIDADE 2: Receber Loot no Inventário
    def adicionar_loot(self, item: str) -> bool:
        if not item or not item.strip():
            raise ValueError("Nome do item inválido.")
        if self.inventario_cheio():
            return False  # Edge Case: Inventário cheio
        self.inventario.append(item)
        return True

    # FUNCIONALIDADE 3: Checar Capacidade Máxima do Inventário
    def inventario_cheio(self) -> bool:
        return len(self.inventario) >= self.capacidade_inventario

    # FUNCIONALIDADE 4: Usar Poção de Vida (Cura respeitando o teto de HP Máximo)
    def usar_pocao_vida(self, valor_cura: int = 35) -> int:
        if valor_cura <= 0:
            raise ValueError("O valor de cura deve ser positivo.")
        if "Poção de Vida" not in self.inventario:
            return self.hp_atual
        
        self.inventario.remove("Poção de Vida")
        # Edge Case: HP nunca ultrapassa o HP Máximo
        self.hp_atual = min(self.hp_maximo, self.hp_atual + valor_cura)
        return self.hp_atual

    # FUNCIONALIDADE 5: Usar Poção de Dano (Aumenta o ataque e o poder de abate)
    def usar_pocao_dano(self, bonus: int = 20) -> int:
        if bonus <= 0:
            raise ValueError("O bónus de dano deve ser positivo.")
        if "Poção de Dano" not in self.inventario:
            return self.ataque_total

        self.inventario.remove("Poção de Dano")
        self.bonus_dano += bonus
        return self.ataque_total