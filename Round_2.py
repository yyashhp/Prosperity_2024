# buying requires import fee per unit, selling requires export fee per unit
# each transcation requires transport fee (once per load)
# storage costs .1 per orchid held, per time
# if humidity between 60 and 80 percent, orchids grow, else production falls by 2% for every 5% deviation
# if sunlight less than 7 hours, production decreases 4% for every 10 minutes
# 2500 equals 7 hours of sunlight
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
    conversions = 1
    if state.timestamp == 0:
      prev_data = [[],[],[]]
    else:
      prev_data = pickle.loads(bytes(state.traderData, "latin1"))
    orchid_look_window = len(prev_data[0]) if len(prev_data[0]) < 10 else 10
    result = {}
    
    for product in state.order_depths: 
      order_depth: OrderDepth = state.order_depths[product]
      orders: List[Order] = []
     
      if product == 'ORCHIDS' and state.timestamp > 0:
        mom_avg = ewma(prev_data[2], orchid_look_window, prod = 'S')
          
      if len(order_depth.buy_orders) != 0 and product == 'ORCHIDS' and state.timestamp > 0:
                    
        best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
        if best_ask < mom_avg:
                    # print("SELL", str(best_ask_amount) + "x", best_ask)
          orders.append(Order(product, best_ask, -best_ask_amount))
          conversions = -best_ask_amount

      if len(order_depth.sell_orders) != 0 and product == 'ORCHIDS' and state.timestamp > 0:
        best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
        if best_bid > mom_avg:
                    # print("BUY", str(best_bid_amount) + "x", best_bid)
          orders.append(Order(product, best_bid, -best_bid_amount))
          conversions = -best_bid_amount

        prev_data[0].append((best_ask + best_bid)/2)
                                      
      if product == 'ORCHIDS' and state.timestamp == 0:
        prev_data[0].append((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0])/2)
        
                    
      result[product] = orders
    traderData = str(pickle.dumps(prev_data), encoding = 'latin1')

  
    return result, conversions, traderData