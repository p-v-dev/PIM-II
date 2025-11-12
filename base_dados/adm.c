#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "adm.h"
#include "main.h"

//OPERACOES ALUNOS

void incluir_aluno(sqlite3 *db, Aluno aluno){
    char sql[1000];
    char *erro = 0;
    char senha_db[20]; 

    // Faz hash da senha
    hash_simples(aluno.senha, senha_db);
    
    // Query corrigida 
    snprintf(sql, sizeof(sql),"INSERT INTO alunos_nova (nome, sobrenome, matricula, email, senha, rg, cpf, endereco, turma) VALUES('%s', '%s','%s', '%s','%s','%s','%s', '%s', '%s')", 
        aluno.nome,  
        aluno.sobrenome, 
        aluno.matricula,
        aluno.email,
        senha_db, 
        aluno.rg, 
        aluno.cpf, 
        aluno.endereco,
        aluno.turma
    );

    int add_aluno = sqlite3_exec(db, sql, 0, 0, &erro);

    if(add_aluno != SQLITE_OK) {
        printf("Erro ao adicionar aluno: %s\n", erro);
        sqlite3_free(erro);
    } else {
        printf("Aluno '%s' adicionado com sucesso!\n", aluno.nome);
    }
}

void listar_alunos(sqlite3 *db){
    sqlite3_stmt *stmt;
    const char *sql = "SELECT * FROM alunos_nova";
    
    printf("\n=== ALUNOS ===\n");
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        fprintf(stderr, "Erro ao preparar SELECT alunos: %s\n", sqlite3_errmsg(db));
        return;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        printf("ID: %d\n", sqlite3_column_int(stmt, 0));
        printf("Nome: %s\n", sqlite3_column_text(stmt, 1));
        printf("Sobrenome: %s\n", sqlite3_column_text(stmt, 2));
        printf("Matricula: %s\n", sqlite3_column_text(stmt, 3));
        printf("Turma: %s\n", sqlite3_column_text(stmt, 4));
        printf("Email: %s\n", sqlite3_column_text(stmt, 5));
        printf("Senha: %s\n", sqlite3_column_text(stmt, 6));
        printf("RG: %s\n", sqlite3_column_text(stmt, 7));
        printf("Cpf: %s\n", sqlite3_column_text(stmt, 8));
        printf("Endereco: %s\n", sqlite3_column_text(stmt, 9));
        printf("Faltas: %d\n", sqlite3_column_int(stmt, 10));
        printf("Linguagem C - Bim1: %.1f\n", sqlite3_column_double(stmt, 11));
        printf("Linguagem C - Bim2: %.1f\n", sqlite3_column_double(stmt, 12));
        printf("Linguagem C - Media: %.1f\n", sqlite3_column_double(stmt, 13));
        printf("Python - Bim1: %.1f\n", sqlite3_column_double(stmt, 14));
        printf("Python - Bim2: %.1f\n", sqlite3_column_double(stmt, 15));
        printf("Python - Media: %.1f\n", sqlite3_column_double(stmt, 16));
        printf("Engenharia Software - Bim1: %.1f\n", sqlite3_column_double(stmt, 17));
        printf("Engenharia Software - Bim2: %.1f\n", sqlite3_column_double(stmt, 18));
        printf("Engenharia Software - Media: %.1f\n", sqlite3_column_double(stmt, 19));
        printf("Inteligencia Artificial - Bim1: %.1f\n", sqlite3_column_double(stmt, 20));
        printf("Inteligencia Artificial - Bim2: %.1f\n", sqlite3_column_double(stmt, 21));
        printf("Inteligencia Artificial - Media: %.1f\n", sqlite3_column_double(stmt, 22));
        printf("----------------------------------------\n");
    }
    
    sqlite3_finalize(stmt);
}

void excluir_aluno(sqlite3 *db, const char *matricula){
    char sql[200];
    char *erro = 0;

    snprintf(sql, sizeof(sql), "DELETE FROM alunos_nova WHERE matricula = '%s';", matricula);

    int excluir_aluno = sqlite3_exec(db, sql, 0, 0, &erro);

    if(excluir_aluno != SQLITE_OK) {
        printf("Erro ao excluir aluno: %s\n", erro);
        sqlite3_free(erro);
    } else {
        int linhas_afetadas = sqlite3_changes(db);
        if(linhas_afetadas > 0) {
            printf("Aluno com matrícula '%s' excluído com sucesso! (%d registro(s) removido(s))\n", matricula, linhas_afetadas);
        } else {
            printf("Nenhum aluno encontrado com matrícula '%s'\n", matricula);
        }
    }
}   

// OPERACOES PROFESSORES

void incluir_professor(sqlite3 *db, Professor professor){
    char sql[1000];
    char *erro = 0;
    char senha_db[20];

    // Faz hash da senha
    hash_simples(professor.senha, senha_db);
    
    snprintf(sql, sizeof(sql), 
    "INSERT INTO professores (nome, sobrenome, disciplina, email, senha, rg, cpf, endereco) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');",
        professor.nome, 
        professor.sobrenome, 
        professor.disciplina,
        professor.email,
        senha_db, 
        professor.rg,  
        professor.cpf, 
        professor.endereco 
    );

    int add_prof = sqlite3_exec(db, sql, 0, 0, &erro);

    if(add_prof != SQLITE_OK) {
        printf("Erro ao adicionar professor: %s\n", erro);
        sqlite3_free(erro);
    } else {
        printf("Professor '%s' adicionado com sucesso!\n", professor.nome);
    }
}

void listar_professores(sqlite3 *db){
    sqlite3_stmt *stmt;
    const char *sql = "SELECT * FROM professores";
    
    printf("\n=== PROFESSORES ===\n");
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        fprintf(stderr, "Erro ao preparar SELECT professores: %s\n", sqlite3_errmsg(db));
        return;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        printf("ID: %d\n", sqlite3_column_int(stmt, 0));
        printf("Nome: %s\n", sqlite3_column_text(stmt, 1));
        printf("Sobrenome: %s\n", sqlite3_column_text(stmt, 2));
        printf("Disciplina: %s\n", sqlite3_column_text(stmt, 3));
        printf("Email: %s\n", sqlite3_column_text(stmt, 4));
        printf("Senha: %s\n", sqlite3_column_text(stmt, 5));
        printf("RG: %s\n", sqlite3_column_text(stmt, 6));
        printf("CPF: %s\n", sqlite3_column_text(stmt, 7));
        printf("Endereco: %s\n", sqlite3_column_text(stmt, 8));
        printf("----------------------------------------\n");
    }
    
    sqlite3_finalize(stmt);
}

void excluir_professor(sqlite3 *db, const char *email){
    char sql[200];
    char *erro = 0;
    
    snprintf(sql, sizeof(sql), "DELETE FROM professores WHERE email = '%s';", email);
    
    int deletar_professor = sqlite3_exec(db, sql, 0, 0, &erro);
    
    if(deletar_professor != SQLITE_OK) {
        printf("Erro ao excluir professor: %s\n", erro);
        sqlite3_free(erro);
    } else {
        int linhas_afetadas = sqlite3_changes(db);
        if(linhas_afetadas > 0) {
            printf("Professor com email '%s' excluído com sucesso! (%d registro(s) removido(s))\n", email, linhas_afetadas);
        } else {
            printf("Nenhum professor encontrado com email '%s'\n", email);
        }
    }
}

//OPERACOES ADMS

void incluir_administrador(sqlite3 *db, Administrador administrador) {
    char sql[1000];
    char *erro = 0;
    char senha_db[20];

    // Faz hash da senha
    hash_simples(administrador.senha, senha_db);
    
    snprintf(sql, sizeof(sql), 
    "INSERT INTO administradores (nome, sobrenome, email, senha, rg, cpf, endereco) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');", 
        administrador.nome, 
        administrador.sobrenome,
        administrador.email, 
        senha_db, 
        administrador.rg, 
        administrador.cpf, 
        administrador.endereco
    );
    
    int add_adm = sqlite3_exec(db, sql, 0, 0, &erro);
    
    if(add_adm != SQLITE_OK) {
        printf("Erro ao adicionar administrador: %s\n", erro);
        sqlite3_free(erro);
    } else {
        printf("Administrador '%s' adicionado com sucesso!\n", administrador.nome);
    }
}

void listar_administradores(sqlite3 *db) {
    sqlite3_stmt *stmt;
    const char *sql = "SELECT * FROM administradores";
    
    printf("\n=== ADMINISTRADORES ===\n");
    
    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        fprintf(stderr, "Erro ao preparar SELECT administradores: %s\n", sqlite3_errmsg(db));
        return;
    }
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        printf("ID: %d\n", sqlite3_column_int(stmt, 0));
        printf("Nome: %s\n", sqlite3_column_text(stmt, 1));
        printf("Sobrenome: %s\n", sqlite3_column_text(stmt, 2));
        printf("Email: %s\n", sqlite3_column_text(stmt, 3));
        printf("Senha: %s\n", sqlite3_column_text(stmt, 4));
        printf("RG: %s\n", sqlite3_column_text(stmt, 5));
        printf("CPF: %s\n", sqlite3_column_text(stmt, 6));
        printf("Endereco: %s\n", sqlite3_column_text(stmt, 7));
        printf("----------------------------------------\n");
    }
    
    sqlite3_finalize(stmt);
}

void excluir_administrador(sqlite3 *db, const char *email) {
    char sql[200];
    char *erro = 0;
    
    snprintf(sql, sizeof(sql), "DELETE FROM administradores WHERE email = '%s';", email);
    
    int rc = sqlite3_exec(db, sql, 0, 0, &erro);
    
    if(rc != SQLITE_OK) {
        printf("Erro ao excluir administrador: %s\n", erro);
        sqlite3_free(erro);
    } else {
        int linhas_afetadas = sqlite3_changes(db);
        if(linhas_afetadas > 0) {
            printf("Administrador com email '%s' excluído com sucesso! (%d registro(s) removido(s))\n", email, linhas_afetadas);
        } else {
            printf("Nenhum administrador encontrado com email '%s'\n", email);
        }
    }
}