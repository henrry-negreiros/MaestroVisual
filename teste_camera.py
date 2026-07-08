import cv2

# 1. Liga a webcam do computador (0 é a câmera padrão)
webcam = cv2.VideoCapture(0)

print("Iniciando a câmera... Aperte 'Q' para fechar a janela!")

while True:
    # 2. Captura a imagem da câmera frame por frame
    sucesso, frame = webcam.read()
    
    if not sucesso:
        print("Erro ao acessar a webcam.")
        break

    # 3. Abre uma janela na tela mostrando o que a câmera vê
    cv2.imshow("Olho do Jarvis - Teste", frame)

    # 4. Se o usuário apertar a tecla 'q', o programa fecha
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. Desliga a câmera e fecha a janela
webcam.release()
cv2.destroyAllWindows()
print("Câmera desligada com sucesso.")