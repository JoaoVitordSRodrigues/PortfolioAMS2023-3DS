#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
import re

#CLASSE FUNCIONARIO QUE IRA GERIR OS DADOS DO FUNCIONARIO
class Funcionario:
    def funcionario(self, usuario, senha):#recebedo os parametros da tela de login
        #iniciando as variaveis com nenhum valor
        resultado, nome_funcionario = None, None

        #consulta sql que seleciona tudo sobre o funcionario com as credenciais inseridas(usuario e senha)
        consulta_funcionario = "SELECT * FROM funcionario WHERE usuario = ? AND senha = ?"
        BancoTcc.cursor.execute(consulta_funcionario, (usuario, senha,))
        #armazenando os dados do funcionario
        dados_funcionario = BancoTcc.cursor.fetchone()
        
        #se a consulta obter os dados
        if dados_funcionario is not None:
            nome_funcionario = dados_funcionario[1]  #variavel que recebe o nome do funcionario, '1' é coluna em que o nome do funcionario esta  
            funcao_funcionario = dados_funcionario[4]  #variavel que recebe a funcao do funcionario, '4' é coluna em que a funcao do funcionario esta  
            #se a funcao do funcionario for 'Diretor'
            if (funcao_funcionario == 'Diretor'):
                resultado = "Diretor" #setando o 'resultado' com 'Diretor'
            #se a funcao do funcionario for 'Seguranca'
            elif (funcao_funcionario == 'Segurança'):
                resultado = "Segurança"  #setando o 'resultado' com 'Segurança'                      
        #se a consulta nao obter os dados
        else:
            resultado = "Credenciais incorretas ou usuário não encontrado" #setando o 'resultado' com uma mensagem
        
        return resultado, nome_funcionario #retornado a classe de login as variaveis com valores