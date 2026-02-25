# 🎓 PIM II - Sistema de Gestão Educacional

**Disciplina:** PIM II - Projeto Interdisciplinar II  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Semestre:** 2º/2025  
**Instituição:** UNIP

## 📋 Sobre o Projeto

Este é o projeto de grade curricular, PIM II, um **Sistema de Gestão Educacional** desenvolvido contendo uma CLI **C** e uma app Desktop em **Python**. O sistema foi criado para gerenciar uma instituição de ensino, controlando alunos, professores, disciplinas e matrículas.

## 🚀 Funcionalidades Principais

### 👨‍🎓 Módulo de Alunos
- Cadastro de alunos com dados completos
- Controle de matrículas e situações
- Histórico acadêmico

### 👨‍🏫 Módulo de Professores  
- Cadastro de professores 
- Vinculação de professores às disciplinas


## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade | Arquivos |
|------------|-------------|----------|
| `C` | Linguagem principal e parte crítica lógica de negócio | `main.c`, `adm.c` |
| `Python` | App con Interface gráfica | `interface.py` |
| `SQLite` | Banco de dados embutido |

## 🏗️ Estrutura do Projeto
PIM-II/
├── main.c # Ponto de entrada do sistema em C
├── adm.c # Funções administrativas e CRUD
├── interface.py # Interface gráfica em Python
├── controllers.py # Controladores para consultas no banco de dados em python
└── database.db # Banco de dados SQLite (gerado)

## 📦 Como Executar o Projeto

### Pré-requisitos
- GCC (compilador C)
- Python 3.x
- Bibliotecas Python: `tkinter`, `tkintercustom`, `sqlite3`

### 🚀 Execução Passo a Passo

1. **Compilar o código C:**
   
   gcc -o sistema main.c adm.c sqlite3.c 

2. **Executar Interface em C**

    python3 interface.py

🎯 Funcionalidades Detalhadas

CLI (C)

    main.c: Menu CLI principal e fluxo do sistema

    adm.c: Operações de CRUD (Create, Read, Update, Delete)

    Gestão de Alunos e Professores.

APP Desktop (Python)

    interface.py: Interface gráfica com Tkinter

    controllers.py: Consultar no banco de dados

    Formulários intuitivos para todas as operações


📊 Estrutura do Banco de Dados

O sistema utiliza SQLite com tabelas para:

    Alunos: matrícula, nome, matricula, etc.

    Professores: nome, disciplina, etc.

🤝 Como Contribuir

Se você é um colega de classe ou está interessado no projeto:

    Faça um fork do repositório

    Crie uma branch para sua feature (git checkout -b feature/novaFuncionalidade)

    Commit suas mudanças (git commit -m 'Add nova funcionalidade')

    Push para a branch (git push origin feature/novaFuncionalidade)

    Abra um Pull Request

⚠️ Observações Importantes

    Este é um projeto acadêmico, desenvolvido para fins educacionais

    O código pode conter simplificações próprias de um projeto universitário

    Sistema desenvolvido para rodar em ambiente Windows 11
