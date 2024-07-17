#include <stdio.h>
#include <stdlib.h>

int fact(int n) {
  if (n < 0) {
    return -1;
  } else if (n == 0) {
    return 1;
  }
  return n * fact(n - 1);
}

int main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <n>\n", argv[0]);
    return 1;
  }

  int n = atoi(argv[1]);
  return fact(n);
}
