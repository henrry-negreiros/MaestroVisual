import cv2
import time
import os
from app.camera import Camera
from app.detector import DetectorMaos
from app.gestos import CalculadorGestos
from app.controlador import ControladorSO
from app.interface import InterfaceHUD

def main():
    obj_camera = Camera()
    obj_detector = DetectorMaos()
    obj_gestos = CalculadorGestos()
    obj_audio = ControladorSO()
    obj_hud = InterfaceHUD()

    volume_atual = 50
    estado_atual = "INICIANDO"
    modo_atual = "MIDIA"  # Alterna entre "MIDIA" e "APRESENTACAO"

    print(" Maestro Virtual Fase 4 iniciado!")
    print(" Pressione 'm' para alternar o modo (Mídia / Apresentação)")
    print(" Pressione 'q' para sair.")

    while True:
        sucesso, frame = obj_camera.capturar_frame()
        if not sucesso:
            break
 
        # Processa a mão via IA
        frame = obj_detector.encontrar_maos(frame)
        lista_pontos = obj_detector.pegar_posicoes(frame)

        tempo_atual = time.time()

        # Chama o analisador de gestos
        estado_gesto, novo_vol = obj_gestos.analisar_gestos(lista_pontos, tempo_atual, modo_atual)

        # PROCESSAMENTO DOS ESTADOS E COMANDOS
        if estado_gesto in ["PLAYPAUSE", "MUTE"]:
            obj_audio.executar_comando_midia(estado_gesto)
            estado_atual = estado_gesto

        # --- TRATAMENTO DO NOVO GESTO: ABRIR SLIDE ---
        elif estado_gesto == "ABRIR_SLIDE":
            # Caminho opcional do arquivo de apresentação (caso queira abrir direto um arquivo)
            caminho_slide = r"C:\Users\Gabriel\OneDrive\Anexos\Área de Trabalho\TRABALHO-VTO\apresentação_VTO.ppsx"
            
            if os.path.exists(caminho_slide):
                os.startfile(caminho_slide)

                # Traz o PowerPoint para a frente automaticamente!
                obj_audio.focar_janela_powerpoint()
                print(" Apresentação iniciada e focada!") 
            else:
                obj_audio.executar_comando_slide("INICIAR")
            
            modo_atual = "APRESENTACAO"  # Muda o modo para apresentação automaticamente
            estado_atual = "ABRINDO SLIDE"

        elif estado_gesto == "PROXIMA":
            if modo_atual == "MIDIA":
                obj_audio.executar_comando_midia("PROXIMA")
            elif modo_atual == "APRESENTACAO":
                obj_audio.executar_comando_slide("PROXIMO")
            estado_atual = "PROXIMO SLIDE" if modo_atual == "APRESENTACAO" else "PROXIMA MUSICA"

        elif estado_gesto == "ANTERIOR":
            if modo_atual == "MIDIA":
                obj_audio.executar_comando_midia("ANTERIOR")
            elif modo_atual == "APRESENTACAO":
                obj_audio.executar_comando_slide("ANTERIOR")
            estado_atual = "SLIDE ANTERIOR" if modo_atual == "APRESENTACAO" else "MUSICA ANTERIOR"

        elif estado_gesto == "AJUSTANDO":
            volume_atual = novo_vol
            obj_audio.atualizar_volume(volume_atual)
            estado_atual = "AJUSTANDO"

        elif estado_gesto != "NENHUM":
            estado_atual = estado_gesto

        else:
            if len(lista_pontos) == 0:
                estado_atual = "AGUARDANDO MAO"

        # Desenha a Interface Gráfica (HUD)
        obj_hud.desenhar_painel_status(frame, estado_atual, volume_atual, modo_atual)
        obj_hud.desenhar_barra_volume(frame, volume_atual)

        # Exibe o frame final
        cv2.imshow("Maestro Virtual - Controle por Gestos", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m'):
            # Alterna entre os modos MIDIA e APRESENTACAO
            modo_atual = "APRESENTACAO" if modo_atual == "MIDIA" else "MIDIA"
            print(f" Modo alterado para: {modo_atual}")

    obj_camera.liberar()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 