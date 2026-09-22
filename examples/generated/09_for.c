#include <stdio.h>

int main(void) {
    int sw_v0 = 7;
    for (int sw_v1 = 1, sw_v2 = 5; sw_v1 <= sw_v2; sw_v1++) {
        printf("%d", sw_v0);
        printf("%s", " x ");
        printf("%d", sw_v1);
        printf("%s", " = ");
        printf("%d", (sw_v0 * sw_v1));
        printf("\n");
    }
    int sw_v3 = 0;
    for (int sw_v4 = 1, sw_v5 = 10; sw_v4 <= sw_v5; sw_v4++) {
        sw_v3 = (sw_v3 + sw_v4);
    }
    printf("%s", "Soma de 1 até 10: ");
    printf("%d", sw_v3);
    printf("\n");
    return 0;
}
