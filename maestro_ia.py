import cv2 
import time
import os
from app.camera import Camera
from app.detector import DetectorMaos
from app.gestos import CalculadorGestos
from app.controlador import ControladorSO
from app.interface import InterfaceHUD
from dashboard import start_dashboard, update_hud  # Importação do painel web (Stark HUD)

def main():
    print("==================================================")
    print(" [MAESTRO VIRTUAL] - SISTEMA DE DEFESA VTO  ")
    print("==================================================")
    
    # 1. Bloco de Inicialização Segura
    
    try:
        print("[INFO] A inicializar câmara e módulos de IA...")
        obj_camera = Camera()
        obj_detector = DetectorMaos()
        obj_gestos = CalculadorGestos()
        obj_audio = ControladorSO()
        obj_hud = InterfaceHUD()

        start_dashboard()  # Inicia o servidor web no celular em segundo plano
        
        volume_atual = 50
        estado_atual = "INICIANDO"
        modo_atual = "MIDIA"  # Alterna entre "MIDIA" e "APRESENTACAO"

        print("[INFO] Maestro Virtual Iniciado com Sucesso!")
        print("[INFO] Pressione 'm' para alternar o modo (Mídia / Apresentação)")
        print("[INFO] Pressione 'q' para sair.")
        print("--------------------------------------------------")

    except Exception as e:
        print(f"[ERRO CRÍTICO NA INICIALIZAÇÃO]: {e}")
        return

    # 2. Loop Principal Blindado
    try:
        while True:
            # Proteção na captura de frame (evita quebrar se houver oscilação na porta USB do datashow)
            try:
                sucesso, frame = obj_camera.capturar_frame()
                if not sucesso or frame is None:
                    print("[AVISO] Frame instável ou vazio. A tentar recuperar...")
                    time.sleep(0.1)
                    continue
            except Exception as cam_err:
                print(f"[AVISO CÂMARA]: {cam_err}")
                time.sleep(0.1)
                continue
     
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

            # --- TRATAMENTO DO GESTO: ABRIR SLIDE ---
            elif estado_gesto == "ABRIR_SLIDE":
                caminho_slide = r"C:\Users\Gabriel\OneDrive\Anexos\Área de Trabalho\TRABALHO-VTO\apresentação_VTO.ppsx"
                
                if os.path.exists(caminho_slide):
                    os.startfile(caminho_slide)
                    obj_audio.focar_janela_powerpoint()
                    print(" Apresentação iniciada e focada!") 
                else:
                    obj_audio.executar_comando_slide("INICIAR")
                
                modo_atual = "APRESENTACAO"
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

            # Atualiza o painel do celular em tempo real com o estado atual
            try:
                update_hud(f"[MAESTRO] Status: {estado_atual}")
            except:
                pass  # Evita quebra caso haja perda momentânea de conexão web móvel

            # Desenha a Interface Gráfica (HUD no PC)
            obj_hud.desenhar_painel_status(frame, estado_atual, volume_atual, modo_atual)
            obj_hud.desenhar_barra_volume(frame, volume_atual)

            # Exibe o frame final
            cv2.imshow("Maestro Virtual - Controle por Gestos", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n[INFO] Encerramento manual solicitado pelo operador.")
                break
            elif key == ord('m'):
                modo_atual = "APRESENTACAO" if modo_atual == "MIDIA" else "MIDIA"
                print(f" Modo alterado para: {modo_atual}")

    except KeyboardInterrupt:
        print("\n[INFO] Execução interrompida manualmente pelo utilizador (Ctrl+C).")

    except Exception as e:
        print(f"\n[EXCEÇÃO CRÍTICA CAPTURADA NO LOOP]: {e}")
        print("[INFO] A manter a estabilidade do sistema...")

    finally:
        # 3. Bloco de Encerramento e Libertação Segura de Recursos
        print("[INFO] A libertar recursos de vídeo e a fechar janelas...")
        try:
            obj_camera.liberar()
            cv2.destroyAllWindows()
        except Exception as cleanup_err:
            print(f"[AVISO LIMPEZA]: {cleanup_err}")
        print("[MAESTRO VIRTUAL] Sessão encerrada com segurança. Boa apresentação!")

if __name__ == "__main__":
    main()