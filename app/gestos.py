import math

class CalculadorGestos:
    def __init__(self):
        self.intervalo_botoes = 1.2  
        self.ultimo_comando_tempo = 0
        self.volume_bloqueado = False
        
        # Novas variáveis para rastrear o movimento de Swipe (Passar Música)
        self.historico_x = []
        self.tamanho_historico = 5 # Guarda os últimos 5 frames para análise

    def analisar_gestos(self, pontos, tempo_atual):
        if not pontos:
            self.historico_x.clear() # Limpa o histórico se a mão sumir da tela
            return "NENHUM", 0

        # --- 1. MAPEAMENTO DAS COORDENADAS DOS DEDOS ---
        p_polegar = next(p for p in pontos if p['id'] == 4)
        p_indicador = next(p for p in pontos if p['id'] == 8)
        p_medio = next(p for p in pontos if p['id'] == 12)
        p_anelar = next(p for p in pontos if p['id'] == 16)
        p_mindinho = next(p for p in pontos if p['id'] == 20)

        p_indicador_base = next(p for p in pontos if p['id'] == 6)
        p_medio_base = next(p for p in pontos if p['id'] == 10)
        p_anelar_base = next(p for p in pontos if p['id'] == 14)
        p_mindinho_base = next(p for p in pontos if p['id'] == 18)
        p_polegar_base = next(p for p in pontos if p['id'] == 3)
        p_mindinho_raiz = next(p for p in pontos if p['id'] == 17)

        # --- 2. LÓGICA DE DEDOS ABERTOS ---
        indicador_aberto = p_indicador['y'] < p_indicador_base['y']
        medio_aberto = p_medio['y'] < p_medio_base['y']
        anelar_aberto = p_anelar['y'] < p_anelar_base['y']
        mindinho_aberto = p_mindinho['y'] < p_mindinho_base['y']
        polegar_aberto = p_polegar['x'] < p_polegar_base['x'] if p_polegar['x'] > p_mindinho_raiz['x'] else p_polegar['x'] > p_polegar_base['x']

        distancia_volume = math.hypot(p_indicador['x'] - p_polegar['x'], p_indicador['y'] - p_polegar['y'])

        # --- 3. RASTREAMENTO HORIZONTAL (SWIPE DETECTOR) ---
        # Guardamos a posição X do centro da mão (usando a base do dedo médio como referência)
        x_atual = p_medio_base['x']
        self.historico_x.append(x_atual)
        
        # Mantém o histórico apenas com o tamanho necessário
        if len(self.historico_x) > self.tamanho_historico:
            self.historico_x.pop(0)

        # Só tenta detetar o Swipe se todos os dedos estiverem bem abertos/esticados para cima
        mao_totalmente_aberta = indicador_aberto and medio_aberto and anelar_aberto and mindinho_aberto

        if mao_totalmente_aberta and len(self.historico_x) == self.tamanho_historico:
            # Se a posição inicial (antiga) era na direita e a atual é bem mais à esquerda
            # Lembra-se: o X cresce da esquerda para a direita. Então Direita -> Esquerda significa diminuir o X.
            movimento_horizontal = self.historico_x[0] - self.historico_x[-1]
            
            # Se a mão se moveu mais de 80 pixels para a esquerda rapidamente
            if movimento_horizontal > 80: 
                if tempo_atual - self.ultimo_comando_tempo > self.intervalo_botoes:
                    self.ultimo_comando_tempo = tempo_atual
                    self.historico_x.clear() # Limpa para não disparar duas vezes seguidas
                    return "PROXIMA", 0

        # --- 4. REGRAS DOS OUTROS GESTOS ---
        # Gesto A: "V de Vitória" (✌️) -> MUTE
        if indicador_aberto and medio_aberto and (not anelar_aberto) and (not mindinho_aberto):
            if tempo_atual - self.ultimo_comando_tempo > self.intervalo_botoes:
                self.ultimo_comando_tempo = tempo_atual
                return "MUTE", 0
            return "MUTE_ESPERA", 0

        # Gesto B: NOVO GESTO "Joinha" (👍) -> PLAY/PAUSE
        # Polegar apontado para cima e TODOS os outros 4 dedos totalmente fechados
        gesto_joinha = polegar_para_cima and (not indicador_aberto) and (not medio_aberto) and (not anelar_aberto) and (not mindinho_aberto)
        
        if gesto_joinha:
            if tempo_atual - self.ultimo_comando_tempo > self.intervalo_botoes:
                self.ultimo_comando_tempo = tempo_atual
                return "PLAYPAUSE", 0
            return "PLAYPAUSE_ESPERA", 0

        # Gesto C: Mão Fechada (Punho) -> TRAVAR VOLUME
        if (not indicador_aberto) and (not medio_aberto) and (not anelar_aberto):
            self.volume_bloqueado = True
            return "TRAVADO", 0

        # Gesto D: Pinça Próxima -> DESTRAVAR VOLUME
        if distancia_volume < 30:
            self.volume_bloqueado = False

        # --- 5. RETORNO DO ESTADO DO VOLUME ---
        if self.volume_bloqueado:
            return "TRAVADO", 0
        else:
            return "AJUSTANDO", distancia_volume