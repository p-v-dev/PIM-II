import sqlite3

# Conectar ao banco de dados (cria se não existir)
conn = sqlite3.connect('database.db')
db = conn.cursor()



nota = 1.23
cpf =273871




# Sempre confirmar as mudanças
#conn.commit()

# Fechar a conexão
#conn.close()

#listar alunos

def listar_alunos():
    db.execute("SELECT * FROM alunos_nova")
    data = db.fetchall()

    for linha in data:
        alunos = []
        alunos.append(linha)

    return alunos

def dar_nota(materia,matricula, nota):

    query = f"UPDATE alunos_nova SET {materia} = ? WHERE matricula = ?"
    db.execute(query, (nota, matricula))


def hash_simples(senha):
    """
    Função hash idêntica à versão em C
    Retorna o mesmo hash para a mesma senha
    """
    SALT = "abds14"
    
    # Combina senha + SALT (igual ao snprintf)
    combinacao = senha + SALT
    
    # Soma todos os caracteres (igual ao loop for em C)
    soma = 0
    for char in combinacao:
        soma += ord(char)  # ord() equivale ao valor ASCII do char em C
    
    # Converte para hexadecimal e multiplica por 123
    # Usando format(soma * 123, 'x') para ser idêntico ao %x do snprintf
    hash_resultado = format(soma * 123, 'x')
    
    return hash_resultado

#criar atividades