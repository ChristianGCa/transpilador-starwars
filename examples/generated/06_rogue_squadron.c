#include <stdio.h>
#include <stdlib.h>

int sw_f0(int sw_v0, int sw_v1);
int sw_f1(int sw_v2, int sw_v3);
int sw_f2(int sw_v4, int sw_v5, int sw_v6);
float sw_f3(int sw_v7, int sw_v8);
void sw_f4(float sw_v9);

int sw_f0(int sw_v0, int sw_v1) {
    return (sw_v0 - ((sw_v0 / sw_v1) * sw_v1));
}

int sw_f1(int sw_v2, int sw_v3) {
    if (sw_v3 != 0) {
        return sw_f1(sw_v3, sw_f0(sw_v2, sw_v3));
    } else {
        return sw_v2;
    }
}

int sw_f2(int sw_v4, int sw_v5, int sw_v6) {
    if (sw_v5 <= sw_v4) {
        if (sw_v4 <= sw_v6) {
            return 1;
        }
    }
    return 0;
}

float sw_f3(int sw_v7, int sw_v8) {
    return ((sw_v7 * 100.0f) / sw_v8);
}

void sw_f4(float sw_v9) {
    if (sw_v9 >= 80.0f) {
        printf("%s", "\tpatente: Jedi\n");
        return;
    }
    if (sw_v9 >= 50.0f) {
        printf("%s", "\tpatente: Padawan\n");
    } else {
        printf("%s", "\tpatente: Youngling\n");
    }
}

int main(void) {
    printf("%s", "=== Avaliação de tiro ao alvo do Esquadrão Rogue ===\n");
    printf("%s", "Para cada piloto, informe os tiros disparados e quantos acertaram o alvo.\n");
    printf("%s", "O programa calcula a precisão e a patente de cada piloto:\n");
    printf("%s", "Jedi (80% ou mais), Padawan (50% ou mais) ou Youngling (abaixo de 50%).\n");
    printf("%s", "Um piloto é aprovado com 50% ou mais de precisão (Padawan ou Jedi).\n");
    printf("%s", "O esquadrão só parte em missão se todos os pilotos forem aprovados.\n\n");
    int sw_v10 = 0;
    printf("%s", "Quantos pilotos\? ");
    fflush(stdout);
    if (scanf("%d", &sw_v10) != 1) {
        fprintf(stderr, "ERRO DE ENTRADA (linha 56): esperado valor numerico.\n");
        return 1;
    }
    while (sw_v10 < 1) {
        printf("%s", "O esquadrão precisa de pelo menos 1 piloto.\n");
        printf("%s", "Quantos pilotos\? ");
        fflush(stdout);
        if (scanf("%d", &sw_v10) != 1) {
            fprintf(stderr, "ERRO DE ENTRADA (linha 59): esperado valor numerico.\n");
            return 1;
        }
    }
    float sw_v11 = 0.0f;
    int sw_v12 = 0;
    int sw_v13 = 0;
    int sw_v14 = 0;
    float sw_v15 = (0 - 1.0f);
    for (int sw_v16 = 1, sw_v17 = sw_v10; sw_v16 <= sw_v17; sw_v16++) {
        printf("%s", "Piloto ");
        printf("%d", sw_v16);
        printf("%s", ":");
        printf("\n");
        int sw_v18 = 0;
        printf("%s", "\ttiros disparados: ");
        fflush(stdout);
        if (scanf("%d", &sw_v18) != 1) {
            fprintf(stderr, "ERRO DE ENTRADA (linha 72): esperado valor numerico.\n");
            return 1;
        }
        while (sw_v18 < 1) {
            printf("%s", "\tinforme pelo menos 1 tiro.\n");
            printf("%s", "\ttiros disparados: ");
            fflush(stdout);
            if (scanf("%d", &sw_v18) != 1) {
                fprintf(stderr, "ERRO DE ENTRADA (linha 75): esperado valor numerico.\n");
                return 1;
            }
        }
        int sw_v19 = 0;
        printf("%s", "\tacertos: ");
        fflush(stdout);
        if (scanf("%d", &sw_v19) != 1) {
            fprintf(stderr, "ERRO DE ENTRADA (linha 79): esperado valor numerico.\n");
            return 1;
        }
        while (sw_f2(sw_v19, 0, sw_v18) == 0) {
            printf("%s", "\tos acertos devem ficar entre 0 e ");
            printf("%d", sw_v18);
            printf("%s", ".");
            printf("\n");
            printf("%s", "\tacertos: ");
            fflush(stdout);
            if (scanf("%d", &sw_v19) != 1) {
                fprintf(stderr, "ERRO DE ENTRADA (linha 82): esperado valor numerico.\n");
                return 1;
            }
        }
        float sw_v20 = sw_f3(sw_v19, sw_v18);
        int sw_v21 = sw_f1(sw_v19, sw_v18);
        printf("%s", "\t");
        printf("%d", (sw_v19 / sw_v21));
        printf("%s", " em cada ");
        printf("%d", (sw_v18 / sw_v21));
        printf("%s", " tiros (");
        printf("%g", (double)(sw_v20));
        printf("%s", "%)");
        printf("\n");
        sw_f4(sw_v20);
        sw_v11 = (sw_v11 + sw_v20);
        if (sw_v20 >= 50.0f) {
            sw_v12 = (sw_v12 + 1);
        }
        if (sw_v20 > sw_v15) {
            sw_v13 = sw_v16;
            sw_v15 = sw_v20;
            sw_v14 = 1;
        } else {
            if (sw_v20 == sw_v15) {
                sw_v14 = (sw_v14 + 1);
            }
        }
    }
    float sw_v22 = (sw_v11 / sw_v10);
    int sw_v23 = (sw_v10 - sw_v12);
    printf("%s", "\n=== Resultado do esquadrão ===\n");
    printf("%s", "Precisão média: ");
    printf("%g", (double)(sw_v22));
    printf("%s", "%");
    printf("\n");
    printf("%s", "Aprovados (50% ou mais): ");
    printf("%d", sw_v12);
    printf("%s", " de ");
    printf("%d", sw_v10);
    printf("\n");
    if (sw_v14 == 1) {
        printf("%s", "Melhor piloto: ");
        printf("%d", sw_v13);
        printf("%s", " (");
        printf("%g", (double)(sw_v15));
        printf("%s", "%)");
        printf("\n");
    } else {
        if (sw_v14 == sw_v10) {
            printf("%s", "Melhor piloto: empate entre todos os ");
            printf("%d", sw_v10);
            printf("%s", " pilotos (");
            printf("%g", (double)(sw_v15));
            printf("%s", "%)");
            printf("\n");
        } else {
            printf("%s", "Melhor piloto: empate entre ");
            printf("%d", sw_v14);
            printf("%s", " pilotos (");
            printf("%g", (double)(sw_v15));
            printf("%s", "%)");
            printf("\n");
        }
    }
    if (sw_v23 == 0) {
        printf("%s", "Todos aprovados: esquadrão pronto para a missão. Que a Força esteja com vocês!\n");
    } else {
        printf("%s", "Esquadrão não está pronto: ");
        printf("%d", sw_v23);
        printf("%s", " piloto(s) abaixo de 50%. Mais treino no simulador.");
        printf("\n");
    }
    return 0;
}
