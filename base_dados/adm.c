#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "adm.h"
#include "main.h"

// menu adm

//void login(){
//     char email_login[31];
//     char senha_login[31];
//     printf("====LOGIN====\n");
//     printf("email:");
//     scanf("%s", &email_login);
//     printf("senha:");
//     scanf("%s", &senha_login);
// }

//OPERACOES ALUNOS

void incluir_aluno(sqlite3 *db, Aluno aluno){
    char sql[1000];
    char *erro = 0;

    Aluno aluno_novo =  aluno;

  
    // precisa fazer hash da senha
    snprintf(sql, sizeof(sql),"INSERT INTO alunos_nova (nome, sobrenome, senha, email, rg, cpf, endereco) VALUES('%s', '%s','%s', '%s','%s','%s')", 
        aluno_novo.nome,  
        aluno_novo.sobrenome, 
        aluno_novo.senha, 
        aluno_novo.email,
        aluno_novo.rg, 
        aluno_novo.cpf, 
        aluno_novo.endereco
    );

    int add_aluno = sqlite3_exec(db, sql, 0, 0, &erro);

    if(add_aluno != SQLITE_OK) {
        printf("Erro ao adicionar aluno: %s\n", erro);
        sqlite3_free(erro);
    } else {
        printf("Aluno '%s' adicionado com sucesso!\n", aluno_novo.nome);
    }
}

void listar_alunos(sqlite3 *db){
    sqlite3_stmt *stmt;
    
    const char *sql_count = "SELECT COUNT(*) FROM alunos_nova;";
    int query_prep = sqlite3_prepare_v2(db, sql_count, -1, &stmt, NULL);
    
    int total_alunos = 0;
    if(sqlite3_step(stmt) == SQLITE_ROW) {
        total_alunos = sqlite3_column_int(stmt, 0);
    }
    sqlite3_finalize(stmt);
    
    printf("Alunos cadastrados: %d\n", total_alunos);
    
    if(total_alunos == 0) {
        printf("tabela vazia. Nenhum aluno.\n");
        return;
    }
    
    //listar alunos
    const char *sql = "SELECT * FROM alunos_nova;";
    query_prep = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);

    if(query_prep != SQLITE_OK) {
        printf("Erro ao preparar query: %s\n", sqlite3_errmsg(db));
        return;
    }

    printf("\n==== DADOS DOS ALUNOS ====\n");

    int alunos_encontrados = 0;
    while(sqlite3_step(stmt) == SQLITE_ROW){
        alunos_encontrados++;
        
        int id = sqlite3_column_int(stmt,0);
        const char *nome = (const char*)sqlite3_column_text(stmt,1);
        const char *sobrenome = (const char*)sqlite3_column_text(stmt,2);
        //const char *senha = (const char*)sqlite3_column_text(stmt, 4);
        const char *email = (const char*)sqlite3_column_text(stmt, 3);
        const char *rg = (const char*)sqlite3_column_text(stmt, 4);
        const char *cpf = (const char*)sqlite3_column_text(stmt, 5);
        const char *endereco = (const char*)sqlite3_column_text(stmt, 6);

        double ling_est_c_bim1 = sqlite3_column_double(stmt, 7);
        double ling_est_c_bim2 = sqlite3_column_double(stmt, 8);
        double python_bim1 = sqlite3_column_double(stmt, 9);
        double python_bim2 = sqlite3_column_double(stmt, 10);
        double eng_soft_bim1 = sqlite3_column_double(stmt, 11);
        double eng_soft_bim2 = sqlite3_column_double(stmt, 12);
        double ia_bim1 = sqlite3_column_double(stmt, 13);
        double ia_bim2 = sqlite3_column_double(stmt, 14);

        printf("ID: %d\n", id);
        printf("Nome: %s\n", nome);
        printf("Sobrenome: %s\n", sobrenome);
        printf("Email: %s\n", email);
        printf("RG: %s\n", rg);
        printf("CPF: %s\n", cpf);
        printf("Endereco: %s\n", endereco);
        printf("Nota Linguagem C Bim1: %.1f\n", ling_est_c_bim1);
        printf("Nota Linguagem C Bim2: %.1f\n", ling_est_c_bim2);
        printf("Nota Python Bim1: %.1f\n", python_bim1);
        printf("Nota Python Bim2: %.1f\n", python_bim2);
        printf("Nota Eng. Software Bim1: %.1f\n", eng_soft_bim1);
        printf("Nota Eng. Software Bim2: %.1f\n", eng_soft_bim2);
        printf("Nota IA Bim1: %.1f\n", ia_bim1);
        printf("Nota IA Bim2: %.1f\n", ia_bim2);
        printf("----------------------------\n");
    }
    
    sqlite3_finalize(stmt);
    
    if(alunos_encontrados == 0) {
        printf("executou mas nao retornou nada\n");
    } else {
        printf("Total de alunos: %d\n", alunos_encontrados);
    }
}
void excluir_aluno(sqlite3 *db, const char *nome){
    char sql[200];
    char *erro = 0;

    snprintf(sql, sizeof(sql), "DELETE FROM alunos_nova WHERE nome = '%s';", nome);

    int excluir_aluno = sqlite3_exec(db, sql, 0, 0, &erro);

    if(excluir_aluno != SQLITE_OK) {
        printf("Erro ao excluir aluno: %s\n", erro);
        sqlite3_free(erro);
    } else {
        int linhas_afetadas = sqlite3_changes(db);
        if(linhas_afetadas > 0) {
            printf("Aluno '%s' excluído com sucesso! (%d registro(s) removido(s))\n", nome, linhas_afetadas);
        } else {
            printf("Nenhum aluno encontrado com nome '%s'\n", nome);
        }
    }

}   

// OPERACOES PROFESSORES

void incluir_professor(sqlite3 *db, Professor professor){
    char sql[1000];
    char *erro = 0;

    Professor professor_novo = professor;

    // precisa fazer hash da senha
    snprintf(sql, sizeof(sql), 
    "INSERT INTO professores (nome, sobrenome, senha, email, rg, cpf,disciplina, endereco, ) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');",
        professor_novo.nome, 
        professor_novo.sobrenome, 
        professor_novo.senha, 
        professor_novo.email,
        professor_novo.rg,  
        professor_novo.cpf, 
        professor_novo.disciplina,
        professor_novo.endereco 
    );

    int add_prof = sqlite3_exec(db, sql, 0, 0, &erro);

    if(add_prof != SQLITE_OK) {
        printf("Erro ao adicionar professor: %s\n", erro);
        sqlite3_free(erro);
    } else {
        printf("Professor '%s' adicionado com sucesso!\n", professor_novo.nome);
    }
}

void listar_professores(sqlite3 *db){
    sqlite3_stmt *stmt;
    const char *sql = "SELECT * FROM professores;";
    
    int query_prep = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    
    if(query_prep != SQLITE_OK) {
        printf("Erro ao preparar query: %s\n", sqlite3_errmsg(db));
        return;
    }
    
    printf("==== LISTA DE PROFESSORES ====\n");
    
    int contador = 0;
    while(sqlite3_step(stmt) == SQLITE_ROW) {
        contador++;
        
        int id = sqlite3_column_int(stmt, 0);
        const char *nome = (const char*)sqlite3_column_text(stmt, 1);
        const char *sobrenome = (const char*)sqlite3_column_text(stmt, 2);
        const char *senha = (const char*)sqlite3_column_text(stmt, 3);
        const char *email = (const char*)sqlite3_column_text(stmt, 4);
        const char *rg = (const char*)sqlite3_column_text(stmt, 5);
        const char *cpf = (const char*)sqlite3_column_text(stmt, 6);
        const char *disciplina = (const char*)sqlite3_column_text(stmt, 7);
        const char *endereco = (const char*)sqlite3_column_text(stmt, 8);
        
        
        printf("ID: %d\n", id);
        printf("Nome: %s\n", nome);
        printf("Sobrenome: %s\n", nome);
        printf("RG: %s\n", rg);
        printf("CPF: %s\n", cpf);
        printf("Email: %s\n", email); 
        printf("Endereço: %s\n", endereco);
        printf("Disciplina: %s\n", disciplina);
        printf("---------------------\n");
    }
    
    sqlite3_finalize(stmt);
    
    if(contador == 0) {
        printf("Nenhum professor cadastrado.\n");
    } else {
        printf("Total de professores: %d\n", contador);
    }
}

void excluir_professor(sqlite3 *db, const char *nome){
    char sql[200];
    char *erro = 0;
    
    snprintf(sql, sizeof(sql), "DELETE FROM professores WHERE nome = '%s';", nome);
    
    int deletar_professor = sqlite3_exec(db, sql, 0, 0, &erro);
    
    if(deletar_professor != SQLITE_OK) {
        printf("Erro ao excluir professor: %s\n", erro);
        sqlite3_free(erro);
    } else {
        int linhas_afetadas = sqlite3_changes(db);
        if(linhas_afetadas > 0) {
            printf("Professor '%s' excluído com sucesso! (%d registro(s) removido(s))\n", nome, linhas_afetadas);
        } else {
            printf("Nenhum professor encontrado com nome '%s'\n", nome);
        }
    }
}

//OPERACOES ADMS

void incluir_administrador(sqlite3 *db, Admnistrador admnistrador) {
    char sql[1000];
    char *erro = 0;
      
    Admnistrador novo_administrador = admnistrador;

    snprintf(sql, sizeof(sql), 
    "INSERT INTO administradores (nome, sobrenome, senha, rg,  cpf,  email, endereco) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');", 
        novo_administrador.nome, 
        novo_administrador.sobrenome,
        novo_administrador.senha, 
        novo_administrador.cpf, 
        novo_administrador.rg, 
        novo_administrador.email, 
        novo_administrador.endereco
    );
    
    int add_adm = sqlite3_exec(db, sql, 0, 0, &erro);
    
    if(add_adm != SQLITE_OK) {
        printf("Erro ao adicionar administrador: %s\n", erro);
        sqlite3_free(erro);
    } else {
        printf("Administrador '%s' adicionado com sucesso!\n", novo_administrador.nome);
    }
}

void listar_administradores(sqlite3 *db) {
    sqlite3_stmt *stmt;
    const char *sql = "SELECT * FROM administradores;";
    
    int query_prep = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    
    if(query_prep != SQLITE_OK) {
        printf("Erro ao preparar query: %s\n", sqlite3_errmsg(db));
        return;
    }
    
    printf("==== LISTA DE ADMINISTRADORES ====\n");
    
    int contador = 0;
    while(sqlite3_step(stmt) == SQLITE_ROW) {
        contador++;
        
        int id = sqlite3_column_int(stmt, 0);
        const char *nome = (const char*)sqlite3_column_text(stmt, 1);
        const char *sobrenome = (const char*)sqlite3_column_text(stmt, 2);
        const char *senha = (const char*)sqlite3_column_text(stmt, 3);
        const char *rg = (const char*)sqlite3_column_text(stmt, 4);
        const char *cpf = (const char*)sqlite3_column_text(stmt, 5);
        const char *email = (const char*)sqlite3_column_text(stmt, 6);
        const char *endereco = (const char*)sqlite3_column_text(stmt, 7);
        
        printf("ID: %d\n", id);
        printf("Nome: %s\n", nome);
        printf("Sobrenome: %s\n", sobrenome);
        printf("Email: %s\n", email);
        printf("CPF: %s\n", cpf);
        printf("RG: %s\n", rg);
        printf("Endereço: %s\n", endereco);
        printf("---------------------\n");
    }
    
    sqlite3_finalize(stmt);
    
    if(contador == 0) {
        printf("Nenhum administrador cadastrado.\n");
    } else {
        printf("Total de administradores: %d\n", contador);
    }
}

void excluir_administrador(sqlite3 *db, const char *nome) {
    char sql[200];
    char *erro = 0;
    
    snprintf(sql, sizeof(sql), "DELETE FROM administradores WHERE nome = '%s';", nome);
    
    int rc = sqlite3_exec(db, sql, 0, 0, &erro);
    
    if(rc != SQLITE_OK) {
        printf("Erro ao excluir administrador: %s\n", erro);
        sqlite3_free(erro);
    } else {
        int linhas_afetadas = sqlite3_changes(db);
        if(linhas_afetadas > 0) {
            printf("Administrador '%s' excluído com sucesso! (%d registro(s) removido(s))\n", nome, linhas_afetadas);
        } else {
            printf("Nenhum administrador encontrado com nome '%s'\n", nome);
        }
    }
}