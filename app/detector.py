import cv2
import mediapipe as mp

class DetectorMaos:
    def __init__(self):
        # Inicializa as ferramentas de desenho e o modelo de mãos do MediaPipe
        self.mp_maos = mp.solutions.hands
        self.mp_desenho = mp.solutions.drawing_utils
        self.maos = self.mp_maos.Hands(
            max_num_hands=1, 
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.7
        )
        
    def encontrar_maos(self, frame):
        
        # O MediaPipe precisa da imagem em RGB, mas o OpenCV lê em BGR
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultado = self.maos.process(frame_rgb)
        
        # Se encontrou alguma mão, desenha os pontos e linhas na tela
        if self.resultado.multi_hand_landmarks:
            for hand_landmarks in self.resultado.multi_hand_landmarks:
                self.mp_desenho.draw_landmarks(frame, hand_landmarks, self.mp_maos.HAND_CONNECTIONS)
                
        return frame

    def pegar_posicoes(self, frame):
        lista_pontos = []
        altura, largura, _ = frame.shape
        
        # Se existirem pontos detectados, vamos extrair as coordenadas
        if self.resultado.multi_hand_landmarks:
            # Pegamos apenas a primeira mão detectada
            minha_mao = self.resultado.multi_hand_landmarks[0]
            
            # O MediaPipe nos dá valores de 0 a 1 (proporcional). 
            # Multiplicamos pela largura e altura para transformar em pixels reais da tela!
            for id, landmark in enumerate(minha_mao.landmark):
                cx, cy = int(landmark.x * largura), int(landmark.y * altura)
                lista_pontos.append({'id': id, 'x': cx, 'y': cy, 'raw_y': landmark.y})
                
        return lista_pontos