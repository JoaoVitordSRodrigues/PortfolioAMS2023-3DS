import cv2
import sqlite3
import numpy as np
import time
from bd import BancoTcc
import threading
import pygame
from pygame import mixer

class Face:
    def __init__(self):
        # Carregar o classificador
        xml_haar_cascade = 'haarcascade_frontalface_alt2.xml'
        self.faceClassifier = cv2.CascadeClassifier(xml_haar_cascade)

        self.capture = cv2.VideoCapture(0)

        # Definir as dimensões desejadas para a imagem do rosto
        self.desired_width = 47
        self.desired_height = 47

        # Definir a resolução da imagem capturada
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 660)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.countdown_duration = 6  # Duração da contagem regressiva em segundos
        self.start_time = time.time()


    def cadastrarFace(self):
        while True:
            ret, frame_color = self.capture.read()
            gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
            faces = self.faceClassifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for x, y, w, h in faces:
                cv2.rectangle(frame_color, (x, y), (x + w, y + h), (0, 0, 255), 2)

                elapsed_time = time.time() - self.start_time

                if elapsed_time < self.countdown_duration:
                    countdown = self.countdown_duration - int(elapsed_time)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 1
                    font_color = (0, 0, 255)  # Vermelho
                    line_type = 2
                    cv2.putText(frame_color, f"Contagem: {countdown}", (50, 50), font, font_scale, font_color, line_type)
                else:
                    # Região do rosto para cadastro
                    face_for_db = gray[y:y + h, x:x + w]
                    face_color  = frame_color[y:y + h, x:x + w]
                    
                    new_height = 100  # Defina a altura desejada
                    resize_scale = new_height / face_color.shape[0]  # Calcula o fator de escala para a altura
                    resized_face_color = cv2.resize(face_color, (int(face_color.shape[1] * resize_scale), new_height))

                    face_color_bytes = cv2.imencode('.png', resized_face_color)[1].tobytes()

                    # Redimensionar a imagem da câmera para as dimensões desejadas
                    resized_face_for_db = cv2.resize(face_for_db, (self.desired_width, self.desired_height))

                    # Salvar a imagem no disco
                    cv2.imwrite('imgFace.jpg', resized_face_for_db)

                    cv2.imwrite('imgAluno.png', face_color)

                    # Converter a matriz em uma sequência de bytes para armazenamento no banco de dados
                    face_bytes = resized_face_for_db.tobytes()

                    print("Rosto cadastrado com sucesso.")

                    # Exibir a imagem capturada em uma janela separada
                    cv2.imshow('Imagem de Cadastro', resized_face_for_db)
                    cv2.waitKey(3000)  # Mostrar a imagem por 3 segundos

                    # Fechar a janela de visualização
                    cv2.destroyWindow('Imagem de Cadastro')

                    return face_bytes, face_color_bytes

                    # Encerrar o programa após cadastrar um rosto
                    exit(0)
                
            cv2.imshow('color', frame_color)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
