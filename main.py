import os
import time
import random
from src.model import HeroiModel
from src.view import ConsoleView
from src.presenter import HeroiPresenter

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_lento(linhas: list, delay: float = 0.06):
    """Imprime linha por linha dando efeito de carregamento de monitor antigo."""
    for linha in linhas:
        print(linha, flush=True)
        time.sleep(delay)

def cabecalho_robco():
    linhas = [
        "========================================================",
        "   ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM v.85       ",
        "   COPYRIGHT 2075-2077 ROBCO INDUSTRIES                 ",
        "   [PIP-BOY 2000 // MODULO DE SOBREVIVENCIA ATIVO]      ",
        "========================================================"
    ]
    print_lento(linhas, delay=0.04)

def rodar_jogo():
    # Ativa cor verde fosforo no terminal
    if os.name == 'nt':
        os.system('color 0A')
    print("\033[92m", end="")

    heroi = HeroiModel("Sobrevivente", hp_maximo=100, ataque_base=20, capacidade_inventario=3)
    view = ConsoleView()
    presenter = HeroiPresenter(heroi, view)

    loots_possiveis = ["Poção de Vida", "Poção de Dano"]

    while heroi.hp_atual > 0:
        # 1. Limpa a tela a cada novo turno
        limpar_tela()
        cabecalho_robco()

        blocos_hp = int((heroi.hp_atual / heroi.hp_maximo) * 10)
        barra_hp = "#" * blocos_hp + "-" * (10 - blocos_hp)
        itens_txt = ", ".join(heroi.inventario) if heroi.inventario else "VAZIO"

        # 2. Carrega o menu linha por linha
        menu = [
            "",
            "--------------------------------------------------------",
            f" STATUS  :: HP [{barra_hp}] {heroi.hp_atual}/{heroi.hp_maximo} | ATK: {heroi.ataque_total} | KILLS: {heroi.inimigos_derrotados}",
            f" MOCHILA :: [{len(heroi.inventario)}/{heroi.capacidade_inventario} SLOTS] -> {itens_txt}",
            "--------------------------------------------------------",
            " SELECIONE O COMANDO:",
            "  [1] Explorar a Wasteland (Entrar em Combate)",
            "  [2] Usar Pocao de Vida   (+35 HP)",
            "  [3] Usar Pocao de Dano   (+20 ATK)",
            "  [4] Desligar Terminal"
        ]
        print_lento(menu, delay=0.05)
        
        opcao = input("\nroot@pipboy:~# ")

        if opcao == "1":
            print_lento(["\n[SISTEMA] Rastreando sinais hostis na zona..."], delay=0.25)
            qtd_inimigos = random.randint(2, 6)
            dano_inimigo = random.randint(5, 10)
            loot_sorteado = random.choice(loots_possiveis)
            presenter.iniciar_incursao(qtd_inimigos, dano_inimigo, loot_sorteado)

        elif opcao == "2":
            if "Poção de Vida" not in heroi.inventario:
                print_lento(["\n[ERRO] Voce nao tem nenhuma Pocao de Vida na mochila."])
            elif heroi.hp_atual == heroi.hp_maximo:
                print_lento(["\n[AVISO] Seu HP ja ta no maximo, nao precisa gastar pocao agora."])
            else:
                heroi.usar_pocao_vida()
                print_lento([f"\n[OK] Pocao de Vida aplicada. HP recuperado para {heroi.hp_atual}/{heroi.hp_maximo}."])

        elif opcao == "3":
            atk_antes = heroi.ataque_total
            if heroi.usar_pocao_dano() > atk_antes:
                print_lento([
                    f"\n[OK] Buff de dano ativado! Seu ataque subiu pra {heroi.ataque_total}.",
                    "     Agora voce leva mais inimigos por rodada."
                ])
            else:
                print_lento(["\n[ERRO] Voce nao tem Pocao de Dano na mochila."])

        elif opcao == "4":
            print_lento(["\n[SISTEMA] Encerrando sessao do terminal... Ate mais."])
            break
        else:
            print_lento(["\n[ERRO DE SINTAXE] Comando invalido. Digita de 1 a 4."])

        # 3. Se o heroi ainda estiver vivo, espera dar ENTER antes de limpar a tela pro proximo turno
        if heroi.hp_atual > 0:
            input("\n[Pressione ENTER para atualizar o terminal...]")

    if heroi.hp_atual == 0:
        fim_de_jogo = [
            "",
            "========================================================",
            " [SINAL VITAL PERDIDO // VOCE MORREU]                   ",
            f" Fim da linha, cara. Voce levou {heroi.inimigos_derrotados} inimigos antes de cair.",
            "========================================================"
        ]
        print_lento(fim_de_jogo, delay=0.12)

    print("\033[0m", end="") # Reseta a cor ao sair

if __name__ == "__main__":
    rodar_jogo()