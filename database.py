# --- App Dramas ---

# database do prjeto

# Importar Biblioteca
import sqlite3

# Criar a Classe 
class Database:
    def __init__(self, nome = 'Dramapp.db'):
        self.nome = nome

    def connect(self):
        return sqlite3.connect(self.nome)
    
    def executar_query(self, query, parametros=(), fetch=False):
        conn = self.connect()
        cursor = conn.cursor()
        resultado = None

        try:
            cursor.execute(query, parametros)
            if fetch:
                resultado = cursor.fetchall()
            else:
                conn.commit()
        except sqlite3.Error as e:
            print("Erro no Banco:", e)
        finally:
            conn.close()
        
        return resultado
           

    def criar_tabela(self):
        query = """
                    CREATE TABLE IF NOT EXISTS lista_dramas
                    (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    streaming TEXT,
                    nota REAL,
                    status TEXT,
                    recomendo TEXT,
                    comentario TEXT
                    )
        """
        self.executar_query(query)


    def inserir(self, nome, streaming, nota, status, recomendo, comentario):
        query = """
                       INSERT INTO lista_dramas (nome, streaming, nota, status, recomendo, comentario)  VALUES (?, ?, ?, ?, ?, ?)
        """        

        self.executar_query(query, (nome, streaming, nota, status, recomendo, comentario))


    def listar(self):
        query = "SELECT id, nome, streaming, nota, status, recomendo, comentario FROM lista_dramas"
        return self.executar_query(query, fetch=True)
    
    
    def atualizar(self, id_drama, nome=None, streaming=None, nota=None, status=None, recomendo=None, comentario=None):
        campos = []
        parametros = []

        for chave, valor in {"nome": nome, 
                             "streaming": streaming, 
                             "nota": nota, 
                             "status": status, 
                             "recomendo": recomendo, 
                             "comentario": comentario
                             }.items():
            
            if valor is not None:
                campos.append(f"{chave} = ?")
                parametros.append(valor)
        
        if not campos:
            return
        
        query = f"UPDATE lista_dramas SET {', '.join(campos)} WHERE id = ?"
        parametros.append(id_drama)

        self.executar_query(query, tuple(parametros))


    def deletar(self, id_drama):
        query = "DELETE FROM lista_dramas WHERE id = ?"
        self.executar_query(query, (id_drama,))

    def buscar_comentario(self, id_drama):
        query = "SELECT comentario From lista_dramas WHERE id = ?"

        resultado = self.executar_query(query, (id_drama,), fetch=True)

        if resultado:
            return resultado[0][0]
        else:
            return ""