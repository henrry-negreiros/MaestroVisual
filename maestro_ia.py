import cv2
import time
import numpy as np
from app.camera import Camera
from app.detector import DetectorMaos
from app.gestos import CalculadorGestos
from app.controlador import ControladorSO

def main():
    # Inicializa todos os módulos do nosso sistema estruturado
    obj_camera = Camera()
    obj_detector = DetectorMaos()
    obj_gestos = CalculadorGestos()
    obj_controlador = ControladorSO()

    print("Controlador Multimídia Modular Iniciado com Sucesso!")
    print("Pressione 'q' na janela da câmera para encerrar.")

    while True:
        # 1. Captura o frame através do módulo Camera
        sucesso, frame = obj_camera.capturar_frame()
        if not sucesso:
            break

        tempo_atual = time.time()

        # 2. Processa a IA e desenha o esqueleto através do módulo Detector
        frame = obj_detector.encontrar_maos(frame)
        pontos_mao = obj_detector.pegar_posicoes(frame)

        # 3. Analisa a matemática dos dedos através do módulo Gestos
        estado, valor_distancia = obj_gestos.analisar_gestos(pontos_mao, tempo_atual)

        # 4. Executa as ações no Windows baseadas no estado retornado
        if estado == "AJUSTANDO":
            obj_controlador.ajustar_volume(valor_distancia)
            cv2.putText(frame, "VOLUME AJUSTAVEL", (150, frame.shape[0] - 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
        elif estado in ["MUTE", "PLAYPAUSE", "PROXIMA"]:
            obj_controlador.executar_comando_midia(estado)
            
        # Feedbacks visuais na tela para o usuário (Interface)
        if estado == "TRAVADO":
            cv2.putText(frame, "VOLUME TRANCADO", (150, frame.shape[0] - 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        elif "MUTE" in estado:
            cv2.putText(frame, "Gesto: MUTE DE EMERGENCIA", (130, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        elif "PLAYPAUSE" in estado:
            cv2.putText(frame, "Gesto: PLAY / PAUSE", (170, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        elif "PROXIMA" in estado:
            cv2.putText(frame, "Gesto: PRÓXIMA MÚSICA", (150, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # 5. Renderização do Painel Visual de Volume (Barra Dinâmica)
        porcentagem = obj_controlador.pegar_porcentagem_atual()
        cor_painel = (0, 0, 255) if obj_gestos.volume_bloqueado else (0, 255, 0)

        # Mostra a porcentagem numérica
        cv2.putText(frame, f"{porcentagem}%", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, cor_painel, 3)

        # Desenha o fundo e o preenchimento da barra lateral
        altura_barra = int(np.interp(porcentagem, [0, 100], [400, 150]))
        cv2.rectangle(frame, (50, 150), (85, 400), (80, 80, 80), -1)
        cv2.rectangle(frame, (50, altura_barra), (85, 400), cor_painel, -1)
        cv2.rectangle(frame, (50, 150), (85, 400), (255, 255, 255), 2)

        # Exibe o frame final na tela
        cv2.imshow("Calibrador de Som por Gestos", frame)

        # Condição de saída: pressionar a tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera os recursos do hardware ao fechar
    obj_camera.liberar()

if __name__ == "__main__":
    main()