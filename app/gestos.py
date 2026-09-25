import math
import time

class CalculadorGestos:
    def __init__(self):
        self.intervalo_botoes = 1.2  # Cooldown entre comandos
        self.ultimo_comando_tempo = 0
        self.volume_bloqueado = False
        
        self.historico_x = []
        self.tamanho_historico = 6 

        # --- MÁQUINA DE ESTADOS DO SLIDE (INICIAR) ---
        self.estado_slide = 0          # 0: Aguardando, 1: Fechada (Timer), 2: Pronto para abrir
        self.tempo_inicio_fechado = 0
        self.TEMPO_FECHADO_NECESSARIO = 2.0 

        # --- MÁQUINA DE ESTADOS DO SLIDE (SAIR - MINDINHO) ---
        self.tempo_inicio_sair = None
        self.TEMPO_SAIR_NECESSARIO = 1.5

    def processar_gesto_apresentacao(self, quatro_dedos_fechados, polegar_para_cima, mao_aberta, tempo_atual):
        mao_fechada = quatro_dedos_fechados and (not polegar_para_cima)

        if self.estado_slide == 0:
            if mao_fechada:
                self.estado_slide = 1
                self.tempo_inicio_fechado = tempo_atual

        elif self.estado_slide == 1:
            if mao_fechada:
                if (tempo_atual - self.tempo_inicio_fechado) >= self.TEMPO_FECHADO_NECESSARIO:
                    self.estado_slide = 2
                    print("✨ Gesto carregado! Abra a mão para abrir a apresentação.")
            else:
                self.estado_slide = 0

        elif self.estado_slide == 2:
            if mao_aberta:
                self.estado_slide = 0
                self.ultimo_comando_tempo = tempo_atual
                return True
            elif not mao_fechada:
                # Se soltou a mão sem ser aberta, limpa para não travar o estado
                self.estado_slide = 0

        return False

    def analisar_gestos(self, pontos, tempo_atual, modo_atual="MIDIA"):
        if not pontos:
            self.historico_x.clear()
            self.estado_slide = 0
            self.tempo_inicio_sair = None
            return "NENHUM", 0

        # Mapeamento dos pontos principais
        p_polegar = next(p for p in pontos if p['id'] == 4)
        p_indicador = next(p for p in pontos if p['id'] == 8)
        p_medio = next(p for p in pontos if p['id'] == 12)
        p_anelar = next(p for p in pontos if p['id'] == 16)
        p_mindinho = next(p for p in pontos if p['id'] == 20)

        p_indicador_base = next(p for p in pontos if p['id'] == 6)
        p_medio_base = next(p for p in pontos if p['id'] == 10)
        p_anelar_base = next(p for p in pontos if p['id'] == 14)
        p_mindinho_base = next(p for p in pontos if p['id'] == 18)
        p_polegar_base = next(p for p in pontos if p['id'] == 2)

        # Checagem de elevação vertical
        indicador_aberto = p_indicador['y'] < p_indicador_base['y']
        medio_aberto = p_medio['y'] < p_medio_base['y']
        anelar_aberto = p_anelar['y'] < p_anelar_base['y']
        mindinho_aberto = p_mindinho['y'] < p_mindinho_base['y']
        polegar_para_cima = p_polegar['y'] < p_polegar_base['y'] and p_polegar['y'] < p_indicador_base['y']

        # Verificação global
        mao_aberta = indicador_aberto and medio_aberto and anelar_aberto and mindinho_aberto
        quatro_dedos_fechados = (not indicador_aberto) and (not medio_aberto) and (not anelar_aberto) and (not mindinho_aberto)

        # --- 1. MÁQUINA DE ESTADOS: ABRIR APRESENTAÇÃO (PUNHO FECHADO 2S -> ABRE A MÃO) ---
        if tempo_atual - self.ultimo_comando_tempo > self.intervalo_botoes:
            disparou_abrir = self.processar_gesto_apresentacao(
                quatro_dedos_fechados, polegar_para_cima, mao_aberta, tempo_atual
            )
            if disparou_abrir:
                return "ABRIR_SLIDE", 0

        if self.estado_slide == 2:
            return "CARREGADO_ABRA_A_MAO", 0

        ### --- 2. GESTO DE SAIR DA APRESENTAÇÃO (APENAS MINDINHO LEVANTADO POR 1.5S) ---
        apenas_mindinho = mindinho_aberto and (not indicador_aberto) and (not medio_aberto) and (not anelar_aberto)
        
        if apenas_mindinho:
            if self.tempo_inicio_sair is None:
                self.tempo_inicio_sair = tempo_atual
            
            tempo_decorrido = tempo_atual - self.tempo_inicio_sair
            
            # Se completou o tempo de 1.5s, dispara o comando de saída imediatamente
            if tempo_decorrido >= self.TEMPO_SAIR_NECESSARIO:
                self.tempo_inicio_sair = None
                self.ultimo_comando_tempo = tempo_atual
                return "SAIR", 0
            
            return "SAIR_CARREGANDO", 0
        else:
            # Se soltar o gesto antes dos 1.5s, reseta o temporizador
            self.tempo_inicio_sair = None

        # --- 3. GESTO INDICADOR APONTADO (PASSAR SLIDES - FUNCIONA NOS DOIS MODOS) ---
        apenas_indicador = indicador_aberto and (not medio_aberto) and (not anelar_aberto) and (not mindinho_aberto)

        if apenas_indicador:
            x_indicador = p_indicador['x']
            self.historico_x.append(x_indicador)

            if len(self.historico_x) > self.tamanho_historico:
                self.historico_x.pop(0)

            if len(self.historico_x) == self.tamanho_historico:
                movimento_horizontal = self.historico_x[0] - self.historico_x[-1]

                # Mover a mão para a esquerda -> Próximo Slide / Próxima Música
                if movimento_horizontal > 35:
                    if tempo_atual - self.ultimo_comando_tempo > self.intervalo_botoes:
                        self.ultimo_comando_tempo = tempo_atual
                        self.historico_x.clear()
                        return "PROXIMA", 0

                # Mover a mão para a direita -> Slide Anterior / Música Anterior
                elif movimento_horizontal < -35:
                    if tempo_atual - self.ultimo_comando_tempo > self.intervalo_botoes:
                        self.ultimo_comando_tempo = tempo_atual
                        self.historico_x.clear()
                        return "ANTERIOR", 0
            return "INDICADOR_DETECTADO", 0
        else:
            self.historico_x.clear()

        # --- SE ESTIVER NO MODO APRESENTACAO, DESATIVA O CONTROLE DE VOLUME ---
        if modo_atual == "APRESENTACAO":
            return "MODO_SLIDES_ATIVO", 0

        # --- 4. CONTROLES EXCLUSIVOS DO MODO MÍDIA ---
        distancia_pinca = math.hypot(p_indicador['x'] - p_polegar['x'], p_indicador['y'] - p_polegar['y'])

        # JOINHA (👍) -> PLAY/PAUSE
        if polegar_para_cima and quatro_dedos_fechados:
            if tempo_atual - self.ultimo_comando_tempo > self.intervalo_botoes:
                self.ultimo_comando_tempo = tempo_atual
                return "PLAYPAUSE", 0
            return "PLAYPAUSE_AGUARDANDO", 0

        # V DE VITÓRIA (✌️) -> MUTE
        if indicador_aberto and medio_aberto and (not anelar_aberto) and (not mindinho_aberto):
            if tempo_atual - self.ultimo_comando_tempo > self.intervalo_botoes:
                self.ultimo_comando_tempo = tempo_atual
                return "MUTE", 0
            return "MUTE_AGUARDANDO", 0

        # PUNHO (✊) -> TRAVAR VOLUME
        if quatro_dedos_fechados and (not polegar_para_cima) and self.estado_slide == 0:
            self.volume_bloqueado = True
            return "TRAVADO", 0

        # DESTRAVAR E AJUSTAR VOLUME (PINÇA)
        if distancia_pinca < 30:
            self.volume_bloqueado = False

        if self.volume_bloqueado:
            return "TRAVADO", 0

        vol_porcentagem = int(((distancia_pinca - 30) / (180 - 30)) * 100)
        vol_porcentagem = max(0, min(100, vol_porcentagem))

        return "AJUSTANDO", vol_porcentagem 
