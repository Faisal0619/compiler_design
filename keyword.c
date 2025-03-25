#include <stdio.h>
#include <string.h>

// List of C keywords
const char *keywords[] = {
    "auto", "break", "case", "char", "const", "continue", "default", "do", 
    "double", "else", "enum", "extern", "float", "for", "goto", "if", 
    "int", "long", "register", "return", "short", "signed", "sizeof", "static", 
    "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
};

int isKeyword(const char *str) {
    int numKeywords = sizeof(keywords) / sizeof(keywords[0]);
    for (int i = 0; i < numKeywords; i++) {
        if (strcmp(str, keywords[i]) == 0) {
            return 1; 
        }
    }
    return 0; 
}

int main() {
    char str[100];

    printf("Enter a string: ");
    scanf("%s", str);

    if (isKeyword(str)) {
        printf("\"%s\" is a valid C keyword.\n", str);
    } else {
        printf("\"%s\" is not a C keyword.\n", str);
    }

    return 0;
}

