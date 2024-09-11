import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication
import pygame
import time
import threading
from pygame import mixer
from bd import BancoTcc

class Teste:
    def __init__(self):
        self.app = QApplication([])

        # Inicialize o mixer do pygame
        pygame.mixer.init()

        # Carregar o classificador
        self.xml_haar_cascade = 'haarcascade_frontalface_alt2.xml'
        self.faceClassifier = cv2.CascadeClassifier(self.xml_haar_cascade)

        self.capture = cv2.VideoCapture(0)

        # Definir as dimensões desejadas para a imagem do rosto
        self.desired_width = 47
        self.desired_height = 47

        # Controle do tempo de exibição da mensagem
        self.message_display_time = 5  # 5 segundos
        self.message_display_start_time = None

        # Controle do tempo de atraso
        self.validation_delay = 5  # 3 segundos

        # Controle do bloqueio de validação
        self.validation_locked = False

        # Variável de controle para encerrar o loop
        self.face_found = False

        # Inicializar a thread de áudio
        self.audio_thread = None

    def play_audio(self, audio_file):
        mixer.init()
        mixer.music.load(audio_file)
        mixer.music.play()
        mixer.music.set_volume(1)
        time.sleep(4.5)  # Tempo de duração do áudio
        mixer.music.stop()

    def reset_variables(self):
        self.message_display_start_time = None
        self.face_found = False
        self.faces = []  # Limpe a lista de faces detectadas

    def start(self):
        # Inicialize o tempo de contagem regressiva
        countdown_start_time = time.time()
        countdown_duration = self.validation_delay
        
        while True:  # Continuar enquanto o rosto não for encontrado
            self.reset_variables()
            ret, frame_color = self.capture.read()

            if ret and frame_color is not None and frame_color.shape[0] > 0 and frame_color.shape[1] > 0:
                cv2.imshow('color', frame_color)
                gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)
                self.faces = self.faceClassifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if time.time() - countdown_start_time < countdown_duration:
                    # Exibir contagem regressiva na webcam
                    countdown = int(countdown_duration - (time.time() - countdown_start_time))
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 1
                    font_color = (0, 0, 255)  # Vermelho
                    line_type = 2
                    cv2.putText(frame_color, f"Posicione seu rosto: {countdown}", (50, 50), font, font_scale, font_color, line_type)

                else:
                    if len(self.faces) == 0:
                        # Nenhum rosto correspondente encontrado
                        pass
                    else:
                        face_corresponding = False
                        for x, y, w, h in self.faces:
                            cv2.rectangle(frame_color, (x, y), (x + w, y + h), (0, 0, 255), 2)

                            # Resto do código para processar o rosto e verificar a correspondência
                            face_encoding = gray[y:y + h, x:x + w]
                            face_encoding = cv2.resize(face_encoding, (self.desired_width, self.desired_height))

                            BancoTcc.cursor.execute('SELECT face_aluno, id_turma, nome_aluno, rm_aluno FROM aluno')
                            rows = BancoTcc.cursor.fetchall()

                            for row in rows:
                                existing_face_encoding = np.frombuffer(row[0], dtype=np.uint8)
                                existing_face_encoding = existing_face_encoding.reshape(self.desired_height, self.desired_width)

                                result = cv2.matchTemplate(face_encoding, existing_face_encoding, cv2.TM_CCOEFF_NORMED)

                                threshold = 0.6

                                _, max_val, _, _ = cv2.minMaxLoc(result)

                                if max_val > threshold:
                                    face_corresponding = True
                                    if self.message_display_start_time is None:
                                        self.message_display_start_time = time.time()  # Iniciar contagem de tempo
                                        print("Rosto correspondente encontrado!")

                                        id_turma, nome_aluno, rm_aluno = row[1], row[2], row[3]
                                        print(f"Informações do aluno: ID Turma: {id_turma}, Nome: {nome_aluno}, RM: {rm_aluno}")
                                        self.audio_thread = threading.Thread(target=self.play_audio, args=('audio_validacao/audio_aluno_matriculado.mp3',))
                                        self.audio_thread.start()   
                                        resultado = 'Rosto encontrado'
                                        # Não libere a câmera e a janela aqui, pois você quer continuar o processamento
                                        result_list = [id_turma, nome_aluno, rm_aluno, resultado]
                                        cv2.destroyAllWindows()
                                        return result_list
                                    else:
                                        current_time = time.time()
                                        elapsed_time = current_time - self.message_display_start_time
                                        if elapsed_time >= self.message_display_time:
                                            self.message_display_start_time = None

                        if not face_corresponding:
                            # Nenhum rosto correspondente encontrado no banco de dados
                            if self.message_display_start_time is None:
                                self.message_display_start_time = time.time()  # Iniciar contagem de tempo
                                print("Rosto detectado, mas não corresponde a nenhum rosto no banco de dados!")
                                self.audio_thread = threading.Thread(target=self.play_audio, args=('audio_validacao/audio_aluno_naoMatriculado.mp3',))
                                self.audio_thread.start()
                                resultado = 'Rosto nao encontrado'
                                # Não libere a câmera e a janela aqui, pois você quer continuar o processamento
                                result_list = [resultado]
                                cv2.destroyAllWindows()
                                return result_list 
                            else:
                                current_time = time.time()
                                elapsed_time = current_time - self.message_display_start_time
                                if elapsed_time >= self.message_display_time:
                                    self.message_display_start_time = None

            key = cv2.waitKey(1)
            if key == 27:  # Verifica se a tecla "Esc" foi pressionada
                self.capture.release()
                cv2.destroyAllWindows()
                break


if __name__ == '__main__':
    teste = Teste()
    teste.start()
    # Certifique-se de lidar com a finalização do programa conforme necessário
    # Você pode querer esperar que a thread de áudio termine e fazer outras ações de limpeza
    # Por exemplo:
    # teste.audio_thread.join()
    # Outras ações de limpeza, se necessário
