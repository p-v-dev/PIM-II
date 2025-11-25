# sofiagpt.py
import sqlite3
import json
from google import genai
from google.genai.types import Schema, Type


# ============================================================
# Configuração do Gemini (API)
# ============================================================
API_KEY = "AIzaSyAJ72U_oI3z1435M3WblU-Mnk_y8LbJQmM"


def get_client():
    return genai.Client(api_key=API_KEY)


# ============================================================
# Estrutura JSON - Schema (Interpretação)
# ============================================================
QUESTION_SCHEMA = Schema(
    type=Type.OBJECT,
    properties={
        "aluno": Schema(type=Type.STRING, nullable=True),
        "materia": Schema(
            type=Type.STRING,
            enum=["ling_est_c", "python", "eng_soft", "ia"],
            nullable=True
        ),
        "bimestre": Schema(
            type=Type.STRING,
            enum=["1", "2", "media"],
            nullable=True
        ),
    },
    required=[],
)


def interpretar_pergunta(pergunta: str) -> dict:
    """
    Interpreta a pergunta do usuário e retorna um JSON contendo:
    aluno, materia e bimestre.
    Caso a pergunta não seja sobre notas, retorna {}.
    """
    client = get_client()

    prompt = (
        "Extraia as informações solicitadas na pergunta a seguir.\n"
        "Retorne SOMENTE um JSON com as chaves: aluno, materia e bimestre.\n"
        "Materias válidas: ling_est_c, python, eng_soft, ia.\n"
        "Bimestres válidos: 1, 2 ou media.\n"
        "Se a frase for apenas uma saudação, responda com JSON vazio ({}).\n\n"
        f"Pergunta: {pergunta}"
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[{"role": "user", "parts": [prompt]}],
        config={
            "response_mime_type": "application/json",
            "response_schema": QUESTION_SCHEMA,
            "temperature": 0.2,
        },
    )

    # Protege contra respostas fora do formato JSON
    try:
        data = json.loads(response.text)
        if not isinstance(data, dict):
            return {}
        return data
    except Exception:
        return {}


# ============================================================
# Consulta ao banco de dados (SQLite)
# ============================================================
COLMAP = {
    "ling_est_c": "ling_est_c",
    "python": "python",
    "eng_soft": "eng_soft",
    "ia": "ia",
}


def identificar_coluna(prefixo, bimestre):
    if bimestre == "media":
        return f"{prefixo}_media"
    elif bimestre == "1":
        return f"{prefixo}_bim1"
    elif bimestre == "2":
        return f"{prefixo}_bim2"
    return None


def consultar_notas(db, aluno_nome, materia_key, bimestres):
    prefixo = COLMAP.get(materia_key)
    if not prefixo:
        print("❌ Matéria inválida.")
        return

    for b in bimestres:
        coluna = identificar_coluna(prefixo, b)
        if not coluna:
            continue

        db.execute(
            f"SELECT {coluna} FROM alunos_nova WHERE nome = ? OR sobrenome = ?",
            (aluno_nome, aluno_nome)
        )
        row = db.fetchone()
        if row and row[0] is not None:
            print(f"📊 {aluno_nome} — {materia_key} ({b}): {row[0]}")
        else:
            print(
                f"❌ Nenhuma nota encontrada para {aluno_nome} — {materia_key} ({b})")

# ============================================================
# Apresentação da Sofia
# ============================================================


def apresentacao():
    print("👋| Olá! Eu sou a Sofia — Sistema de Orientação e Facilitação de Informações Acadêmicas.")
    print(" Fui criada para ajudar você a consultar notas de forma rápida e inteligente.")
    print("\n✨| Minhas funções principais:")
    print("- Consultar notas por nome, matéria e bimestre (1 ou 2).")
    print("\n📝| Como usar:")
    print(" - 'Qual a minha nota em Python no 2º bimestre?'")
    print(" - 'Engenharia de Software' (Mostra a nota dois bimestres)")
    print("\nDigite 'sair' a qualquer momento para encerrar.")
    print("───────────────────────────────────────────────\n")

# ============================================================
# Loop
# ============================================================


def iniciar_chatbot(db, aluno_logado=None, pode_ver_todos=False):
    apresentacao()

    while True:
        pergunta = input("Você: ")

        if any(saud in pergunta.lower() for saud in ["olá", "oi", "tudo bem", "bom dia", "boa tarde", "boa noite"]):
            print(
                "Sofia: Olá! 😊 Como posso te ajudar? Quer consultar alguma nota ou matéria?")
            continue

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("👋 Sessão encerrada. Até mais!")
            break

        try:
            dados = interpretar_pergunta(pergunta)
        except Exception as e:
            print("⚠️ Ocorreu um erro ao processar a pergunta. Tente novamente.")
            continue

        aluno = dados.get("aluno")
        materia = dados.get("materia")
        bimestre = dados.get("bimestre")

        # Controle de acesso
        if not pode_ver_todos and aluno_logado:
            if aluno and aluno.lower() != aluno_logado.lower():
                print("🚫 Você só pode consultar suas próprias informações.")
                aluno = aluno_logado
            elif not aluno:
                aluno = aluno_logado

        if not aluno:
            print("❌ Não identifiquei o aluno.")
            continue

        if not materia:
            print("❌ Não identifiquei a matéria.")
            continue

        bimestres = [bimestre] if bimestre else ["1", "2"]
        consultar_notas(db, aluno, materia, bimestres)


# ============================================================
# Execução direta
# ============================================================
if __name__ == "__main__":
    conn = sqlite3.connect("database.db")
    db = conn.cursor()

    iniciar_chatbot(db, aluno_logado="Pedro", pode_ver_todos=True)

    conn.close()
