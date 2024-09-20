import cv2
import mediapipe as mp
import requests
import os
from gtts import gTTS

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Erro ao abrir a câmera. Verifique o índice da câmera ou o DroidCam.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def texto_para_audio(texto):
    tts = gTTS(text=texto, lang='pt')
    tts.save("output.mp3")
    os.system("start output.mp3")

def reconhecer_gesto(imagem):
    _, img_encoded = cv2.imencode('.jpg', imagem)
    response = requests.post(
        "https://vlibras.gov.br/api/v1/gesto",  # Use a URL correta da API VLibras
        files={"image": img_encoded.tobytes()},
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na API: {response.status_code}, {response.text}")
        return None

while True:
    success, img = cap.read()

    if not success:
        print("Falha ao capturar o vídeo")
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            resultado = reconhecer_gesto(img)
            if resultado:
                print("Resultado da API:", resultado)
                if "gesture" in resultado:
                    descricao = resultado.get("description", "Descrição não encontrada")
                    print(descricao)
                    cv2.putText(img, descricao, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                    texto_para_audio(descricao)
                else:
                    print("Gesto desconhecido.")
            else:
                print("Erro na chamada à API ou resposta inválida.")

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
