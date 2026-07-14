import cv2
import mediapipe as mp
import math
import numpy as np

# A forma moderna de controlar o som no Windows (Sem comtypes, sem Activate!)
from pycaw.pycaw import AudioUtilities

# 1. Configurar o controle de áudio do Windows (Super Direto)
dispositivo = AudioUtilities.GetSpeakers()
volume = dispositivo.EndpointVolume

# Obter o alcance do volume do computador (mínimo e máximo em dB)
alcance_vol = volume.GetVolumeRange()
vol_min = alcance_vol[0]
vol_max = alcance_vol[1]

# 2. Inicializar o MediaPipe
mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils
maos = mp_maos.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Obter o alcance do volume do computador (mínimo e máximo em dB)
alcance_vol = volume.GetVolumeRange()
vol_min = alcance_vol[0]
vol_max = alcance_vol[1]

# 2. Inicializar o MediaPipe
mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils
maos = mp_maos.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# 3. Inicializar a câmera
webcam = cv2.VideoCapture(0)
print("Iniciando o Maestro com Controle de Volume... Aperte 'q' para sair.")

while True:
    sucesso, frame = webcam.read()
    if not sucesso:
        print("Erro ao acessar a webcam.")
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = maos.process(frame_rgb)

    if resultado.multi_hand_landmarks:
        for pontos_maos in resultado.multi_hand_landmarks:
            # Desenhar os pontos vermelhos e conexões na tela
            mp_desenho.draw_landmarks(frame, pontos_maos, mp_maos.HAND_CONNECTIONS)

            # Obter coordenadas do Polegar (ponto 4) e Indicador (ponto 8)
            polegar = pontos_maos.landmark[4]
            indicador = pontos_maos.landmark[8]

            # Converter coordenadas normalizadas para pixels na tela
            x1, y1 = int(polegar.x * w), int(polegar.y * h)
            x2, y2 = int(indicador.x * w), int(indicador.y * h)

            # Desenhar círculos destacados nesses dois dedos
            cv2.circle(frame, (x1, y1), 10, (255, 0, 0), cv2.FILLED) # Azul no polegar
            cv2.circle(frame, (x2, y2), 10, (255, 0, 0), cv2.FILLED) # Azul no indicador
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)      # Linha conectando os dois

            # Calcular o centro da linha (onde vamos exibir a bolinha de status)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Calcular a distância matemática (Hipotenusa) entre os dois pontos
            distancia = math.hypot(x2 - x1, y2 - y1)

            # Mapear a distância da câmera para a escala do volume do Windows
            # Se a distância for menor que 30px -> Volume 0%. Se for maior que 200px -> Volume 100%
            vol_ajustado = np.interp(distancia, [30, 200], [vol_min, vol_max])
            porcentagem_vol = np.interp(distancia, [30, 200], [0, 100])

            # Aplicar o volume de fato no Windows
            volume.SetMasterVolumeLevel(vol_ajustado, None)

            # Mudar a cor da bolinha central se o volume estiver no mínimo (mudo)
            if distancia < 30:
                cv2.circle(frame, (cx, cy), 10, (0, 0, 255), cv2.FILLED) # Vermelho (Mudo)
            else:
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED) # Verde (Ativo)

            # Exibir a porcentagem do volume na tela
            cv2.putText(frame, f'Volume: {int(porcentagem_vol)}%', (40, 50), 
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Maestro Virtual - Controle de Volume", frame)

    # Aperte 'q' para fechar a tela
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()