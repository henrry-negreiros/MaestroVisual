# MaestroVirtual - Sistema de Controle Computacional por Visão Computacional

O **MaestroVirtual** é um software autoral de Interação Natural do Usuário (NUI) desenvolvido em Python para permitir o controle de sistemas operacionais e apresentações (como PowerPoint) sem contato físico, utilizando uma webcam convencional.

O sistema processa o fluxo de vídeo em tempo real, mapeia os pontos articulares das mãos e converte gestos específicos em comandos nativos do Windows OS (via atalhos de teclado e manipulação de janelas), eliminando a necessidade de periféricos físicos como mouses ou passadores de slide.

---

## 1. Modos de Operação e Mapeamento de Gestos

O software opera com uma Máquina de Estados Finitos (FSM) para validar a intenção dos gestos e evitar disparos acidentais (*falsos positivos*).

### Modo Apresentação
* **Iniciar Apresentação (`F5`):** Manter o punho fechado por 2,0 segundos e abrir a mão. O sistema dispara a tecla `F5` e altera o foco do SO para trazer a janela do PowerPoint para o primeiro plano.
* **Navegação de Slides (`Direita` / `Esquerda`):** Dedo indicador levantado, realizando movimento de varredura horizontal no eixo X (arraste para a esquerda avança; arraste para a direita retorna).


### Modo Mídia
* **Ajuste de Volume (0% a 100%):** Distância vetorial euclidiana entre as extremidades do polegar e do indicador (gesto de pinça).
* **Play / Pause:** Polegar apontado para cima com os demais dedos recolhidos.
* **Mute / Unmute:** Gestos com os dedos indicador e médio levantados (sinal de V).
* **Trava de Segurança de Áudio:** Punho fechado no modo mídia para congelar a barra de volume e permitir a movimentação livre da mão.

---

## 2. Arquitetura Técnica e Tecnologias

* **Linguagem:** Python 3.10+
* **Processamento de Vídeo:** OpenCV (captura em resolução otimizada $320 \times 240$ a 30 FPS para minimizar uso de CPU/GPU).
* **Reconhecimento de Gestos:** Google MediaPipe Hands (extração e rastreamento de 21 coordenadas tridimensionais das articulações da mão).
* **Integração com SO:** PyAutoGUI (emulação de eventos de teclado) e PyGetWindow (gerenciamento e alternância de foco entre janelas ativas).
* **Compilação:** PyInstaller (empacotamento na modalidade `--onedir` para otimização de tempo de inicialização em ambiente de execução final).

---

## 3. Estrutura do Projeto

```text
MaestroVirtual/
├── app/
│   ├── camera.py        # Inicialização da webcam e tratamento dos frames OpenCV
│   ├── controlador.py   # Gerenciamento de foco de janelas e emulação de comandos do SO
│   └── gestos.py        # Mapeamento vetorial, cálculo de distâncias e máquina de estados
├── maestro_ia.py        # Loop principal e inicialização dos componentes
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação técnica

1. Clone o repositório:
```bash
git clone https://github.com/henrry-negreiros/MaestroVisual 
cd MaestroVisual

2. ative o ambiente virtual: 
'' no Windows:
venv\Scripts\activate

3. instale as dependencias necessárias:
pip install -r requirements.txt

4.execute a aplicação: 
python maestro_ia.py 

5. geração executável (exe) 
 pyinstaller --noconsole --onedir --noconfirm --name "MaestroVirtual_v2" --collect-all mediapipe maestro_ia.py