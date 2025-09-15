import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# dicionario criado para armazenar os dados usuarios cadastrados
usuarios = {}

# tela de cadastro
# def __init__ : para criar um objeto de uma classe
class CadastroScreen(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro")
        self.geometry("600x500")
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
        self.toggle_label.pack(anchor="e", padx=50, pady=(2, 15))  # no canto inferior direito logo abaixo da senha
        self.toggle_label.bind("<Button-1>", lambda e: self.toggle_password())

        # botao para cadastrar
        ctk.CTkButton(frame, text="Cadastrar", fg_color="#34C759", hover_color="#28a745",
                      text_color="white", corner_radius=10, width=200, height=40,
                      command=self.cadastrar).pack(pady=(10, 25))

    # definir função de: botão ocultar/mostrar
    def toggle_password(self):
        if self.show_password:
            self.entry_senha.configure(show="*")
            self.toggle_label.configure(text="Mostrar")
            self.show_password = False
        else:
            self.entry_senha.configure(show="")
            self.toggle_label.configure(text="Ocultar")
            self.show_password = True

    # definir função de: cadastrar o usuario e seus dados
    def cadastrar(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        ra = self.entry_ra.get().strip()
        senha = self.entry_senha.get().strip()

        if not nome or not email or not ra or not senha:
            messagebox.showwarning("Cadastro", "Por favor, preencha todos os campos.")
            return

        if email in usuarios:
            messagebox.showwarning("Cadastro", "E-mail já cadastrado.")
            return

        # salva dados do usuário na memória
        usuarios[email] = {
            "nome": nome,
            "ra": ra,
            "senha": senha
        }

        messagebox.showinfo("Cadastro", f"{nome} cadastrado com sucesso!")
        self.destroy()

# tela do portal do aluno
class PortalAluno(ctk.CTk):
    def __init__(self, nome_usuario, email_usuario):
        super().__init__()

        self.title("Portal do(a) Aluno(a)")
        self.geometry("900x550")
        self.configure(fg_color="#001A80")

        # centro
        main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="white")
        main_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        # titulo 
        title = ctk.CTkLabel(
            main_frame,
            text="Portal do(a) Aluno(a)",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#001A80",
        )
        title.pack(pady=(20, 5))

        # saudação do nome do usuario cadastrado
        subtitle = ctk.CTkLabel(
            main_frame,
            text=f"Olá, {nome_usuario}!",
            font=ctk.CTkFont(size=14),
            text_color="#444444",
        )
        subtitle.pack(pady=(0, 20))

        # frame para botões em grade
        grid_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        grid_frame.pack(expand=True)

        # estilo dos botões
        btn_opts = dict(width=180, height=110, corner_radius=15, fg_color="#34C759", hover_color="#28a745",
                        text_color="white", font=ctk.CTkFont(size=16))

        # botões em si 
        btn_aulas = ctk.CTkButton(grid_frame, text="Aulas", **btn_opts)
        btn_notas = ctk.CTkButton(grid_frame, text="Notas", **btn_opts)
        btn_faltas = ctk.CTkButton(grid_frame, text="Faltas", **btn_opts)
        btn_dados = ctk.CTkButton(grid_frame, text="Dados pessoais", **btn_opts)

        # posicionamento em 2x2 com espaçamento
        btn_aulas.grid(row=0, column=0, padx=25, pady=20)
        btn_notas.grid(row=0, column=1, padx=25, pady=20)
        btn_faltas.grid(row=1, column=0, padx=25, pady=20)
        btn_dados.grid(row=1, column=1, padx=25, pady=20)

        # menu lateral direito onde aparece os dados do usuario
        side_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#002699", width=220)
        side_frame.pack(side="right", fill="y", pady=30, padx=(0, 30))

        # botão de ajuda
        btn_help = ctk.CTkButton(
            side_frame,
            text="?",
            width=25,
            height=25,
            fg_color="#FFD700",       
            hover_color="#FFC107",    # hover: efeito que acontece quando voce passa o mouse por cima do botao
            text_color="#001A80",     # "?"
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=15,
            command=None              # ---
        )
        btn_help.place(relx=1, rely=0, anchor="ne", x=-10, y=10)

        # nome do usuário (com padding - espaço interno entre o conteudo e a borda da caixa - para não ficar grudado na parede)
        lbl_nome = ctk.CTkLabel(
            side_frame,
            text=nome_usuario,
            text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        lbl_nome.pack(pady=(40, 10), padx=10)

        # email do usuário (com padding - espaço interno entre o conteudo e a borda da caixa - para não ficar grudado na parede)
        lbl_email = ctk.CTkLabel(
            side_frame,
            text=email_usuario,
            text_color="white",
            font=ctk.CTkFont(size=14),
        )
        lbl_email.pack(pady=(0, 40), padx=10)

        # botão sair 
        btn_sair = ctk.CTkButton(
            side_frame,
            text="Sair",
            fg_color="#E57373",  
            hover_color="#EF5350", # hover: efeito que acontece quando voce passa o mouse por cima do botao
            width=140,
            height=40,
            corner_radius=15,
            font=ctk.CTkFont(size=16),
            command=self.sair,
        )
        btn_sair.pack(side="bottom", pady=30)
  
    # definir função de: sair / deslogar
    def sair(self):
        self.destroy()

# tela de Login
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("600x500")
        self.configure(fg_color="#001A80")

        # frame central
        frame = ctk.CTkFrame(self, width=400, height=400, corner_radius=10, fg_color="#e6e6e6")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # título
        ctk.CTkLabel(frame, text="Área do(a) Aluno(a)", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="black").pack(pady=(30, 20))

        # campo email
        ctk.CTkLabel(frame, text="Digite seu e-mail:", anchor="w", text_color="black").pack(anchor="w", padx=40)
        
        # entry do email
        self.email_entry = ctk.CTkEntry(frame, placeholder_text="E-mail", width=300, height=30, corner_radius=8)
        self.email_entry.pack(pady=(5, 15), padx=40)

        # campo senha
        ctk.CTkLabel(frame, text="Digite sua senha:", anchor="w", text_color="black").pack(anchor="w", padx=40)

        # entry da senha
        self.senha_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=300, height=30, corner_radius=8)
        self.senha_entry.pack(padx=40)

        # botao de mostrar/ocultar label clicável na senha
        self.show_password = False
        self.toggle_label = ctk.CTkLabel(
            frame,
            text="Mostrar",
            text_color="blue",
            font=ctk.CTkFont(size=10, underline=True),
            cursor="hand2"
        )
        self.toggle_label.pack(anchor="e", padx=50, pady=(2, 20))  # canto inferior direito do entry da senha
        self.toggle_label.bind("<Button-1>", lambda e: self.toggle_password())

        # botão entrar
        ctk.CTkButton(frame, text="Entrar", fg_color="#34C759", hover_color="#28a745",
                      text_color="white", corner_radius=10, width=200, height=40,
                      command=self.login).pack(pady=(10, 25))

        # label e botão de cadastro
        ctk.CTkLabel(frame, text="Não é aluno?", text_color="black").pack(pady=(0, 5))
        ctk.CTkButton(frame, text="Cadastre-se", fg_color="#d3d3d3", text_color="black",
                      hover_color="#c0c0c0", corner_radius=10, width=120, height=30,
                      command=self.abrir_cadastro).pack(pady=(0, 20))

    def toggle_password(self):
        if self.show_password:
            self.senha_entry.configure(show="*")
            self.toggle_label.configure(text="Mostrar")
            self.show_password = False
        else:
            self.senha_entry.configure(show="")
            self.toggle_label.configure(text="Ocultar")
            self.show_password = True

    # definir função de: logar o usuario
    def login(self):
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not email or not senha:
            messagebox.showwarning("Login", "Por favor, preencha e-mail e senha.")
            return

        if email not in usuarios or usuarios[email]["senha"] != senha:
            messagebox.showerror("Login", "E-mail ou senha incorretos.")
            return

        nome_usuario = usuarios[email]["nome"]
        self.destroy()
        portal = PortalAluno(nome_usuario=nome_usuario, email_usuario=email)
        portal.mainloop()

    # definir função de: abrir a tela de usuario
    def abrir_cadastro(self):
        CadastroScreen(self)

# só roda o programa se este arquivo for o principal, abrindo a janela de login para o usuário interagir
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
