# Interface e Lógica do DramApp

# Importar Bibliotecas
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import * 
from tkinter import messagebox
from database import Database

# Criar Classe
class InterfaceApp:

    def __init__(self, janela, database):
        self.janela = janela
        self.database = database

        self.configurar_janela()
        self.criar_interface()

    def configurar_janela(self):
        self.janela.title("DramApp")
        self.janela.geometry("600x400")

    def criar_interface(self):
        self.titulo = ttk.Label(
            self.janela,
            text="DramApp",
            font=("Segoe UI", 20, "bold")
        )
        self.titulo.pack(pady=10)

        self.notebook = ttk.Notebook(self.janela )
        self.notebook.pack(expand=True, fill="both")
        
        self.aba_cadastro = ttk.Frame(self.notebook)
        self.aba_assistidos = ttk.Frame(self.notebook)
        self.aba_quero = ttk.Frame(self.notebook)
        self.aba_recomendo = ttk.Frame(self.notebook)

        self.notebook.add(self.aba_cadastro, text="Cadastro")
        self.notebook.add(self.aba_assistidos, text="Assistidos")
        self.notebook.add(self.aba_quero, text="Quero Assistir")
        self.notebook.add(self.aba_recomendo, text="Recomendados")
        
        self.aba_cadastro.columnconfigure(1, weight=1)

        self.criar_formulario()
        self.criar_botoes()
        self.criar_treeviews()
        

    def criar_campo(self, texto, linha, variavel=None):
        label = ttk.Label(self.aba_cadastro, text=texto)
        label.grid(row=linha, column=0, padx=10, pady=10, sticky="w")
        
        entry = ttk.Entry(self.aba_cadastro, textvariable=variavel)
        entry.grid(row=linha, column=1, padx=10, pady=5, sticky="we")
        return entry
    
    def criar_radio_grupo(self, texto, linha, opcoes, variavel):

        label = ttk.Label(self.aba_cadastro, text=texto)
        label.grid(row=linha, column=0, padx=10, pady=10, sticky="w")

        frame = ttk.Frame(self.aba_cadastro)
        frame.grid(row=linha, column=1, padx=10, pady=5, sticky="w")

        radios = []
        for opcao in opcoes:
            if variavel is self.status_var:
                radio = ttk.Radiobutton(
                frame,
                text=opcao,
                variable=variavel,
                value=opcao,
                command=self.atualizar_recomendacao
            )
            else:
                radio = ttk.Radiobutton(
                frame,
                text=opcao,
                variable=variavel,
                value=opcao
            )
            radios.append(radio)
            radio.pack(side="left", padx=5)
        return label, radios      

    def criar_formulario(self):

        self.entry_nome = self.criar_campo("Nome do Drama:", 0)
        self.entry_stream = self.criar_campo("Streaming:", 1)
        self.entry_nota = self.criar_campo("Nota:", 2)
        
        self.status_var = tk.StringVar(value="Assistidos")
        self.criar_radio_grupo("Status:", 3,["Assistidos", "Quero Assistir"], self.status_var)

        self.recomendo_var = tk.StringVar(value="SIM")
        self.recomendo_label, self.recomendo_radios = self.criar_radio_grupo("Recomendo:", 4, ["SIM", "NÃO"], self.recomendo_var)
        self.atualizar_recomendacao()

    def criar_botoes(self):

        frame_btn = tk.Frame(self.aba_cadastro)
        frame_btn.grid(row=5, column=1, padx=10, pady=5)

        btn_salvar = ttk.Button(frame_btn, text="Salvar", command=self.salvar_dados, bootstyle=SUCCESS)
        btn_salvar.grid(row=0, column=0, padx=5)

        btn_deletar = ttk.Button(frame_btn, text="Deletar", command=self.deletar_dados, bootstyle=SUCCESS)
        btn_deletar.grid(row=0, column=1, padx=5)

    def criar_treeview(self, aba):
        aba_frame = tk.Frame(aba)
        aba_frame.pack(fill="both", expand=True)

        colunas = ("id", "Nome", "Streaming", "Nota", "Status", "Recomendo")
        tree = ttk.Treeview(
            aba_frame,
            columns=colunas,
            show="headings")
        
        for coluna in colunas:
            tree.heading(coluna, text=coluna)
            tree.column(coluna, width=120)

        tree.column("Nome", width=200)
        tree.column("Streaming", width=100)
        tree.column("Nota", width=40)

        tree.column("id", width=0, stretch=False)

        tree.pack(fill="both", expand=True)
        return tree
    
    def criar_treeviews(self):
        self.assistidos_tree = self.criar_treeview(self.aba_assistidos)
        self.quero_tree = self.criar_treeview(self.aba_quero)
        self.recomendo_tree = self.criar_treeview(self.aba_recomendo)
        self.assistidos_tree.bind("<Double-1>", self.mostrar_comentario)

    def atualizar_recomendacao(self):
        if self.status_var.get() == "Quero Assistir":
            self.recomendo_label.grid_remove()
            for radio in self.recomendo_radios:
                radio.pack_forget()
        else:
            self.recomendo_label.grid()
            for radio in self.recomendo_radios:
                radio.pack(side="left", padx=5)

    def limpar_dados(self):
        tabelas = [self.assistidos_tree, self.quero_tree, self.recomendo_tree]
        for tree in tabelas:
            for linha in tree.get_children():
                tree.delete(linha)
                
    def salvar_dados(self):
        nome = self.entry_nome.get()
        streaming = self.entry_stream.get()
        nota = self.entry_nota.get()
        status = self.status_var.get()
        recomendo = self.recomendo_var.get()
       
        if status == "Quero Assistir":
            recomendo = ""
        
        if not nome or not streaming or not nota:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return
        try:
            nota = float(nota)
        except ValueError:
            messagebox.showerror("Erro", "A nota deve ser um número válido.")
            return
        
        self.database.inserir(nome, streaming, nota, status, recomendo, "")
        self.carregar_dados()

        messagebox.showinfo("Sucesso", "Drama salvo com sucesso.")

        self.entry_nome.delete(0, tk.END)
        self.entry_stream.delete(0, tk.END)
        self.entry_nota.delete(0, tk.END)
        self.status_var.set("Assistidos")
        self.recomendo_var.set("SIM")

        self.atualizar_recomendacao()
    

    def deletar_dados(self):
        tree_atual = None
        tabelas = [self.assistidos_tree, 
                   self.quero_tree, 
                   self.recomendo_tree
                   ]
        
        for tree in tabelas:
            if tree.selection():
                tree_atual = tree
                break

        else:
            messagebox.showwarning("Aviso", "Selecione um drama para deletar.")
            return
        
        selecionado = tree_atual.selection()[0]
        item = tree_atual.item(selecionado)
        valores = item["values"]

        id_drama = valores[0]
        self.database.deletar(id_drama)
        self.carregar_dados()

        messagebox.showinfo("Sucesso", "Drama deletado com sucesso.")

    def carregar_dados(self):

        self.limpar_dados()
        dados = self.database.listar()

        for item_id, nome, streaming, nota, status, recomendo, comentario in dados:
    
            valores = (item_id, nome, streaming, nota, status, recomendo)
            
            if status == "Assistidos":
                self.assistidos_tree.insert("", "end", values=valores)

                if recomendo == "SIM":
                    self.recomendo_tree.insert("", "end", values=valores)

            elif status == "Quero Assistir":
                self.quero_tree.insert("", "end", values=valores)
    
    def mostrar_comentario(self, event):
        selecionado = self.assistidos_tree.selection()

        if not selecionado:
            return
        
        item = self.assistidos_tree.item(selecionado[0])
        valores = item["values"]

        id_drama = valores[0]

        comentario = self.database.buscar_comentario(id_drama)

        self.abrir_popup(comentario, id_drama)

    def abrir_popup(self, comentario, id_drama):

        janela = tk.Toplevel(self.janela)
        janela.title("Comentário")
        janela.geometry("350x250")

        label = ttk.Label(janela, text="Comentário:")
        label.pack(pady=5)

        texto = tk.Text(janela, height=8, width=40)
        texto.pack(padx=10, pady=5)

        if comentario:
            texto.insert("1.0", comentario)

        def salvar():
            novo_comentario = texto.get("1.0", tk.END).strip()
            self.database.atualizar(id_drama, comentario=novo_comentario)
            messagebox.showinfo("Sucesso", "Comentário Salvo.")
            janela.destroy()

        btn_salvar = ttk.Button(janela, text="Salvar", command=salvar, bootstyle=SUCCESS)
        btn_salvar.pack(pady=10)
