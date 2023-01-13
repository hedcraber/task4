
#!/usr/bin/env python
# coding: utf-8

# In[3]:

# python-3.11.0

from io import StringIO
import csv
import math
import numpy as np
import pandas as pd

def task(csvString):
  # Переводим csv в более удобное представление, в моем случае
  # в словарь, где ключ - номер вершины, которая имеет ребра,
  # а значение - массив нормеров вершин, в которые эти ребра приходят
  f = StringIO(csvString)
  reader = csv.reader(f)
  graph = {}
  vertices = []
  for row in reader:
    edge = list(map(int, row))
    edge.sort()
    # Добавляем отношение в граф
    if edge[0] in graph:
      if not edge[1] in graph[edge[0]]:
        graph[edge[0]].append(edge[1])
    else:
      graph[edge[0]] = [edge[1]]
    # Заполняем список вершин
    if not edge[0] in vertices:
      vertices.append(edge[0])
    if not edge[1] in vertices:
      vertices.append(edge[1])

  # Создаем результирующий массив
  out = [[0 for i in range(5)] for i in range(len(vertices))]


  # Заполняем количество r1 - прямого управления - для каждой вершины
  for i in graph:
    out[i - 1][0] += len(graph[i])

  # Заполняем количество r2 - прямого подчинения, и r5 - соподчинения
  # Допольнительно сохраним все вершины, которые учавствуют в r2
  r2 = []
  for i in graph:
    for j in graph[i]:
      out[j - 1][1] += 1
      if len(graph[i]) > 1:
        out[j - 1][4] += 1
      if not j in r2:
        r2.append(j)
  r2.sort()

  # Заполняем количество r3 - опосредованное управление
  # и r4 - опосредованное подчинение
  for i in r2:
    if i in graph.keys():
      for j in graph[i]:
          out[j - 1][3] += 1
      for j in graph:
        if i in graph[j]:
          out[j - 1][2] += len(graph[i])
  for i in r2:
    if i in graph.keys():
      for j in graph[i]:
        out[j - 1][3] += out[i - 1][3]
  for i in sorted(graph.keys(), reverse=True):
    for j in graph[i]:
      out[i - 1][2] += out[j - 1][2]


  #Считаем энтропию
  sum = 0
  for i in out:
    for j in i:
      if j != 0:
        sum -= (j / (len(vertices) - 1)) * math.log2(j / (len(vertices) - 1))

  return sum

csvString = '1,2\n1,3\n3,4\n3,5'
print(task(csvString))

# Иван Левчук БПМ-19-4