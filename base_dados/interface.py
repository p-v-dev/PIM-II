import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import controllers
from chatbot_interface import processar_mensagem_chatbot, apresentacao


conn = sqlite3.connect("database.db")
db = conn.cursor()
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
        
        ctk.CTkButton(self.main_frame, text="Atividades", width=180, height=110,
                      corner_radius=15, fg_color="#34C759",
                      hover_color="#28a745", text_color="white",
                      font=ctk.CTkFont(size=16), 
                      command = self.listar_atividades).pack(pady=10)

        # botão do chatbot
        chatbot_btn = ctk.CTkButton(
            self.main_frame, text="🤖", width=50, height=50,
            corner_radius=25, fg_color="#287DFD",
            hover_color="#231FE6", text_color="white",
            font=ctk.CTkFont(size=20),
            command=self.abrir_chatbot  # abre o chat
        )
        chatbot_btn.place(relx=0.95, rely=0.95, anchor="se")

    def listar_atividades(self):
            janela = ctk.CTkToplevel(self)
            janela.title("Minhas Atividades")
            janela.geometry("800x500")
            janela.configure(fg_color="white")

            janela.transient(self) 
            janela.grab_set()      
            janela.focus_force()

            ctk.CTkLabel(janela, text="Minhas Atividades",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#001A80").pack(pady=15)
            frame_lista = ctk.CTkScrollableFrame(janela, width=750, height=350, fg_color="#f2f2f2")
            frame_lista.pack(pady=10)

            atividades = controllers.listar_atividades(db)

            ctk.CTkLabel(frame_lista, text="Título", width=200, anchor="w", 
                    font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5)
            
            ctk.CTkLabel(frame_lista, text="Descrição", width=300, anchor="w",
                    font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=5)
            
            ctk.CTkLabel(frame_lista, text="Data de Entrega", width=150, anchor="w",
                    font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=10, pady=5)
            
            ctk.CTkLabel(frame_lista, text="Link", width=100, anchor="w",
                    font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=10, pady=5)

            
            for i, atividade in enumerate(atividades, start=1):
                ctk.CTkLabel(frame_lista, text=atividade['titulo'], anchor="w").grid(
                    row=i, column=0, sticky="w", padx=10, pady=3)
                ctk.CTkLabel(frame_lista, text=atividade['descricao'], anchor="w").grid(
                    row=i, column=1, sticky="w", padx=10, pady=3)
                ctk.CTkLabel(frame_lista, text=atividade['data_entrega'], anchor="w").grid(
                    row=i, column=2, sticky="w", padx=10, pady=3)
                
            link_text = atividade['link'] if atividade['link'] else "Sem link"
            ctk.CTkLabel(frame_lista, text=link_text, anchor="w").grid(
                row=i, column=3, sticky="w", padx=10, pady=3)

# aplicação do chatbot ================================================
        
# portal do docente (professor)        
class PortalDocente(BasePortal):
    def __init__(self, nome_usuario, email_usuario):
        super().__init__(nome_usuario, email_usuario,
                         "Portal do Docente",
                         f"Bem-vindo(a), Professor!")

        # frame interno para organizar os botões (3 colunas)
        botoes_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=0)
        botoes_frame.pack(pady=10)

        botoes = [
            ("Gerenciar Atividades", self.abrir_gerenciar_atividades),
            ("Listar Alunos", self.abrir_listar_alunos),
            ("Dar Nota", self.dar_nota_popup),
            ("Dar Falta", self.dar_falta_popup),
            ("Consultar Notas", self.consultar_notas_popup)
        ]

        cols = 3  # número de colunas na grade
        for i, (texto, func) in enumerate(botoes):
            btn = ctk.CTkButton(
                botoes_frame,
                text=texto,
                width=180,
                height=110,
                corner_radius=15,
                fg_color="#34C759",
                hover_color="#28a745",
                text_color="white",
                font=ctk.CTkFont(size=16),
                command=func
            )
            btn.grid(row=i//cols, column=i%cols, padx=15, pady=15)


    def abrir_listar_alunos(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Lista de Alunos")
        janela.geometry("850x500")
        janela.configure(fg_color="white")

        ctk.CTkLabel(janela, text="Alunos Cadastrados",
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color="#001A80").pack(pady=10)

        # frame com a lista
        self.frame_lista_alunos = ctk.CTkScrollableFrame(
            janela, width=820, height=350, fg_color="#f2f2f2"
        )
        self.frame_lista_alunos.pack(pady=10)

        self._carregar_alunos()
 
    def _cabecalho_alunos(self):
        ctk.CTkLabel(self.frame_lista_alunos, text="Nome", width=200, anchor="w").grid(row=0, column=0, padx=10)
        ctk.CTkLabel(self.frame_lista_alunos, text="Matrícula", width=120, anchor="w").grid(row=0, column=1, padx=10)
        ctk.CTkLabel(self.frame_lista_alunos, text="Turma", width=80, anchor="w").grid(row=0, column=2, padx=10)
        ctk.CTkLabel(self.frame_lista_alunos, text="E-mail", width=250, anchor="w").grid(row=0, column=3, padx=10)
        
    def _carregar_alunos(self):
        for widget in self.frame_lista_alunos.winfo_children():
            widget.destroy()

        self._cabecalho_alunos()
        alunos = controllers.listar_alunos(db)


        if not alunos:
            ctk.CTkLabel(
                self.frame_lista_alunos,
                text="Nenhum aluno encontrado.",
                text_color="red"
            ).grid(row=1, column=0, padx=10, pady=10)
            return

        for i, aluno in enumerate(alunos, start=1):
            nome_completo = f"{aluno['nome']} {aluno['sobrenome']}"

            ctk.CTkLabel(self.frame_lista_alunos, text=nome_completo, anchor="w").grid(row=i, column=0, sticky="w", padx=10)
            ctk.CTkLabel(self.frame_lista_alunos, text=aluno['matricula'], anchor="w").grid(row=i, column=1, sticky="w", padx=10)
            ctk.CTkLabel(self.frame_lista_alunos, text=aluno['turma'], anchor="w").grid(row=i, column=2, sticky="w", padx=10)
            ctk.CTkLabel(self.frame_lista_alunos, text=aluno['email'], anchor="w").grid(row=i, column=3, sticky="w", padx=10)

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

        self._carregar_atividades()  # já chama o cabeçalho dentro da função

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

        atividades = controllers.listar_atividades(db)
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

       # USE CRIAR ATIVIDADE DO CONTROLLERS.PY
        #+++++++++++++++++++++++++++++++++++++++++++++
    # popup - excluir atividade
    def excluir_atividade_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Excluir Atividade")
        popup.geometry("400x150")
        popup.configure(fg_color="white")

        ctk.CTkLabel(popup, text="Título da Atividade a excluir:").pack(pady=10)
        entry = ctk.CTkEntry(popup, width=300)
        entry.pack(pady=5)

        # USE excluir atividade NOTA DO CONTROLLERS.PY
        #+++++++++++++++++++++++++++++++++++++++++++++

    # popup - dar nota ao aluno
    def dar_nota_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Lançar Nota")
        popup.geometry("450x400")
        popup.configure(fg_color="white")

        # MATRÍCULA
        ctk.CTkLabel(popup, text="Matrícula do aluno:", font=ctk.CTkFont(size=15)).pack(pady=5)
        matricula_entry = ctk.CTkEntry(popup, width=250)
        matricula_entry.pack()

        # MATÉRIA
        ctk.CTkLabel(popup, text="Matéria:", font=ctk.CTkFont(size=15)).pack(pady=5)
        materia_option = ctk.CTkOptionMenu(
            popup,
            values=[
                "Linguagem Estruturada em C (B1)",
                "Linguagem Estruturada em C (B2)",
                "Python (B1)",
                "Python (B2)",
                "Engenharia de Software (B1)",
                "Engenharia de Software (B2)",
                "Inteligência Artificial (B1)",
                "Inteligência Artificial (B2)"
            ]
        )
        materia_option.pack(pady=5)

        # NOTA
        ctk.CTkLabel(popup, text="Nota (0 a 10):", font=ctk.CTkFont(size=15)).pack(pady=5)
        nota_entry = ctk.CTkEntry(popup, width=100)
        nota_entry.pack()

        # USE DAR NOTA DO CONTROLLERS.PY
        #+++++++++++++++++++++++++++++++++++++++++++++
        

        # botão confirmar
        ctk.CTkButton(
            popup,
            text="Salvar Nota",
            fg_color="#34C759",
            hover_color="#28a745",
            command=salvar_nota
        ).pack(pady=20)

# popup para consultar notas com médias
    def consultar_notas_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Consultar Notas do Aluno")
        popup.geometry("500x500")
        popup.configure(fg_color="white")

        # Matrícula
        ctk.CTkLabel(popup, text="Matrícula do aluno:", font=ctk.CTkFont(size=15)).pack(pady=5)
        matricula_entry = ctk.CTkEntry(popup, width=250)
        matricula_entry.pack(pady=5)

        def mostrar_notas():
            matricula = matricula_entry.get()
            conn = sqlite3.connect("database.db")
            db = conn.cursor()
            notas = controllers.consultar_notas(db, matricula)
            conn.close()

            if not notas:
                messagebox.showerror("Erro", "Aluno não encontrado ou erro ao consultar notas!")
                return

            # pega o primeiro registro (normalmente só tem um)
            n = notas[0]

            # Calcula médias automaticamente (se alguma nota for None, ignora)
            medias = {}
            for mat in ["ling_est_c", "python", "eng_soft", "ia"]:
                bim1 = n[f"{mat}_bim1"] or 0
                bim2 = n[f"{mat}_bim2"] or 0
                medias[mat] = round((bim1 + bim2)/2, 2)

            # Mostra as notas e médias
            texto = ""
            for mat in ["ling_est_c", "python", "eng_soft", "ia"]:
                texto += f"{mat.upper()}:\n"
                texto += f"  B1: {n[f'{mat}_bim1']}\n"
                texto += f"  B2: {n[f'{mat}_bim2']}\n"
                texto += f"  Média: {medias[mat]}\n\n"

            notas_label = ctk.CTkLabel(popup, text=texto, justify="left", font=ctk.CTkFont(size=14))
            notas_label.pack(pady=10)

        # botão confirmar
        ctk.CTkButton(popup, text="Consultar", fg_color="#34C759", hover_color="#28a745", command=mostrar_notas).pack(pady=20)

    # popup para dar falta
    def dar_falta_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Lançar Falta")
        popup.geometry("400x300")
        popup.configure(fg_color="white")

        # Matrícula
        ctk.CTkLabel(popup, text="Matrícula do aluno:", font=ctk.CTkFont(size=15)).pack(pady=5)
        matricula_entry = ctk.CTkEntry(popup, width=250)
        matricula_entry.pack()

        # Quantidade de faltas
        ctk.CTkLabel(popup, text="Quantidade de faltas:", font=ctk.CTkFont(size=15)).pack(pady=5)
        falta_entry = ctk.CTkEntry(popup, width=100)
        falta_entry.pack()

        # Função para salvar no banco
        def salvar_falta():
            matricula = matricula_entry.get()
            try:
                faltas = int(falta_entry.get())
                if faltas < 0:
                    raise ValueError
            except:
                messagebox.showerror("Erro", "Informe um número válido de faltas!")
                return

            conn = sqlite3.connect("database.db")
            db = conn.cursor()
            try:
                # incrementa as faltas no banco
                db.execute("UPDATE alunos_nova SET faltas = faltas + ? WHERE matricula = ?", (faltas, matricula))
                conn.commit()
                messagebox.showinfo("Sucesso", f"{faltas} faltas registradas para o aluno!")
                popup.destroy()
            except:
                messagebox.showerror("Erro", "Falha ao registrar a falta.")
            conn.close()

        # botão salvar
        ctk.CTkButton(popup, text="Salvar Falta", fg_color="#E57373", hover_color="#EF5350",
                      command=salvar_falta).pack(pady=20)


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
conn.close()

# main (ponto de partida do sistema)
if __name__ == "__main__":
    
    app = LoginApp()
    app.mainloop()
    

