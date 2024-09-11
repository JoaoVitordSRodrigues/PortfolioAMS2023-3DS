#IMPORTANDO AS BIBLIOTECAS
import sys
import io
from bd import BancoTcc
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
from main import MainWindow
from telas_py.telas_Seguranca import Ui_MainWindow as Ui_Telas_Seguranca
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
#importando da pasta 'classes' a classe entrada em python
from classes.Entrada import Entrada
from rec_facial.cadastro_face import Face

from rec_facial.reconhecimento_facial import Teste
# Importa a Biblioteca OPENCV --> Usada para o Reconhecimento em si 
import cv2
import sqlite3
import numpy as np
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys, os
from datetime import datetime, time




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

        self.classeEntrada = Entrada()
        self.Face = Face()
        self.Teste = Teste()
        #variavel que recebe o nome do funcionario
        self.nome_funcionario = nome_funcionario
        #setando o nome do funcionario na label da pagina de inicio
        self.ui.label_2.setText(f'Olá, {self.nome_funcionario}')
        self.timer = QTimer(self)
        #ESCONDER ICONES DO MENU E CONFIGURAR INDICE DA PAG INICIAL
        self.ui.menu_icons.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btnIconMenu.setChecked(True)
        self.timer = QTimer(self)
        #FUNÇAO DOS BOTOES VOLTAR
        self.ui.btnVoltarLAberto.clicked.connect(self.on_btnVoltarLateral_clicked)
        
        #FUNÇOES DOS BOTOES DESCONECTAR
        self.ui.btnDesconectar_PgHome.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLateral.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLAberto.clicked.connect(self.abrirTelaLogin)

        #=============CONFIG PAG SCANNER=============
        self.ui.btnScanner.clicked.connect(self.chamarExibirDadosValidacaoNovamente)
        self.ui.btnScannerLateral.clicked.connect(self.chamarExibirDadosValidacaoNovamente)
        

        self.ui.etyPesquisar_PgEntradas.textChanged.connect(self.filtrarTabela)


    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #                    FUNÇOES DA CLASSE DIRETOR                        -
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------          
    def consultar_aluno(self):
        self.executarAudioValidacao()
        

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
        self.inserirDadosTabelaEntrada()
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
        self.inserirDadosTabelaEntrada()
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_btnEntradasLAberto_clicked(self):
        self.inserirDadosTabelaEntrada()
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

    def inserirDadosTabelaEntrada(self):#botao que redireciona para a pag de cadastro
        nomeTela = 'Seguranca'
        nome_funcionario = self.nome_funcionario
        # Conectar ao banco de dados (substitua 'seu_banco_de_dados.db' pelo nome do seu banco de dados)
        dados_entrada = self.classeEntrada.dadosTabelaEntrada(nomeTela, nome_funcionario)

        if dados_entrada == "Não há dados para a exibição.":
            QMessageBox.warning(self, "Aviso", "Não foi possível exibir dados da tabela.")
        else:
            # Preencher a tabela com os dados do banco de dados
            self.ui.tbl_historicoEntradas.setRowCount(len(dados_entrada))
            for row, data in enumerate(dados_entrada):
                for col, value in enumerate(data):
                    item = QTableWidgetItem(str(value))
                    self.ui.tbl_historicoEntradas.setItem(row, col, item)
    
    def filtrarTabela(self):
        search_text = self.ui.etyPesquisar_PgEntradas.text().lower()
        for row in range(self.ui.tbl_historicoEntradas.rowCount()):
            row_hidden = True
            for col in range(self.ui.tbl_historicoEntradas.columnCount()):
                item = self.ui.tbl_historicoEntradas.item(row, col)
                if item.text().lower().startswith(search_text):
                    row_hidden = False
                    break
            self.ui.tbl_historicoEntradas.setRowHidden(row, row_hidden)

    def chamarExibirDadosValidacaoNovamente(self):
        self.exibirDadosValidacao()

    def limparReco(self):
        # Limpe os widgets ou labels se necessário
        self.ui.lbl_nomeAluno.setText("")
        self.ui.lbl_RmAluno.setText("")
        self.ui.lbl_periodoAluno.setText("")
        self.ui.lbl_infosAcesso.setText("")
        self.ui.lbl_imgValidacao.clear()
        self.ui.lbl_imgStatusHorario.clear()


    #dados que irão ser exibidos apos validar o rosto do aluno
    def exibirDadosValidacao(self):
        self.limparReco()

        result_list = self.Teste.start()

        dados_dia = datetime.now()  # setando na variável os dados do dia (dia, mês, ano, hora, etc.)
        data_hoje_formatada = dados_dia.strftime("%d/%m/%Y")  # setando na variável a data formatada (00/00/0000)
        horario_hoje_formatado = dados_dia.strftime("%H:%M")  # setando na variável o horário formatado (00:00)
        self.ui.lbl_dataDoDia.setText(data_hoje_formatada)  # setando o dia formatado na label
        self.ui.lbl_horarioDoDia.setText(horario_hoje_formatado)  # setando o horário formatado na label

        if result_list is not None:
            if len(result_list) == 4:
                id_turma, nome_aluno, rm_aluno, resultado = result_list
                
                consulta_aluno = "SELECT * FROM aluno WHERE rm_aluno = ?"  # consulta SQL para selecionar os dados da turma com base no ID
                BancoTcc.cursor.execute(consulta_aluno, (rm_aluno,))
                dados_aluno = BancoTcc.cursor.fetchone()

                id_aluno = dados_aluno[0]
                id_turma = dados_aluno[1]
                rm_aluno = dados_aluno[2]
                nome_aluno = dados_aluno[3]

                consulta_turma = "SELECT * FROM turma WHERE id_turma = ?"  # consulta SQL para selecionar os dados da turma com base no ID
                BancoTcc.cursor.execute(consulta_turma, (id_turma,))
                dados_turma = BancoTcc.cursor.fetchone()  # armazenando os dados da turma

                id_periodo = dados_turma[2]  # variável que recebe o ID do período, '2' é a coluna onde o ID do período está

                consulta_periodo = "SELECT * FROM periodo WHERE id_periodo = ?"  # consulta SQL para selecionar os dados do período com base no ID do período
                BancoTcc.cursor.execute(consulta_periodo, (id_periodo,))
                dados_periodo = BancoTcc.cursor.fetchone()  # armazenando os dados do período

                turno_periodo = dados_periodo[1]  # variável que recebe o turno do curso, '1' é a coluna onde o turno do curso está
                print(turno_periodo)

                self.ui.lbl_nomeAluno.setText(nome_aluno)
                self.ui.lbl_RmAluno.setText(str(rm_aluno))
                self.ui.lbl_periodoAluno.setText(turno_periodo)

                # Obtenha o horário atual
                horario_atual = datetime.now().time()

                # Defina os horários de entrada e limite para cada período
                horario_entrada_min_MANHA = time(6, 45)
                horario_entrada_max_MANHA = time(7, 0)
                horario_limite_MANHA = time(7, 15)

                horario_entrada_min_TAR = time(12, 45)
                horario_entrada_max_TAR = time(13, 0)
                horario_limite_TAR = time(13, 15)

                horario_entrada_min_NOI = time(18, 15)
                horario_entrada_max_NOI = time(19, 0)
                horario_limite_NOI = time(19, 15)

                pixmap = QPixmap("imagens/simbolo_validado.png")  # imagem da validação central
                pixmap2 = QPixmap("imagens/relogio.png")  # imagem do status do horário

                # Defina a imagem na QLabel
                self.ui.lbl_imgValidacao.setPixmap(pixmap)
                self.ui.lbl_imgStatusHorario.setPixmap(pixmap2)
                pixmap2 = pixmap.scaled(60, 70)

                if turno_periodo == 'Manhã':
                    if horario_atual < horario_entrada_min_MANHA:
                        self.ui.lbl_infosAcesso.setMinimumSize(350, 22)
                        status_horario = 'adiantado'
                    elif horario_atual >= horario_entrada_min_MANHA and horario_atual <= horario_entrada_max_MANHA:
                        self.ui.lbl_infosAcesso.setMinimumSize(300, 22)
                        status_horario = 'no horário'
                    elif horario_atual > horario_entrada_max_MANHA and horario_atual <= horario_limite_MANHA:
                        self.ui.lbl_infosAcesso.setMinimumSize(300, 22)
                        status_horario = 'atrasado'
                    else: 
                        self.ui.lbl_infosAcesso.setMinimumSize(450, 22)
                        status_horario = 'limite excedido'
                elif turno_periodo == 'Tarde':
                    if horario_atual < horario_entrada_min_TAR:
                        self.ui.lbl_infosAcesso.setMinimumSize(350, 22)
                        status_horario = 'adiantado'
                    elif horario_atual >= horario_entrada_min_TAR and horario_atual <= horario_entrada_max_TAR:
                        self.ui.lbl_infosAcesso.setMinimumSize(300, 22)
                        status_horario = 'no horário'
                    elif horario_atual > horario_entrada_max_TAR and horario_atual <= horario_limite_TAR:
                        self.ui.lbl_infosAcesso.setMinimumSize(300, 22)
                        status_horario = 'atrasado'
                    else: 
                        self.ui.lbl_infosAcesso.setMinimumSize(450, 22)
                        status_horario = 'limite excedido'
                else:
                    if horario_atual < horario_entrada_min_NOI:
                        self.ui.lbl_infosAcesso.setMinimumSize(350, 22)
                        status_horario = 'adiantado'
                    elif horario_atual >= horario_entrada_min_NOI and horario_atual <= horario_entrada_max_NOI:
                        self.ui.lbl_infosAcesso.setMinimumSize(300, 22)
                        status_horario = 'no horário'
                    elif horario_atual > horario_entrada_max_NOI and horario_atual <= horario_limite_NOI:
                        self.ui.lbl_infosAcesso.setMinimumSize(300, 22)
                        status_horario = 'atrasado'
                    else:
                        self.ui.lbl_infosAcesso.setMinimumSize(450, 22)
                        status_horario = 'limite excedido'

                if status_horario == 'adiantado':
                    self.ui.lbl_infosAcesso.setText("Acesso liberado: adiantado")
                elif status_horario == 'no horário':
                    self.ui.lbl_infosAcesso.setText("Acesso liberado: no horário")
                elif status_horario == 'atrasado':
                    self.ui.lbl_infosAcesso.setText("Acesso liberado: atrasado")
                else:
                    self.ui.lbl_infosAcesso.setText("Acesso não liberado: limite excedido")


                BancoTcc.cursor.execute("INSERT INTO entrada (nome_aluno, rm_aluno, periodo, data_entrada, horario_entrada, status_horario, nome_seguranca) VALUES (?, ?, ?, ?, ?, ?, ?)", ( nome_aluno, rm_aluno, turno_periodo, data_hoje_formatada, str(horario_atual)[:5], status_horario, self.nome_funcionario))
                BancoTcc.conn.commit()
                
                self.timer.timeout.connect(self.chamarExibirDadosValidacaoNovamente)
                self.timer.start(5000)  # 5000 milissegundos = 5 segundos
            else:
                nome_aluno = rm_aluno = turno_periodo = 'Não encontrado'

                self.ui.lbl_nomeAluno.setText(nome_aluno)
                self.ui.lbl_RmAluno.setText(str(rm_aluno))
                self.ui.lbl_periodoAluno.setText(turno_periodo)

                pixmap3 = QPixmap("imagens/simbolo_negado.png")  # imagem do status do horário
                pixmap3 = pixmap3.scaled(140, 140)
                self.ui.lbl_imgValidacao.setPixmap(pixmap3)
                
                resultado = result_list[0]

                self.timer.timeout.connect(self.chamarExibirDadosValidacaoNovamente)
                self.timer.start(5000)
        else:
            pass
