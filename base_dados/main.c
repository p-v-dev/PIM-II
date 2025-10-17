#include "main.h"

sqlite3 *db;

void menu_adm(){
    int opt_menu;

    while(1){

        
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
                printf("Senha: ");
                scanf("%s", aluno.senha);
                getchar();
                printf("---------------------\n");
                printf("Email: ");
                scanf("%s", aluno.email);
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
                scanf("%s", aluno.endereco);
                getchar();
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
                printf("Senha: ");
                scanf("%s", professor.senha);
                getchar();
                printf("---------------------\n");
                printf("Email: ");
                scanf("%s", professor.email);
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
                scanf("%s", professor.endereco);
                getchar();
                printf("---------------------\n");
                printf("Disciplina: ");
                scanf("%s", professor.disciplina);
                getchar();
                printf("---------------------\n");

                incluir_professor(db, professor);
                break;
            }
            case 6: {
                Admnistrador administrador;  // Corrigido o nome
        
                printf("======ADICIONAR ADMINISTRADOR======\n");
                printf("Nome: ");
                scanf("%s", administrador.nome);
                getchar();
                printf("---------------------\n");
                printf("Sobrenome: ");
                scanf("%s", administrador.sobrenome);
                getchar();
                printf("---------------------\n");
                printf("Senha: ");
                scanf("%s", administrador.senha);
                getchar();
                printf("---------------------\n");
                printf("Email: ");
                scanf("%s", administrador.email);
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
                scanf("%s", administrador.endereco);
                getchar();
                printf("---------------------\n");

                incluir_administrador(db, administrador);
                break;
            }
            case 7: {
                char nome[CAMPO_LONGO]; 

                printf("======EXCLUIR ALUNO======\n");
                printf("Nome: ");
                scanf("%s", nome);
                getchar();
                printf("---------------------\n");
                excluir_aluno(db, nome);
                
                break;
            }
            case 8: {
                char nome_prof[CAMPO_LONGO];  // Nome diferente para evitar conflito
                printf("======EXCLUIR PROFESSOR======\n");
                printf("Nome: ");
                scanf("%s", nome_prof);
                getchar();
                printf("---------------------\n");
                excluir_professor(db, nome_prof);
               
                break;
            }
            case 9: {
                char nome_adm[CAMPO_LONGO];  // Nome diferente para evitar conflito
                printf("======EXCLUIR ADMINISTRADOR======\n");
                printf("Nome: ");
                scanf("%s", nome_adm);
                getchar();
                printf("---------------------\n");
                excluir_administrador(db, nome_adm);
               
                break;
            }
        }
    }
}

void menu_professor(){
    int opt_menu;

    while(1){
        printf("======MENU======\n");
        printf("1. Listar alunos\n");
        printf("2. Dar nota\n");
        printf("3. Sair\n");
        printf(">>");
        scanf("%d", &opt_menu);
        getchar(); 
        printf("---------------------\n");

        if(opt_menu == 3){  // Corrigido: deve ser 3, não 10
            printf("Saindo...\n");
            return;
        }

        switch (opt_menu) {
            case 1:
                listar_alunos(db);
                
                break;

            case 2: {
                int opt_disciplina;
                printf("======SELECIONE A DISCIPLINA======\n");
                printf("1. Programacao estruturada em C\n");
                printf("2. Estruturas e Algoritmos em Python\n");
                printf("3. Engenharia de Software Agil\n");
                printf("4. Inteligencia Artificial\n");
                printf(">>");
                scanf("%d", &opt_disciplina);
                getchar();
                printf("---------------------\n");

                char cpf[15];
                printf("======SELECAO DE ALUNO======\n");
                printf("Digite o CPF do aluno:\n");
                printf(">>");
                scanf("%14s", cpf);  // Corrigido: %s para string, não %d
                getchar();
                printf("---------------------\n");

                int bim;
                printf("======BIMESTRE======\n");
                printf("Bimestre 1 ou Bimestre 2?\n");
                printf(">>");
                scanf("%d", &bim);
                getchar();
                printf("---------------------\n");

                float nota;
                printf("======NOTA======\n");
                printf("Digite a nota do bimestre:\n");
                printf(">>");
                scanf("%f", &nota);  // Corrigido: %f para float, não %d
                getchar();
                printf("---------------------\n");

                // SELECAO BIMESTRE 1 OU 2
                switch(bim){
                    case 1:
                        // SELECAO DISCIPLINA
                        switch (opt_disciplina) {
                            case 1:
                                dar_nota(db, cpf, nota, 7);
                                break;
                            case 2:
                                dar_nota(db, cpf, nota, 9);
                                break;
                            case 3:
                                dar_nota(db, cpf, nota, 11);
                                break;
                            case 4:
                                dar_nota(db, cpf, nota, 13);
                                break;
                        }
                        break;    

                    case 2:
                        switch (opt_disciplina) {
                            case 1:
                                dar_nota(db, cpf, nota, 8);
                                break;
                            case 2:
                                dar_nota(db, cpf, nota, 10);
                                break;
                            case 3:
                                dar_nota(db, cpf, nota, 12);
                                break;
                            case 4:
                                dar_nota(db, cpf, nota, 14);
                                break;
                        }
                        break;
                }
                break;
            }
        }
    }
}

int main(){
    if(sqlite3_open("database.db", &db) == SQLITE_OK){
        printf("Entrar como:\n");
        printf("1. Professor\n");   
        printf("2. Administrador\n");
        printf(">>");
        int sw;
        scanf("%d", &sw);
        getchar();
        
        switch(sw){
            case 1:
                menu_professor();
                break;

            case 2:
                menu_adm();
                break;
        }
        
        sqlite3_close(db);  // Fechar o banco de dados
    } else {
        printf("Erro ao abrir o banco de dados!\n");
        return 1;
    }

    return 0;
}