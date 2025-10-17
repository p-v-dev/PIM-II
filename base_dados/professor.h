#ifndef PROFESSOR_H
#define PROFESSOR_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sqlite3.h"
#include "main.h"


void dar_nota(sqlite3 *db, char *cpf, float nota, int coluna);        




#endif 