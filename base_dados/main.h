#ifndef MAIN_H
#define MAIN_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#define CAMPO_LONGO 80
#define CAMPO_CURTO 40
#define SALT "abds14"
#define MAX_EMAIL 100
#define MAX_SENHA 50
#define MAX_HASH 20

typedef struct{
    int id;
    char nome[CAMPO_LONGO];
    char sobrenome [CAMPO_LONGO];
    char disciplina[CAMPO_CURTO];
    char email[CAMPO_LONGO];
    char senha[CAMPO_CURTO];
    char rg[CAMPO_CURTO];
    char cpf[CAMPO_CURTO];  
    char endereco[CAMPO_LONGO];
} Professor;

typedef struct{
    int id;
    char nome[CAMPO_LONGO];
    char sobrenome [CAMPO_LONGO];
    char email[CAMPO_LONGO];
    char senha[CAMPO_CURTO];
    char rg[CAMPO_CURTO];
    char cpf[CAMPO_CURTO];
    char endereco[CAMPO_LONGO];
} Administrador;

typedef struct{
    int id;
    char nome[CAMPO_LONGO];
    char sobrenome [CAMPO_LONGO];
    char matricula[CAMPO_CURTO];
    char turma[CAMPO_CURTO];
    char email[CAMPO_LONGO];
    char senha[CAMPO_CURTO];
    char rg[CAMPO_CURTO];
    char cpf[CAMPO_CURTO];
    char endereco[CAMPO_LONGO];
    int faltas;
    float ling_est_c_bim1;
    float ling_est_c_bim2;
    float ling_est_c_media;
    float python_bim1; 
    float python_bim2;
    float python_media;
    float eng_soft_bim1; 
    float eng_soft_bim2; 
    float eng_soft_media; 
    float ia_bim1; 
    float ia_bim2;
    float ia_media;
} Aluno;

#include "sqlite3.h"
#include "adm.h"

void menu_adm();
void hash_simples(const char *senha, char *hash_resultado);


#endif