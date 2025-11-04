import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import controllers

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# classe base (estrutura padrão dos portais)
class BasePortal(ctk.CTk):
    def __init__(self, nome_usuario, email_usuario, titulo, subtitulo):
        super().__init__()
        self.title(titulo)
        self.geometry("900x550")
        self.configure(fg_color="#001A80")

        # frame principal (onde ficam os botões e textos)
        main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        main_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        self.main_frame = main_frame

        # título e subtítulo
        ctk.CTkLabel(main_frame, text=titulo,
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#001A80").pack(pady=(20, 5))
        ctk.CTkLabel(main_frame, text=subtitulo,
                     font=ctk.CTkFont(size=14),
                     text_color="#444444").pack(pady=(0, 20))

        # menu lateral (com nome, e-mail e botão sair)
        side_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#002699", width=220)
        side_frame.pack(side="right", fill="y", pady=30, padx=(0, 30))

        ctk.CTkLabel(side_frame, text=nome_usuario,
                     text_color="white",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(40, 10), padx=10)
        ctk.CTkLabel(side_frame, text=email_usuario,
                     text_color="white",
                     font=ctk.CTkFont(size=14)).pack(pady=(0, 40), padx=10)

        # botão sair (fecha o portal)
        ctk.CTkButton(side_frame, text="Sair", fg_color="#E57373", hover_color="#EF5350",
                      width=105, height=15, corner_radius=15,
                      font=ctk.CTkFont(size=15),
                      command=self.sair).pack(side="bottom", pady=30)
        
    # confirmar saída
    def sair(self):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja sair?"):
            self.destroy()


# tela de cadastro (nova janela)
class CadastroScreen(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro")
        self.geometry("650x550")
        self.configure(fg_color="#001A80")

        # frame central (onde ficam os campos e botões)
        frame = ctk.CTkFrame(self, width=400, height=430, fg_color="#e6e6e6", corner_radius=10)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Cadastro", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="black").pack(pady=(30, 20))

        # campos de entrada (nome, email, ra, senha)
        self.entry_nome = self._criar_campo(frame, "Digite seu nome completo:", "Nome")
        self.entry_email = self._criar_campo(frame, "Digite seu e-mail:", "E-mail")
        self.entry_ra = self._criar_campo(frame, "Digite seu RA:", "RA")
        self.entry_senha = self._criar_campo(frame, "Digite sua senha:", "Senha", senha=True)

        # mostrar/ocultar senha
        self.show_password = False
        self.toggle_label = ctk.CTkLabel(frame, text="Mostrar", text_color="blue",
                                         font=ctk.CTkFont(size=10, underline=True),
                                         cursor="hand2")
        self.toggle_label.pack(anchor="e", padx=50, pady=(2, 15))
        self.toggle_label.bind("<Button-1>", lambda e: self.toggle_password())

        # botão cadastrar (salva as informações)
        ctk.CTkButton(frame, text="Cadastrar", fg_color="#34C759", hover_color="#28a745",
                      text_color="white", corner_radius=10, width=200, height=40,
                      command=self.cadastrar).pack(pady=(10, 25))

    # função pra criar cada campo de texto
    def _criar_campo(self, parent, label, placeholder, senha=False):
        ctk.CTkLabel(parent, text=label, text_color="black", anchor="w").pack(anchor="w", padx=40)
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=300, height=30, corner_radius=8,
                             show="*" if senha else "")
        entry.pack(pady=(5, 15), padx=40)
        return entry

    # mostrar/ocultar senha
    def toggle_password(self):
        if self.show_password:
            self.entry_senha.configure(show="*")
            self.toggle_label.configure(text="Mostrar")
        else:
            self.entry_senha.configure(show="")
            self.toggle_label.configure(text="Ocultar")
        self.show_password = not self.show_password
        
    # validação dos campos e mensagem
    def cadastrar(self):

        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        ra = self.entry_ra.get().strip()
        senha = self.entry_senha.get().strip()

        if not nome or not email or not ra or not senha:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")
            return

        messagebox.showinfo("Cadastro", f"Cadastro do aluno '{nome}' realizado com sucesso!")
        self.destroy()


# portal do aluno (estudante)
class PortalAluno(BasePortal):
    def __init__(self, nome_usuario, email_usuario):
        super().__init__(nome_usuario, email_usuario,
                         "Portal do(a) Aluno(a)",
                         f"Bem-vindo(a), Estudante!")

        # botões principais do aluno
        ctk.CTkButton(self.main_frame, text="Aulas", width=180, height=110,
                      corner_radius=15, fg_color="#34C759",
                      hover_color="#28a745", text_color="white",
                      font=ctk.CTkFont(size=16)).pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Notas", width=180, height=110,
                      corner_radius=15, fg_color="#34C759",
                      hover_color="#28a745", text_color="white",
                      font=ctk.CTkFont(size=16)).pack(pady=10)
        
        chatbot_btn = ctk.CTkButton(self.main_frame, text="🤖", width=50, height=50,
                             corner_radius=25, fg_color="#287DFD",
                             hover_color="#231FE6", text_color="white",
                             font=ctk.CTkFont(size=20))
        chatbot_btn.place(relx=0.95, rely=0.95, anchor="se")
        


# portal do docente (professor)
class PortalDocente(BasePortal):
    def __init__(self, nome_usuario, email_usuario):
        super().__init__(nome_usuario, email_usuario,
                         "Portal do Docente",
                         f"Bem-vindo(a), Professor!")

        # botão pra abrir gerenciador de atividades
        ctk.CTkButton(self.main_frame, text="Gerenciar Atividades", width=180, height=110,
                      corner_radius=15, fg_color="#34C759",
                      hover_color="#28a745", text_color="white",
                      font=ctk.CTkFont(size=16),
                      command=self.abrir_gerenciar_atividades).pack(pady=10)

    # abre nova janela pra gerenciar atividades
    def abrir_gerenciar_atividades(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Gerenciar Atividades")
        janela.geometry("750x450")
        janela.configure(fg_color="white")

        ctk.CTkLabel(janela, text="Lista de Atividades",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#001A80").pack(pady=10)

        # frame que mostra as atividades do banco
        self.frame_lista = ctk.CTkScrollableFrame(janela, width=700, height=280, fg_color="#f2f2f2")
        self.frame_lista.pack(pady=10)

        self._cabecalho_lista()
        self._carregar_atividades()

        # botões criar e excluir
        frame_botoes = ctk.CTkFrame(janela, fg_color="white")
        frame_botoes.pack(pady=10)

        ctk.CTkButton(frame_botoes, text="Criar Atividade", fg_color="#34C759",
                      hover_color="#28a745", command=self.criar_atividade_popup).grid(row=0, column=0, padx=10)

        ctk.CTkButton(frame_botoes, text="Excluir Atividade", fg_color="#E57373",
                      hover_color="#EF5350", command=self.excluir_atividade_popup).grid(row=0, column=1, padx=10)

    # cabeçalho da tabela de atividades
    def _cabecalho_lista(self):
        ctk.CTkLabel(self.frame_lista, text="Título", width=200, anchor="w").grid(row=0, column=0, padx=10)
        ctk.CTkLabel(self.frame_lista, text="Descrição", width=300, anchor="w").grid(row=0, column=1, padx=10)
        ctk.CTkLabel(self.frame_lista, text="Data de Entrega", width=150, anchor="w").grid(row=0, column=2, padx=10)

    # carrega atividades do banco de dados
    def _carregar_atividades(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        self._cabecalho_lista()

        conn = sqlite3.connect("database.db")
        db = conn.cursor()
        atividades = controllers.listar_atividades(db)
        conn.close()

        for i, a in enumerate(atividades, start=1):
            ctk.CTkLabel(self.frame_lista, text=a['titulo'], anchor="w").grid(row=i, column=0, sticky="w", padx=10)
            ctk.CTkLabel(self.frame_lista, text=a['descricao'], anchor="w").grid(row=i, column=1, sticky="w", padx=10)
            ctk.CTkLabel(self.frame_lista, text=a['data_entrega'], anchor="w").grid(row=i, column=2, sticky="w", padx=10)

    # popup - criar nova atividade
    def criar_atividade_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Criar Atividade")
        popup.geometry("500x400")
        popup.configure(fg_color="white")

        campos = {}
        for label in ["Título", "Descrição", "Data de Entrega (AAAA-MM-DD)", "Link (opcional)"]:
            ctk.CTkLabel(popup, text=label).pack(pady=5)
            campos[label] = ctk.CTkEntry(popup, width=300)
            campos[label].pack(pady=5)

        # botão salvar (grava no banco)
        def salvar():
            titulo = campos["Título"].get()
            descricao = campos["Descrição"].get()
            data = campos["Data de Entrega (AAAA-MM-DD)"].get()
            link = campos["Link (opcional)"].get() or None

            conn = sqlite3.connect("database.db")
            db = conn.cursor()
            sucesso = controllers.criar_atividade(db, titulo, descricao, data, link)
            conn.commit()
            conn.close()

            if sucesso:
                messagebox.showinfo("Sucesso", f"Atividade '{titulo}' criada com sucesso!")
                popup.destroy()
                self._carregar_atividades()
            else:
                messagebox.showerror("Erro", "Erro ao criar atividade. Verifique os dados.")

        ctk.CTkButton(popup, text="Salvar", fg_color="#34C759", command=salvar).pack(pady=10)

    # popup - excluir atividade
    def excluir_atividade_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Excluir Atividade")
        popup.geometry("400x150")
        popup.configure(fg_color="white")

        ctk.CTkLabel(popup, text="Título da Atividade a excluir:").pack(pady=10)
        entry = ctk.CTkEntry(popup, width=300)
        entry.pack(pady=5)

        def excluir():
            titulo = entry.get()
            conn = sqlite3.connect("database.db")
            db = conn.cursor()
            sucesso = controllers.excluir_atividade(db, titulo)
            conn.commit()
            conn.close()

            if sucesso:
                messagebox.showinfo("Sucesso", f"Atividade '{titulo}' excluída com sucesso!")
                popup.destroy()
                self._carregar_atividades()
            else:
                messagebox.showerror("Erro", "Erro ao excluir atividade. Verifique o título.")

        ctk.CTkButton(popup, text="Excluir", fg_color="#E57373", command=excluir).pack(pady=10)


# portal administrativo (Administrador)
class PortalAdm(BasePortal):
    def __init__(self, nome_usuario, email_usuario):
        super().__init__(nome_usuario, email_usuario,
                         "Portal Administrativo",
                         f"Bem-vindo(a), Administrador!")

        # botões do painel adm
        ctk.CTkButton(self.main_frame, text="Gerenciar Usuários", width=180, height=110,
                      corner_radius=15, fg_color="#34C759",
                      hover_color="#28a745", text_color="white",
                      font=ctk.CTkFont(size=16)).pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Relatórios", width=180, height=110,
                      corner_radius=15, fg_color="#34C759",
                      hover_color="#28a745", text_color="white",
                      font=ctk.CTkFont(size=16)).pack(pady=10)


# tela de login (primeira tela)
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("650x550")
        self.configure(fg_color="#001A80")

        self.tipo_usuario = "Aluno"

        # frame central (formulário de login)
        frame = ctk.CTkFrame(self, width=400, height=440, corner_radius=10, fg_color="#e6e6e6")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Logar como:", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="black").pack(pady=(20, 10))

        # botões de seleção do tipo de usuário
        tipo_frame = ctk.CTkFrame(frame, fg_color="#e6e6e6")
        tipo_frame.pack(pady=(0, 15))

        self.btns = {}
        for tipo in ["Aluno", "Docente", "Administrador"]:
            btn = ctk.CTkButton(tipo_frame, text=tipo, width=110, corner_radius=15,
                                fg_color="#34C759", hover_color="#28a745", text_color="white",
                                command=lambda t=tipo: self.selecionar_tipo(t))
            btn.grid(row=0, column=len(self.btns), padx=8)
            self.btns[tipo] = btn

        self.tipo_label = ctk.CTkLabel(frame, text="Aluno selecionado", text_color="green")
        self.tipo_label.pack(pady=(0, 10))
        self.selecionar_tipo("Aluno")

        # campos de login (email e senha)
        ctk.CTkLabel(frame, text="Digite seu e-mail:", anchor="w", text_color="black").pack(anchor="w", padx=40)
        self.email_entry = ctk.CTkEntry(frame, placeholder_text="E-mail", width=300, height=30)
        self.email_entry.pack(pady=(5, 15), padx=40)

        ctk.CTkLabel(frame, text="Digite sua senha:", anchor="w", text_color="black").pack(anchor="w", padx=40)
        self.senha_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=300, height=30)
        self.senha_entry.pack(padx=40)

        # mostrar/ocultar senha
        self.show_password = False
        toggle = ctk.CTkLabel(frame, text="Mostrar", text_color="blue",
                              font=ctk.CTkFont(size=10, underline=True),
                              cursor="hand2")
        toggle.pack(anchor="e", padx=50, pady=(2, 20))
        toggle.bind("<Button-1>", lambda e: self.toggle_password(toggle))

        # botão entrar
        ctk.CTkButton(frame, text="Entrar", fg_color="#34C759", hover_color="#28a745",
                      text_color="white", corner_radius=10, width=200, height=40,
                      command=self.login).pack(pady=(10, 25))

        # botão cadastrar
        ctk.CTkButton(frame, text="Cadastre-se", fg_color="#d3d3d3", text_color="black",
                      hover_color="#c0c0c0", corner_radius=10, width=120, height=30,
                      command=self.abrir_cadastro).pack(pady=(0, 20))

    # muda o tipo de usuário selecionado
    def selecionar_tipo(self, tipo):
        self.tipo_usuario = tipo
        self.tipo_label.configure(text=f"{tipo} selecionado")
        for t, btn in self.btns.items():
            cor = "#2fa84f" if t == tipo else "#34C759"
            sub = True if t == tipo else False
            btn.configure(fg_color=cor, text_color="white", font=ctk.CTkFont(size=14, underline=sub))

    # mostrar/ocultar senha
    def toggle_password(self, toggle_label):
        if self.show_password:
            self.senha_entry.configure(show="*")
            toggle_label.configure(text="Mostrar")
        else:
            self.senha_entry.configure(show="")
            toggle_label.configure(text="Ocultar")
        self.show_password = not self.show_password

    # faz o login e abre o portal correspondente
    def login(self):
        nome = self.tipo_usuario
        email = self.email_entry.get().strip() or "email@exemplo.com"
        self.destroy()

        if self.tipo_usuario == "Aluno":
            portal = PortalAluno(nome_usuario=nome, email_usuario=email)
        elif self.tipo_usuario == "Docente":
            portal = PortalDocente(nome_usuario=nome, email_usuario=email)
        else:
            portal = PortalAdm(nome_usuario=nome, email_usuario=email)
        portal.mainloop()

    # abre a janela de cadastro
    def abrir_cadastro(self):
        CadastroScreen(self)


# main (ponto de partida do sistema)
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
