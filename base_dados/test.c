#include <stdio.h>
#include <time.h>

#define BOOL int
#define TRUE 1
#define FALSE 0
#define NOME 50

struct aluno{
    char matricula;
    char nome[NOME];
    char turma[NOME];
    //char senha[30];
};

struct professor{
    char nome[NOME];
    char email[30];
    char disciplina[30];
    char senha[30];
};

struct turma{
    char nome[NOME];
<<<<<<< Updated upstream
    int quantidade_alunos;
};

struct atividade{
    char titulo[NOME];
    char descricao[150];
    char nome_turma[NOME];
    BOOL status;
    time_t data_expiracao;
};
=======
    char turma[NOME];
    char senha[20];
    Disciplina disciplinas[10];
}Aluno;

int qtd;

// struct atividade{
//     char titulo[NOME];
//     char descricao[150];
//     char turma[NOME];
//     char status[20];
//     time_t data_expiracao;
// };
>>>>>>> Stashed changes


int main(){

<<<<<<< Updated upstream
}

void incluir_aluno(){

}

void incluir_professor(){

}

void criar_turma(){

}

// void criar_atividade(){

=======
    int escolha;

     while (escolha != 7){
        menu();
        scanf("%d", &escolha);

        switch (escolha)
        {
        //cadastrar novo aluno
        case 1:
            
            printf("Quantos alunos deseja incluir?");
            scanf("%i", &qtd);
            // loop for cadastrando os alunos
            
            break;

        //deletar aluno
        case 2:
            // aaaa
            break;

        //listar alunos
        case 3:
            // listar todos os alunos de uma turma
            break;
        case 4:
            printf("Quantos professores deseja incluir?");
            scanf("%i", &qtd);
            // for loop incluindo cadastro dos professores
            break;
        case 5:
            // aaaa
            break;
        case 6:
            // aaaa
            break;
        
        case 7:
            printf("Saindo...");
            break;
        default:
            printf("Opção inválida! Tente novamente.\n");
        }
    }
}

void menu(){
    int opt;
    printf("\n=== SISTEMA DE GESTÃO ===\n");
    printf("1. Cadastrar novo aluno\n");
    //printf("2
    printf("3. Listar todos os alunos da turma\n");
    printf("4. Cadastrar novo professor\n");
    printf("5. Listar todos os professor\n");
    //printf("6. Deletar professor\n");
    printf("7. Sair\n");
    printf("Escolha uma opção: ");
    scanf("%i\n", &opt);
}


//PROTOTIPO
// void incluir_aluno(char matricula, char nome, char turma){
//     Aluno aluno;

//     aluno.disciplinas;
//     aluno.matricula;
//     aluno.nome;
//     aluno.turma;


>>>>>>> Stashed changes
// }

