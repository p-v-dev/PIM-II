#ifndef ADM_H
#define ADM_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sqlite3.h"
#include "main.h"


void listar_alunos(sqlite3 *db);        
void listar_professores(sqlite3 *db);
void listar_administradores(sqlite3 *db);

void incluir_aluno(sqlite3 *db, Aluno aluno);
void incluir_professor(sqlite3 *db, Professor professor);
void incluir_administrador(sqlite3 *db, Admnistrador admnistrador);

void excluir_aluno(sqlite3 *db, const char *nome);        
void excluir_professor(sqlite3 *db, const char *nome);
void excluir_administrador(sqlite3 *db, const char *nome);
#endif 