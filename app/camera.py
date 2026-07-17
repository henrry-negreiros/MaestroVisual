import cv2

class Camera:
    def __init__(self):

        # Inicia a captura da webcam padrão (índice 0)
        self.webcam = cv2.VideoCapture(0)
        
    def capturar_frame(self):

        # Lê o frame atual da câmera
        sucesso, frame = self.webcam.read()
        if not sucesso:
            return False, None
            
        # Inverte o frame horizontalmente (efeito espelho)
        frame = cv2.flip(frame, 1)
        return True, frame
        
    def liberar(self):
        # Desliga a câmera e fecha as janelas quando o programa encerrar
        self.webcam.release()
        cv2.destroyAllWindows()