#include "adm.h"
#include "main.h"
#include "professor.h"

void dar_nota(sqlite3 *db, char *cpf, float nota, int coluna) {
    char *erro = 0;
    char sql[500];
    
    // Verificar se a nota está no intervalo válido (0-10)
    if(nota < 0 || nota > 10) {
        printf("Nota inválida! Deve ser entre 0 e 10.\n");
        return;
    }
    
    // Montar a query UPDATE
    snprintf(sql, sizeof(sql), "UPDATE alunos SET %s = %.1f WHERE cpf = '%s';", coluna, nota, cpf);
    
    int rc = sqlite3_exec(db, sql, 0, 0, &erro);
    
    if(rc != SQLITE_OK) {
        printf("Erro ao dar nota: %s\n", erro);
        sqlite3_free(erro);
    } else {
        int linhas_afetadas = sqlite3_changes(db);
        if(linhas_afetadas > 0) {
            printf("Nota %.1f atribuída com sucesso para %s!\n", 
                   nota, cpf);
        } else {
            printf("Nenhum aluno encontrado com cpf '%s'\n", cpf);
        }
    }
}
