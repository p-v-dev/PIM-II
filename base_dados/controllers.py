import sqlite3
import datetime
"""
Conecta ao banco de dados 
PRECISA DE INICIAR O BANCO DE DADOS JUNTO DA APLICACAO SE NN DA BOSTA

copia e cola e cola essa parte de baixo e passa o db como o primeiro argumento quando usar as funcoes
    |
    |
    v
conn = sqlite3.connect('database.db')
db = conn.cursor()


"""


"""
Essa funcao de hash e para login, ignore por enquanto
"""
def hash_simples(senha):
    """
    Função hash idêntica à versão em C
    Retorna o mesmo hash para a mesma senha
    """
    SALT = "abds14"
    
    combinacao = senha + SALT
    
    
    soma = 0
    for char in combinacao:
        soma += ord(char)  # ord() equivale ao valor ASCII do char em C
    
    hash_resultado = format(soma * 123, 'x')
    
    return hash_resultado


#conn.close()


def listar_alunos(db):
   
   """
   Essa funcao retorna uma lista de dicionarios se tiver certo

   Se der erro retorna um valor None
   """
   try:
    db.execute('''SELECT nome, sobrenome, matricula, turma, email, faltas, 
               ling_est_c_bim1, ling_est_c_bim2, ling_est_c_media, 
               python_bim1, python_bim2, python_media, 
               eng_soft_bim1, eng_soft_bim2, eng_soft_media, 
               ia_bim1, ia_bim2, ia_media  
               FROM alunos_nova''')
    
    data = db.fetchall()
    
    alunos = []

    for aluno in data:
        alunos.append({
            'nome' : aluno[0],
            'sobrenome' : aluno[1],
            'matricula' : aluno[2],
            'turma' : aluno[3],
            'email' : aluno[4],
            'faltas' : aluno[5],
            'ling_est_c_bim1' : aluno[6],
            'ling_est_c_bim2' : aluno[7],
            'ling_est_c_media' : aluno[8],
            'python_bim1' : aluno[9],
            'python_bim2' : aluno[10],
            'python_media' : aluno[11],
            'eng_soft_bim1' : aluno[12],
            'eng_soft_bim2' : aluno[13],
            'eng_soft_media' : aluno[14],
            'ia_bim1' : aluno[15],
            'ia_bim2' : aluno[16],
            'ia_media' : aluno[17],
        })

    return alunos
   
   except:
        print("erro ao consultar alunos no banco de dados")
        return None
   
   

def dar_nota(db, materia, matricula, nota):

    """
    Lista do nome das materias (TEM QUE PASSAR O NOME DA MATERIA EXATAMENTE DESSE JEITO SE NN DA ERRO):
    Obs: tem que especificar bim1, bim2 ou media 

    Exemplo de uso : python_bim1, ia_media, ling_est_c_bim2

    Materias aceitas como argumento:

    ling_est_c
    python
    eng_soft
    ia
    """
    try:
        query = f"UPDATE alunos_nova SET {materia} = ? WHERE matricula = ?"
        db.execute(query, (nota, matricula,))

        print(f"nota: {nota} para o aluno de matricula: {matricula} na materia{materia} com sucesso")

        return True

    except:
        print("erro ao dar nota")
        return False
    

def consultar_notas(db, matricula):
    """
    Retorna uma list de dicionarios ou valor None se houver erro
    """

    query = '''SELECT 
    ling_est_c_bim1, ling_est_c_bim2, ling_est_c_media, 
    python_bim1, python_bim2, python_media, 
    eng_soft_bim1, eng_soft_bim2, eng_soft_media, 
    ia_bim1, ia_bim2, ia_media  
    FROM alunos_nova WHERE matricula = ?'''
    try:
        db.execute(query, (matricula,))

        data = db.fetchall()
        
        notas = []

        for nota in data:
            notas.append({
                'ling_est_c_bim1' : nota[0],
                'ling_est_c_bim2' : nota[1],
                'ling_est_c_media' : nota[2],
                'python_bim1' : nota[3],
                'python_bim2' : nota[4],
                'python_media' : nota[5],
                'eng_soft_bim1' : nota[6],
                'eng_soft_bim2' : nota[7],
                'eng_soft_media' : nota[8],
                'ia_bim1' : nota[9],
                'ia_bim2' : nota[10],
                'ia_media' : nota[11],
            })
        return notas

    except:

        print("erro ao consultar notas")
        return None
    

#criar atividades

def criar_atividade(db, titulo, descricao, data_entrega=None, link=None):

    """
    NAO DEIXE O CAMPO DE TITULO E DESCRICAO NULOS

    o campo de link e data de entrega PODEM ser nulos

    link e data de entrega podem ser nulos
    
    formato de data: ano-mes-dia
    """

    try:
            datetime.strptime(data_entrega, '%Y-%m-%d')

    except ValueError:
            
            print("Formato de data inválido Use AAAA-MM-DD")
            return None
    
    if link:
        db.execute('''INSERT INTO atividades 
                   (titulo, descricao, link, data_entrega)
                    VALUES (?, ?, ?, ?)''', 
                    (titulo, descricao, link, data_entrega,))
        return True
    
    else:
        db.execute('''INSERT INTO atividades 
                (titulo, descricao, data_entrega)
                VALUES (?, ?, ?)''', 
                (titulo, descricao, data_entrega,))
        print(f"Atividade '{titulo}' adicionada")   
        return True
        
          

        

def listar_atividades(db):
    """
    Retorna uma lista de dicionarios, cada item da lista e uma atividade
    """

    db.execute("SELECT titulo, descricao, link, data_entrega FROM atividades")

    data = db.fetchall()

    atividades = []

    for atividade in data:

        atividades.append({
            'titulo': atividade[0],
            'descricao': atividade[1],
            'link': atividade[2],
            'data_entrega': atividade[3]
        })

    return atividades


def excluir_atividade(db, titulo):

    try:
        db.execute("FROM atividades DELETE WHERE titulo = ?", (titulo,))
        print(f"atividade {titulo} deletada ")
        return True

    except:
        print("erro ao excluir atividade")
        return None
    

def dar_falta(db, matricula, falta):
    try:
        query = f"UPDATE alunos_nova SET falta = ? WHERE {matricula} = ?"
        db.execute(query, (falta,matricula,))
        return True
    
    except:
        print(f"erro ao dar {falta} faltas para aluno de matricula: {matricula}")
        return False


def  consultar_falta(db, matricula):

    """
    Retorna um dicionario 
    {
    matricula : str,
    faltas : int
    }
    """
    query = "SELECT faltas FROM alunos_nova WHERE matricula = ?"

    db.execute(query, (matricula,))

    data = db.fetchone()

    if data:
        return{
            'matricula' : matricula,
            'faltas' : data[0]
        }
    
    else:
        return None

    
def login_aluno(db, matricula, senha):
    """
    recebe db, matricula, senha

    retorna bool True se senha correta

    False se estiver incorreto
    """

    query = "SELECT senha FROM alunos_nova WHERE matricula=?"
    db.execute(query, (matricula,))

    senha_db = db.fetchone()

    senha_hash = hash_simples(senha)

    if senha_db and senha_db[0] == senha_hash:
        print("aluno logado com sucesso")
        return True
    else:
        print("erro ao logar como aluno")
        return False


def login_professor(db, cpf, senha):
    """
    recebe db, cpf, senha

    retorna bool True se senha correta

    False se estiver incorreto
    """

    query = "SELECT senha FROM professores WHERE cpf=?"
    db.execute(query, (cpf,))

    senha_db = db.fetchone()

    senha_hash = hash_simples(senha)

    if senha_db and senha_db[0] == senha_hash:
        print("professor logado com sucesso")
        return True
    else:
        print("erro ao logar como professor")
        return False
    
def consultar_aluno(db, matricula):
    query = '''SELECT nome, sobrenome, turma, 
    ling_est_c_bim1, ling_est_c_bim2, ling_est_c_media, 
    python_bim1, python_bim2, python_media, 
    eng_soft_bim1, eng_soft_bim2, eng_soft_media, 
    ia_bim1, ia_bim2, ia_media 
    FROM alunos_nova WHERE matricula=?'''
    db.execute(query, (matricula,))

    dados = db.fetchone()
    if dados:
       return{
            "nome" : dados[0],
            "sobrenome" : dados[1],
            "matricula" : matricula,
            "turma" : dados[2],
            'ling_est_c_bim1' :  dados[3],
            'ling_est_c_bim2' :  dados[4],
            'ling_est_c_media' :  dados[5],
            'python_bim1' :  dados[6],
            'python_bim2' :  dados[7],
            'python_media' :  dados[8],
            'eng_soft_bim1' :  dados[9],
            'eng_soft_bim2' :  dados[10],
            'eng_soft_media' :  dados[11],
            'ia_bim1' :  dados[12],
            'ia_bim2' :  dados[13],
            'ia_media' : dados[14],
        }
    else:
        return None