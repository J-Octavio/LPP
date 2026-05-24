#include <stdio.h>
#include <string.h>
#include <ctype.h>

int contarDigitos(const char *str, int indice) {
    if (str[indice] == '\0') {
        return 0;
    }
    int ehDigito = isdigit(str[indice]) ? 1 : 0;
    return ehDigito + contarDigitos(str, indice + 1);
}

int main() {
    // 1. DECLARACAO VS. INSTRUCAO
    char senha[100];
    int tamanhoMinimo = 8;

    printf("--- Validador de Senha Forte ---\n");
    printf("A senha deve conter no minimo %d caracteres, letras maiusculas, minusculas, numeros e caracteres especiais.\n", tamanhoMinimo);
    printf("Digite a senha: ");

    // Instrucao de leitura
    fgets(senha, sizeof(senha), stdin);

    // Mutabilidade: removendo a quebra de linha inserida pelo fgets
    senha[strcspn(senha, "\n")] = '\0';

    // 2. ESTADO
    int tamanhoAtual = strlen(senha);
    int temMaiuscula = 0;
    int temMinuscula = 0;
    int temEspecial = 0;

    // 3. ITERACAO E CONTROLE DE FLUXO (Mutabilidade em acao)
    for (int i = 0; i < tamanhoAtual; i++) {
        if (isupper(senha[i])) {
            temMaiuscula = 1;
        } else if (islower(senha[i])) {
            temMinuscula = 1;
        } else if (ispunct(senha[i])) {
            temEspecial = 1;
        }
    }

    // 4. RECURSAO
    int totalDigitos = contarDigitos(senha, 0);
    int temNumero = (totalDigitos > 0) ? 1 : 0;

    // Avaliacao final do estado para determinar o fluxo de saida
    printf("\n--- Relatorio de Validacao ---\n");
    if (tamanhoAtual >= tamanhoMinimo && temMaiuscula && temMinuscula && temNumero && temEspecial) {
        printf("[OK] Senha valida e forte!\n");
    } else {
        printf("[ERRO] Senha fraca. Verifique os criterios pendentes:\n");
        if (tamanhoAtual < tamanhoMinimo) printf(" - Faltam caracteres (Tamanho atual: %d)\n", tamanhoAtual);
        if (!temMaiuscula) printf(" - Falta pelo menos uma letra maiuscula.\n");
        if (!temMinuscula) printf(" - Falta pelo menos uma letra minuscula.\n");
        if (!temNumero) printf(" - Falta pelo menos um numero.\n");
        if (!temEspecial) printf(" - Falta pelo menos um caractere especial.\n");
    }

    return 0; // Altera o estado do sistema operacional informando que o programa terminou com sucesso
}
