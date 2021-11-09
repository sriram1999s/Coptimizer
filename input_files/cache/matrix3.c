#include <stdio.h>

void printMatrix(int nV, int matrix[][nV])
{
  int INF = 9999;
  for (int i = 0; i < nV; i++) {
    for (int j = 0; j < nV; j++) {
      printf("%4d", matrix[i][j]);
    }
    printf("\n");
  }
}

void init(int nV, int graph[][nV], int matrix[][nV])
{
  for (int i = 0; i < nV; i++) {
    for (int j = 0; j < nV; j++) {
      matrix[i][j] = graph[i][j];
    }
  }
}

void floydWarshall(int nV, int graph[][nV])
{
  int matrix[nV][nV];
  init(nV, graph, matrix);
  for (int k = 0; k < nV; k++) {
    for (int i = 0; i < nV; i++) {
      for (int j = 0; j < nV; j++) {
        if (matrix[i][k] + matrix[k][j] < matrix[i][j]) {
          matrix[i][j] = matrix[i][k] + matrix[k][j];
        }
      }
    }
  }
  printMatrix(nV, matrix);
}

int main()
{
  int nV = 4;
  int INF = 9999;
  int graph[4][4] = {{0, 3, INF, 5}, {2, 0, INF, 4}, {INF, 1, 0, INF}, {INF, INF, 2, 0}};
  floydWarshall(nV, graph);
}
