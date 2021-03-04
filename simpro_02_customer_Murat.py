
import numpy as np
import pandas as pd

transition_matrix = pd.read_csv("trans_matrix_prob.csv", index_col = 0)

class Customer:

   def __init__(self, id, state, transition_mat):
        self.id = id
        self.state = state
        self.transition_mat = transition_matrix

   def __repr__(self):
      """
      Returns a csv string for that customer.
      """
      return f'{self.id}, {self.state}, {self.transition_mat}'

   def is_active(self):
      """
      Returns True if the customer has not reached the checkout
      for the second time yet, False otherwise.
      """
      if self.state == 'checkout':
        return False
      else:
        return True

   def next_state(self):
      """
      Propagates the customer to the next state
      using a weighted random choice from the transition probabilities
      conditional on the  current state.
      Returns nothing.
      """
      next_location = np.random.choice(self.transition_mat.columns.values, p=self.transition_mat.loc[self.state])
      self.state = next_location