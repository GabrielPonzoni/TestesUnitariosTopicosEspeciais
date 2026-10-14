# Testabilidade em Jogos: Sistema de Batalha e Sobrevivência (Arquitetura MVP)



Trabalho prático desenvolvido para a disciplina de Tópicos Especiais em Jogos e Entretenimento Digital (Unisinos). O objetivo principal é demonstrar a aplicação de Testes Unitários e de Integração, isolando as regras de negócio em classes puras desacopladas de qualquer motor gráfico ou interface.



## 📂 Estrutura do Repositório



O projeto segue uma estrutura limpa organizada em pacotes para o código-fonte e para os testes automatizados:



```text

TestesUnitariosTopicosEspeciais/

├── .vscode/

│   └── settings.json        # Configuração do Test Runner (unittest)

├── src/

│   ├── __init__.py

│   ├── model.py             # Classes puras (Regras de negócio de Combate e Inventário)

│   ├── presenter.py         # Camada Presenter (Interligação Model <-> View)

│   └── view.py              # Camada View (Interface estilo terminal retro)

├── tests/

│   ├── __init__.py

│   └── test_rpg.py          # Bateria de 6 Testes Unitários (Padrão AAA + Edge Cases + Mocks)

├── main.py                  # Ponto de entrada do jogo (Loop jogável no terminal)

└── README.md

```



## 📐 Arquitetura Utilizada (MVP)



O sistema foi construído aplicando o padrão **Model-View-Presenter (MVP)**:

- **Model (`src/model.py`)**: Contém a lógica pura do herói, cálculos de incursão na wasteland, controle de abates, gerenciamento de slots do inventário e limites de atributos (HP e Ataque).

- **Presenter (`src/presenter.py`)**: Intermedeia a comunicação escutando eventos/callbacks disparados pelo Model e repassando as atualizações para a View.

- **View (`src/view.py`)**: Exibe os relatórios formatados de combate.



## 🧪 Cobertura de Testes Unitários



O ficheiro `tests/test_rpg.py` contém **6 testes unitários** desenvolvidos sob o padrão **AAA (Arrange-Act-Assert)**, cobrindo fluxos principais e *Edge Cases* essenciais:

1. **Regra de Combate**: Validação do registo de abates, cálculo de dano sofrido e coleta de loot.

2. **Buffs e Progressão**: Uso de poções de dano para elevar o poder de fogo e a capacidade de abates.

3. **Casos de Borda (HP Mínimo)**: Garantia de que o HP do herói nunca ultrapassa o limite inferior de `0` (morte em combate letal).

4. **Casos de Borda (HP Máximo)**: Garantia de que o uso de poções de cura respeita estritamente o teto de `HP Máximo`.

5. **Casos de Borda (Inventário e Exceções)**: Validação de recusa de itens com mochila cheia e disparo de exceções (`ValueError`) para entradas inválidas.

6. **Integração MVP com Mocks**: Uso de simulações (`MagicMock`) para atestar que o Presenter repassa corretamente os relatórios para a View sem acoplamento rígido.



---



## 🚀 Como Executar o Jogo



Certifique-se de ter o **Python 3** instalado em sua máquina. Para iniciar a simulação interativa no terminal (estilo Pip-Boy / Anos 80):



```bash

python main.py

```



## 🛠️ Como Executar os Testes Unitários



Pode rodar os testes de duas formas:



1. **Pelo VS Code**: Abra a aba de testes (**Tubo de Ensaio / Testing** na barra lateral esquerda) e clique em *Run Tests*.

2. **Pelo Terminal**:

   ```bash

   python -m unittest discover -s tests -p "test_*.py" -t . -v