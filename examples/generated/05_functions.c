#include <stdio.h>
#include <stdlib.h>

int sw_f0(int sw_v0);
float sw_f1(float sw_v1, float sw_v2);
void sw_f2(void);

int sw_f0(int sw_v0) {
    if (sw_v0 <= 1) {
        return 1;
    }
    return (sw_v0 * sw_f0((sw_v0 - 1)));
}

float sw_f1(float sw_v1, float sw_v2) {
    return ((sw_v1 + sw_v2) / 2);
}

void sw_f2(void) {
    printf("%s", "----------\n");
}

int main(void) {
    sw_f2();
    for (int sw_v3 = 1, sw_v4 = 5; sw_v3 <= sw_v4; sw_v3++) {
        printf("%d", sw_v3);
        printf("%s", "! = ");
        printf("%d", sw_f0(sw_v3));
        printf("\n");
    }
    sw_f2();
    printf("%s", "Média de 7 e 8: ");
    printf("%g", (double)(sw_f1(7, 8)));
    printf("\n");
    return 0;
}
