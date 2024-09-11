#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
import re


#CLASSE ENTRADA QUE IRA GERIR OS DADOS DA ENTRADA
class Entrada:
    #funcao de dados da tabela entrada que recebe o parametro do nome da tela da tela de entrada do sistema
    def dadosTabelaEntrada(self, nomeTela, nome_funcionario):
        #A EXIBIÇÃO DOS DADOS DA TABELA DA TELA DE ENTRADA DO DIRETOR E SEGURANÇA SÃO DIFERENTES,ENTAO:
        #se o nome da tela for 'Diretor' 
        if nomeTela == 'Diretor':
            #consulta SQL para buscar todas as informações da tabela "entrada"
            BancoTcc.cursor.execute("SELECT nome_aluno, rm_aluno, periodo, data_entrada, horario_entrada, status_horario, nome_seguranca FROM entrada")
            dados_entrada = BancoTcc.cursor.fetchall() #armazenando os dados da entrada
            #se a consulta obter os dados
            if dados_entrada is not None:
                return dados_entrada #retornado os dados da entrada para a tela de entrada do sistema                     
            #se a consulta nao obter os dados
            else:
                resultado = "Não há dados para a exibição."  #setando uma mensagem no 'resultado'  
                return resultado #retornado os dados da entrada para a tela de entrada do sistema   
        #se o nome da tela for 'Seguranca' 
        if nomeTela == 'Seguranca':
            #consulta SQL para buscar todas as informações da tabela "entrada"
            BancoTcc.cursor.execute("SELECT nome_aluno, rm_aluno, periodo, data_entrada, horario_entrada, status_horario FROM entrada WHERE nome_seguranca = ?", (nome_funcionario,))
            dados_entrada = BancoTcc.cursor.fetchall() #armazenando os dados da entrada 
            #se a consulta obter os dados
            if dados_entrada is not None:
                return dados_entrada #retornado os dados da entrada para a tela de entrada do sistema                       
            #se a consulta nao obter os dados
            else:
                resultado = "Não há dados para a exibição."  #setando uma mensagem no 'resultado'    
                return resultado #retornado os dados da entrada para a tela de entrada do sistema  