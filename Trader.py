# NECESSARY IMPORTS

from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import pickle
import numpy as np
import pandas as pd


# HELPER FUNCTIONS

def ewma(vals, window, prod):
  df = pd.DataFrame(vals[(len(vals)-window):])
  if prod == 'S':
    alph = 0.45 # originally 0.45
  else:
    alph = 0.3
  avg = df.ewm(alpha = alph, adjust = True).mean()
  return avg.iloc[-1].values[0]
                    

# START OF TRADER CLASS

class Trader:
    
  def run(self, state: TradingState):
            #  print("traderData: " + state.traderData)
            #  print("Observations: " + str(state.observations))
    if state.timestamp == 0:
      prev_data = [[],[]]
    else:
      prev_data = pickle.loads(bytes(state.traderData, "latin1"))
    star_look_window = len(prev_data[0]) if len(prev_data[0]) < 10 else 10
    am_look_window = len(prev_data[1]) if len(prev_data[1]) < 28 else 28
    result = {}
    
    for product in state.order_depths: 
      order_depth: OrderDepth = state.order_depths[product]
      orders: List[Order] = []
      mean_reverting_star = False
     
      if product == 'STARFRUIT' and state.timestamp > 0:
        mom_avg = ewma(prev_data[0], star_look_window, prod = 'S')
          
      if len(order_depth.buy_orders) != 0 and product == 'STARFRUIT' and state.timestamp > 0:
                    
        best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
        if best_ask < mom_avg:
                    # print("SELL", str(best_ask_amount) + "x", best_ask)
          orders.append(Order(product, best_ask, -best_ask_amount))

      if len(order_depth.sell_orders) != 0 and product == 'STARFRUIT' and state.timestamp > 0:
        best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
        if best_bid > mom_avg:
                    # print("BUY", str(best_bid_amount) + "x", best_bid)
          orders.append(Order(product, best_bid, -best_bid_amount))
        prev_data[0].append((best_ask + best_bid)/2)
                                      
      if product == 'STARFRUIT' and state.timestamp == 0:
        prev_data[0].append((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0])/2)
                  
      
      
      
      
      
      if product == 'AMETHYSTS' and state.timestamp > 0:
        if am_look_window < 6:
          acceptable_price = 10000
        else:
          acceptable_price = ewma(prev_data[1], am_look_window, prod = 'A')
        print(f"Acceptable price: {acceptable_price}")

      if product == 'AMETHYSTS' and state.timestamp == 0:
        acceptable_price = 10000
                

      if len(order_depth.sell_orders) != 0 and product == 'AMETHYSTS' and state.timestamp > 0:
               
        for best_ask, best_ask_amount in order_depth.sell_orders.items():
          if best_ask and best_ask < acceptable_price:
                  #   print("BUY", str(-best_ask_amount) + "x", best_ask)
            orders.append(Order(product, best_ask, -best_ask_amount))
        
      if len(order_depth.buy_orders) != 0 and product == 'AMETHYSTS' and state.timestamp > 0:
                  
        for best_bid, best_bid_amount in order_depth.buy_orders.items():
          if best_bid and best_bid > acceptable_price:
                      #  print("SELL", str(best_bid_amount) + "x", best_bid)
            orders.append(Order(product, best_bid, -best_bid_amount))
        prev_data[1].append((best_ask + best_bid)/2)
        
      if product == 'AMETHYSTS' and state.timestamp == 0:
          prev_data[1].append((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0])/2)
         
                    
      result[product] = orders
    traderData = str(pickle.dumps(prev_data), encoding = 'latin1')

          
  
    conversions = 1
    return result, conversions, traderData