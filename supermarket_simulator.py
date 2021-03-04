"""
Cleaned up code
Still runs
pylint score is 8.78/10
"""

import datetime
import pandas as pd
import numpy as np
from faker import Faker

transition_matrix = transition_matrix = pd.read_csv("data/trans_matrix_prob.csv")
transition_matrix.set_index('location', inplace = True)

class Customer:
    """Customer class for Supermarket simulation"""
    def __init__(self, customer_no, state, transition_matrix):
        self.customer_no = customer_no
        self.state = state
        self.transition_matrix = transition_matrix

    def __repr__(self):
        return f'Customer {self.customer_no} is in the {self.state} section'

    def change_state(self):
        print('Customer is moving to another section')
        self.state = np.random.choice(self.transition_matrix.columns.values, p=self.transition_matrix.loc[self.state])

fake = Faker()
open_supermarket = datetime.datetime(year= 2021, month=1, day=1,hour=7, minute=0)
close_supermarket = datetime.datetime(year= 2021, month=1, day=1,hour=21, minute=0)

class Supermarket:
    """manages multiple Customer instances that are currently in the market."""
    def __init__(self, customers):
        self.customers = customers
        self.current_time = 0

    def get_time(self):  #open supermarket
        """opening hour"""
        self.current_time = open_supermarket  # opening hour
        return self.current_time

    def next_minute(self):
        """propagates all customers to the next state w/ change_state"""
        self.current_time = self.current_time + datetime.timedelta(minutes=1)
        for element in self.customers:
            element.change_state()
        return self.current_time   #?

    def remove_ex_customers(self):
        """remove churned from list"""
        for element in self.customers:
            if element.state == 'checkout':
                self.customers.remove(element)
                print(f'{element} and has checked out')

    def simulate(self):
        self.get_time()
        self.next_minute()
        while self.current_time > open_supermarket:
            self.next_minute()
            self.remove_ex_customers()
            c = Customer(fake.name(), 'drinks', transition_matrix)
            self.customers.append(c)
            if self.current_time > close_supermarket:
                break

customers = [Customer(i, 'fruit', transition_matrix) for i in range(100)]
s = Supermarket(customers)
s.simulate()
