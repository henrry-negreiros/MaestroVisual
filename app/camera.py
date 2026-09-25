import cv2

class Camera:
    def __init__(self):
        # cv2.CAP_DSHOW no Windows acelera a abertura da câmera
        self.webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # Otimiza a resolução para tornar o processamento da IA mais leve e rápido
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Configura a janela para iniciar em tamanho compacto
        nome_janela = "Maestro Virtual - Controle por Gestos"
        cv2.namedWindow(nome_janela, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(nome_janela, 320, 240)
        
    # Força a janela a NÃO ficar no topo (0 = Normal/Segundo plano)
        try:
            propriedade_topo = getattr(cv2, 'WND_PROP_TOPMOST', getattr(cv2, 'WNDPROP_TOPMOST', 1))
            cv2.setWindowProperty(self.nome_janela, propriedade_topo, 0)
        except Exception:
            pass

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