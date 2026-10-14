from src.model import HeroiModel

class HeroiPresenter:
    def __init__(self, model: HeroiModel, view):
        self.model = model
        self.view = view
        self.model.registar_ouvinte(self.ao_terminar_batalha)

    def ao_terminar_batalha(self, relatorio: dict):
        self.view.exibir_relatorio_batalha(relatorio, self.model.hp_maximo, self.model.ataque_total)

    def iniciar_incursao(self, qtd_inimigos: int, dano_por_inimigo: int, possivel_loot: str):
        return self.model.ir_para_batalha(qtd_inimigos, dano_por_inimigo, possivel_loot)