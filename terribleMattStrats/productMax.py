from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import pickle
import numpy as np
import pandas as pd


def ewma(vals, window, times):
  df = pd.DataFrame(vals[(len(vals)-window):])
  avg = df.ewm(alpha = 0.45, adjust = True).mean()
  return avg.iloc[-1].values[0]


                    
class Trader:
    
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        if state.timestamp == 0:
           prev_data = []
        else:
           prev_data = pickle.loads(bytes(state.traderData, "latin1"))
        look_window = len(prev_data) if len(prev_data) < 10 else 10
				# Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths: #order_depths is a dictinonary where the key is the product and the value is the order depth object
            #each order depth is a dict where key is price and value is quantity
            order_depth: OrderDepth = state.order_depths[product]
            # Initialize the list of Orders to be sent as an empty list
            orders: List[Order] = []
            # Define a fair value for the PRODUCT. Might be different for each tradable item
            # Note that this value of 10 is just a dummy value, you should likely change it!
            if product == 'STARFRUIT' and state.timestamp > 0:
              mom_avg = ewma(prev_data, look_window, state.timestamp)
              best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
              if best_ask < mom_avg:
                print("SELL", str(best_ask_amount) + "x", best_ask)
                orders.append(Order(product, best_ask, -best_ask_amount))
              best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
              if best_bid > mom_avg:
                print("BUY", str(best_bid_amount) + "x", best_bid)
                orders.append(Order(product, best_bid, -best_bid_amount))
              prev_data.append((best_ask + best_bid)/2)
            elif product == 'STARFRUIT' and state.timestamp == 0:
               prev_data.append((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0])/2)
            
            elif product == 'AMETHYSTS':
              acceptable_price = 10000
            else:
              acceptable_price = 10
           # print(product, acceptable_price)  # Participant should calculate this value
            # All print statements output will be delivered inside test results

           # print("Acceptable price : " + str(acceptable_price))
          #  print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
            print(state.own_trades)
            # Order depth list come already sorted. 
						# We can simply pick first item to check first item to get best bid or offer
            if len(order_depth.sell_orders) != 0 and product == 'AMETHYSTS':
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price:
                    # In case the lowest ask is lower than our fair value,
                    # This presents an opportunity for us to buy cheaply
                    # The code below therefore sends a BUY order at the price level of the ask,
                    # with the same quantity
                    # We expect this order to trade with the sell order
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
    
            if len(order_depth.buy_orders) != 0 and product == 'AMETHYSTS':
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