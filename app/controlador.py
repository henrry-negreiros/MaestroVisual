import pyautogui
import ctypes
import time

try:
    import pygetwindow as gw
except ImportError:
    gw = None

# Configuração de segurança do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

class ControladorSO:
    def __init__(self):
        self.volume = None
        self.inicializar_audio()

    def inicializar_audio(self):
        try:
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

            # Método usando a lista de dispositivos ativas do pycaw
            sessions = AudioUtilities.GetAllSessions()
            # Pega o ponteiro da interface COM de áudio master
            devices = AudioUtilities.GetSpeakers()
            
            # Acessa a interface COM por meio do objeto de interface nativo do comtypes
            from comtypes import GUID
            IID_IAudioEndpointVolume = GUID("{5CDF2C82-841E-4546-9722-0CF74078229A}")
            
            # Tenta conectar na interface nativa do endpoint
            if hasattr(devices, 'Activate'):
                self.volume = devices.Activate(IID_IAudioEndpointVolume, CLSCTX_ALL, None)
            elif hasattr(devices, '_dev'):
                self.volume = devices._dev.Activate(IID_IAudioEndpointVolume, CLSCTX_ALL, None)
        except Exception as e:
            print(f"Aviso: Usando modo de fallback de volume ({e})")

    def atualizar_volume(self, porcentagem):
        """
        Ajusta a porcentagem real (0 a 100) do Windows.
        """
        porcentagem_limpa = max(0, min(100, int(porcentagem)))
        nivel_escalar = porcentagem_limpa / 100.0

        if self.volume:
            try:
                # Altera na escala real (0.0 a 1.0) do slider do Windows
                self.volume.SetMasterVolumeLevelScalar(nivel_escalar, None)
                return
            except Exception:
                pass

        # Fallback: Se o ponteiro COM falhar, usa simulação do teclado do Windows
        porcentagem_atual = self.pegar_porcentagem_atual()
        diferenca = porcentagem_limpa - porcentagem_atual
        passos = int(abs(diferenca) / 2)

        if diferenca > 0:
            for _ in range(passos):
                pyautogui.press('volumeup')
        elif diferenca < 0:
            for _ in range(passos):
                pyautogui.press('volumedown')

    def pegar_porcentagem_atual(self):
        if self.volume:
            try:
                nivel = self.volume.GetMasterVolumeLevelScalar()
                return int(nivel * 100)
            except Exception:
                pass
        return 50

    # --- COMANDOS DE MÍDIA ---
    def executar_comando_midia(self, comando):
        """
        Executa comandos do reprodutor de mídia do Windows.
        """
        if comando == "MUTE":
            pyautogui.press('volumemute')
        elif comando == "PLAYPAUSE":
            pyautogui.press('playpause')
        elif comando in ["PROXIMA", "PROXIMO"]:
            pyautogui.press('nexttrack')
        elif comando == "ANTERIOR":
            pyautogui.press('prevtrack')

    # --- COMANDOS DE APRESENTAÇÃO (SLIDES) ---
    def focar_janela_powerpoint(self):
        """
        Busca e força a janela do PowerPoint/Apresentação a vir para o primeiro plano.
        """
        if not gw:
            return
            
        try:
            # Busca janelas do PowerPoint ou Apresentação de Slides
            janelas = gw.getWindowsWithTitle('PowerPoint')
            if not janelas:
                janelas = gw.getWindowsWithTitle('Apresentação do PowerPoint')
                
            if janelas:
                janela = janelas[0]
                # Se a janela estiver minimizada, restaura
                if janela.isMinimized:
                    janela.restore()
                # Traz para o primeiro plano e dá foco ativo
                janela.activate()
                time.sleep(0.3)  # Pequena pausa para o Windows processar a troca de foco
        except Exception as e:
            print(f"Aviso ao focar PowerPoint: {e}")

    def executar_comando_slide(self, comando):
        """
        Executa comandos de navegação para apresentações (PowerPoint, PDF, Canva).
        """
        if comando in ["PROXIMO", "PROXIMA"]:
            pyautogui.press('right')
            print(" Comando enviado: Próximo Slide")
        elif comando == "ANTERIOR":
            pyautogui.press('left')
            print("⬅ Comando enviado: Slide Anterior")
        elif comando == "INICIAR":
            pyautogui.press('f5')
            print(" Comando enviado: Iniciar Apresentação (F5)")
            time.sleep(0.6)
            self.focar_janela_powerpoint()  # Garante que o slide ganhe foco e cubra a câmera
        elif comando == "SAIR":
            pyautogui.press('esc')
            print(" Comando enviado: Sair da Apresentação") 