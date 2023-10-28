import sqlite3 

conn = sqlite3.connect('bd/ScannerRF.db')

cursor = conn.cursor()

#cursor.execute("""
#CREATE TABLE IF NOT EXISTS cadastroAlu (
 #   nome TEXT, 
  #  rm INTEGER,
   # checbox_periodo INTEGER, 
    #checkbox_curso  INTEGER,
    #checkbox_turma  INTEGER,
    #fotoAlu BLOB
#);
#""")
