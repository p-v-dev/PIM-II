#ifndef MAIN_H
#define MAIN_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#define CAMPO_LONGO 80
#define CAMPO_CURTO 40

typedef struct{
    int id;
    char nome[CAMPO_LONGO];
    char sobrenome [CAMPO_LONGO];
    char senha[CAMPO_CURTO];
    char email[CAMPO_LONGO];
    char rg[CAMPO_CURTO];
    char cpf[CAMPO_CURTO];
    char disciplina[CAMPO_CURTO];
    char endereco[CAMPO_LONGO];
} Professor;

typedef struct{
    int id;
    char nome[CAMPO_LONGO];
    char sobrenome [CAMPO_LONGO];
    char senha[CAMPO_CURTO];
    char email[CAMPO_LONGO];
    char rg[CAMPO_CURTO];
    char cpf[CAMPO_CURTO];
    char endereco[CAMPO_LONGO];
} Admnistrador;

typedef struct{
    int id;
    char nome[CAMPO_LONGO];
    char sobrenome [CAMPO_LONGO];
    char senha[CAMPO_CURTO];
    char email[CAMPO_LONGO];
    char rg[CAMPO_CURTO];
    char cpf[CAMPO_CURTO];
    char endereco[CAMPO_LONGO];
    float ling_estc_bim1;
    float ling_estc_bim2;
    float python_bim1; 
    float python_bim2;
    float eng_soft_bim1; 
    float eng_soft_bim2; 
    float ia_bim1; 
    float ia_bim2;
} Aluno;

#include "sqlite3.h"
#include "adm.h"
#include "professor.h"

void menu_adm();
void menu_professor();

#endif