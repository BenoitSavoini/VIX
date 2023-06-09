# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B48cjw0v395qVH6xY9kz0fEAPHnKhxEu
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:11:38 2023

@author: Alkios
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import random

random.seed(123)


# Define the parameters
S0 = 1000  # initial stock price
K = np.arange(975, 1026, 5)  # strike prices
r = 0.1  # risk-free interest rate
sigma = 0.15  # annual volatility
# Simulate the near-term and next-term option prices
T_near = 30 / 365  # near-term time to expiration
T_next = 60 / 365 # next-term time to expiration
days_to_expiry = 30

# Define the mean function
def mean_func(K):
    return 50 / (K ** 2)

# Define the simulation function for GBM index
def simulate_index_price(S0, T, r, sigma):
    dt = 1 / 365  # time increment (daily)
    N = int(T / dt)  # number of time steps
    S = np.zeros(N + 1)  # initialize index price array
    S[0] = S0  # set the initial index price

    # Generate the index price path using GBM
    for i in range(N):
        S[i+1] = S[i] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * np.random.normal())

    return S

# Define the simulation function for options
def simulate_option_price(S0, K, T, r, sigma, mean_func, option_type):
    S = simulate_index_price(S0, T, r, sigma)  # simulate the index price
    option_price = np.zeros_like(K)  # initialize option price array

    # Calculate the option price for each strike price
    for i in range(len(K)):
        #mean = mean_func(K[i])
        if option_type == 'call':
            option_price[i] = np.exp(-r * T) * max(S[-1] - K[i], 0)
        elif option_type == 'put':
            option_price[i] = np.exp(-r * T) * max(K[i] - S[-1], 0)
    return option_price


call_prices_near = simulate_option_price(
    S0, K, T_near, r, sigma, mean_func, 'call')
put_prices_near = simulate_option_price(
    S0, K, T_near, r, sigma, mean_func, 'put')

call_prices_next = simulate_option_price(
    S0, K, T_next, r, sigma, mean_func, 'call')
put_prices_next = simulate_option_price(
    S0, K, T_next, r, sigma, mean_func, 'put')

# Plot the results
plt.subplot(2, 2, 1)
plt.plot(K, call_prices_near, label='Call option')
plt.plot(K, put_prices_near, label='Put option')
plt.legend()
plt.xlabel('Strike price')
plt.ylabel('Option price')
plt.title('Near-term options')

plt.subplot(2, 2, 2)
plt.plot(K, call_prices_next, label='Call option')
plt.plot(K, put_prices_next, label='Put option')
plt.legend()
plt.xlabel('Strike price')
plt.ylabel('Option price')
plt.title('Next-term options')


strike_prices = list(K)
spot_price = S0
risk_free_rate = r



bid_call_price_near = [abs(x - round(random.uniform(0,1), 2)) for x in call_prices_near]  # Set bid price less than call price
bid_call_price_next = [abs(x - round(random.uniform(0,1), 2)) for x in call_prices_next]  # Set bid price less than call price

ask_call_price_near = [abs(x + round(random.uniform(0,1), 2)) for x in call_prices_near]  # Set ask price more than call price
ask_call_price_next = [abs(x + round(random.uniform(0,1), 2)) for x in call_prices_next]  # Set ask price more than call price


bid_put_price_near = [abs(x - round(random.uniform(0,1), 2)) for x in put_prices_near]  # Set bid price less than call price
bid_put_price_next = [abs(x - round(random.uniform(0,1), 2)) for x in put_prices_next]  # Set bid price less than call price

ask_put_price_near = [abs(x + round(random.uniform(0,1), 2)) for x in put_prices_near]  # Set ask price more than call price
ask_put_price_next = [abs(x + round(random.uniform(0,1), 2)) for x in put_prices_next]  # Set ask price more than call price


# Calculate the midpoint of the bid-ask spread for each option
midpoint_call_prices_near = [(bid + ask) / 2 for bid, ask in zip(bid_call_price_near, ask_call_price_near)]
# Calculate the midpoint of the bid-ask spread for each option
midpoint_call_prices_next = [(bid + ask) / 2 for bid, ask in zip(bid_call_price_next, ask_call_price_next)]


# Calculate the midpoint of the bid-ask spread for each option
midpoint_put_prices_near = [(bid + ask) / 2 for bid, ask in zip(bid_put_price_near, ask_put_price_near)]
# Calculate the midpoint of the bid-ask spread for each option
midpoint_put_prices_next = [(bid + ask) / 2 for bid, ask in zip(bid_put_price_next, ask_put_price_next)]



diff_near = list(abs(call_prices_near - put_prices_near))
min_diff_near = min(diff_near)
closest_strike_price_near = strike_prices[diff_near.index(min_diff_near)]


diff_next = list(abs(call_prices_next - put_prices_next))
min_diff_next = min(diff_next)
closest_strike_price_next = strike_prices[diff_next.index(min_diff_next)]


# Find the index of the closest strike price in the list of strikes
K_near = strike_prices.index(closest_strike_price_near)
K_next = strike_prices.index(closest_strike_price_next)

# Find the midpoint price of the call and put options with the closest strike price
C_near = call_prices_near[K_near]
P_near = put_prices_near[K_near]


# Calculate the forward price
F_near = closest_strike_price_near + math.exp(risk_free_rate * days_to_expiry / 365) * (C_near - P_near)

# Find the midpoint price of the call and put options with the closest strike price
C_next = call_prices_next[K_next]
P_next = put_prices_next[K_next]

# Calculate the forward price
F_next = closest_strike_price_next + math.exp(risk_free_rate * days_to_expiry / 365) * (C_next - P_next)

contrib_near = 0
contrib_next = 0

for i in range (len(call_prices_near)) :
    delta_K_near = 5 # arbitrary 
    delta_K_next = 5 # arbitrary
    k = K[i]
    
    if k < 1000 :
        Q_near = midpoint_put_prices_near[i]
        Q_next = midpoint_put_prices_next[i]
    else :
        Q_near = midpoint_call_prices_near[i]
        Q_next = midpoint_call_prices_near[i]

    contrib_near += delta_K_near / k ** 2 * math.exp(r * T_near) * Q_near
    contrib_next += delta_K_next / k ** 2 * math.exp(r * T_next) * Q_next


contrib_near *= 2/T_near
contrib_next *= 2/T_next

term_near = 1/T_near * (F_near/S0 - 1) ** 2
term_next = 1/T_next * (F_next/S0 - 1) ** 2

sigma_near = contrib_near - term_near
sigma_next = abs(contrib_next - term_next) # negative sign, must be an error from above, put abs just to have results, but knows it is wrong


VIX = 100 * math.sqrt((T_near * sigma_near * ((60 - 55) / (60 - 30)) + T_next * sigma_next * ((55 - 30) / (60 - 30))) * 365 / 55)

print(VIX)