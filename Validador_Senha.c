#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

// Protótipo (Declaração)
bool validar_senha(char s[], int i, bool tem_mai, bool tem_min, bool tem_num);

int main() {
    // Declaração de variáveis (Estado inicial)
    char senha[100];

    printf("Digite sua senha: ");
    scanf("%99s", senha);

    int tamanho = strlen(senha);

    // Instrução de controle (Verificação de tamanho)
    if (tamanho < 8) {
        printf("Estado: Inválida. Motivo: Muito curta.\n");
    } else {
        // Chamada de função que usa recursão para percorrer a string
        if (validar_senha(senha, 0, false, false, false)) {
            printf("Estado: Senha Forte!\n");
        } else {
            printf("Estado: Senha Fraca. Requisitos não atendidos.\n");
        }
    }

    return 0;
}

// Implementação da lógica usando Recursão e Mutabilidade de flags
bool validar_senha(char s[], int i, bool tem_mai, bool tem_min, bool tem_num) {
    // Caso base: fim da string
    if (s[i] == '\0') {
        return tem_mai && tem_min && tem_num;
    }

    // Atualização do estado local baseado no caractere atual (Instruções)
    if (isupper(s[i])) tem_mai = true;
    if (islower(s[i])) tem_min = true;
    if (isdigit(s[i])) tem_num = true;

    // Passo recursivo
    return validar_senha(s, i + 1, tem_mai, tem_min, tem_num);
}