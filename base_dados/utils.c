#include <stdio.h>
#include <string.h>

// SALT fixo
#define SALT "SALT123"

// Função de hash super simples (soma de caracteres + SALT)
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