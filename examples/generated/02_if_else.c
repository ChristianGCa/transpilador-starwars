#include <stdio.h>

int main(void) {
    int sw_v0 = 0;
    printf("%s", "Nível do cristal kyber (0 a 10): ");
    fflush(stdout);
    if (scanf("%d", &sw_v0) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 6): esperado valor numerico.\n");
        return 1;
    }
    int sw_v1 = (sw_v0 + (3 * 4));
    int sw_v2 = ((sw_v0 + 3) * 4);
    printf("%s", "\nnível + 3 * 4 = ");
    printf("%d", sw_v1);
    printf("\n");
    printf("%s", "(nível + 3) * 4 = ");
    printf("%d", sw_v2);
    printf("\n");
    if (sw_v2 >= 40) {
        printf("%s", "O sabre de luz acendeu!\n");
    } else {
        printf("%s", "O cristal ainda está fraco: são necessários 40 de energia.\n");
    }
    return 0;
}
