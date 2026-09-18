#include <stdio.h>

int main(void) {
    int sw_v0 = 0;
    float sw_v1 = 0;
    printf("%s", "Repeticoes: ");
    fflush(stdout);
    if (scanf("%d", &sw_v0) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 4): esperado valor numerico.\n");
        return 1;
    }
    printf("%s", "Nivel inicial: ");
    fflush(stdout);
    if (scanf("%f", &sw_v1) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 5): esperado valor numerico.\n");
        return 1;
    }
    while (sw_v0 > 0) {
        printf("%d", sw_v0);
        printf("\n");
        sw_v1 = (sw_v1 + (2 * 1.5f));
        sw_v0 = (sw_v0 - 1);
    }
    printf("%s", "Resultado: ");
    printf("%d", (2 + (3 * 4)));
    printf("%s", " / ");
    printf("%d", ((2 + 3) * 4));
    printf("\n");
    if (sw_v1 >= 10) {
        int sw_v2 = 1;
        printf("%s", "acesso liberado\n");
        printf("%s", "Codigo: ");
        printf("%d", sw_v2);
        printf("\n");
    } else {
        int sw_v3 = 0;
        printf("%s", "acesso negado\n");
        printf("%s", "Codigo: ");
        printf("%d", sw_v3);
        printf("\n");
    }
    printf("%s", "Nivel: ");
    printf("%g", (double)(sw_v1));
    printf("\n");
    return 0;
}
