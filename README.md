#  Maestro Virtual - Inteligência Artificial para Controle de Áudio

Este é o primeiro projeto do meu portfólio de engenharia de software e inteligência artificial. O **Maestro Virtual** é um sistema de Visão Computacional projetado para interpretar gestos manuais capturados pela webcam para controlar e manipular a reprodução de áudio em tempo real.

##  Status do Projeto
Atualmente, o projeto concluiu com sucesso a sua **Fase 1**, atingindo o marco de mapeamento de hardware, criação de ambiente virtual isolado e teste do fluxo bruto de vídeo capturado pela câmera através do OpenCV.

##  Tecnologias Utilizadas
* **Python 3.11+**: Linguagem base do projeto.
* **OpenCV**: Responsável pela captura de vídeo frame por frame e manipulação de matrizes de imagem.
* **MediaPipe (Google)**: Pipeline de IA utilizado para o mapeamento dos 21 pontos tridimensionais (landmarks) da mão humana em tempo real (*Próxima Fase*).

##  Configuração do Ambiente e Instalação

Para replicar o ambiente de desenvolvimento isolado deste projeto na sua máquina, siga os passos abaixo no terminal:

1. Clone o repositório:
```bash
git clone https://github.com/henrry-negreiros/MaestroVisual 
cd MaestroVisual