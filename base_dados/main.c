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
    int quantidade_alunos;
};

struct atividade{
    char titulo[NOME];
    char descricao[150];
    char nome_turma[NOME];
    BOOL status;
    time_t data_expiracao;
};


int main(){

}

void incluir_aluno(){

}

void incluir_professor(){

}

void criar_turma(){

}

// void criar_atividade(){

// }

//ronaldo

