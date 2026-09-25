#include <stdio.h>
#include <stdlib.h>

int sw_f0(int sw_v0, int sw_v1);
int sw_f1(int sw_v2);
float sw_f2(int sw_v3, float sw_v4);
void sw_f3(float sw_v5);

int sw_f0(int sw_v0, int sw_v1) {
    return (sw_v0 - ((sw_v0 / sw_v1) * sw_v1));
}

int sw_f1(int sw_v2) {
    if (sw_v2 <= 1) {
        return 1;
    } else {
        return (sw_v2 * sw_f1((sw_v2 - 1)));
    }
}

float sw_f2(int sw_v3, float sw_v4) {
    return ((sw_v3 * sw_v4) / 100.0f);
}

void sw_f3(float sw_v5) {
    if (sw_v5 < 0.0f) {
        printf("%s", "\tpatente: inválida\n");
        return;
    }
    if (sw_v5 >= 80.0f) {
        printf("%s", "\tpatente: \"Jedi\"\n");
    } else {
        if (sw_v5 > 50.0f) {
            printf("%s", "\tpatente: Padawan\n");
        } else {
            printf("%s", "\tpatente: Youngling\n");
        }
    }
}

int main(void) {
    int sw_v6 = 0;
    printf("%s", "Quantos pilotos\? ");
    fflush(stdout);
    if (scanf("%d", &sw_v6) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 41): esperado valor numerico.\n");
        return 1;
    }
    float sw_v7 = 0.0f;
    int sw_v8 = 0;
    int sw_v9 = 0;
    for (int sw_v10 = 1, sw_v11 = sw_v6; sw_v10 <= sw_v11; sw_v10++) {
        int sw_v12 = 0;
        float sw_v13 = 0;
        printf("%s", "Piloto ");
        printf("%d", sw_v10);
        printf("%s", ":");
        printf("\n");
        printf("%s", "\tpontos: ");
        fflush(stdout);
        if (scanf("%d", &sw_v12) != 1) {
            fprintf(stderr, "ERRO DE ENTRADA (linha 52): esperado valor numerico.\n");
            return 1;
        }
        printf("%s", "\tprecisão (%): ");
        fflush(stdout);
        if (scanf("%f", &sw_v13) != 1) {
            fprintf(stderr, "ERRO DE ENTRADA (linha 53): esperado valor numerico.\n");
            return 1;
        }
        float sw_v14 = sw_f2(sw_v12, sw_v13);
        printf("%s", "\tnota: ");
        printf("%g", (double)(sw_v14));
        printf("\n");
        sw_f3(sw_v14);
        sw_v7 = (sw_v7 + sw_v14);
        if (sw_f0(sw_v12, 2) == 0) {
            sw_v8 = (sw_v8 + 1);
        }
        if (sw_v12 > sw_v9) {
            sw_v9 = sw_v12;
        }
    }
    if (sw_v6 > 0) {
        float sw_v15 = (sw_v7 / sw_v6);
        printf("%s", "Média do esquadrão: ");
        printf("%g", (double)(sw_v15));
        printf("\n");
        printf("%s", "Pilotos com pontuação par: ");
        printf("%d", sw_v8);
        printf("\n");
        printf("%s", "Melhor pontuação: ");
        printf("%d", sw_v9);
        printf("%s", " (faltam ");
        printf("%d", (100 - sw_v9));
        printf("%s", " para 100)");
        printf("\n");
        printf("%s", "Formações possíveis: ");
        printf("%d", sw_f1(sw_v6));
        printf("\n");
    } else {
        printf("%s", "Nenhum piloto para treinar.\n");
    }
    int sw_v16 = 3;
    while (sw_v16 != 0) {
        printf("%s", "Salto em ");
        printf("%d", sw_v16);
        printf("%s", "...");
        printf("\n");
        sw_v16 = (sw_v16 - 1);
    }
    int sw_v17 = (0 - 5);
    printf("%s", "Desvio de rota corrigido: ");
    printf("%d", sw_v17);
    printf("%s", " graus");
    printf("\n");
    printf("%s", "Que a Força esteja com vocês!\n");
    return 0;
}
