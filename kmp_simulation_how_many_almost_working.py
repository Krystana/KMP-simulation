"""supermarket_simulation with Classes Customers and Supermarket"""

import datetime

from faker import Faker
import pandas as pd
import numpy as np
from collections import Counter


fake = Faker()
open_supermarket = datetime.datetime(year= 2021, month=1, day=1,hour=7, minute=0)
close_supermarket = datetime.datetime(year= 2021, month=1, day=1,hour=21, minute=0)
transition_matrix = pd.read_csv("~/Desktop/spiced_projects/WEEK_08/KMP-simulation/trans_prob_entrance.csv", index_col='location' )




class Customer:
    """Customer class for Supermarket simulation"""

    def __init__(self, customer_name, transition_matrix):

        self.customer_name = customer_name
        self.state = 'entrance'
        self.transition_matrix = transition_matrix

    def initial_state(self):
        """ prints actual state of customer"""

        print(f' Customer starts at {self.state}')

    def __repr__(self):
        return f'Customer {self.customer_name} is in the {self.state} section'


    def change_state(self):
        """ makes customers change from actual state to next state with a probabilty
         according to transition probability matrix"""

        self.state = np.random.choice(self.transition_matrix.columns.values,
                                                p=self.transition_matrix.loc[self.state])
        print(f'Customer {self.customer_name} is in the {self.state} section')


customers = [Customer(fake.name(), transition_matrix) for i in range(100)]


class Supermarket:
    """manages multiple Customer instances that are currently in the market.
 """


    def __init__(self, customers):

        self.customers = customers
        self.current_time = 0

    def start_at_entrance(self):
        """ prints the initial state for each customer w/ initial_state"""

        for element in customers:
            element.initial_state()
            print(f'{element}')


    def get_time(self):
        """ assining the  opening hour of the supermarket to the current time"""

        self.current_time = open_supermarket
        return self.current_time


    def next_minute(self):
        """ makes time elapse 1 minute and propagates all customers
            to the next state w/ change_state"""

        self.current_time = self.current_time + datetime.timedelta(minutes=1)
        for element in self.customers:
            element.change_state()
            print(f'{element}')

    def remove_ex_customers(self):
        """remove customers that entered state 'checkout' from list """

        for element in self.customers:
            if element.state == 'checkout':
                self.customers.remove(element)
                print(f'{element} and is removed')

    def generate_cust_append(self):
        """generate list with random number between 0 and 2 of of customers to append """

        no_of_appends = np.random.randint(0,2)
        appended_cust = []
        for i in range(no_of_appends):
            cust_new = Customer(fake.name(), transition_matrix)
            appended_cust.append(cust_new)

        return appended_cust

    def how_many_where(self):
        """how many proceed the simulation and where they are now"""
        how_many = len(self.customers)
        location=[]
        for customer in self.customers:
            location.append(customer.state)
        count_drinks = location.count('drinks')
        count_fruit = location.count('fruit')
        count_dairy = location.count('dairy')
        count_spices = location.count('spices')
        print(f'KMP current situation:\nTotal customers: {how_many}')
        print(f'{count_drinks} customers in drink section')
        print(f'{count_fruit} customers in fruit section')
        print(f'{count_dairy} customers in dairy section')
        print(f'{count_spices} customers in spices section')
        r = Counter(location)
        print(f'the most common: {r.most_common(5)}')


    def simulate(self):
        """ supermarket simulation that takes in a list of customers, starts at opening hour,
        ends at closing hour and lets the customers change state at every minute.
        Removes customers at checkout section and append 0-2 new customers every minute"""

        self.get_time()
        self.start_at_entrance()
        self.next_minute()

        while  close_supermarket > self.current_time > open_supermarket:
            
            print(f'\n\n\n---CURRENT TIME: {self.current_time}---')
            self.next_minute()
            self.remove_ex_customers()
            
            appended_cust = self.generate_cust_append()

            for append in appended_cust:
                self.customers.append(append)

            for element in self.customers:
                if element.state == 'entrance':
                    print(f'{element} and happy to start shopping')
            
            self.how_many_where()
            
                          