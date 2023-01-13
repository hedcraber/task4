#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
import numpy as np
import pandas as pd

def to_json(s):
    js = json.loads(s)
    s1 = []
    for j in js:
        if isinstance(j, list):
            s1.append(j)
        if isinstance(j, str):
            a = []
            a.append(j)
            s1.append(a)
    return s1

def matrix_transpose(js):
    groups_ranks = dict(enumerate(js))
    objects = [item for sublist in js for item in sublist]
    object_to_id = {v: k for k, v in dict(enumerate(objects)).items()}
    matrix = np.zeros((len(objects), len(objects)))
    prev_objects = []
    for rank, group in groups_ranks.items():
        ids = [object_to_id[x] for x in group]
        self_ids = np.array(list(zip(ids, ids)))
        matrix[self_ids[:, :, None], ids] = 1
        matrix[np.array(prev_objects, dtype=np.int8)[:, None], ids] = 1
        prev_objects.extend(ids)

    result = pd.DataFrame(matrix, columns=object_to_id.keys(), index=object_to_id.keys())
    result_t = result.transpose()
    return result, result_t

def mult(df1, df2):
    res = df1.copy()
    for c in res.columns:
        for i in res.index:
            res[c][i] = df1[c][i] * df2[c][i]
    return res

def task(str1, str2):
    j1 = to_json(str1)
    j2 = to_json(str2)

    m1, m1_t = matrix_transpose(j1)
    m2, m2_t = matrix_transpose(j2)

    m12 = mult(m1, m2)
    m12_t = mult(m1_t, m2_t)

    result = m12.copy()
    contr = []
    for c in result.columns:
        for i in result.index:
            result[c][i] = m12[c][i] + m12_t[c][i]
            if result[c][i] == 0.0 and [i, c] not in contr and [c, i] not in contr:
                contr.append([c, i])
    return contr


# In[5]:


""" Хонер БПМ-19-4 """


# In[ ]:




