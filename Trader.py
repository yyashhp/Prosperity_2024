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

        # COLLECTING PREVIOUS DATA

        if state.timestamp == 0:
           prev_data = [[],[]]
        else:
           prev_data = pickle.loads(bytes(state.traderData, "latin1"))
        star_look_window = len(prev_data[0]) if len(prev_data[0]) < 10 else 10
        am_look_window = len(prev_data[1]) if len(prev_data[1]) < 28 else 28
				# Orders to be placed on exchange matching engine
        result = {}


        # THE FOR LOOP FOR PRODUCTS
        
        for product in state.order_depths: #order_depths: dict where key is the product and value is the order depth object
            
            #each order depth is a dict where key is price and value is quantity
            order_depth: OrderDepth = state.order_depths[product]

            # Initialize the list of Orders to be sent as an empty list
            orders: List[Order] = []

            # Define a fair value for the PRODUCT. Might be different for each tradable item
            
            # STARFRUIT STRATEGY: ewma momentum-based strat

            if len(order_depth.buy_orders) != 0 and product == 'STARFRUIT' and state.timestamp > 0:
              mom_avg = ewma(prev_data[0], star_look_window, prod = 'S')
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

            elif product == 'STARFRUIT' and state.timestamp == 0:
               prev_data[0].append((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0])/2)
          

            # AMETHYST STRATEGY: ewma momentum-based strat

            elif product == 'AMETHYSTS' and state.timestamp > 0:
              if am_look_window < 6:
                acceptable_price = 10000 # if we have no data, set a default value for acceptable price
              else:
                acceptable_price = ewma(prev_data[1], am_look_window, prod = 'A') # if we have data
                print(f"Acceptable price: {acceptable_price}") 

            elif product == 'AMETHYSTS' and state.timestamp == 0:
              acceptable_price = 10000
            
            else: # NOTE: I don't think this last else statement is necessary, but for saftey, we keep
              acceptable_price = 10 


            # ACTUAL TRADING STARTS (NOW THAT WE HAVE NUMBERS...)

						# We can simply pick first item to check first item to get best bid or offer
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price:
                    print("BUY", str(best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
    
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_price:
                    # Similar situation with sell orders
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders

    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = str(pickle.dumps(prev_data), encoding = 'latin1')

        
				# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData