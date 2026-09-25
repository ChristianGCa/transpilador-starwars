#include <stdio.h>

int main(void) {
    int sw_v0 = 0;
    int sw_v1 = 0;
    printf("%s", "Tripulantes a bordo: ");
    fflush(stdout);
    if (scanf("%d", &sw_v0) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 7): esperado valor numerico.\n");
        return 1;
    }
    printf("%s", "Dias de viagem: ");
    fflush(stdout);
    if (scanf("%d", &sw_v1) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 8): esperado valor numerico.\n");
        return 1;
    }
    int sw_v2 = (sw_v0 * sw_v1);
    printf("%s", "\nRações necessárias: ");
    printf("%d", sw_v2);
    printf("\n");
    int sw_v3 = (sw_v2 / 6);
    int sw_v4 = (sw_v2 - (sw_v3 * 6));
    printf("%s", "Caixas de 6 rações: ");
    printf("%d", sw_v3);
    printf("%s", " cheias e ");
    printf("%d", sw_v4);
    printf("%s", " rações avulsas");
    printf("\n");
    float sw_v5 = ((sw_v2 * 2.5f) + 100);
    printf("%s", "Custo total (rações + taxa do porto): ");
    printf("%g", (double)(sw_v5));
    printf("%s", " créditos");
    printf("\n");
    printf("%s", "Custo por tripulante: ");
    printf("%g", (double)((sw_v5 / sw_v0)));
    printf("%s", " créditos");
    printf("\n");
    return 0;
}
