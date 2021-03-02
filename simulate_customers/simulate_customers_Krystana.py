import pandas as pd 
import numpy as np 

transition_matrix = transition_matrix = pd.read_csv("./data/transition_matrix.csv")
transition_matrix.set_index('location', inplace = True)

print(transition_matrix)
