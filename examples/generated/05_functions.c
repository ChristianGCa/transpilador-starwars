#include <stdio.h>
#include <stdlib.h>

int sw_f0(int sw_v0);
float sw_f1(float sw_v1);
void sw_f2(int sw_v2);

int sw_f0(int sw_v0) {
    if (sw_v0 == 0) {
        return 1;
    }
    return (2 * sw_f0((sw_v0 - 1)));
}

float sw_f1(float sw_v1) {
    return (sw_v1 * 3.26f);
}

void sw_f2(int sw_v2) {
    printf("%s", "Geração ");
    printf("%d", sw_v2);
    printf("%s", ": ");
    printf("%d", sw_f0(sw_v2));
    printf("%s", " Jedi");
    printf("\n");
}

int main(void) {
    printf("%s", "A Ordem Jedi cresce: cada Jedi treina 2 padawans por geração.\n");
    for (int sw_v3 = 0, sw_v4 = 4; sw_v3 <= sw_v4; sw_v3++) {
        sw_f2(sw_v3);
    }
    printf("%s", "\nKessel Run da Millennium Falcon: 12 parsecs = ");
    printf("%g", (double)(sw_f1(12)));
    printf("%s", " anos-luz");
    printf("\n");
    return 0;
}
