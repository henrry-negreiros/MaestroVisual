import cv2
import numpy as np

class InterfaceHUD:
    """
    Módulo responsável por desenhar a interface gráfica (HUD) 
    sobre o frame da webcam com cores dinâmicas e notificações de gestos.
    """
    def __init__(self):
        # Cores BGR
        self.COR_AZUL_NEON = (255, 191, 0)
        self.COR_VERDE_NEON = (50, 205, 50)
        self.COR_VERMELHO = (50, 50, 255)
        self.COR_ROXO = (255, 0, 128)
        self.COR_AMARELO_NEON = (0, 215, 255)  # Cor para o modo Apresentação
        self.COR_PAINEL = (20, 20, 20)
        self.COR_TEXTO = (240, 240, 240)

    def _obter_cor_estado(self, estado_atual):
        """ Retorna a cor do painel de acordo com a ação realizada """
        if "AJUSTANDO" in estado_atual:
            return self.COR_VERDE_NEON
        elif "SWIPE" in estado_atual or "PROXIM" in estado_atual or "ANTERIOR" in estado_atual or "SLIDE" in estado_atual:
            return self.COR_ROXO
        elif "AGUARDANDO" in estado_atual or "NENHUM" in estado_atual:
            return self.COR_AZUL_NEON
        return self.COR_AZUL_NEON

    def desenhar_painel_status(self, frame, estado_atual, porcentagem_vol, modo_atual="MIDIA"):
        """
        Desenha o painel superior com cor dinâmica e o modo ativo.
        """
        cor_destaque = self._obter_cor_estado(estado_atual)

        # Retângulo escuro semi-transparente (Aumentado para acomodar a linha do MODO)
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (340, 115), self.COR_PAINEL, -1)
        
        alpha = 0.65
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Borda estilizada com a cor do estado atual
        cv2.rectangle(frame, (10, 10), (340, 115), cor_destaque, 2)

        # Cor do texto de MODO
        cor_modo = self.COR_AMARELO_NEON if modo_atual == "APRESENTACAO" else self.COR_VERDE_NEON

        # Texto do Modo
        cv2.putText(frame, f"MODO: {modo_atual}", (20, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor_modo, 2)

        # Texto do Estado Atual
        cv2.putText(frame, f"ESTADO: {estado_atual}", (20, 65), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, cor_destaque, 2)

        # Texto do Volume
        cv2.putText(frame, f"VOL: {int(porcentagem_vol)}%", (20, 95), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, self.COR_TEXTO, 1)

    def desenhar_barra_volume(self, frame, porcentagem_vol):
        """
        Desenha a barra lateral de volume limpa.
        """
        vol_int = int(porcentagem_vol)
        altura_barra = int(np.interp(vol_int, [0, 100], [400, 150]))

        # Fundo da barra
        cv2.rectangle(frame, (50, 150), (85, 400), (40, 40, 40), -1)

        # Preenchimento
        cv2.rectangle(frame, (50, altura_barra), (85, 400), self.COR_VERDE_NEON, -1)

        # Moldura
        cv2.rectangle(frame, (50, 150), (85, 400), (200, 200, 200), 2)