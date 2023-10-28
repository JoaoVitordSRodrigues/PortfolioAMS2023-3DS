import cv2
import numpy as np
import sqlite3
import pyttsx3

# Inicialize a conexão com o banco de dados
conn = sqlite3.connect('bd/scannerRF.db')
c = conn.cursor()

# Inicialize o reconhecedor facial
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('rec_facial/treinamento.yml')

# Inicialize a câmera
capture = cv2.VideoCapture(0)

#Define o Tamanho da largura na captura de acordo com o tamanho da webcam 
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

#Define o Tamanho da altura na captura de acordo com o tamanho da webcam 
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Inicialize o classificador de face
classificador = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Inicialize o mecanismo de fala
engine = pyttsx3.init()

def consultar_aluno(id_aluno):
    c.execute("SELECT nome_aluno, rm_aluno FROM aluno WHERE id_aluno = ?", (id_aluno,))
    resultado = c.fetchone()
    if resultado:
        nome_aluno, rm_aluno = resultado
        if rm_aluno:
            return f"{nome_aluno} está matriculado."
        else:
            return f"{nome_aluno} não está matriculado."
    else:
        return "Aluno não encontrado."

while True:
    # Capture o frame da câmera
    _, imagem = capture.read()

    # Converta a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Detecte rostos na imagem
    faces = classificador.detectMultiScale(imagem_cinza, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Realize o reconhecimento facial
        id_aluno, confianca = recognizer.predict(imagem_cinza[y:y + h, x:x + w])

        mensagem = consultar_aluno(id_aluno)

        # Exiba o retângulo ao redor do rosto
        cv2.rectangle(imagem, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Fale o status do aluno
        engine.say(mensagem)
        engine.runAndWait()

    # Exiba a imagem capturada
    cv2.imshow('Reconhecimento Facial', imagem)

    # Saia do loop quando a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libere a câmera e feche todas as janelas
capture.release()
cv2.destroyAllWindows()
conn.close()