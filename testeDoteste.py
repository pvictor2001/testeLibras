import cv2
import mediapipe as mp
import requests
import os
from gtts import gTTS
import json

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(1)  # Verifique o índice correto para o DroidCam

# Verifica se a câmera foi aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a câmera. Verifique o índice da câmera ou o DroidCam.")
    exit()

# Definir a resolução da câmera (opcional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Inicializa o detector de mãos do MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Função para converter texto em áudio
def texto_para_audio(texto):
    tts = gTTS(text=texto, lang='pt')
    tts.save("output.mp3")
    os.system("start output.mp3")  # Para Windows, use "start". Em Linux ou Mac, use "xdg-open" ou "open".

# Função simulada para buscar na internet o significado do gesto (API de exemplo)
def buscar_significado_na_internet(gesto_descricao):
    # Aqui vamos simular uma busca na internet com uma API fictícia
    url = "https://api.exemplo.com/buscar_significado"  # Exemplo fictício
    data = {
        "descricao": gesto_descricao
    }
    
    try:
        # Simulando uma resposta
        response = {
            "status": "success",
            "significado": "Este gesto significa 'Eu te amo'"
        }
        # Simular uma resposta JSON
        significado = response["significado"]
        return significado
    except Exception as e:
        return "Significado não encontrado"

# Função para detectar o gesto e descrever o gesto com base nas posições das articulações
def descrever_gesto(landmarks):
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]

    # Exemplo simples de descrição: Relação entre o polegar, indicador e dedo mínimo
    descricao = f"Polegar em {thumb_tip.y}, Indicador em {index_tip.y}, Mínimo em {pinky_tip.y}"
    
    return descricao

# Função para armazenar o gesto e o significado localmente (em um arquivo JSON, por exemplo)
def armazenar_gesto(gesto, significado):
    dados = {"gesto": gesto, "significado": significado}
    with open("gestos_armazenados.json", "a") as f:
        f.write(json.dumps(dados) + "\n")

while True:
    success, img = cap.read()

    if not success:
        print("Falha ao capturar o vídeo")
        break

    # Converte a imagem de BGR para RGB (necessário para MediaPipe)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    gesto_reconhecido = None  # Armazena o gesto reconhecido

    # Verifica se há detecção de mãos
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Descreve o gesto com base nas posições
            descricao_gesto = descrever_gesto(hand_landmarks.landmark)
            print(f"Descrição do gesto: {descricao_gesto}")
            
            # Buscar o significado do gesto na internet (simulação)
            significado = buscar_significado_na_internet(descricao_gesto)
            
            # Exibe legenda na tela
            cv2.putText(img, significado, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            
            # Armazena o gesto e o significado
            armazenar_gesto(descricao_gesto, significado)
            
            # Converte o gesto em áudio
            texto_para_audio(significado)

    # Exibe o vídeo com a legenda
    cv2.imshow("Video", img)

    # Pressiona 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
