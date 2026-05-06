# ------- Programa App Dramas -------

# Importar Bibliotecas
import ttkbootstrap as ttk
from database import Database
from interfaceApp import InterfaceApp

# Janela Principal
janela = ttk.Window(themename="darkly")

# Intanciar Objetos
db = Database()
db.criar_tabela()


app = InterfaceApp(janela, db)


# Carregar, Janela Mainloop
app.carregar_dados()
janela.mainloop()
