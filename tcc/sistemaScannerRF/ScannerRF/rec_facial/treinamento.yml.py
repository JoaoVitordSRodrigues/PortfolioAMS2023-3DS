import cv2
import numpy as np
import sqlite3

#Inicializa a conexão com o banco de dados
conn = sqlite3.connect('bd/ScannerRF.db')
c = conn.cursor()

#Inicializa o reconhecedor facial
recognizer = cv2.face.LBPHFaceRecognizer_create()
classificador = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Inicializa a câmera
camera = cv2.VideoCapture(0)

#Define o Tamanho da largura na captura de acordo com o tamanho da webcam 
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

#Define o Tamanho da altura na captura de acordo com o tamanho da webcam 
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#Inicializa listas vazias para faces e ids
ids = []
faces = []

#Recupera os dados dos alunos do banco de dados
c.execute("SELECT id_aluno, nome_aluno, rm_aluno , face_aluno FROM aluno")
registros = c.fetchall()

for registro in registros:
    id_aluno, nome_aluno, rm_aluno, buffer_rosto = registro
    ids.append(id_aluno)
    rosto = np.frombuffer(buffer_rosto, np.uint8)
    face = rosto.reshape(50, 50) 
    faces.append(face)


recognizer.train(faces, np.array(ids))
recognizer.write('treinamento.yml')

print("Treinamento concluído com sucesso.")

#Fecha a conexão com o banco de dados
conn.close()