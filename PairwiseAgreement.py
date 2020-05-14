#!/usr/bin/env python
# coding: utf-8
# In[1]:

import pandas as pd
import numpy as np
import scipy as sp
import seaborn as sns
import itertools

pd.set_option('display.max_columns', 500)

# In[3]:

# scores 1 is the ground truth
def pairwise_agreement(scores1, scores2, which_group = 'first', agr_comparison='<', removeties=False):
    uguals = 0
    assert len(scores1) == len(scores2), 'Error on lengths'

    # whoch group deals with which is the fine grained scale among the two
    if which_group=='second': 
        scores1, scores2 = scores2, scores1
    
    # borderline case, there is nothing to group
    if len(np.unique(scores1))==1:
        return 1
    
    scores1, scores2 = (list(t) for t in zip(*sorted(zip(scores1, scores2)))) 
    groups = np.unique(scores1)
    lst_groups = [np.array([]) for i in range(len(groups))]
    dict_group = {}
    for i in range(len(groups)):
        dict_group[groups[i]] = i
    for i in range(len(scores1)):    
        lst_groups[dict_group[scores1[i]]] = np.append( lst_groups[dict_group[scores1[i]]], scores2[i])        
    groups_to_check  = list(  itertools.combinations(range(len(lst_groups)), 2)  )
    list_couples =  [ list(itertools.product(lst_groups[j[0]], lst_groups[j[1]])) for j in groups_to_check ] 
    list_couples = [item for sublist in list_couples for item in sublist]
    agreement_couple = 0
    possible_couples = len(list_couples)
    
    less_than_cuples = 0
    less_than_equal_cuples = 0
    equal_cuples = 0
    
    for k in list_couples:        
        if k[0] < k[1]:
            less_than_cuples +=1
            less_than_equal_cuples +=1
        elif k[0] <= k[1]:
            less_than_equal_cuples +=1
            equal_cuples +=1
        else:
            pass
    try:
        if (agr_comparison == "<") & (removeties==True):
            return float( (less_than_cuples)/(possible_couples-equal_cuples) )
        if (agr_comparison == "<") & (removeties==False):
            return float( (less_than_cuples)/(possible_couples) ) 
        if (agr_comparison == "<=") & (removeties==True):
            return float( (less_than_equal_cuples-equal_cuples)/(possible_couples-equal_cuples) ) 
        if (agr_comparison == "<=") & (removeties==False):
            return float( (less_than_equal_cuples)/(possible_couples) )  
    except:
        print(f"error on {agr_comparison} -- {removeties}: less_than_cuples:{less_than_cuples}, possible_couples:{possible_couples}, equal_cuples:{equal_cuples}")
        print(f"scores1: {scores1}")
        print(f"scores2: {scores2}")
        print()
        return np.nan
        assert False
    
    assert False
    return -1




