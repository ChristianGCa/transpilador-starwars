#include <stdio.h>

int main(void) {
    int sw_v0 = 3;
    float sw_v1 = 1.5f;
    while (sw_v0 > 0) {
        printf("%d", sw_v0);
        printf("\n");
        sw_v1 = (sw_v1 + (2 * 1.5f));
        sw_v0 = (sw_v0 - 1);
    }
    if (sw_v1 >= 5) {
        printf("%s", "acesso liberado");
    } else {
        printf("%s", "acesso negado");
    }
    return 0;
}
