#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtGui import QPixmap, QImage, QColor
#importando da pasta 'telas_py' as telas do diretor em python
from telas_py.telas_Diretor import Ui_MainWindow as Ui_Telas_Diretor
import re

#CLASSE TURMA QUE IRA GERIR OS DADOS DA TURMA
class Turma:
    def __init__(self):
        pass
    #funcao de dados da turma que recebe os parametros tela de visualizar turma do sistema
    def visualizarTurma(self, periodo, curso, serie_turma):
        #variaveis que irao armazenar os id's do periodo e curso, setando com nenhum valor
        id_periodo, id_curso = 0, 0
        nomeAbrevi_cursoPgTurma = ''

        #setando o id do periodo
        if(periodo == 'Manhã'):
            id_periodo = 1
        elif(periodo == 'Tarde'):
            id_periodo = 2
        else:#periodo da noite
            id_periodo = 3

        #setando o id do curso e setando o nome abreviado do curso para exibição
        if(curso == 'Administração'):
            id_curso = 1
            nomeAbrevi_cursoPgTurma = 'ADM'
        elif(curso == 'Contabilidade'):
            id_curso = 2
            nomeAbrevi_cursoPgTurma = 'CONT'
        elif(curso == 'Desenvolvimento de Sistemas'):
            id_curso = 3
            nomeAbrevi_cursoPgTurma = 'DS'
        elif(curso == 'Logística'):
            id_curso = 4
            nomeAbrevi_cursoPgTurma = 'LOG'
        elif(curso == 'Recursos Humanos'):
            id_curso = 5
            nomeAbrevi_cursoPgTurma = 'RH'
        else:#servicos juridicos
            id_curso = 6
            nomeAbrevi_cursoPgTurma = 'JUR'
        
        #consulta a tabela 'turma' para encontrar o id da turma correspondente
        BancoTcc.cursor.execute("SELECT id_turma FROM turma WHERE id_periodo = ? AND id_curso = ? AND serie_turma = ?", (id_periodo, id_curso, serie_turma))
        resultado_busca = BancoTcc.cursor.fetchone()#armazena o resultado da busca na variavel
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
                               
                    #retornando as variaveis com valores para a tela de visualizar turma do sistema
                    return serie_turma, nomeAbrevi_cursoPgTurma, turno_periodo, nome_curso, dados_alunos
                #se nao obter os dados do curso e do periodo
                else:
                    resultado = "Nenhum resultado encontrado para o ID do Curso ou do Período." #setando o 'resultado' com uma mensagem
            #se nao obter os dados da turma
            else:
                resultado = "Nenhum resultado encontrado para o ID da Turma." #setando o 'resultado' com uma mensagem
        #se a busca não obter dados
        else:
            resultado = "Turma não encontrada. A turma pesquisada não existe." #setando o 'resultado' com uma mensagem  
        return resultado  #retornando o resultado de algum erro para a tela de visualizar turma do sistema