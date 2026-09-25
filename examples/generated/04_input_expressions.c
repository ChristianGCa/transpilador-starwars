#include <stdio.h>

int main(void) {
    int sw_v0 = 0;
    int sw_v1 = 0;
    float sw_v2 = 0;
    printf("%s", "Naves na frota: ");
    fflush(stdout);
    if (scanf("%d", &sw_v0) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 6): esperado valor numerico.\n");
        return 1;
    }
    printf("%s", "Tripulantes por nave: ");
    fflush(stdout);
    if (scanf("%d", &sw_v1) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 7): esperado valor numerico.\n");
        return 1;
    }
    printf("%s", "Combustível total (toneladas): ");
    fflush(stdout);
    if (scanf("%f", &sw_v2) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 8): esperado valor numerico.\n");
        return 1;
    }
    int sw_v3 = (sw_v0 * sw_v1);
    printf("%s", "\nTripulação total: ");
    printf("%d", sw_v3);
    printf("\n");
    printf("%s", "Combustível por nave: ");
    printf("%g", (double)((sw_v2 / sw_v0)));
    printf("%s", " t");
    printf("\n");
    int sw_v4 = (sw_v3 / 4);
    int sw_v5 = (sw_v3 - (sw_v4 * 4));
    printf("%s", "Esquadrões de 4 pilotos: ");
    printf("%d", sw_v4);
    printf("%s", " (sobram ");
    printf("%d", sw_v5);
    printf("%s", ")");
    printf("\n");
    return 0;
}
