import time
import cv2
from app.camera import Camera
from app.detector import DetectorMaos
from app.gestos import CalculadorGestos

def testar_maquina_estados():
    obj_camera = Camera()
    obj_detector = DetectorMaos()
    obj_gestos = CalculadorGestos()

    print("==================================================")
    print("🧪 INICIANDO TESTE DA MÁQUINA DE ESTADOS DO SLIDE")
    print("==================================================")
    print(" Passos do teste:")
    print(" 1. Feche a mão (✊) e segure por 2 segundos.")
    print(" 2. Aguarde a mensagem de confirmação no terminal.")
    print(" 3. Abra a mão (🖐️) para disparar o comando.")
    print(" Pressione 'q' na janela do vídeo para sair.\n")

    ultimo_estado_impresso = None

    while True:
        sucesso, frame = obj_camera.capturar_frame()
        if not sucesso:
            print("❌ Falha ao capturar imagem da câmera.")
            break

        # Processa os pontos da mão
        frame = obj_detector.encontrar_maos(frame)
        lista_pontos = obj_detector.pegar_posicoes(frame)

        tempo_atual = time.time()

        # Chama a análise de gestos
        estado_gesto, _ = obj_gestos.analisar_gestos(lista_pontos, tempo_atual)

        # Monitoramento do Estado Interno no Terminal
        estado_interno = obj_gestos.estado_slide

        # Imprime no terminal sempre que o estado interno mudar
        if estado_interno != ultimo_estado_impresso:
            if estado_interno == 0:
                print("🔵 [ESTADO 0]: Aguardando mão fechada (✊)...")
            elif estado_interno == 1:
                print("🟡 [ESTADO 1]: Mão fechada detectada! Contando 2 segundos...")
            elif estado_interno == 2:
                print("🟢 [ESTADO 2]: 2 segundos atingidos! Abra a mão (🖐️) para disparar!")
            ultimo_estado_impresso = estado_interno

        # Se o gesto final for disparado
        if estado_gesto == "ABRIR_SLIDE":
            print("\n🚀 [SUCESSO]: Comando 'ABRIR_SLIDE' disparado com sucesso!\n")

        # Exibe o preview simples da câmera
        cv2.imshow("Teste da Maquina de Estados (Pressione 'q' para sair)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    obj_camera.liberar()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    testar_maquina_estados()