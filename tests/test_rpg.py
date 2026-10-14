import unittest
from unittest.mock import MagicMock
from src.model import HeroiModel
from src.presenter import HeroiPresenter

class TestSistemaRPG(unittest.TestCase):

    # TESTE 1: Ir para a batalha (Verifica abates, vida restante e loot recebido)
    def test_1_batalha_registra_abates_reduz_hp_e_coleta_loot(self):
        # Arrange (Ataque 30 mata até 3 inimigos por batalha)
        heroi = HeroiModel("Guerreiro", hp_maximo=100, ataque_base=30, capacidade_inventario=3)
        
        # Act (Enfrenta 3 inimigos causando 10 de dano cada = 30 de dano total)
        relatorio = heroi.ir_para_batalha(qtd_inimigos=3, dano_por_inimigo=10, loot_dropado="Poção de Vida")
        
        # Assert
        self.assertEqual(relatorio["inimigos_mortos_na_batalha"], 3)
        self.assertEqual(relatorio["hp_restante"], 70)
        self.assertEqual(relatorio["loot_recebido"], "Poção de Vida")
        self.assertIn("Poção de Vida", heroi.inventario)

    # TESTE 2: Uso de Poção de Dano (Aumenta ataque e capacidade de abates na batalha)
    def test_2_usar_pocao_dano_aumenta_ataque_e_abates(self):
        # Arrange
        heroi = HeroiModel("Berserker", hp_maximo=100, ataque_base=20, capacidade_inventario=3)
        heroi.adicionar_loot("Poção de Dano")
        
        # Act (Usa a poção ganhando +20 de bónus -> Ataque vai para 40 -> Abate até 4 inimigos)
        novo_ataque = heroi.usar_pocao_dano(bonus=20)
        relatorio = heroi.ir_para_batalha(qtd_inimigos=4, dano_por_inimigo=5)
        
        # Assert
        self.assertEqual(novo_ataque, 40)
        self.assertEqual(relatorio["inimigos_mortos_na_batalha"], 4)

    # TESTE 3: Edge Case de Limite Mínimo (HP nunca fica negativo em batalha letal)
    def test_3_batalha_letal_nao_deixa_hp_abaixo_de_zero(self):
        # Arrange
        heroi = HeroiModel("Soldado", hp_maximo=50, ataque_base=20, capacidade_inventario=2)
        
        # Act (Enfrenta 10 inimigos com 20 de dano cada = 200 de dano para 50 de HP)
        relatorio = heroi.ir_para_batalha(qtd_inimigos=10, dano_por_inimigo=20, loot_dropado="Poção de Vida")
        
        # Assert (HP trava em 0 e herói morto não coleta o loot final)
        self.assertEqual(relatorio["hp_restante"], 0)
        self.assertIsNone(relatorio["loot_recebido"])

    # TESTE 4: Edge Case de Limite Máximo (Poção de Vida não ultrapassa o HP Máximo)
    def test_4_pocao_de_vida_nao_ultrapassa_hp_maximo(self):
        # Arrange
        heroi = HeroiModel("Paladino", hp_maximo=100, ataque_base=20, capacidade_inventario=2)
        heroi.ir_para_batalha(qtd_inimigos=1, dano_por_inimigo=15, loot_dropado="Poção de Vida") # Fica com 85 HP
        
        # Act (Cura 35 de vida tendo 85/100)
        hp_apos_cura = heroi.usar_pocao_vida(valor_cura=35)
        
        # Assert
        self.assertEqual(hp_apos_cura, 100)

    # TESTE 5: Edge Case de Limite de Inventário e Exceções
    def test_5_mochila_cheia_recusa_loot_e_valores_invalidos_lancam_erro(self):
        # Arrange (Capacidade para apenas 1 item)
        heroi = HeroiModel("Ladino", hp_maximo=100, ataque_base=20, capacidade_inventario=1)
        heroi.adicionar_loot("Poção de Dano")
        
        # Act & Assert 1: Batalha tenta dar 2º loot com mochila cheia
        relatorio = heroi.ir_para_batalha(qtd_inimigos=1, dano_por_inimigo=5, loot_dropado="Poção de Vida")
        self.assertIsNone(relatorio["loot_recebido"])
        self.assertEqual(len(heroi.inventario), 1)

        # Act & Assert 2: Passar inimigos zerados/negativos dispara ValueError
        with self.assertRaises(ValueError):
            heroi.ir_para_batalha(qtd_inimigos=0, dano_por_inimigo=10)

    # TESTE 6: Teste do Presenter com Mock (Verifica se a View recebe o relatório da batalha)
    def test_6_presenter_envia_relatorio_de_batalha_para_view(self):
        # Arrange
        model = HeroiModel("Arqueiro", hp_maximo=100, ataque_base=20, capacidade_inventario=3)
        mock_view = MagicMock()
        presenter = HeroiPresenter(model, mock_view)
        
        # Act
        presenter.iniciar_incursao(qtd_inimigos=2, dano_por_inimigo=10, possivel_loot="Poção de Dano")
        
        # Assert
        mock_view.exibir_relatorio_batalha.assert_called_once()

if __name__ == "__main__":
    unittest.main()