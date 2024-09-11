#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QStackedWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
#importando da pasta 'telas_py' a tela de login em python
from telas_py.telaLogin import Ui_MainWindow
#importando da pasta 'classes' a classe do funcionario em python
from classes.Funcionario import Funcionario
from PyQt5.QtCore import Qt



#=========================================================================#
#                                                                         #
#                 CLASSE P/ A TELA DE LOGIN (TELA INICIAL)                #
#                                                                         #
#=========================================================================#
class MainWindow(QMainWindow):
    #CONFIG INICIAIS P/ SER EXECUTADAS AO ABRIR A TELA LOGIN
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #instanciando a classe funcionario
        self.classeFuncionario = Funcionario()
        
        #=============================================BOTOES==================================================
        #botao(checkbox) de exibir a senha
        self.ui.chkboxExibirSenha.stateChanged.connect(self.exibirSenha)
        #botao de fazer o login
        self.ui.btnLogin.clicked.connect(self.fazerLogin)


    #-----------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------
    #                                    FUNÇOES DA CLASSE LOGIN                                   -
    #-----------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------
    #FUNCAO QUE IRA EXIBIR E ESCONDER A SENHA
    def exibirSenha(self, state):
        #ira exibir a senha ao marcar a checkbox
        if (state == 2):#state 2 representa a caixa de seleção marcada
            self.ui.etySenha.setEchoMode(QtWidgets.QLineEdit.Normal)
        #ira esconder a senha ao desmarcar a checkbox        
        else:
            self.ui.etySenha.setEchoMode(QtWidgets.QLineEdit.Password)

    #FUNCAO QUE IRA FAZER O LOGIN
    def fazerLogin(self):
        usuario = self.ui.etyUsuario.text() #  setando o que o usuario escreveu no campo 'usuario' na variavel
        senha = self.ui.etySenha.text()  #  setando o que o usuario escreveu no campo 'senha' na variavel

        erro = 'background-color: #454648;  border: 2px solid red; color:#ffffff'#caracteristica do campo com feedback errado
        valido = 'background-color: #454648; border: 2px solid green; color:#ffffff'#caracteristica do campo com feedback correto

        #ira fazer a validação dos campos não preechidos
        if(usuario == '' or senha == ''):
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")#mensagem informando o usuario
            #campos nao preechidos, ira setar os campos que nao foram preechidos com borda vermelha
            if(usuario == ''):
                self.ui.etyUsuario.setStyleSheet(erro)
            if(senha == ''):
                self.ui.etySenha.setStyleSheet(erro)
            #campos preechidos, ira setar os campos que foram preechidos com borda verde    
            if(usuario != ''):
                self.ui.etyUsuario.setStyleSheet(valido)
            if(senha != ''):
                self.ui.etySenha.setStyleSheet(valido)
        #se os campos estiverem preechidos
        else: 
            #ira passar as variaveis 'usuario' e 'senha' como parametro para a funcao da classe funcionario
            #apos executar a funcao da classe ira retornar os dados e serao setados nas variaveis 'resultado' e 'nome_funcionario'
            resultado, nome_funcionario = self.classeFuncionario.funcionario(usuario, senha)
            #se caso o login nao estiver correto
            if resultado == "Credenciais incorretas ou usuário não encontrado":
                QMessageBox.warning(self, 'Aviso', resultado)#mensagem informando o usuario
                self.ui.etyUsuario.setStyleSheet(erro)
                self.ui.etySenha.setStyleSheet(erro)
            #caso o login estiver correto
            else:
                QMessageBox.warning(self, 'Aviso', 'Credenciais corretas! Acesso permitido.')#mensagem informando o usuario
                self.ui.etyUsuario.setStyleSheet(valido)
                self.ui.etySenha.setStyleSheet(valido)
                #se a varivel 'resultado' for retornada com o valor 'Diretor', ira abrir as telas do mesmo
                if resultado == "Diretor":  
                    from func_telas.func_TelasDiretor import Config_TelasDiretor#importando a classe func_TelasDiretor da pasta 'func_telas'
                    self.telas_diretor = Config_TelasDiretor(nome_funcionario)#passando como parametro o nome do diretor
                    self.telas_diretor.show()  #exibindo as telas do diretor   
                    
                #se a varivel 'resultado' for retornada com o valor 'Segurança', ira abrir as telas do mesmo
                elif resultado == "Segurança":
                    from func_telas.func_TelasSeguranca import Config_TelasSeguranca#importando a classe func_TelasSeguranca da pasta 'func_telas'
                    self.telas_seguranca = Config_TelasSeguranca(nome_funcionario)#passando como parametro o nome do segurança
                    self.telas_seguranca.show()  #exibindo as telas do seguranca

                self.close()  #fechando a tela de login
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

