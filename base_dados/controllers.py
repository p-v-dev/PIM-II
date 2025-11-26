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
    
    # Combina senha + SALT 
    combinacao = senha + SALT
    
    # Soma todos os caracteres 
    soma = 0
    for char in combinacao:
        soma += ord(char)  # ord() equivale ao valor ASCII do char em C
    
    # Converte para hexadecimal e multiplica por 123
    # Usando format(soma * 123, 'x') para ser idêntico ao %x do snprintf
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
    Retorna um dicionário com as notas do aluno, ou None se não existir.
    """
    try:
        query = """
            SELECT ling_est_c_bim1, ling_est_c_bim2, ling_est_c_media,
                   python_bim1, python_bim2, python_media,
                   eng_soft_bim1, eng_soft_bim2, eng_soft_media,
                   ia_bim1, ia_bim2, ia_media
            FROM alunos_nova
            WHERE matricula = ?
        """
        db.execute(query, (matricula,))
        result = db.fetchone()

        if result:
            return {
                "ling_est_c_bim1": result[0],
                "ling_est_c_bim2": result[1],
                "ling_est_c_media": result[2],
                "python_bim1": result[3],
                "python_bim2": result[4],
                "python_media": result[5],
                "eng_soft_bim1": result[6],
                "eng_soft_bim2": result[7],
                "eng_soft_media": result[8],
                "ia_bim1": result[9],
                "ia_bim2": result[10],
                "ia_media": result[11],
            }
        else:
            return None
    except Exception as e:
        print("Erro ao consultar notas:", e)
        return None

    

#criar atividades

def criar_atividade(db, titulo, descricao, data_entrega=None, link=None):

    """
    NAO DEIXE O CAMPO DE TITULO E DESCRICAO NULOS, VAI DAR ERRO

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
        db.execute('''INSERT INTO atividades (titulo, descricao, link, data_entrega)
                    VALUES (?, ?, ?, ?)''', 
                    (titulo, descricao, link, data_entrega))
        return True
    
    else:
        db.execute('''INSERT INTO atividades (titulo, descricao, data_entrega)
                VALUES (?, ?, ?)''', 
                (titulo, descricao, data_entrega))
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
        db.execute("FROM atividades DELETE WHERE titulo = ?", (titulo))
        print(f"atividade {titulo} deletada ")
        return True

    except:
        print("erro ao excluir atividade")
        return None
    

def dar_falta(db, matricula, falta):
    try:
        query = f"UPDATE alunos_nova SET falta = ? WHERE {matricula} = ?"
        db.execute(query, (falta,matricula))
        return True
    
    except:
        print(f"erro ao dar {falta} faltas para aluno de matricula: {matricula}")
        return False


def consultar_faltas(db, matricula):
    try:
        query = "SELECT faltas FROM alunos_nova WHERE matricula = ?"
        result = db.execute(query, (matricula,)).fetchone()

        if result:
            return result[0]  # retorna só o número de faltas
        else:
            return None

    except Exception as e:
        print("Erro ao consultar faltas:", e)
        return None



    
def login_aluno(db, matricula, senha):
    """
    recebe db, matricula, senha

    retorna bool True se senha correta

    False se estiver incorreto
    """

    query = "SELECT senha FROM alunos_nova WHERE matricula=?"
    db.execute(query,(matricula))

    senha_db = db.fetchone()

    senha_hash = hash_simples(senha)

    if senha_db == senha_hash:
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
    db.execute(query,(cpf))

    senha_db = db.fetchone()

    senha_hash = hash_simples(senha)

    if senha_db == senha_hash:
        print("professor logado com sucesso")
        return True
    
    else:
        print("erro ao logar como professor")
        return False
    
def consultar_aluno(db, matricula):
    query = "SELECT nome, sobrenome, turma, ling_est_c_bim1, ling_est_c_bim2, ling_est_c_media, python_bim1, python_bim2, python_media, eng_soft_bim1, eng_soft_bim2, eng_soft_media, ia_bim1, ia_bim2, ia_media FROM alunos_nova WHERE matricula=?"
    db.execute(query,(matricula))

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