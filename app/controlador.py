import pyautogui
import numpy as np
from pycaw.pycaw import AudioUtilities

class ControladorSO:
    def __init__(self):
        # Desativa o delay padrão do PyAutoGUI para as ações de mídia serem instantâneas
        pyautogui.PAUSE = 0
        
        # Inicializa o controle de áudio nativo do Windows (PyCaw)
        self.dispositivo = AudioUtilities.GetSpeakers()
        self.volume = self.dispositivo.EndpointVolume
        
        # Pega os limites de volume do seu computador em decibéis (dB)
        alcance_vol = self.volume.GetVolumeRange()
        self.vol_min = alcance_vol[0]
        self.vol_max = alcance_vol[1]

    def ajustar_volume(self, distancia_pixels):
        # Mapeia a distância geométrica dos dedos (30 a 200 pixels) para a escala de dB do Windows
        vol_ajustado = np.interp(distancia_pixels, [30, 200], [self.vol_min, self.vol_max])
        self.volume.SetMasterVolumeLevel(vol_ajustado, None)

    def executar_comando_midia(self, comando):
        # Simula o pressionamento das teclas multimídia físicas do teclado
        if comando == "MUTE":
            pyautogui.press('volumemute')
        elif comando == "PLAYPAUSE":
            pyautogui.press('playpause')
        elif comando == "PROXIMA":
            # Usamos uma combinação robusta: pressiona a tecla de mídia e garante o comando
            pyautogui.keyDown('nexttrack')
            pyautogui.keyUp('nexttrack')
            
            # Caso o player seja o navegador/Spotify Web, o atalho universal abaixo ajuda:
            # pyautogui.hotkey('ctrl', 'right')
        

    def pegar_porcentagem_atual(self):
        # Lê o volume atual do Windows e converte de decibéis para uma escala bonita de 0 a 100%
        vol_atual_db = self.volume.GetMasterVolumeLevel()
        porcentagem = int(np.interp(vol_atual_db, [self.vol_min, self.vol_max], [0, 100]))
        return porcentagem