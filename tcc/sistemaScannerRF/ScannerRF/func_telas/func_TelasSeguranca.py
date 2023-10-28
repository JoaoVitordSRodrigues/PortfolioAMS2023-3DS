#IMPORTANDO AS BIBLIOTECAS
import sys
import io
from bd import BancoTcc
import messagebox
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QStackedWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
from main import MainWindow
from telas_py.telas_Seguranca import Ui_MainWindow as Ui_Telas_Seguranca
from PyQt5.QtCore import Qt
# Importa a Biblioteca OPENCV --> Usada para o Reconhecimento em si 
import cv2
import pyttsx3
import sqlite3

#=========================================================================#
#                                                                         #
#     CLASSE COM FUNCIONALIDADES P/ A TELA PRINCIPAL PARA O SEGURANÇA     #
#                                                                         #
#=========================================================================#
class Config_TelasSeguranca(QMainWindow):
    #CONFIG INICIAIS P/ SER EXECUTADAS AO ABRIR A TELA SEGURANÇA
    def __init__(self, nome_funcionario):
        super(Config_TelasSeguranca, self).__init__()
        self.ui = Ui_Telas_Seguranca()
        self.ui.setupUi(self)

        #variavel que recebe o nome do funcionario
        self.nome_funcionario = nome_funcionario
        #setando o nome do funcionario na label da pagina de inicio
        self.ui.label_2.setText(f'Olá, {self.nome_funcionario}')

        #ESCONDER ICONES DO MENU E CONFIGURAR INDICE DA PAG INICIAL
        self.ui.menu_icons.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btnIconMenu.setChecked(True)

        #FUNÇAO DOS BOTOES VOLTAR
        self.ui.btnVoltarLAberto.clicked.connect(self.on_btnVoltarLateral_clicked)
        
        #FUNÇOES DOS BOTOES DESCONECTAR
        self.ui.btnDesconectar_PgHome.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLateral.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLAberto.clicked.connect(self.abrirTelaLogin)

        #=============CONFIG PAG SCANNER=============
        self.ui.btnScannerLateral.clicked.connect(self.cameraReconhecimento)

    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #                    FUNÇOES DA CLASSE DIRETOR                        -
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------          
    def cameraReconhecimento(self):
        
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
        classificador = cv2.CascadeClassifier('rec_facial/haarcascade_frontalface_default.xml')

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

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.menu_icons.findChildren(QPushButton) \
                    + self.ui.menu_todo.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    #================FUNCOES P/ TROCAR DE PAG================
    #================BOTOES DO MENU DE CIMA (HEADER)================
    #botao que ira redirecionar p/ pag scanner
    def on_btnScanner_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    #botao que ira redirecionar p/ pag entradas
    def on_btnEntradas_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    #================BOTOES DO MENU LATERAL================
    #botoes que ira redirecionar p/ pag home
    def on_btnHomeLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_btnHomeLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    #botoes que ira redirecionar p/ pag scanner
    def on_btnScannerLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def on_btnScannerLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    #botoes que ira redirecionar p/ pag entradas
    def on_btnEntradasLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_btnEntradasLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    #funcao para verificar a pagina atual e funcionar o botão voltar
    def on_btnVoltarLateral_clicked(self):
        #0 = pag home
        #1 = pag scanner
        #2 = pag entradas

        telaAtual = self.ui.stackedWidget.currentIndex()

        #se tiver na tela home, irá voltar para tela home
        if telaAtual == 0:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela scanner, irá voltar para tela home
        elif telaAtual == 1:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela entradas, irá voltar para tela home
        elif telaAtual == 2:
            self.ui.stackedWidget.setCurrentIndex(0)

    #===============funcao de abrir tela de login, que ira ser exibida ao desconectar===============
    def abrirTelaLogin(self):
        #criando uma instancia da tela de login
        self.main = MainWindow()  
        #exibindo a tela
        self.main.show()
        #fecha a tela anterior
        self.close()  


