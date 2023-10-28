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
        usuario = self.ui.etyUsuario.text() 
        senha = self.ui.etySenha.text()  

        #ira fazer a validação dos campos não preechidos
        if(usuario == '' or senha == ''):
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")
            #campos nao preechidos, ira setar os campos que nao foram preechidos
            if(usuario == ''):
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')
            if(senha == ''):
                self.ui.etySenha.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')
            #campos preechidos, ira setar os campos que foram preechidos        
            if(usuario != ''):
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid green; color:#ffffff')
            if(senha != ''):
                self.ui.etySenha.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid green; color:#ffffff')
        #se os campos estiverem preechidos
        else: 
            #consulta sql que seleciona tudo sobre o funcionario com as credenciais inseridas(usuario e senha)
            consulta_funcionario = "SELECT * FROM funcionario WHERE usuario = ? AND senha = ?"
            BancoTcc.cursor.execute(consulta_funcionario, (usuario, senha,))
            #armazenando os dados da turma 
            dados_funcionario = BancoTcc.cursor.fetchone()
            #se a consulta obter os dados
            if dados_funcionario is not None:
                nome_funcionario = dados_funcionario[1]  #variavel que recebe o nome do funcionario, '1' é coluna em que o nome do funcionario esta  
                funcao_funcionario = dados_funcionario[4]  #variavel que recebe a funcao do funcionario, '4' é coluna em que a funcao do funcionario esta  
                #se a funcao do funcionario for 'diretor', ira abrir a tela do diretor
                if (funcao_funcionario == 'Diretor'):
                    from func_telas.func_TelasDiretor import Config_TelasDiretor 
                    self.telas_diretor = Config_TelasDiretor(nome_funcionario)#passando como parametro o nome do diretor
                    self.telas_diretor.show()
                    self.close()  #fecha a tela de login
                #se a funcao do funcionario for 'seguranca', ira abrir a tela do seguranca
                elif (funcao_funcionario == 'Segurança'):
                    from func_telas.func_TelasSeguranca import Config_TelasSeguranca   
                    self.telas_seguranca = Config_TelasSeguranca(nome_funcionario)#passando como parametro o nome do segurança
                    self.telas_seguranca.show()
                    self.close()  #fecha a tela de login
            #se a consulta nao obter os dados
            else:
                QMessageBox.warning(self, "Login Falhou", "Credenciais incorretas ou usuário não encontrado")
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

