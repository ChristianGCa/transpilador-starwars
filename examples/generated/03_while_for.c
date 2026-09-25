#include <stdio.h>

int main(void) {
    int sw_v0 = 3;
    while (sw_v0 > 0) {
        printf("%s", "Salto para o hiperespaço em ");
        printf("%d", sw_v0);
        printf("%s", "...");
        printf("\n");
        sw_v0 = (sw_v0 - 1);
    }
    printf("%s", "Salto!\n");
    int sw_v1 = 0;
    for (int sw_v2 = 1, sw_v3 = 4; sw_v2 <= sw_v3; sw_v2++) {
        sw_v1 = (sw_v1 + 3);
        printf("%s", "Salto ");
        printf("%d", sw_v2);
        printf("%s", ": ");
        printf("%d", sw_v1);
        printf("%s", " parsecs percorridos");
        printf("\n");
    }
    printf("%s", "Kessel Run completada em ");
    printf("%d", sw_v1);
    printf("%s", " parsecs!");
    printf("\n");
    return 0;
}
