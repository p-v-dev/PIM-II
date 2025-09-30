#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINHA 1024
#define DELIMITADOR ";"
#define CSV_ARQUIVO "dados.csv"

//armazenar um usuario

typedef struct {
    char nome[100];
    int idade;
} Pessoa;

// Inserir novo usuario

void inserir_pessoa(const char *nome, int idade) {
    FILE *arquivo = fopen(CSV_ARQUIVO, "a");
    if (arquivo == NULL) {
        perror("Erro ao abrir o arquivo");
        return;
    }

    fprintf(arquivo, "%s;%d\n", nome, idade);
    fclose(arquivo);
    printf("Pessoa inserida com sucesso.\n");
}

// Função para buscar usurio pelo nome

int buscar_pessoa(const char *nome_busca, Pessoa *pessoa_encontrada) {
    FILE *arquivo = fopen(CSV_ARQUIVO, "r");
    if (arquivo == NULL) {
        perror("Erro ao abrir o arquivo");
        return 0;
    }

    char linha[MAX_LINHA];
    while (fgets(linha, MAX_LINHA, arquivo)) {
        char *nome = strtok(linha, DELIMITADOR);
        char *idade_str = strtok(NULL, DELIMITADOR);

        if (nome && idade_str && strcmp(nome, nome_busca) == 0) {
            strcpy(pessoa_encontrada->nome, nome);
            pessoa_encontrada->idade = atoi(idade_str);
            fclose(arquivo);
            return 1; // Encontrado
        }
    }

    fclose(arquivo);
    return 0; // Não encontrado
}

// Função para editar um usuario existente

int editar_pessoa(const char *nome_busca, const char *novo_nome, int nova_idade) {
    FILE *arquivo = fopen(CSV_ARQUIVO, "r");
    FILE *temp = fopen("temp.csv", "w");
    int editado = 0;

    if (arquivo == NULL || temp == NULL) {
        perror("Erro ao abrir os arquivos");
        return 0;
    }

    char linha[MAX_LINHA];
    while (fgets(linha, MAX_LINHA, arquivo)) {
        char linha_copia[MAX_LINHA];
        strcpy(linha_copia, linha); // Para preservar a linha original caso não seja editada

        char *nome = strtok(linha, DELIMITADOR);
        char *idade_str = strtok(NULL, DELIMITADOR);

        if (nome && idade_str && strcmp(nome, nome_busca) == 0) {
            fprintf(temp, "%s;%d\n", novo_nome, nova_idade);
            editado = 1;
        } else {
            fputs(linha_copia, temp);
        }
    }

    fclose(arquivo);
    fclose(temp);

    // Substitui o original pelo temporário

    remove(CSV_ARQUIVO);
    rename("temp.csv", CSV_ARQUIVO);

    if (editado) {
        printf("Pessoa '%s' editada com sucesso.\n", nome_busca);
    } else {
        printf("Pessoa '%s' não encontrada para edição.\n", nome_busca);
    }

    return editado;
}

// Função principal para testes

int main() {
    // Inserindo dados
    inserir_pessoa("João", 12);
    inserir_pessoa("Maria", 13);

    // Buscando usuario
    Pessoa encontrada;
    if (buscar_pessoa("Maria", &encontrada)) {
        printf("Encontrado: %s tem %d anos.\n", encontrada.nome, encontrada.idade);
    } else {
        printf("Pessoa não encontrada.\n");
    }

    // Editando usuario
    editar_pessoa("João", "João Silva", 14);

    return 0;
}