import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# tela de cadastro
class CadastroScreen(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro")
        self.geometry("650x550")
        self.configure(fg_color="#001A80")
       
        frame = ctk.CTkFrame(self, width=400, height=430, fg_color="#e6e6e6", corner_radius=10)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="Cadastro", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="black").pack(pady=(30, 20))

        # nome
        ctk.CTkLabel(frame, text="Digite seu nome completo:", text_color="black", anchor="w").pack(anchor="w", padx=40)
        self.entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome", width=300, height=30, corner_radius=8)
        self.entry_nome.pack(pady=(5, 15), padx=40)

        # email
        ctk.CTkLabel(frame, text="Digite seu e-mail:", text_color="black", anchor="w").pack(anchor="w", padx=40)
        self.entry_email = ctk.CTkEntry(frame, placeholder_text="E-mail", width=300, height=30, corner_radius=8)
        self.entry_email.pack(pady=(5, 15), padx=40)

        # ra
        ctk.CTkLabel(frame, text="Digite seu RA:", text_color="black", anchor="w").pack(anchor="w", padx=40)
        self.entry_ra = ctk.CTkEntry(frame, placeholder_text="RA", width=300, height=30, corner_radius=8)
        self.entry_ra.pack(pady=(5, 15), padx=40)

        # senha
        ctk.CTkLabel(frame, text="Digite sua senha:", text_color="black", anchor="w").pack(anchor="w", padx=40)
        self.entry_senha = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=300, height=30, corner_radius=8)
        self.entry_senha.pack(padx=40)

        # mostrar/ocultar label clicável para senha 
        self.show_password = False
        self.toggle_label = ctk.CTkLabel(
            frame,
            text="Mostrar",
            text_color="blue",
            font=ctk.CTkFont(size=10, underline=True),
            cursor="hand2"
        )
        self.toggle_label.pack(anchor="e", padx=50, pady=(2, 15))  # canto inferior direito logo abaixo da senha
        self.toggle_label.bind("<Button-1>", lambda e: self.toggle_password())

        # botao para cadastrar
        ctk.CTkButton(frame, text="Cadastrar", fg_color="#34C759", hover_color="#28a745",
                      text_color="white", corner_radius=10, width=200, height=40,
                      command=self.cadastrar).pack(pady=(10, 25))

    def toggle_password(self):
        if self.show_password:
            self.entry_senha.configure(show="*")
            self.toggle_label.configure(text="Mostrar")
            self.show_password = False
        else:
            self.entry_senha.configure(show="")
            self.toggle_label.configure(text="Ocultar")
            self.show_password = True
    #define 
    def cadastrar(self):
        messagebox.showinfo("Cadastro", "Cadastro concluído.")
        self.destroy()

# tela do portal do aluno (usuario: aluno)
class PortalAluno(ctk.CTk):
    def __init__(self, nome_usuario, email_usuario):
        super().__init__()

        self.title("Portal do(a) Aluno(a)")
        self.geometry("900x550")
        self.configure(fg_color="#001A80")

        main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        main_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        title = ctk.CTkLabel(
            main_frame,
            text="Portal do(a) Aluno(a)",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#001A80",
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            main_frame,
            text=f"Bem-vindo(a), {nome_usuario}!",
            font=ctk.CTkFont(size=14),
            text_color="#444444",
        )
        subtitle.pack(pady=(0, 20))

        # botões exemplo
        btn_aulas = ctk.CTkButton(main_frame, text="Aulas", width=180, height=110, corner_radius=15, fg_color="#34C759",
                                  hover_color="#28a745", text_color="white", font=ctk.CTkFont(size=16))
        btn_notas = ctk.CTkButton(main_frame, text="Notas", width=180, height=110, corner_radius=15, fg_color="#34C759",
                                  hover_color="#28a745", text_color="white", font=ctk.CTkFont(size=16))

        btn_aulas.pack(pady=10)
        btn_notas.pack(pady=10)

        # menu lateral
        side_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#002699", width=220)
        side_frame.pack(side="right", fill="y", pady=30, padx=(0, 30))

        lbl_nome = ctk.CTkLabel(
            side_frame,
            text=nome_usuario,
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        lbl_nome.pack(pady=(40, 10), padx=10)

        lbl_email = ctk.CTkLabel(
            side_frame,
            text=email_usuario,
            text_color="white",
            font=ctk.CTkFont(size=14),
        )
        lbl_email.pack(pady=(0, 40), padx=10)

        btn_sair = ctk.CTkButton(
            side_frame,
            text="Sair",
            fg_color="#E57373",
            hover_color="#EF5350",
            width=105,
            height=15,
            corner_radius=15,
            font=ctk.CTkFont(size=15),
            command=self.sair,
        )
        btn_sair.pack(side="bottom", pady=30)
  
    def sair(self):
        self.destroy()

# tela do portal docente (usuario: docente)
class PortalDocente(ctk.CTk):
    def __init__(self, nome_usuario, email_usuario):
        super().__init__()

        self.title("Portal do Docente")
        self.geometry("900x550")
        self.configure(fg_color="#001A80")

        main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        main_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        title = ctk.CTkLabel(
            main_frame,
            text="Portal do Docente",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#001A80",
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            main_frame,
            text=f"Bem-vindo(a), Professor {nome_usuario}!",
            font=ctk.CTkFont(size=14),
            text_color="#444444",
        )
        subtitle.pack(pady=(0, 20))

        # botões exemplo
        btn_aulas = ctk.CTkButton(main_frame, text="Turmas", width=180, height=110, corner_radius=15, fg_color="#34C759",
                                  hover_color="#28a745", text_color="white", font=ctk.CTkFont(size=16))
        btn_notas = ctk.CTkButton(main_frame, text="Lançar Notas", width=180, height=110, corner_radius=15, fg_color="#34C759",
                                  hover_color="#28a745", text_color="white", font=ctk.CTkFont(size=16))

        btn_aulas.pack(pady=10)
        btn_notas.pack(pady=10)

        # menu lateral
        side_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#002699", width=220)
        side_frame.pack(side="right", fill="y", pady=30, padx=(0, 30))

        lbl_nome = ctk.CTkLabel(
            side_frame,
            text=nome_usuario,
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        lbl_nome.pack(pady=(40, 10), padx=10)

        lbl_email = ctk.CTkLabel(
            side_frame,
            text=email_usuario,
            text_color="white",
            font=ctk.CTkFont(size=14),
        )
        lbl_email.pack(pady=(0, 40), padx=10)

        btn_sair = ctk.CTkButton(
            side_frame,
            text="Sair",
            fg_color="#E57373",
            hover_color="#EF5350",
            width=105,
            height=15,
            corner_radius=15,
            font=ctk.CTkFont(size=15),
            command=self.sair,
        )
        btn_sair.pack(side="bottom", pady=30)

    def sair(self):
        self.destroy()

# tela do portal administrador (usuario: administrador)
class PortalAdm(ctk.CTk):
    def __init__(self, nome_usuario, email_usuario):
        super().__init__()

        self.title("Portal do Administrador")
        self.geometry("900x550")
        self.configure(fg_color="#001A80")

        main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        main_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        title = ctk.CTkLabel(
            main_frame,
            text="Portal do Administrador",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#001A80",
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            main_frame,
            text=f"Bem-vindo(a), {nome_usuario}!",
            font=ctk.CTkFont(size=14),
            text_color="#444444",
        )
        subtitle.pack(pady=(0, 20))

        # botões exemplo
        btn_usuarios = ctk.CTkButton(main_frame, text="Gerenciar Usuários", width=180, height=110, corner_radius=15, fg_color="#34C759",
                                  hover_color="#28a745", text_color="white", font=ctk.CTkFont(size=16))
        btn_relatorios = ctk.CTkButton(main_frame, text="Relatórios", width=180, height=110, corner_radius=15, fg_color="#34C759",
                                  hover_color="#28a745", text_color="white", font=ctk.CTkFont(size=16))

        btn_usuarios.pack(pady=10)
        btn_relatorios.pack(pady=10)

        # menu lateral
        side_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#002699", width=220)
        side_frame.pack(side="right", fill="y", pady=30, padx=(0, 30))

        lbl_nome = ctk.CTkLabel(
            side_frame,
            text=nome_usuario,
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        lbl_nome.pack(pady=(40, 10), padx=10)

        lbl_email = ctk.CTkLabel(
            side_frame,
            text=email_usuario,
            text_color="white",
            font=ctk.CTkFont(size=14),
        )
        lbl_email.pack(pady=(0, 40), padx=10)

        btn_sair = ctk.CTkButton(
            side_frame,
            text="Sair",
            fg_color="#E57373",
            hover_color="#EF5350",
            width=105,
            height=15,
            corner_radius=15,
            font=ctk.CTkFont(size=15),
            command=self.sair,
        )
        btn_sair.pack(side="bottom", pady=30)

    def sair(self):
        self.destroy()
        
# tela de login 
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("650x550")
        self.configure(fg_color="#001A80")

        self.tipo_usuario = "Aluno"  # padrão

        frame = ctk.CTkFrame(self, width=400, height=440, corner_radius=10, fg_color="#e6e6e6")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # texto "Logar como:"
        ctk.CTkLabel(frame, text="Logar como:", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="black").pack(pady=(20, 10))

        # frame botões do tipo de usuário
        tipo_frame = ctk.CTkFrame(frame, fg_color="#e6e6e6")
        tipo_frame.pack(pady=(0, 15))

        # botões dos tipos de usuário
        self.btn_aluno = ctk.CTkButton(tipo_frame, text="Aluno", width=110, corner_radius=15,
                                  fg_color="#34C759", hover_color="#28a745", text_color="white",
                                  command=lambda: self.selecionar_tipo("Aluno"))
        self.btn_docente = ctk.CTkButton(tipo_frame, text="Docente", width=110, corner_radius=15,
                                    fg_color="#34C759", hover_color="#28a745", text_color="white",
                                    command=lambda: self.selecionar_tipo("Docente"))
        self.btn_adm = ctk.CTkButton(tipo_frame, text="Administrador", width=110, corner_radius=15,
                                fg_color="#34C759", hover_color="#28a745", text_color="white",
                                command=lambda: self.selecionar_tipo("Administrador"))

        # posicionar lado a lado com espaçamento
        self.btn_aluno.grid(row=0, column=0, padx=8)
        self.btn_docente.grid(row=0, column=1, padx=8)
        self.btn_adm.grid(row=0, column=2, padx=8)

        # mensagem que mostra o tipo selecionado (visual)
        self.tipo_selecionado_label = ctk.CTkLabel(frame, text="Aluno selecionado", text_color="green")
        self.tipo_selecionado_label.pack(pady=(0, 10))

        # inicialmente seleciona aluno
        self.selecionar_tipo("Aluno")

        # email
        ctk.CTkLabel(frame, text="Digite seu e-mail:", anchor="w", text_color="black").pack(anchor="w", padx=40)
        self.email_entry = ctk.CTkEntry(frame, placeholder_text="E-mail", width=300, height=30, corner_radius=8)
        self.email_entry.pack(pady=(5, 15), padx=40)

        # senha
        ctk.CTkLabel(frame, text="Digite sua senha:", anchor="w", text_color="black").pack(anchor="w", padx=40)
        self.senha_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=300, height=30, corner_radius=8)
        self.senha_entry.pack(padx=40)

        self.show_password = False
        self.toggle_label = ctk.CTkLabel(
            frame,
            text="Mostrar",
            text_color="blue",
            font=ctk.CTkFont(size=10, underline=True),
            cursor="hand2"
        )
        self.toggle_label.pack(anchor="e", padx=50, pady=(2, 20))
        self.toggle_label.bind("<Button-1>", lambda e: self.toggle_password())

        # botão entrar
        ctk.CTkButton(frame, text="Entrar", fg_color="#34C759", hover_color="#28a745",
                      text_color="white", corner_radius=10, width=200, height=40,
                      command=self.login).pack(pady=(10, 25))

        # botão cadastrar
        ctk.CTkButton(frame, text="Cadastre-se", fg_color="#d3d3d3", text_color="black",
                      hover_color="#c0c0c0", corner_radius=10, width=120, height=30,
                      command=self.abrir_cadastro).pack(pady=(0, 20))

    def selecionar_tipo(self, tipo):
        self.tipo_usuario = tipo
        self.tipo_selecionado_label.configure(text=f"{tipo} selecionado")

        # resetar todos os botões para padrão
        for btn in [self.btn_aluno, self.btn_docente, self.btn_adm]:
            btn.configure(fg_color="#34C759", text_color="white", font=ctk.CTkFont(size=14, underline=False))

        # destaca o botão selecionado com sublinhado e cor diferente
        if tipo == "Aluno":
            self.btn_aluno.configure(fg_color="#2fa84f", text_color="white", font=ctk.CTkFont(size=14, underline=True))
        elif tipo == "Docente":
            self.btn_docente.configure(fg_color="#2fa84f", text_color="white", font=ctk.CTkFont(size=14, underline=True))
        else:
            self.btn_adm.configure(fg_color="#2fa84f", text_color="white", font=ctk.CTkFont(size=14, underline=True))

    def toggle_password(self):
        if self.show_password:
            self.senha_entry.configure(show="*")
            self.toggle_label.configure(text="Mostrar")
            self.show_password = False
        else:
            self.senha_entry.configure(show="")
            self.toggle_label.configure(text="Ocultar")
            self.show_password = True

    def login(self):
        nome_ficticio = self.tipo_usuario  # só pra teste
        email = self.email_entry.get().strip() or "email@exemplo.com"

        self.destroy()

        if self.tipo_usuario == "Aluno":
            portal = PortalAluno(nome_usuario=nome_ficticio, email_usuario=email)
        elif self.tipo_usuario == "Docente":
            portal = PortalDocente(nome_usuario=nome_ficticio, email_usuario=email)
        else:
            portal = PortalAdm(nome_usuario=nome_ficticio, email_usuario=email)

        portal.mainloop()

    def abrir_cadastro(self):
        CadastroScreen(self)

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
