#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QStackedWidget, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
#importando a tela de login
from main import MainWindow
#importando da pasta 'telas_py' as telas do diretor em python
from telas_py.telas_Diretor import Ui_MainWindow as Ui_Telas_Diretor
from PyQt5.QtCore import Qt
import re

#=========================================================================#
#                                                                         #
#      CLASSE COM FUNCIONALIDADES P/ A TELA PRINCIPAL PARA O DIRETOR      #
#                                                                         #
#=========================================================================#
class Config_TelasDiretor(QMainWindow):
    #CONFIG INICIAIS P/ SER EXECUTADAS AO ABRIR A TELA DIRETOR
    def __init__(self, nome_funcionario):
        super(Config_TelasDiretor, self).__init__()
        self.ui = Ui_Telas_Diretor()
        self.ui.setupUi(self)

        #variavel que recebe o nome do funcionario
        self.nome_funcionario = nome_funcionario
        #setando o nome do funcionario na label da pagina de inicio
        self.ui.lbl_NomeHome.setText(f'Olá, Dir. {self.nome_funcionario}')
        #variaveis utilizadas para o crud, que serao acessadas por algumas funcoes
        self.id_aluno = None
        self.turno_periodoAtt = None #turno periodo para exibir na pag atualizar
        self.nome_cursoAtt = None #nome curso para exibir na pag atualizar
        self.serie_turmaAtt = None #serie turma para exibir na pag atualizar
        self.face_aluno = None#face que ira ser usada para cadastrar
        self.face_alunoAtt = None#face que ira ser usada atualizar


        #ESCONDER ICONES DO MENU E CONFIGURAR INDICE DA PAG INICIAL
        self.ui.menu_icons.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btnIconMenu.setChecked(True)
        

        #======================================BOTOES DE NAVEGACAO LATERAIS==============================================
        #FUNÇAO DOS BOTOES VOLTAR
        self.ui.btnVoltarLAberto.clicked.connect(self.on_btnVoltarLateral_clicked)

        #FUNÇOES DOS BOTOES DESCONECTAR
        self.ui.btnDesconectar_PgHome.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLateral.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLAberto.clicked.connect(self.abrirTelaLogin)




        #================================BOTOES DE NAVEGACAO DENTRO DAS PAG(FUNCIONALIDADES)=============================

        #=============================================================================================
        #===================================CONFIG PAG PESQUISAR======================================
        #=============================================================================================
        #botao que ira redirecionar p/ pag de visualizar turma
        self.ui.btnBuscarTurma_PgPesquisar.clicked.connect(self.btnBuscarTurma)
        #botao que ira redirecionar p/ pag de visualizar alunoRm
        self.ui.btnBuscarRM_PgPesquisar_2.clicked.connect(self.btnBuscarRm)
        #=============================================================================================



        #=============================================================================================
        #==================================CONFIG PAG DADOS ALUNO=====================================
        #=============================================================================================
        #botao que ira deletar o cadastro do aluno
        self.ui.btnDeletarAluno_PgAtualizar_2.clicked.connect(self.deletarAluno)
        #botao que ira redirecionar p/ pag atualizar aluno com os dados do aluno
        self.ui.btnAtualizarAluno_PgAtualizar_2.clicked.connect(self.btnAtualizarAluno_PgDadosAluno)
        #=============================================================================================



        #=============================================================================================
        #================================CONFIG PAG CADASTRAR ALUNO===================================
        #=============================================================================================        
        #setando os valores da combobox 'periodo' 
        self.ui.cboxPeriodo_PgCadastro.addItem("Selecione o período do aluno")
        self.ui.cboxPeriodo_PgCadastro.addItem("Manhã")
        self.ui.cboxPeriodo_PgCadastro.addItem("Tarde")
        self.ui.cboxPeriodo_PgCadastro.addItem("Noite")
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxPeriodo_PgCadastro.model().item(0).setFlags(Qt.ItemIsEnabled)
        
        #setando os valores da combobox 'turma'
        self.ui.cboxTurma_PgCadastro.addItem("Selecione a turma do aluno")
        self.ui.cboxTurma_PgCadastro.addItem("1°")
        self.ui.cboxTurma_PgCadastro.addItem("2°")
        self.ui.cboxTurma_PgCadastro.addItem("3°"),
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxTurma_PgCadastro.model().item(0).setFlags(Qt.ItemIsEnabled)

        self.ui.cboxPeriodo_PgCadastro.currentIndexChanged.connect(self.exibirCursosPorPeriodo)
        self.exibirCursosPorPeriodo()  #inicialmente, exibe todos os cursos

        #botao que ira carregar a imagem do aluno      
        self.ui.btnCarregarFT_PgCadastro.clicked.connect(self.carregar_imagem)
        #botao que ira cadastrar aluno
        self.ui.btnCadastrarAluno_PgCadastro.clicked.connect(self.cadastrarAluno)
        #botao que ira limpar todos os campos
        self.ui.btnLimparCampos_PgCadastro.clicked.connect(self.limparCampos)
        #=============================================================================================



        #=============================================================================================
        #================================CONFIG PAG ATUALIZAR ALUNO===================================
        #============================================================================================= 
        #setando os valores da combobox 'periodo' 
        self.ui.cboxPeriodo_PgAtualizar.addItem("Selecione o período do aluno")
        self.ui.cboxPeriodo_PgAtualizar.addItem("Manhã")
        self.ui.cboxPeriodo_PgAtualizar.addItem("Tarde")
        self.ui.cboxPeriodo_PgAtualizar.addItem("Noite")

        #setando na combobox 'curso' para ajudar na seleção(placeholder)
        self.ui.cboxCurso_PgAtualizar.addItem("Selecione o curso do aluno")

        #setando os valores da combobox 'turma'
        self.ui.cboxTurma_PgAtualizar.addItem("Selecione a turma do aluno")
        self.ui.cboxTurma_PgAtualizar.addItem("1°")
        self.ui.cboxTurma_PgAtualizar.addItem("2°")
        self.ui.cboxTurma_PgAtualizar.addItem("3°"),

        self.ui.cboxPeriodo_PgAtualizar.currentIndexChanged.connect(self.exibirCursosPorPeriodo_PgAtualizar)
        self.exibirCursosPorPeriodo()  #inicialmente, exibe todos os cursos

        #botao que ira carregar a imagem do aluno      
        self.ui.btnCarregarFT_PgAtualizar.clicked.connect(self.carregar_imagemPgAtualizar)    
        #botao que ira atualizar os dados do aluno   
        self.ui.btnAtualizarAluno_PgAtualizar.clicked.connect(self.atualizarAluno)
        #=============================================================================================



        #=============================================================================================
        #================================CONFIG PAG PESQUISAR ALUNO===================================
        #============================================================================================= 
        #setando os valores da combobox 'periodo' 
        self.ui.cboxPeriodo_PgPesquisar.addItem("Selecione o período do aluno")
        self.ui.cboxPeriodo_PgPesquisar.addItem("Manhã")
        self.ui.cboxPeriodo_PgPesquisar.addItem("Tarde")
        self.ui.cboxPeriodo_PgPesquisar.addItem("Noite")
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxPeriodo_PgPesquisar.model().item(0).setFlags(Qt.ItemIsEnabled)
        
        #setando na combobox 'curso' para ajudar na seleção(placeholder)
        self.ui.cboxCurso_PgPesquisar.addItem("Selecione o curso do aluno")
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxCurso_PgPesquisar.model().item(0).setFlags(Qt.ItemIsEnabled)

        #setando os valores da combobox 'turma'
        self.ui.cboxTurma_PgPesquisar.addItem("Selecione a turma do aluno")
        self.ui.cboxTurma_PgPesquisar.addItem("1°")
        self.ui.cboxTurma_PgPesquisar.addItem("2°")
        self.ui.cboxTurma_PgPesquisar.addItem("3°"),
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxTurma_PgPesquisar.model().item(0).setFlags(Qt.ItemIsEnabled)

        self.ui.cboxPeriodo_PgPesquisar.currentIndexChanged.connect(self.exibirCursosPorPeriodo_PgPesquisar)
        self.exibirCursosPorPeriodo_PgPesquisar()  #inicialmente, exibe todos os cursos
        #=============================================================================================















    #-------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------
    #                                   FUNÇOES DA CLASSE DIRETOR                                    -
    #-------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------    
    #-------------------------------------------------------------------------------------------------

    '''
    ==================================================================================================
    =                 FUNCOES PARA TROCA DE PAGINAS/ BOTOES SUPERIORES E LATERAIS                    =
    ==================================================================================================
    '''
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
    #botao que ira redirecionar p/ pag alunos
    def on_btnAlunos_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    #botao que ira redirecionar p/ pag entradas
    def on_btnEntradas_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    #================BOTOES DO MENU LATERAL================
    #botoes que ira redirecionar p/ pag home
    def on_btnHomeLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_btnHomeLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    #botoes que ira redirecionar p/ pag alunos
    def on_btnAlunosLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_btnAlunosLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    #botoes que ira redirecionar p/ pag entradas
    def on_btnEntradasLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def on_btnEntradasLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    #funcao para verificar a pagina atual e funcionar o botão voltar
    def on_btnVoltarLateral_clicked(self):
        #0 = pag home
        #1 = pag alunos
        #2 = pag entradas
        #3 = pag cadastro
        #4 = pag atualizar
        #5 = pag pesquisar
        #6 = pag dados turma
        #7 = pag dados aluno

        telaAtual = self.ui.stackedWidget.currentIndex()

        #se tiver na tela home, irá voltar para tela home
        if telaAtual == 0:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela alunos, irá voltar para tela home
        elif telaAtual == 1:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela entradas, irá voltar para tela home
        elif telaAtual == 2:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela cadastro, irá voltar para tela home
        elif telaAtual == 3:
            telaAtual = 3
            self.ui.stackedWidget.setCurrentIndex(1)

    #===============funcao de abrir tela de login, que ira ser exibida ao desconectar===============
    def abrirTelaLogin(self):
        #criando uma instancia da tela de login
        self.main = MainWindow()  
        #exibindo a tela
        self.main.show()
        #fecha a tela anterior
        self.close()  
    
    '''
    #################################
    ==================================================================================================
    =                              FIM FUNCOES PARA TROCA DE PAGINAS                                 =
    ==================================================================================================
    '''



    #=================================================================================================
    #================FUNCAO PAG ALUNOS================================================================
    #=================================================================================================
    #botões pagina alunos, funcoes para trocar de pagina
    def on_btnPgCadastrarAlunos_PgAlunos_clicked(self):#botao que redireciona para a pag de cadastro
        self.ui.stackedWidget.setCurrentIndex(3)
        #iniciando as variaveis de face do aluno para assim a validação de inserção obrigatoria de imagem da certo
        self.face_aluno = None#face que ira ser usada para cadastrar
        self.face_alunoAtt = None#face que ira ser usada atualizar
    def on_btnPgProcurarAlunos_PgAlunos_clicked(self):#botao que redireciona para a pag de procurar
        self.ui.stackedWidget.setCurrentIndex(5)
    #=================================================================================================
    #=================================================================================================

    

    #=================================================================================================
    #==============FUNCAO PAG PESQUISAR===============================================================
    #=================================================================================================
    #botao que ira redirecionar p/ pag turma, com os dados da turma pesquisada
    def btnBuscarTurma(self):
        #armazenando os valores da busca em variaveis
        periodo = self.ui.cboxPeriodo_PgPesquisar.currentText()
        curso = self.ui.cboxCurso_PgPesquisar.currentText()
        serie_turma = self.ui.cboxTurma_PgPesquisar.currentText()

        #ira fazer a validação dos campos não preechidos
        if(periodo == 'Selecione o período do aluno' or curso == 'Selecione o curso do aluno' or 
           serie_turma == 'Selecione a turma do aluno'):
            #mensagem de campos nao preenchidos
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos para concluir a busca!")

            #validações de nao preechimento dos campos, setando os campos nao preenchidos com cor vermelha
            if(periodo == 'Selecione o período do aluno'):
                self.ui.cboxPeriodo_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            
            if(curso == 'Selecione o curso do aluno'):
                self.ui.cboxCurso_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            
            if(serie_turma == 'Selecione a turma do aluno'):
                self.ui.cboxTurma_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')

            #validações de preechimento corretos dos campos, setando os campos preenchidos com cor verde
            if(periodo != 'Selecione o período do aluno'):
                self.ui.cboxPeriodo_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            
            if(curso != 'Selecione o curso do aluno'):
                self.ui.cboxCurso_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            
            if(serie_turma != 'Selecione a turma do aluno'):
                self.ui.cboxTurma_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')         
        #se os campos estiverem preechidos
        else:
            #variaveis que irao armazenar os id's do periodo e curso
            id_periodo = 0
            id_curso = 0

            #setando o id do periodo
            if(periodo == 'Manhã'):
                id_periodo = id_periodo + 1
            elif(periodo == 'Tarde'):
                id_periodo = id_periodo + 2
            else:#periodo da noite
                id_periodo = id_periodo + 3

            #setando o id do curso
            if(curso == 'Administração'):
                id_curso = id_curso + 1
            elif(curso == 'Contabilidade'):
                id_curso = id_curso + 2
            elif(curso == 'Desenvolvimento de Sistemas'):
                id_curso = id_curso + 3
            elif(curso == 'Logística'):
                id_curso = id_curso + 4
            elif(curso == 'Recursos Humanos'):
                id_curso = id_curso + 5
            else:#servicos juridicos
                id_curso = id_curso + 6
            
            #consulta a tabela 'turma' para encontrar o id da turma correspondente
            BancoTcc.cursor.execute("SELECT id_turma FROM turma WHERE id_periodo = ? AND id_curso = ? AND serie_turma = ?", (id_periodo, id_curso, serie_turma))
            #armazena o resultado da busca na variavel
            resultado_busca = BancoTcc.cursor.fetchone()
            #se a busca obter dados
            if resultado_busca:
                id_turma = resultado_busca[0]  #id da turma na qual foi buscada
                consulta_turma = "SELECT * FROM turma WHERE id_turma = ?"  #consulta SQL para selecionar os dados da turma com base no id
                BancoTcc.cursor.execute(consulta_turma, (id_turma,))
                dados_turma = BancoTcc.cursor.fetchone()  #armazenando os dados da turma 
                #se obter os dados da turma de acordo com o id da turma
                if dados_turma is not None:
                    id_curso = dados_turma[1]  #variavel que recebe o id do curso, '1' é coluna em que o id do curso esta 
                    id_periodo = dados_turma[2]  #variavel que recebe o id do periodo, '2' é coluna em que o id do periodo esta 
                    serie_turma = dados_turma[3] #variavel que recebe o id da serie, '3' é coluna em que o id da serie esta 

                    consulta_curso = "SELECT * FROM curso WHERE id_curso = ?"  #consulta SQL para selecionar os dados do curso com base no id do curso
                    BancoTcc.cursor.execute(consulta_curso, (id_curso,))
                    dados_curso = BancoTcc.cursor.fetchone()  #armazenando os dados do curso
  
                    consulta_periodo = "SELECT * FROM periodo WHERE id_periodo = ?"  #consulta SQL para selecionar os dados do período com base no id do período
                    BancoTcc.cursor.execute(consulta_periodo, (id_periodo,))
                    dados_periodo = BancoTcc.cursor.fetchone()  #armazenando os dados do periodo

                    #se obter os dados do curso e do periodo
                    if dados_curso is not None and dados_periodo is not None:
                        nome_curso = dados_curso[1]  #variavel que recebe o nome do curso, '1' é coluna em que o nome do curso esta 
                        turno_periodo = dados_periodo[1]  #variavel que recebe o turno do curso, '1' é coluna em que o turno do curso esta 

                        #consulta SQL para buscar dados dos alunos com base no ID da turma
                        consulta_sql = "SELECT nome_aluno, rm_aluno FROM aluno WHERE id_turma = ?"
                        BancoTcc.cursor.execute(consulta_sql, (id_turma,))
                        dados_alunos = BancoTcc.cursor.fetchall()  #armazenando os dados do aluno

                        #preenchendo a tabela com os dados dos alunos na pagina de visualização dos dados da turma
                        self.ui.tbl_Alunos.setRowCount(len(dados_alunos))#lendo o tamanho dos dados do aluno, e setando os valores na tabela
                        for row, data in enumerate(dados_alunos):
                            for col, value in enumerate(data):
                                item = QTableWidgetItem(str(value))
                                #setando os valores na tabela dos alunos da turma
                                self.ui.tbl_Alunos.setItem(row, col, item)

                        #setando o nome abreviado do curso para exibição
                        if(id_curso == 1):
                            nomeAbrevi_curso = 'ADM'
                        elif(nome_curso == 2):
                            nomeAbrevi_curso = 'CONT'
                        elif(nome_curso == 3):
                            nomeAbrevi_curso = 'DS'
                        elif(nome_curso == 4):
                            nomeAbrevi_curso = 'LOG'
                        elif(nome_curso == 5):
                            nomeAbrevi_curso = 'RH'
                        else:#servicos juridicos
                            nomeAbrevi_curso = 'JUR'

                        #setando os dados na pag Dados Turma para a visualização
                        self.ui.lbl_NomeTurma_PgDadosTurma.setText(serie_turma + ' ' + nomeAbrevi_curso + ' - ' + turno_periodo.upper())
                        self.ui.lbl_NomeCurso_PgDadosTurma.setText(nome_curso)
                        self.ui.lbl_Periodo_PgDadosTurma.setText(turno_periodo)
                        self.ui.lbl_Serie_PgDadosTurma.setText(serie_turma)
                        self.ui.lbl_QtdAlunos_PgDadosTurma.setText(str(len(dados_alunos)))
                        #redirecionando para a pagina de visualização
                        self.ui.stackedWidget.setCurrentIndex(6)
                    #se nao obter os dados do curso e do periodo
                    else:
                        QMessageBox.information(self, "Sem resultados!", "Nenhum resultado encontrado para o ID do Curso ou do Período.")
                #se nao obter os dados da turma
                else:
                    QMessageBox.information(self, "Sem resultados!", "Nenhum resultado encontrado para o ID da Turma.")
            #se a busca não obter dados
            else:
                QMessageBox.information(self, "Turma não encontrada", "Turma não encontrada. A turma pesquisada não existe.")

            #limpando os campos da pesquisa e setando os valores iniciais
            self.restaurarCampos()
                       
    #botao que ira redirecionar p/ pag alunoRm com os dados do aluno pesquisado
    def btnBuscarRm(self):
        #variavel que recebe o rm do aluno
        rm = self.ui.etyPesquisarRM_PgPesquisar.text()
        #ira fazer a validação dos campos não preechidos
        if(rm == ''):
            QMessageBox.warning(self, "Aviso", "Preencha o campo 'RM' para concluir a busca!")  #mensagem de campos nao preenchidos
            #validações de nao preechimento dos campos, setando os campos nao preenchidos com cor vermelha
            if(rm == ''):
                self.ui.etyPesquisarRM_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            #validações de preechimento corretos dos campos, setando os campos preenchidos com cor verde        
            if(rm != ''):
                self.ui.etyPesquisarRM_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
        #verifica se o RM contém apenas dígitos
        elif not re.match(r'^\d+$', rm):
            QMessageBox.warning(self, "Aviso", "O RM deve conter apenas números.")  #mensagem informando o usuario p/ digitar apenas numeros
            self.ui.etyPesquisarRM_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            return  #saia da função se o RM for inválido
        #se os campos estiverem preechidos corretamente
        else:
            consulta_sql = "SELECT * FROM aluno WHERE rm_aluno = ?"  #consulta sql que selcionar os dados do aluno de acordo com o rm dele
            BancoTcc.cursor.execute(consulta_sql, (rm,))
            dados_aluno = BancoTcc.cursor.fetchone()  #armazenando os dados do aluno
            #se obter os dados do aluno
            if dados_aluno:
                self.id_aluno = dados_aluno[0]  #variavel que recebe o id do aluno, o '0' é a coluna em que o id do aluno esta
                id_turma = dados_aluno[1]  #variavel que recebe o id do curso, '1' é coluna em que o id do curso esta 
                rm_aluno = dados_aluno[2]  #variavel que recebe o id do periodo, '2' é coluna em que o id do periodo esta 
                nome_aluno = dados_aluno[3]  #variavel que recebe o nome do aluno, o '3' é a coluna em que o nome do aluno esta
                self.face_alunoAtt = dados_aluno[4]  #variavel que recebe a face do aluno, o '4' é a coluna em que a face do aluno esta

                consulta_turma = "SELECT * FROM turma WHERE id_turma = ?"  #consulta SQL para selecionar os dados da turma com base no id
                BancoTcc.cursor.execute(consulta_turma, (id_turma,))
                dados_turma = BancoTcc.cursor.fetchone()  #armazenando os dados da turma 
                #se obter os dados da turma
                if dados_turma is not None:
                    id_curso = dados_turma[1]  #variavel que recebe o id do curso, '1' é coluna em que o id do curso esta 
                    id_periodo = dados_turma[2]  #variavel que recebe o id do periodo, '2' é coluna em que o id do periodo esta 
                    serie_turma = dados_turma[3] #variavel que recebe o id da serie, '3' é coluna em que o id da serie esta 

                    #consulta SQL para selecionar os dados do curso com base no id do curso
                    consulta_curso = "SELECT * FROM curso WHERE id_curso = ?"
                    BancoTcc.cursor.execute(consulta_curso, (id_curso,))
                    dados_curso = BancoTcc.cursor.fetchone()  #armazenando os dados do curso

                    #consulta SQL para selecionar os dados do período com base no id do período
                    consulta_periodo = "SELECT * FROM periodo WHERE id_periodo = ?"
                    BancoTcc.cursor.execute(consulta_periodo, (id_periodo,))
                    dados_periodo = BancoTcc.cursor.fetchone()  #armazenando os dados do periodo

                    #se obter os dados do curso e do periodo
                    if dados_curso is not None and dados_periodo is not None:
                        nome_curso = dados_curso[1]  #variavel que recebe o nome do curso, '1' é coluna em que o nome do curso esta 
                        turno_periodo = dados_periodo[1]  #variavel que recebe o turno do curso, '1' é coluna em que o turno do curso esta 

                        #setando o nome abreviado do curso para exibição
                        if(id_curso == 1):
                            nomeAbrevi_curso = 'ADM'
                        elif(nome_curso == 2):
                            nomeAbrevi_curso = 'CONT'
                        elif(nome_curso == 3):
                            nomeAbrevi_curso = 'DS'
                        elif(nome_curso == 4):
                            nomeAbrevi_curso = 'LOG'
                        elif(nome_curso == 5):
                            nomeAbrevi_curso = 'RH'
                        else:#servicos juridicos
                            nomeAbrevi_curso = 'JUR'

                        #setando os dados na pag Dados Turma para a visualização
                        self.ui.lbl_Nome_PgDadosAluno.setText(nome_aluno)
                        self.ui.lbl_Rm_PgDadosAluno.setText(str(rm_aluno))
                        self.ui.lbl_Periodo_PgDadosAluno.setText(turno_periodo)
                        self.ui.lbl_NomeCurso_PgDadosAluno.setText(nome_curso)
                        self.ui.lbl_Turma_PgDadosAluno.setText(serie_turma + ' ' + nomeAbrevi_curso + ' - ' + turno_periodo.upper())                
                        # Crie um QPixmap a partir dos dados da imagem
                        pixmap = QPixmap()
                        pixmap.loadFromData(self.face_alunoAtt)
                        # Defina o QPixmap na label
                        self.ui.lbl_ImgAluno_PgDadosAluno.setPixmap(pixmap)
                        self.ui.lbl_ImgAluno_PgDadosAluno.setScaledContents(True)

                        #setando os dados nas variaveis que foram iniciadas no 'def __init__', nas configs iniciais
                        self.turno_periodoAtt = turno_periodo
                        self.nome_cursoAtt = nome_curso
                        self.serie_turmaAtt = serie_turma
                        
                        #redirecionando para pagina de dados do alunos
                        self.ui.stackedWidget.setCurrentIndex(7)
                    #se nao obter os dados do curso e do periodo
                    else:
                        QMessageBox.information(self, "Sem resultados!", "Nenhum resultado encontrado para o ID do curso ou do período.")   
                #se nao obter os dados da turma
                else:
                    QMessageBox.information(self, "Informação", "Nenhuma turma encontrada com o id informado.")
            #se nao obter os dados do aluno    
            else:
                QMessageBox.information(self, "Informação", "Nenhum aluno encontrado com o RM informado.")
            #limpando os campos e setando os valores iniciais
            self.restaurarCampos()

    #funcao que ira limpar os campos e setar os valores iniciais
    def restaurarCampos(self):
        #limpando as caixas de texto
        self.ui.etyPesquisarRM_PgPesquisar.setText('')
        #limpando a seleção da combobox
        self.ui.cboxPeriodo_PgPesquisar.setCurrentIndex(0)
        self.ui.cboxCurso_PgPesquisar.setCurrentIndex(0)
        self.ui.cboxTurma_PgPesquisar.setCurrentIndex(0)

        #retornando as cores iniciais dos campos
        self.ui.etyPesquisarRM_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid #000000; color:#ffffff')
        self.ui.cboxPeriodo_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border-color:#069E6E; color:#ffffff')
        self.ui.cboxCurso_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border-color:#069E6E; color:#ffffff')
        self.ui.cboxTurma_PgPesquisar.setStyleSheet('background-color: #069E6E; border-radius:5px; border-color:#069E6E; color:#ffffff')
    #=================================================================================================
    #=================================================================================================



    #=================================================================================================
    #=============FUNCAO PAG DADOS ALUNO==============================================================
    #=================================================================================================
    #botao que ira redirecionar p/ pag de atualizar os dados do aluno
    def btnAtualizarAluno_PgDadosAluno(self):  
        #consulta sql que ira selecionar os dados do aluno com base no id do aluno   
        consulta_aluno = "SELECT * FROM aluno WHERE id_aluno = ?"
        BancoTcc.cursor.execute(consulta_aluno, (self.id_aluno,))
        dados_aluno = BancoTcc.cursor.fetchone() #armazenando os dados do aluno 
        #se obter os dados do aluno
        if dados_aluno is not None:
            #setando os campos com os valores do respectivo aluno contido no banco
            self.ui.etyNome_PgAtualizar.setText(dados_aluno[3])  #'3' coluna em que esta o nome do aluno na tabela aluno
            self.ui.etyRM_PgAtualizar.setText(str(dados_aluno[2]))  #'2' coluna em que esta o rm do aluno na tabela aluno
            self.ui.cboxPeriodo_PgAtualizar.setCurrentText(self.turno_periodoAtt)
            self.ui.cboxCurso_PgAtualizar.setCurrentText(self.nome_cursoAtt)
            self.ui.cboxTurma_PgAtualizar.setCurrentText(self.serie_turmaAtt)
            # Crie um QPixmap a partir dos dados da imagem
            pixmap = QPixmap()
            pixmap.loadFromData(self.face_alunoAtt)
            # Defina o QPixmap na label
            self.ui.lbl_ImgAluno_PgAtualizar.setPixmap(pixmap)
            self.ui.lbl_ImgAluno_PgAtualizar.setScaledContents(True)
            #redirecionando para a pag de atualizar aluno
            self.ui.stackedWidget.setCurrentIndex(4)
        #se nao obter os dados do aluno
        else:
            QMessageBox("Os dados do aluno estão ausentes ou são None. Por favor, verifique os dados.")  
    #botao que ira deletar o aluno de acordo com o id
    def deletarAluno(self):       
        dialogo = QMessageBox()#caixa de mensagem    
        dialogo.setWindowTitle("Exclusão do aluno")#titulo da caixa de mensagem    
        dialogo.setText("Deseja deletar o cadastro do aluno?:")#texto da caixa de mensagem
        dialogo.setIcon(QMessageBox.Information)#define o ícone da caixa de diálogo
        dialogo.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel)#define os botões padrão como "Ok" e "Cancelar"
        opcao_Selecionada = dialogo.exec_()

        #se o usuario clicar em 'ok' ira deletar o aluno
        if opcao_Selecionada == QMessageBox.Ok:
            #se obter o id do aluno
            if self.id_aluno is not None:
                id_aluno_excluir = self.id_aluno  #id do aluno que ira ser excluido
                #instrução sql que ira deletar o aluno com base no id do aluno
                BancoTcc.cursor.execute("DELETE FROM aluno WHERE id_aluno = ?", (id_aluno_excluir,))
                BancoTcc.conn.commit()
                #mensagem que o aluno foi excluido
                QMessageBox.information(self, "Exclusão do aluno concluída", "Cadastro do aluno deletado com sucesso!")
                self.ui.stackedWidget.setCurrentIndex(5)#redirecionando para a pag pesquisar
            #se nao obter o id do aluno
            else:
                QMessageBox.warning(self, "Exclusão do aluno", "ID do aluno não definido. Selecione um aluno para excluir.")
        #se clicar em 'cancel' ira interromper a exclusão
        elif opcao_Selecionada == QMessageBox.Cancel:
            QMessageBox.warning(self, "Exclusão do aluno interrompida", "Exclusão interrompida com sucesso!")
        
    #=================================================================================================
    #=================================================================================================



    #=================================================================================================
    #===========FUNCAO PAG CADASTRAR ALUNO============================================================
    #=================================================================================================
    #funcao que ira cadastrar aluno
    def cadastrarAluno(self):
        #obtendo os valores contidos nos campos
        nome = self.ui.etyNome_PgCadastro.text().upper()
        rm = self.ui.etyRM_PgCadastro.text()
        periodo = self.ui.cboxPeriodo_PgCadastro.currentText()
        curso = self.ui.cboxCurso_PgCadastro.currentText()
        serie_turma = self.ui.cboxTurma_PgCadastro.currentText()

        #ira fazer a validação dos campos não preechidos
        if(nome == '' or rm == '' or periodo == 'Selecione o período do aluno' or curso == 'Selecione o curso do aluno' or 
           serie_turma == 'Selecione a turma do aluno'):
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")#mensagem de campos nao preenchidos

            #validações de nao preechimento dos campos, setando os campos nao preenchidos com cor vermelha
            if(nome == ''):
                self.ui.etyNome_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            if(rm == ''):
                self.ui.etyRM_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            if(periodo == 'Selecione o período do aluno'):
                self.ui.cboxPeriodo_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            if(curso == 'Selecione o curso do aluno'):
                self.ui.cboxCurso_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            if(serie_turma == 'Selecione a turma do aluno'):
                self.ui.cboxTurma_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')

            #validações de preechimento corretos dos campos, setando os campos preenchidos com cor verde
            if(nome != ''):
                self.ui.etyNome_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            if(rm != ''):
                self.ui.etyRM_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            if(periodo != 'Selecione o período do aluno'):
                self.ui.cboxPeriodo_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            if(curso != 'Selecione o curso do aluno'):
                self.ui.cboxCurso_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            if(serie_turma != 'Selecione a turma do aluno'):
                self.ui.cboxTurma_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
        
        #verifica se o nome é uma string não vazia e contém apenas letras e espaços
        elif not re.match(r'^[A-Za-z\s]+$', nome):
            QMessageBox.warning(self, "Aviso", "O nome deve conter apenas letras e espaços.")
            self.ui.etyNome_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            return  # Saia da função se o nome for inválido

        #verifica se o RM contém apenas dígitos
        elif not re.match(r'^\d+$', rm):
            QMessageBox.warning(self, "Aviso", "O RM deve conter apenas números.")
            self.ui.etyRM_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            return  # Saia da função se o RM for inválido)

        #se os campos estiverem preechidos
        else:
            id_periodo = 0
            id_curso = 0

            #setando o id do periodo
            if(periodo == 'Manhã'):
                id_periodo = id_periodo + 1    
            elif(periodo == 'Tarde'):
                id_periodo = id_periodo + 2       
            else:#periodo da noite
                id_periodo = id_periodo + 3

            #setando o id do curso
            if(curso == 'Administração'):
                id_curso = id_curso + 1      
            elif(curso == 'Contabilidade'):
                id_curso = id_curso + 2        
            elif(curso == 'Desenvolvimento de Sistemas'):
                id_curso = id_curso + 3    
            elif(curso == 'Logística'):
                id_curso = id_curso + 4   
            elif(curso == 'Recursos Humanos'):
                id_curso = id_curso + 5   
            else:#servicos juridicos
                id_curso = id_curso + 6
            
            #se obter a imagem da face do aluno
            if self.face_aluno is not None:
                #consulta a tabela 'turma' para encontrar o ID da turma correspondente
                BancoTcc.cursor.execute("SELECT id_turma FROM turma WHERE id_periodo = ? AND id_curso = ? AND serie_turma = ?", (id_periodo, id_curso, serie_turma))
                result = BancoTcc.cursor.fetchone()
                #se obter o id da turma
                if result:
                    id_turma = result[0]  #setando o id da turma em uma variavel
                    #inserindo o aluno na tabela 'alunos' associando-o à turma correta
                    BancoTcc.cursor.execute("INSERT INTO aluno (id_turma, rm_aluno, nome_aluno, face_aluno) VALUES (?, ?, ?, ?)", (id_turma, rm, nome, self.face_aluno))
                    BancoTcc.conn.commit()
                    QMessageBox.information(self, "Cadastro Concluido", "Cadastro Realizado com Sucesso!!")#mensagem de cadastro concluido
                    #limpando todos os campos apos o cadastro
                    self.limparCampos()
                #se nao obter o id da turma           
                else:
                    QMessageBox.information(self, "Turma não encontrada", "Turma não encontrada. O aluno não foi cadastrado.!")             
            #se nao obter a imagem da face do aluno
            else:
                QMessageBox.information(self, "Imagem não encontrada", "Selecione alguma imagem do aluno. O aluno não contém imagem para cadastrar.")  
    
    #funcao que ira carregar a foto do aluno
    def carregar_imagem(self):
        #cria um objeto de opções para a caixa de dialogo
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg *.gif *.bmp);;Todos os arquivos (*)", options=options)

        #verifica se o caminho do arquivo (filename) não está vazio
        if file_name:
            #cria um objeto QPixmap a partir do arquivo de imagem selecionado
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(200, 210)#tamanho da imagem
            self.ui.lbl_ImgAluno_PgCadastro.setPixmap(pixmap)#setando imagem na label da imagem

            # Lê os dados da imagem e os armazena na variável image_data
            with open(file_name, 'rb') as imagem_aluno:
                self.face_aluno = imagem_aluno.read()
    
    #funcao que ira limpar os campos e setar os valores iniciais
    def limparCampos(self):
        #limpando as caixas de texto
        self.ui.etyNome_PgCadastro.setText('')
        self.ui.etyRM_PgCadastro.setText('')
        #limpando a seleção da combobox
        self.ui.cboxPeriodo_PgCadastro.setCurrentIndex(0)
        self.ui.cboxCurso_PgCadastro.setCurrentIndex(0)
        self.ui.cboxTurma_PgCadastro.setCurrentIndex(0)

        #retornando as cores iniciais dos campos
        self.ui.etyNome_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid #000000; color:#ffffff')
        self.ui.etyRM_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid #000000; color:#ffffff')
        self.ui.cboxPeriodo_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border-color:#069E6E; color:#ffffff')
        self.ui.cboxCurso_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border-color:#069E6E; color:#ffffff')
        self.ui.cboxTurma_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border-color:#069E6E; color:#ffffff')

        #retirando a imagem do aluno
        width, height = 200, 210
        fundoImagem = QImage(width, height, QImage.Format_RGB32)
        fundoImagem.fill(QColor(241, 241, 241))  # Preenche com branco
        self.pixmap = QPixmap.fromImage(fundoImagem)
        self.ui.lbl_ImgAluno_PgCadastro.setPixmap(self.pixmap)

    #funcao que ira exibir os cursos de acordo com o periodo selecionado
    def exibirCursosPorPeriodo(self):
        #varivel contendo os curso existentes por periodo
        cursos_PorPeriodo = {
            "Manhã": ["Administração", "Desenvolvimento de Sistemas", "Recursos Humanos"],
            "Tarde": ["Administração", "Desenvolvimento de Sistemas", "Logística"],
            "Noite": ["Administração", "Contabilidade", "Desenvolvimento de Sistemas", "Logística", "Serviços Jurídicos"]
        }

        #variavel que recebe o periodo que o usuario selecionou
        periodo_selecionado = self.ui.cboxPeriodo_PgCadastro.currentText()
        #variavel que exibi os cursos disponiveis de acordo com o periodo selecionado
        cursos_disponiveis = cursos_PorPeriodo.get(periodo_selecionado, [])
        
        self.ui.cboxCurso_PgCadastro.clear()
        #opcao do combobox para ser utilizada como ajuda(placeholder)
        self.ui.cboxCurso_PgCadastro.addItem("Selecione o curso do aluno")
        #adicionando opções de curso na combobox de acordo com o perido selecionado
        self.ui.cboxCurso_PgCadastro.addItems(cursos_disponiveis)
        #desabilitando a opção 'selecione...'
        self.ui.cboxCurso_PgCadastro.model().item(0).setFlags(Qt.ItemIsEnabled)

    #=================================================================================================
    #=================================================================================================



    #=================================================================================================
    #===========FUNCAO PAG ATUALIZAR ALUNO============================================================
    #=================================================================================================
    #funcao que ira atualizar aluno
    def atualizarAluno(self):
        #id do aluno que sera atualizado
        id_aluno_atualizar = self.id_aluno
        #se obter o id do aluno
        if id_aluno_atualizar is not None:
            #obtendo os valores dos campos 
            nome = self.ui.etyNome_PgAtualizar.text().upper()
            rm = self.ui.etyRM_PgAtualizar.text()
            periodo = self.ui.cboxPeriodo_PgAtualizar.currentText()
            curso = self.ui.cboxCurso_PgAtualizar.currentText()
            serie_turma = self.ui.cboxTurma_PgAtualizar.currentText()
         
            dialogo = QMessageBox()  #caixa de mensagem          
            dialogo.setWindowTitle("Atualização do cadastro do aluno")  #titulo da caixa de mensagem         
            dialogo.setText("Deseja atualizar os dados do cadastro do aluno?:")  #texto da caixa de mensagem      
            dialogo.setIcon(QMessageBox.Information)  #define o ícone da caixa de diálogo
            dialogo.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel)  #define os botões padrão como "Ok" e "Cancelar"
            resultado = dialogo.exec_()

            #se o usuario clicar em 'ok' ira atualizar o aluno
            if resultado == QMessageBox.Ok:
                #se obter o id do aluno
                if id_aluno_atualizar is not None:
                    id_periodo = 0
                    id_curso = 0

                    #setando o id do periodo
                    if(periodo == 'Manhã'):
                        id_periodo = id_periodo + 1
                    elif(periodo == 'Tarde'):
                        id_periodo = id_periodo + 2
                    else:#periodo da noite
                        id_periodo = id_periodo + 3

                    #setando o id do curso
                    if(curso == 'Administração'):
                        id_curso = id_curso + 1
                    elif(curso == 'Contabilidade'):
                        id_curso = id_curso + 2
                    elif(curso == 'Desenvolvimento de Sistemas'):
                        id_curso = id_curso + 3
                    elif(curso == 'Logística'):
                        id_curso = id_curso + 4
                    elif(curso == 'Recursos Humanos'):
                        id_curso = id_curso + 5
                    else:#servicos juridicos
                        id_curso = id_curso + 6
                    
                    #consulta a tabela 'turma' para encontrar o ID da turma correspondente
                    BancoTcc.cursor.execute("SELECT id_turma FROM turma WHERE id_periodo = ? AND id_curso = ? AND serie_turma = ?", (id_periodo, id_curso, serie_turma))
                    result = BancoTcc.cursor.fetchone()
                    #se obter o id da turma
                    if result:
                        id_turma = result[0]  #setando o id da turma em uma variavel
                        #atualizando os dados do aluno com base no id do aluno selecionado, associando-o à turma correta
                        BancoTcc.cursor.execute("UPDATE aluno SET id_turma=?, rm_aluno=?, nome_aluno=?, face_aluno=? WHERE id_aluno = ?", (id_turma, rm, nome, self.face_aluno, id_aluno_atualizar))
                        BancoTcc.conn.commit()
                        QMessageBox.information(self, "Atualização do aluno concluída", "Dados do cadastro do aluno atualizado com sucesso!")
                        #redirecionando para pagina de dados do alunos
                        self.ui.stackedWidget.setCurrentIndex(7)

                        #EXCUTANDO SQL NOVAMENTE PARA OBTER OS NOVOS DADOS CADASTRADOS E ASSIM EXIBIR NA PAG DE DADOS DO ALUNO
                        consulta_sql = "SELECT * FROM aluno WHERE id_aluno = ?"  #consulta sql que selcionar os dados do aluno de acordo com o id dele
                        BancoTcc.cursor.execute(consulta_sql, (self.id_aluno,))
                        dados_aluno = BancoTcc.cursor.fetchone()  #armazenando os dados do aluno
                        #se obter os dados do aluno
                        if dados_aluno:
                            self.id_aluno = dados_aluno[0]  #variavel que recebe o id do aluno, o '0' é a coluna em que o id do aluno esta
                            id_turma = dados_aluno[1]  #variavel que recebe o id do curso, '1' é coluna em que o id do curso esta 
                            rm_aluno = dados_aluno[2]  #variavel que recebe o id do periodo, '2' é coluna em que o id do periodo esta 
                            nome_aluno = dados_aluno[3]  #variavel que recebe o nome do aluno, o '3' é a coluna em que o nome do aluno esta
                            self.face_alunoAtt = dados_aluno[4]  #variavel que recebe a face do aluno, o '4' é a coluna em que a face do aluno esta

                            consulta_turma = "SELECT * FROM turma WHERE id_turma = ?"  #consulta SQL para selecionar os dados da turma com base no id
                            BancoTcc.cursor.execute(consulta_turma, (id_turma,))
                            dados_turma = BancoTcc.cursor.fetchone()  #armazenando os dados da turma 
                            #se obter os dados da turma
                            if dados_turma is not None:
                                id_curso = dados_turma[1]  #variavel que recebe o id do curso, '1' é coluna em que o id do curso esta 
                                id_periodo = dados_turma[2]  #variavel que recebe o id do periodo, '2' é coluna em que o id do periodo esta 
                                serie_turma = dados_turma[3] #variavel que recebe o id da serie, '3' é coluna em que o id da serie esta 

                                #consulta SQL para selecionar os dados do curso com base no id do curso
                                consulta_curso = "SELECT * FROM curso WHERE id_curso = ?"
                                BancoTcc.cursor.execute(consulta_curso, (id_curso,))
                                dados_curso = BancoTcc.cursor.fetchone()  #armazenando os dados do curso

                                #consulta SQL para selecionar os dados do período com base no id do período
                                consulta_periodo = "SELECT * FROM periodo WHERE id_periodo = ?"
                                BancoTcc.cursor.execute(consulta_periodo, (id_periodo,))
                                dados_periodo = BancoTcc.cursor.fetchone()  #armazenando os dados do periodo

                                #se obter os dados do curso e do periodo
                                if dados_curso is not None and dados_periodo is not None:
                                    nome_curso = dados_curso[1]  #variavel que recebe o nome do curso, '1' é coluna em que o nome do curso esta 
                                    turno_periodo = dados_periodo[1]  #variavel que recebe o turno do curso, '1' é coluna em que o turno do curso esta 

                                    #setando os dados na pag Dados Turma para a visualização
                                    self.ui.lbl_Nome_PgDadosAluno.setText(nome_aluno)
                                    self.ui.lbl_Rm_PgDadosAluno.setText(str(rm_aluno))
                                    self.ui.lbl_Periodo_PgDadosAluno.setText(turno_periodo)
                                    self.ui.lbl_NomeCurso_PgDadosAluno.setText(nome_curso)
                                    self.ui.lbl_Turma_PgDadosAluno.setText(serie_turma + ' ' + nome_curso + ' ' + turno_periodo)                 
                                    # Crie um QPixmap a partir dos dados da imagem
                                    pixmap = QPixmap()
                                    pixmap.loadFromData(self.face_alunoAtt)
                                    # Defina o QPixmap na label
                                    self.ui.lbl_ImgAluno_PgDadosAluno.setPixmap(pixmap)
                                    self.ui.lbl_ImgAluno_PgDadosAluno.setScaledContents(True)

                                    #setando os dados nas variaveis que foram iniciadas no 'def __init__', nas configs iniciais
                                    self.turno_periodoAtt = turno_periodo
                                    self.nome_cursoAtt = nome_curso
                                    self.serie_turmaAtt = serie_turma
                                #se nao obter os dados do curso e do periodo
                                else:
                                    QMessageBox.information(self, "Sem resultados!", "Nenhum resultado encontrado para o ID do curso ou do período.")   
                            #se nao obter os dados da turma
                            else:
                                QMessageBox.information(self, "Informação", "Nenhuma turma encontrada com o id informado.")
                        #se nao obter os dados do aluno    
                        else:
                            QMessageBox.information(self, "Informação", "Nenhum aluno encontrado com o RM informado.")
                    #se nao obter o id da turma
                    else:
                        QMessageBox.information(self, "Turma não encontrada", "Turma não encontrada. O aluno não foi atualizado.!")
                #se obter o id do aluno
                else:
                    QMessageBox.warning(self, "Exclusão do aluno", "ID do aluno não definido ou encontrado.")
            #se clicar em 'cancel' ira interromper a atualização
            elif resultado == QMessageBox.Cancel:
                QMessageBox.warning(self, "Atualização do aluno interrompida", "Atualização interrompida com sucesso!")
        #se nao obter o id do aluno
        else:
            QMessageBox.warning(self, "Atualização do aluno falhou", "ID do aluno não definido ou encontrado.")

    #funcao que ira exibir os cursos de acordo com o periodo selecionado
    def exibirCursosPorPeriodo_PgAtualizar(self):
        #varivel contendo os curso existentes por periodo
        cursos_PorPeriodo = {
            "Manhã": ["Administração", "Desenvolvimento de Sistemas", "Recursos Humanos"],
            "Tarde": ["Administração", "Desenvolvimento de Sistemas", "Logística"],
            "Noite": ["Administração", "Contabilidade", "Desenvolvimento de Sistemas", "Logística", "Serviços Jurídicos"]
        }

        #variavel que recebe o periodo que o usuario selecionou
        periodo_selecionado = self.ui.cboxPeriodo_PgAtualizar.currentText()
        #variavel que exibi os cursos disponiveis de acordo com o periodo selecionado
        cursos_disponiveis = cursos_PorPeriodo.get(periodo_selecionado, [])
        
        self.ui.cboxCurso_PgAtualizar.clear()
        #opcao do combobox para ser utilizada como ajuda(placeholder)
        self.ui.cboxCurso_PgAtualizar.addItem("Selecione o curso do aluno")
        #adicionando opções de curso na combobox de acordo com o perido selecionado
        self.ui.cboxCurso_PgAtualizar.addItems(cursos_disponiveis)
        #desabilitando a opção 'selecione...'
        self.ui.cboxCurso_PgAtualizar.model().item(0).setFlags(Qt.ItemIsEnabled)

    #funcao que ira carregar a foto do aluno
    def carregar_imagemPgAtualizar(self):
        #cria um objeto de opções para a caixa de dialogo
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg *.gif *.bmp);;Todos os arquivos (*)", options=options)

        #verifica se o caminho do arquivo (filename) não está vazio
        if file_name:
            #cria um objeto QPixmap a partir do arquivo de imagem selecionado
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(200, 210)#tamanho da imagem
            self.ui.lbl_ImgAluno_PgAtualizar.setPixmap(pixmap)#setando imagem na label da imagem

            # Lê os dados da imagem e os armazena na variável image_data
            with open(file_name, 'rb') as imagem_aluno:
                self.face_aluno = imagem_aluno.read()
    #=================================================================================================
    #=================================================================================================



    #=================================================================================================
    #===========FUNCAO PAG PESQUISAR ALUNO============================================================
    #=================================================================================================
    #funcao que ira exibir os cursos de acordo com o periodo selecionado
    def exibirCursosPorPeriodo_PgPesquisar(self):
        #varivel contendo os curso existentes por periodo
        cursos_PorPeriodo = {
            "Manhã": ["Administração", "Desenvolvimento de Sistemas", "Recursos Humanos"],
            "Tarde": ["Administração", "Desenvolvimento de Sistemas", "Logística"],
            "Noite": ["Administração", "Contabilidade", "Desenvolvimento de Sistemas", "Logística", "Serviços Jurídicos"]
        }

        #variavel que recebe o periodo que o usuario selecionou
        periodo_selecionado = self.ui.cboxPeriodo_PgPesquisar.currentText()
        #variavel que exibi os cursos disponiveis de acordo com o periodo selecionado
        cursos_disponiveis = cursos_PorPeriodo.get(periodo_selecionado, [])
        
        self.ui.cboxCurso_PgPesquisar.clear()
        #opcao do combobox para ser utilizada como ajuda(placeholder)
        self.ui.cboxCurso_PgPesquisar.addItem("Selecione o curso do aluno")
        #adicionando opções de curso na combobox de acordo com o perido selecionado
        self.ui.cboxCurso_PgPesquisar.addItems(cursos_disponiveis)
        #desabilitando a opção 'selecione...'
        self.ui.cboxCurso_PgPesquisar.model().item(0).setFlags(Qt.ItemIsEnabled)
    #=================================================================================================
    #=================================================================================================