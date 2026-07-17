#  Maestro Virtual - Inteligência Artificial para Controle de Áudio

Este é o primeiro projeto do meu portfólio de Engenharia de Software e Inteligência Artificial. O **Maestro Virtual** é um sistema de Visão Computacional de alta performance projetado para interpretar gestos manuais capturados pela webcam para controlar e manipular a reprodução de áudio e mídias do Windows em tempo real.

---

##  Status do Projeto: Fase 2 Concluída (Arquitetura Modular)

Atualmente, o projeto concluiu com sucesso a sua **Fase 2**, atingindo a maturidade de um software comercial: a aplicação foi totalmente refatorada usando princípios de **Engenharia de Software (SOLID e POO)**, dividida em módulos independentes e equipada com filtros temporais e geométricos.

###  Gestos Mapeados e Comandos:
* **Ajuste de Volume Linear:** Distância dinâmica em pixels entre a ponta do Polegar e do Indicador (Pinça).
* **Play / Pause:** Gesto do **Joinha (👍)** (Polegar para cima com os outros 4 dedos fechados).
* **Avançar Música:** Movimento dinâmico de **Swipe** (Deslizar a mão aberta rapidamente da direita para a esquerda).
* **Mute de Emergência:** Gesto do **"V" de Vitória (✌️)**.
* **Trancar Volume:** Mão completamente fechada (Punho).
* **Destrancar Volume:** Juntar o polegar e o indicador em uma pinça curta (menos de 30px).

---

##  Tecnologias Utilizadas e Conceitos Aplicados

* **Python 3.11+:** Linguagem base do projeto.
* **OpenCV:** Captura, espelhamento e tratamento de matrizes de imagem em tempo real (conversão de canais BGR para RGB).
* **MediaPipe (Google):** Pipeline de IA utilizado para o rastreamento dos 21 pontos tridimensionais (landmarks) da mão humana.
* **PyAutoGUI & PyCaw:** Bibliotecas de integração para controle direto de hardware de áudio (dB) e simulação de teclas multimídia do SO.
* **Conceitos de Engenharia:** Encapsulamento, Máquina de Estados (State Machine), Debouncing para tratamento de oscilação de frames e Geometria Analítica (Distância Euclidiana via Teorema de Pitágoras).

---

##  Arquitetura do Sistema (Modular)

O software foi desacoplado para seguir o princípio de responsabilidade única:
```text
MaestroVisual/
│
├── app/
│   ├── __init__.py
│   ├── camera.py      # Responsável exclusivo pelo hardware da webcam
│   ├── detector.py    # Responsável exclusivo por rodar a IA do MediaPipe
│   ├── gestos.py      # Responsável exclusivo pela lógica matemática e estados
│   └── controlador.py # Responsável exclusivo pela ponte com o Windows
│
├── venv/              # Ambiente virtual isolado (Ignorado no Git)
├── maestro_ia.py      # Arquivo Main (Maestro que orquestra os módulos)
└── .gitignore         # Filtro de arquivos locais

1. Clone o repositório:
```bash
git clone https://github.com/henrry-negreiros/MaestroVisual 
cd MaestroVisual

2. ative o ambiente virtual: 
'' no Windows:
venv\Scripts\activate

3. instale as dependencias necessárias:
pip install opencv-python mediapipe pyautogui pycaw numpy

4.execute a aplicação: 
python maestro_ia.py
