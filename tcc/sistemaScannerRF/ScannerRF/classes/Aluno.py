#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtGui import QPixmap, QImage, QColor
#importando da pasta 'telas_py' as telas do diretor em python
from telas_py.telas_Diretor import Ui_MainWindow as Ui_Telas_Diretor
import re

#CLASSE ALUNO QUE IRA GERIR OS DADOS DO ALUNO
class Aluno:
    def __init__(self):
        self.id_aluno = None #iniciando a varivel com nenhum valor

    #funcao de cadastrar o aluno que recebe os parametros da tela de cadastrar do sistema
    def cadastrarAluno(self, nome, rm, periodo, curso, serie_turma, face_bytes, face_alunoCadastro ):
        #iniciando as variaveis com nenhum valor
        id_periodo , id_curso = 0, 0

        #setando o id do periodo
        if(periodo == 'Manhã'):
            id_periodo = 1    
        elif(periodo == 'Tarde'):
            id_periodo = 2       
        else:#periodo da noite
            id_periodo = 3

        #setando o id do curso
        if(curso == 'Administração'):
            id_curso = 1      
        elif(curso == 'Contabilidade'):
            id_curso = 2        
        elif(curso == 'Desenvolvimento de Sistemas'):
            id_curso = 3    
        elif(curso == 'Logística'):
            id_curso = 4   
        elif(curso == 'Recursos Humanos'):
            id_curso = 5   
        else:#servicos juridicos
            id_curso = 6
        
        #consulta a tabela 'turma' para encontrar o ID da turma correspondente
        BancoTcc.cursor.execute("SELECT id_turma FROM turma WHERE id_periodo = ? AND id_curso = ? AND serie_turma = ?", (id_periodo, id_curso, serie_turma))
        dados_turma = BancoTcc.cursor.fetchone() #armazenando os dados da consulta
        #se obter o id da turma
        if dados_turma:
            id_turma = dados_turma[0]  #setando o id da turma em uma variavel, dados_turma[0] pois é a posição coluna do id_turma 
            #consulta que verifica se o RM já existe no banco de dados
            BancoTcc.cursor.execute("SELECT rm_aluno FROM aluno WHERE rm_aluno=?", (rm,))
            dados_rm = BancoTcc.cursor.fetchone()#armazenando os dados da consulta
            #se houver um rm ja existente
            if dados_rm:
                resultado = "Este RM já existe no banco de dados. Digite outro RM." #setando uma mensagem no 'resultado'
            #se nao houver um rm ja existente
            else:
                #inserindo o aluno na tabela 'alunos' associando-o à turma correta
                BancoTcc.cursor.execute("INSERT INTO aluno (id_turma, rm_aluno, nome_aluno, face_aluno, imagem_aluno) VALUES (?, ?, ?, ?, ?)", (id_turma, rm, nome, face_bytes, face_alunoCadastro))
                BancoTcc.conn.commit()
                resultado = "Cadastro Realizado com Sucesso!"  #setando uma mensagem no 'resultado'
        #se nao obter o id da turma           
        else:
            resultado = "Turma não encontrada. O aluno não foi cadastrado."  #setando uma mensagem no 'resultado'
        return resultado #retornando o 'resultado' para a funcao cadastrar da tela do sistema  
       
    #funcao de visualizar o aluno que recebe os parametros da tela de buscar do sistema
    def visualizarAluno(self, rm):
        consulta_sql = "SELECT * FROM aluno WHERE rm_aluno = ?"  #consulta sql que selecionar os dados do aluno de acordo com o rm dele
        BancoTcc.cursor.execute(consulta_sql, (rm,))
        dados_aluno = BancoTcc.cursor.fetchone()  #armazenando os dados do aluno
        #se obter os dados do aluno
        if dados_aluno:
            id_aluno = dados_aluno[0]  #variavel que recebe o id do aluno, o '0' é a coluna em que o id do aluno esta
            id_turma = dados_aluno[1]  #variavel que recebe o id da turma, '1' é coluna em que o id da turma esta 
            rm_aluno = dados_aluno[2]  #variavel que recebe o rm do aluno, '2' é coluna em que o rm do aluno esta 
            nome_aluno = dados_aluno[3]  #variavel que recebe o nome do aluno, o '3' é a coluna em que o nome do aluno esta
            imagem_aluno = dados_aluno[5]  #variavel que recebe a face do aluno, o '5' é a coluna em que a face do aluno esta

            consulta_turma = "SELECT * FROM turma WHERE id_turma = ?"  #consulta SQL para selecionar os dados da turma com base no id da turma
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
                    elif(id_curso == 2):
                        nomeAbrevi_curso = 'CONT'
                    elif(id_curso == 3):
                        nomeAbrevi_curso = 'DS'
                    elif(id_curso == 4):
                        nomeAbrevi_curso = 'LOG'
                    elif(id_curso == 5):
                        nomeAbrevi_curso = 'RH'
                    else:#servicos juridicos
                        nomeAbrevi_curso = 'JUR'
                    #retorna os dados para a visualzação do aluno na funcao de visualizar do sistema
                    return id_aluno, nome_aluno, rm_aluno, turno_periodo, nome_curso, serie_turma, nomeAbrevi_curso, imagem_aluno
                #se nao obter os dados do curso e do periodo
                else:
                    resultado = "Nenhum resultado encontrado para o ID do curso ou do período." #setando uma mensagem no 'resultado'  
                    return resultado #retorna a mensagem na funcao de visualizar do sistema
            #se nao obter os dados da turma
            else:
                resultado = "Nenhuma turma encontrada com o id informado." #setando uma mensagem no 'resultado'
                return resultado #retorna a mensagem na funcao de visualizar do sistema
        #se nao obter os dados do aluno    
        else:
            resultado = "Nenhum aluno encontrado com o RM informado." #setando uma mensagem no 'resultado'
            return resultado #retorna a mensagem na funcao de visualizar do sistema
        
    #funcao de deletar aluno que recebe os parametros da tela de deletar do sistema
    def deletarAluno(self, id_aluno_excluir):  
        # consulta sql que irá obter o rm do aluno
        BancoTcc.cursor.execute("SELECT rm_aluno FROM aluno WHERE id_aluno = ?", (id_aluno_excluir,))
        # Recupere o resultado da consulta
        rm_alunoExc = BancoTcc.cursor.fetchone()

        # verifique se rm_alunoExc não é None antes de acessar o índice
        if rm_alunoExc is not None:
            # instrução sql que irá deletar as entradas do aluno com base no rm do aluno
            # Observe o [0] para acessar o primeiro (e único) elemento da tupla
            BancoTcc.cursor.execute("DELETE FROM entrada WHERE rm_aluno = ?", (rm_alunoExc[0],))
            BancoTcc.conn.commit()

            # instrução sql que irá deletar o aluno com base no id do aluno
            BancoTcc.cursor.execute("DELETE FROM aluno WHERE id_aluno = ?", (id_aluno_excluir,))
            BancoTcc.conn.commit()

            # mensagem que o aluno foi excluído
            resultado = "Cadastro do aluno deletado com sucesso!"  # setando uma mensagem no 'resultado'
            return resultado  # retorna a mensagem na função de deletar do sistema
        else:
            resultado = "Erro: Aluno não encontrado."  # ou outra mensagem de erro apropriada
            return resultado  # retorna a mensagem na função de deletar do sistema     


    #funcao de atualizar aluno que recebe os parametros da tela de atualizar aluno do sistema
    def atualizarAluno(self, id_aluno_atualizar, nome, rm, periodo, curso, serie_turma, face_bytes, face_alunoAtualizar, atualizar):
        #iniciando as variaveis com nenhum valor
        id_periodo , id_curso = 0, 0

        #setando o id do periodo
        if(periodo == 'Manhã'):
            id_periodo = 1    
        elif(periodo == 'Tarde'):
            id_periodo = 2       
        else:#periodo da noite
            id_periodo = 3

        #setando o id do curso
        if(curso == 'Administração'):
            id_curso = 1
        elif(curso == 'Contabilidade'):
            id_curso = 2
        elif(curso == 'Desenvolvimento de Sistemas'):
            id_curso = 3
        elif(curso == 'Logística'):
            id_curso = 4
        elif(curso == 'Recursos Humanos'):
            id_curso = 5
        else:#servicos juridicos
            id_curso = 6
        
        #consulta a tabela 'turma' para encontrar o ID da turma correspondente
        BancoTcc.cursor.execute("SELECT id_turma FROM turma WHERE id_periodo = ? AND id_curso = ? AND serie_turma = ?", (id_periodo, id_curso, serie_turma))
        dados_turma = BancoTcc.cursor.fetchone()
        #se obter o id da turma
        if dados_turma:
            id_turma = dados_turma[0]  #setando o id da turma em uma variavel
            if(atualizar == 'atualizar tudo'):
                #atualizando os dados do aluno com base no id do aluno selecionado, associando-o à turma correta
                BancoTcc.cursor.execute("UPDATE aluno SET id_turma=?, rm_aluno=?, nome_aluno=?, face_aluno=?, imagem_aluno=? WHERE id_aluno = ?", (id_turma, rm, nome, face_bytes, face_alunoAtualizar, id_aluno_atualizar))
                BancoTcc.conn.commit()
            if(atualizar == 'atualizar campos'):
                #atualizando os dados do aluno com base no id do aluno selecionado, associando-o à turma correta
                BancoTcc.cursor.execute("UPDATE aluno SET id_turma=?, rm_aluno=?, nome_aluno=? WHERE id_aluno = ?", (id_turma, rm, nome, id_aluno_atualizar))
                BancoTcc.conn.commit()
            resultado = "Dados do cadastro do aluno atualizado com sucesso!" #setando uma mensagem no 'resultado'
        #se nao obter o id da turma
        else:
            resultado = "Turma não encontrada. O aluno não foi atualizado.!" #setando uma mensagem no 'resultado'

        return resultado #retornando o 'resultado' para a tela de atualização do aluno do sistema
    
            