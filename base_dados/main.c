#include "main.h"

sqlite3 *db;

void menu_adm(){
    int opt_menu;

    //while(1){

        
        printf("======MENU======\n");
        printf("Listar:\n");
        printf("1. alunos\n");
        printf("2. professores\n");
        printf("3. administradores\n");
        printf("\n---------------------\n");
        printf("Adicionar:\n");
        printf("4.  aluno\n");
        printf("5. professor\n");
        printf("6. administrador\n");
        printf("\n---------------------\n");
        printf("Excluir:\n");
        printf("7. aluno\n");
        printf("8. professor\n");
        printf("9. administrador\n");
        printf("\n---------------------\n");
        printf("10. Sair\n");
        printf(">>");
        scanf("%d", &opt_menu);
        getchar(); 

        if(opt_menu == 10){
            printf("Saindo...\n");
            return;
        }

        switch(opt_menu){
            case 1:
                listar_alunos(db);
                break;
            case 2:
                listar_professores(db);
                
                break;
            case 3:
                
                listar_administradores(db);
                break;
            case 4: {
                Aluno aluno;

                printf("======ADICIONAR ALUNO======\n");
                printf("Nome: ");
                scanf("%s", aluno.nome);
                getchar();
                printf("---------------------\n");
                printf("Sobrenome: ");
                scanf("%s", aluno.sobrenome);
                getchar();
                printf("---------------------\n");
                printf("Matricula: ");
                scanf("%s", aluno.matricula);
                getchar();
                printf("---------------------\n");
                printf("Turma: ");
                scanf("%s", aluno.turma);
                getchar();
                printf("---------------------\n");
                printf("Email: ");
                scanf("%s", aluno.email);
                getchar();
                printf("---------------------\n");
                printf("Senha: ");
                scanf("%s", aluno.senha);
                getchar();
                printf("---------------------\n");
                printf("RG: ");
                scanf("%s", aluno.rg);
                getchar();
                printf("---------------------\n");
                printf("CPF: ");
                scanf("%s", aluno.cpf);
                getchar();
                printf("---------------------\n");
                printf("Endereco: ");
                scanf("%99[^\n]", aluno.endereco);
                printf("---------------------\n");
                incluir_aluno(db, aluno);
                break;
            }
            case 5: {
                Professor professor;

                printf("======ADICIONAR PROFESSOR======\n");
                printf("Nome: ");
                scanf("%s", professor.nome);
                getchar();
                printf("---------------------\n");
                printf("Sobrenome: ");
                scanf("%s", professor.sobrenome);
                getchar();
                printf("---------------------\n");
                printf("Disciplina: ");
                scanf("%s", professor.disciplina);
                getchar();
                printf("---------------------\n");
                printf("Email: ");
                scanf("%s", professor.email);
                getchar();
                printf("---------------------\n");
                printf("Senha: ");
                scanf("%s", professor.senha);
                getchar();
                printf("---------------------\n");
                printf("RG: ");
                scanf("%s", professor.rg);
                getchar();  
                printf("---------------------\n");
                printf("CPF: ");
                scanf("%s", professor.cpf);
                getchar();
                printf("---------------------\n");
                printf("Endereco: ");
                scanf("%99[^\n]", professor.endereco);
                getchar();
                printf("---------------------\n");
                incluir_professor(db, professor);
                break;
            }
            case 6: {
                Administrador administrador;  
        
                printf("======ADICIONAR ADMINISTRADOR======\n");
                printf("Nome: ");
                scanf("%s", administrador.nome);
                getchar();
                printf("---------------------\n");
                printf("Sobrenome: ");
                scanf("%s", administrador.sobrenome);
                getchar();
                printf("---------------------\n");
                printf("Email: ");
                scanf("%s", administrador.email);
                getchar();
                printf("---------------------\n");
                printf("Senha: ");
                scanf("%s", administrador.senha);
                getchar();
                printf("---------------------\n");
                printf("RG: ");
                scanf("%s", administrador.rg);
                getchar();  
                printf("---------------------\n");
                printf("CPF: ");
                scanf("%s", administrador.cpf);
                getchar();
                printf("---------------------\n");
                printf("Endereco: ");
                scanf("%99[^\n]", administrador.endereco);
                getchar();
                printf("---------------------\n");
                incluir_administrador(db, administrador);
                break;
            }
            case 7: {
                char matricula[CAMPO_LONGO]; 

                printf("======EXCLUIR ALUNO======\n");
                printf("Matricula: ");
                scanf("%s", matricula);
                getchar();
                printf("---------------------\n");
                excluir_aluno(db, matricula);
                
                break;
            }
            case 8: {
                char email[CAMPO_LONGO];  // Nome diferente para evitar conflito
                printf("======EXCLUIR PROFESSOR======\n");
                printf("Email: ");
                scanf("%s", email);
                getchar();
                printf("---------------------\n");
                excluir_professor(db, email);
               
                break;
            }
            case 9: {
                char email[CAMPO_LONGO];  // Nome diferente para evitar conflito
                printf("======EXCLUIR ADMINISTRADOR======\n");
                printf("Email: ");
                scanf("%s", email);
                getchar();
                printf("---------------------\n");
                excluir_administrador(db, email);
               
                break;
            }
        }
    //}
}

void hash_simples(const char *senha, char *hash_resultado) {
    char combinacao[256];
    int soma = 0;
    int i;
    
  
    snprintf(combinacao, sizeof(combinacao), "%s%s", senha, SALT);
    
    // Soma todos os caracteres
    for(i = 0; combinacao[i] != '\0'; i++) {
        soma += combinacao[i];
    }
    
    // Converter string formato hexadecimal 
    snprintf(hash_resultado, 20, "%x", soma * 123); 
} 

int fazer_login(sqlite3 *db, const char *cpf, const char *senha) {
    sqlite3_stmt *stmt;
    char query[256];
    char hash_senha[MAX_HASH];
    char hash_banco[MAX_HASH];
    int resultado = 0;
    
    // Calcula o hash da senha fornecida
    hash_simples(senha, hash_senha);
    //printf("Hash calculado: %s\n", hash_senha);
    
    // Prepara a query SQL
    snprintf(query, sizeof(query), "SELECT senha FROM administradores WHERE cpf =%s", cpf);
    
    if (sqlite3_prepare_v2(db, query, -1, &stmt, NULL) != SQLITE_OK) {
        fprintf(stderr, "Erro ao preparar query: %s\n", sqlite3_errmsg(db));
        return -1;
    }
    
    // Bind do parâmetro email
    sqlite3_bind_text(stmt, 1, cpf, -1, SQLITE_STATIC);
    
    // Executa a query
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        // Pega o hash do banco de dados
        const char *hash_db = (const char*)sqlite3_column_text(stmt, 0);
        strncpy(hash_banco, hash_db, sizeof(hash_banco) - 1);
        hash_banco[sizeof(hash_banco) - 1] = '\0';
        
       // printf("Hash do banco: %s\n", hash_banco);
        
        // Compara os hashes
        if (strcmp(hash_senha, hash_banco) == 0) {
            printf("Login bem-sucedido!\n");
            resultado = 1; // Login bem-sucedido
        } else {
            printf("Senha incorreta!\n");
            resultado = 0; // Senha incorreta
        }
    } else {
        printf("Usuário não encontrado!\n");
        resultado = -1; // Usuário não encontrado
    }
    
    sqlite3_finalize(stmt);
    return resultado;
}




int main(){
    if(sqlite3_open("database.db", &db) == SQLITE_OK){
        char cpf_login[50];
        char senha_login[50];


        

        printf("===Entrar===\n");
        printf("CPF:\n"); 
        scanf("%s", &cpf_login);  
        getchar();

        printf("Senha:\n");
        scanf("%s", &senha_login);
        getchar();
        
        if(fazer_login(db, cpf_login, senha_login)== 1){
            menu_adm();
        }

        sqlite3_close(db);  // Fechar o banco de dados
    } else {
        printf("Erro ao abrir o banco de dados!\n");
        return 1;
    }

    return 0;
}