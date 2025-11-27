import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import controllers
from chatbot import iniciar_chatbot, apresentacao

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")
conn = sqlite3.connect('database.db')
db = conn.cursor()

# classe base (estrutura padrão dos portais)
class BasePortal(ctk.CTk):
    def __init__(self, nome_usuario, email_usuario, titulo, subtitulo):
        super().__init__()
        # usa a conexão global declarada no topo do módulo
        self.conn = conn
        self.db = db
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
        
        # frame interno para organizar os botões
        botoes_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=0)
        botoes_frame.pack(pady=10)

        # lista de botões do aluno
        botoes = [
            ("Faltas", self.consultar_faltas_popup),
            ("Minhas Notas", self.consultar_notas_popup),
            ("Atividades", self.listar_atividades)
        ]


        cols = 3  # 3 colunas
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
            btn.grid(row=i // cols, column=i % cols, padx=15, pady=15)

        # botão chatbot
        chatbot_btn = ctk.CTkButton(self.main_frame, text="🤖", width=50, height=50,
                                    corner_radius=25, fg_color="#287DFD",
                                    hover_color="#231FE6", text_color="white",
                                    font=ctk.CTkFont(size=20),
                                    command=self.abrir_chatbot)
        chatbot_btn.place(relx=0.95, rely=0.95, anchor="se")
        
    def consultar_notas_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Consultar Notas")
        popup.geometry("400x300")
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="Digite sua matrícula:").pack(pady=10)
        matricula_entry = ctk.CTkEntry(popup, width=250)
        matricula_entry.pack(pady=(0, 15))

        def consultar():
            matricula = matricula_entry.get().strip()
            if not matricula:
                messagebox.showerror("Erro", "Digite uma matrícula válida.")
                return

            dados = controllers.consultar_notas(db, matricula)
            if not dados or len(dados) == 0:
                messagebox.showerror("Erro", "Aluno não encontrado.")
                return

            dados = dados[0]  # Pega o primeiro dict da lista

            def calc_media(b1, b2):
                notas = [n for n in (b1, b2) if n is not None]
                return round(sum(notas)/len(notas), 2) if notas else None

            ling_est_c_media = calc_media(dados['ling_est_c_bim1'], dados['ling_est_c_bim2'])
            python_media = calc_media(dados['python_bim1'], dados['python_bim2'])
            eng_soft_media = calc_media(dados['eng_soft_bim1'], dados['eng_soft_bim2'])
            ia_media = calc_media(dados['ia_bim1'], dados['ia_bim2'])

            texto = (
                f"Linguagem e Comunicação:\n  1º Bim: {dados['ling_est_c_bim1']}\n"
                f"  2º Bim: {dados['ling_est_c_bim2']}\n  Média: {ling_est_c_media}\n\n"
                f"Python:\n  1º Bim: {dados['python_bim1']}\n"
                f"  2º Bim: {dados['python_bim2']}\n  Média: {python_media}\n\n"
                f"Engenharia de Software:\n  1º Bim: {dados['eng_soft_bim1']}\n"
                f"  2º Bim: {dados['eng_soft_bim2']}\n  Média: {eng_soft_media}\n\n"
                f"IA:\n  1º Bim: {dados['ia_bim1']}\n"
                f"  2º Bim: {dados['ia_bim2']}\n  Média: {ia_media}"
            )

            messagebox.showinfo("Suas Notas", texto)

        ctk.CTkButton(popup, text="Consultar", command=consultar).pack(pady=15)

        ctk.CTkButton(
            popup,
            text="Voltar",
            fg_color="#007BFF",       
            hover_color="#0056b3",
            command=popup.destroy
        ).pack(side="bottom", anchor="e", padx=10, pady=10)


    def consultar_faltas_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Consultar Faltas")
        popup.geometry("400x250")
        popup.transient(self) 
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="Digite sua matrícula:").pack(pady=10)
        matricula_entry = ctk.CTkEntry(popup, width=250)
        matricula_entry.pack()

        def consultar():
            matricula = matricula_entry.get().strip()

            if not matricula:
                messagebox.showerror("Erro", "Digite uma matrícula válida.")
                return

            # usa conexão global
            faltas = controllers.consultar_falta(db, matricula)

            if faltas is None:
                messagebox.showerror("Erro", "Matrícula não encontrada.")
            else:
                messagebox.showinfo("Suas Faltas", f"Total de faltas: {faltas}")

        ctk.CTkButton(popup, text="Consultar", command=consultar).pack(pady=15)

        ctk.CTkButton(
            popup,
            text="Voltar",
            fg_color="#007BFF",       
            hover_color="#0056b3",
            command=popup.destroy
        ).pack(side="bottom", anchor="e", padx=10, pady=10)

        
    def abrir_chatbot(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Chatbot Sofia")
        janela.geometry("500x600")
        janela.transient(self) 
        janela.grab_set()      
        janela.focus_force()

        chat_box = ctk.CTkTextbox(janela, width=480, height=500)
        chat_box.pack(pady=10)

        # apresentação da Sofia no chat
        chat_box.insert("end", apresentacao() + "\n")

        entrada = ctk.CTkEntry(janela, width=400)
        entrada.pack(side="left", padx=10, pady=10)

        enviar_btn = ctk.CTkButton(
            janela, 
            text="Enviar",
            command=lambda: self.enviar_mensagem_chat(entrada, chat_box)
        )
        enviar_btn.pack(side="right", padx=10, pady=10)

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
        janela.transient(self) 
        janela.grab_set()      
        janela.focus_force()

        ctk.CTkLabel(janela, text="Alunos Cadastrados",
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color="#001A80").pack(pady=10)
        
        ctk.CTkButton(
            janela,
            text="Voltar",
            fg_color="#007BFF",       
            hover_color="#0056b3",
            command=janela.destroy
        ).pack(side="bottom", anchor="e", padx=10, pady=10)

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
        janela.transient(self) 
        janela.grab_set()      
        janela.focus_force()

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

        ctk.CTkButton(
            janela,
            text="Voltar",
            fg_color="#007BFF",       
            hover_color="#0056b3",
            command=janela.destroy
        ).pack(side="bottom", anchor="e", padx=10, pady=10)

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

        # usa conexão global
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
        popup.transient(self) 
        popup.grab_set()      
        popup.focus_force()

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

            # usa conexão global
            sucesso = controllers.criar_atividade(db, titulo, descricao, data, link)
            conn.commit()

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
        popup.transient(self) 
        popup.grab_set()      
        popup.focus_force()


        ctk.CTkLabel(popup, text="Título da Atividade a excluir:").pack(pady=10)
        entry = ctk.CTkEntry(popup, width=300)
        entry.pack(pady=5)

        def excluir():
            titulo = entry.get()

            # usa conexão global
            sucesso = controllers.excluir_atividade(db, titulo)
            conn.commit()

            if sucesso:
                messagebox.showinfo("Sucesso", f"Atividade '{titulo}' excluída com sucesso!")
                popup.destroy()
                self._carregar_atividades()
            else:
                messagebox.showerror("Erro", "Erro ao excluir atividade. Verifique o título.")

        ctk.CTkButton(popup, text="Excluir", fg_color="#E57373", command=excluir).pack(pady=10)

    # popup - dar nota ao aluno
    def dar_nota_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Lançar Nota")
        popup.geometry("450x400")
        popup.configure(fg_color="white")
        popup.transient(self) 
        popup.grab_set()      
        popup.focus_force()

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

        # FUNÇÃO interna para salvar no banco
        def salvar_nota():
            matricula = matricula_entry.get()
            materia = materia_option.get()
            nota = nota_entry.get()

            # validação da nota
            try:
                nota = float(nota)
                if nota < 0 or nota > 10:
                    raise ValueError
            except:
                messagebox.showerror("Erro", "A nota deve ser um número entre 0 e 10!")
                return

            # converte nome da matéria para coluna correta do banco
            mapa_colunas = {
                "Linguagem Estruturada (B1)": "ling_est_c_bim1",
                "Linguagem Estruturada (B2)": "ling_est_c_bim2",
                "Python (B1)": "python_bim1",
                "Python (B2)": "python_bim2",
                "Engenharia de Software (B1)": "eng_soft_bim1",
                "Engenharia de Software (B2)": "eng_soft_bim2",
                "Inteligência Artificial (B1)": "ia_bim1",
                "Inteligência Artificial (B2)": "ia_bim2",
            }

            coluna = mapa_colunas[materia]

            # salva no banco
            try:
                db.execute(f"UPDATE alunos_nova SET {coluna} = ? WHERE matricula = ?", (nota, matricula))
                # commit usando conexão global
                conn.commit()
                messagebox.showinfo("Sucesso", f"Nota registrada em {materia}!")
                popup.destroy()
            except:
                messagebox.showerror("Erro", "Falha ao registrar a nota.")
            
            conn.close()

        # botão confirmar
        ctk.CTkButton(
            popup,
            text="Salvar Nota",
            fg_color="#34C759",
            hover_color="#28a745",
            command=salvar_nota
        ).pack(pady=20)
        
        ctk.CTkButton(
            popup,
            text="Voltar",
            fg_color="#007BFF",       
            hover_color="#0056b3",
            command=popup.destroy
        ).pack(side="bottom", anchor="e", padx=10, pady=10)

# popup para consultar notas com médias
    def consultar_notas_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Consultar Notas do Aluno")
        popup.geometry("500x600")
        popup.configure(fg_color="white")

        popup.transient(self) 
        popup.grab_set()      
        popup.focus_force()

        # Matrícula
        ctk.CTkLabel(popup, text="Matrícula do aluno:", font=ctk.CTkFont(size=15)).pack(pady=5)
        matricula_entry = ctk.CTkEntry(popup, width=250)
        matricula_entry.pack(pady=5)

        def mostrar_notas():
            matricula = matricula_entry.get()
            # usa conexão global
            notas = controllers.consultar_notas(db, matricula)

            if not notas:
                messagebox.showerror("Erro", "Aluno não encontrado ou erro ao consultar notas!")
                return

            # não use n = notas[0], notas já é um dicionário
            n = notas  # <--- CORREÇÃO

            # Calcula médias, ignorando notas None
            medias = {}
            for mat in ["ling_est_c", "python", "eng_soft", "ia"]:
                bim1 = n[f"{mat}_bim1"]
                bim2 = n[f"{mat}_bim2"]

                # cálculo da média
                if bim1 is not None and bim2 is not None:
                    medias[mat] = round((bim1 + bim2)/2, 2)
                else:
                    medias[mat] = None

            # Formata para exibição
            texto = ""
            for mat in ["ling_est_c", "python", "eng_soft", "ia"]:
                b1_disp = n[f"{mat}_bim1"] if n[f"{mat}_bim1"] is not None else "-"
                b2_disp = n[f"{mat}_bim2"] if n[f"{mat}_bim2"] is not None else "-"
                media_disp = medias[mat] if medias[mat] is not None else "-"
                
                texto += f"{mat.replace('_',' ').title()}:\n"
                texto += f"  1º Bim: {b1_disp}\n"
                texto += f"  2º Bim: {b2_disp}\n"
                texto += f"  Média: {media_disp}\n\n"

            # Exibe as notas em um label
            notas_label = ctk.CTkLabel(popup, text=texto, justify="left", font=ctk.CTkFont(size=14))
            notas_label.pack(pady=10)
        
        # Botão Consultar
        ctk.CTkButton(
            popup,
            text="Consultar",
            fg_color="#34C759",
            hover_color="#28a745",
            command=mostrar_notas
        ).pack(pady=10)

        ctk.CTkButton(
            popup,
            text="Voltar",
            fg_color="#007BFF",       
            hover_color="#0056b3",
            command=popup.destroy
        ).pack(side="bottom", anchor="e", padx=10, pady=10)

    # popup para dar falta
    def dar_falta_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Lançar Falta")
        popup.geometry("400x300")
        popup.configure(fg_color="white")

        popup.transient(self) 
        popup.grab_set()      
        popup.focus_force()

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

            try:
                # incrementa as faltas no banco usando conexão global
                db.execute("UPDATE alunos_nova SET faltas = faltas + ? WHERE matricula = ?", (faltas, matricula))
                conn.commit()
                messagebox.showinfo("Sucesso", f"{faltas} faltas registradas para o aluno!")
                popup.destroy()
            except:
                messagebox.showerror("Erro", "Falha ao registrar a falta.")

        # botão salvar
        ctk.CTkButton(popup, text="Salvar Falta", fg_color="#E57373", hover_color="#EF5350",
                      command=salvar_falta).pack(pady=20)
        
        ctk.CTkButton(
            popup,
            text="Voltar",
            fg_color="#007BFF",       
            hover_color="#0056b3",
            command=popup.destroy
        ).pack(side="bottom", anchor="e", padx=10, pady=10)

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
        for tipo in ["Aluno", "Docente"]:
            btn = ctk.CTkButton(tipo_frame, text=tipo, width=110, corner_radius=15,
                                fg_color="#34C759", hover_color="#28a745", text_color="white",
                                command=lambda t=tipo: self.selecionar_tipo(t))
            btn.grid(row=0, column=len(self.btns), padx=8)
            self.btns[tipo] = btn

        self.tipo_label = ctk.CTkLabel(frame, text="Aluno selecionado", text_color="green")
        self.tipo_label.pack(pady=(0, 10))

        # campos de login (email e senha)
        self.identifier_label = ctk.CTkLabel(frame, text="Digite sua matrícula:", anchor="w", text_color="black")
        self.identifier_label.pack(anchor="w", padx=40)
        self.email_entry = ctk.CTkEntry(frame, placeholder_text="Matrícula / CPF", width=300, height=30)
        self.email_entry.pack(pady=(5, 15), padx=40)

        # aplica seleção inicial após widgets estarem criados
        self.selecionar_tipo(self.tipo_usuario)

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

    # muda o tipo de usuário selecionado
    def selecionar_tipo(self, tipo):
        self.tipo_usuario = tipo
        # atualiza label informativa e placeholder do campo de identificação
        if tipo == "Aluno":
            self.identifier_label.configure(text="Digite sua matrícula:")
            self.email_entry.configure(placeholder_text="Matrícula")
        else:
            self.identifier_label.configure(text="Digite seu CPF:")
            self.email_entry.configure(placeholder_text="CPF")

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
        identificador = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not identificador or not senha:
            messagebox.showerror("Erro", "Preencha identificação e senha.")
            return

        # usa conexão global `conn` e cursor `db` declarados no topo
        try:
            if self.tipo_usuario == "Aluno":
                ok = controllers.login_aluno(db, identificador, senha)
                if not ok:
                    messagebox.showerror("Erro", "Matrícula ou senha inválida.")
                    return

                # obtém dados do aluno (nome e e-mail)
                aluno = controllers.consultar_aluno(db, identificador)
                if aluno:
                    nome_usuario = f"{aluno.get('nome')} {aluno.get('sobrenome')}"
                else:
                    nome_usuario = identificador

                # tenta buscar e-mail no banco
                db.execute("SELECT email FROM alunos_nova WHERE matricula = ?", (identificador,))
                row = db.fetchone()
                email_usuario = row[0] if row and row[0] else f"{identificador}@aluno"

                self.destroy()
                portal = PortalAluno(nome_usuario=nome_usuario, email_usuario=email_usuario)

            else:  # Docente
                ok = controllers.login_professor(db, identificador, senha)
                if not ok:
                    messagebox.showerror("Erro", "CPF ou senha inválida.")
                    return

                # obter nome e e-mail do professor
                db.execute("SELECT nome, sobrenome, email FROM professores WHERE cpf = ?", (identificador,))
                row = db.fetchone()
                if row:
                    nome_usuario = f"{row[0]} {row[1]}"
                    email_usuario = row[2] or f"{identificador}@professor"
                else:
                    nome_usuario = identificador
                    email_usuario = f"{identificador}@professor"

                self.destroy()
                portal = PortalDocente(nome_usuario=nome_usuario, email_usuario=email_usuario)

            portal.mainloop()

        finally:
            # não fecha a conexão aqui — será fechada ao sair da aplicação
            pass

# main (ponto de partida do sistema)
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
    # fecha a conexão global ao encerrar a aplicação
    try:
        conn.close()
    except Exception:
        pass