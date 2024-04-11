from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import pickle
import numpy as np
import pandas as pd


def ewma(vals, window, prod):
  df = pd.DataFrame(vals[(len(vals)-window):])
  if prod == 'S':
    alph = 0.45
  else:
    alph = 0.3
  avg = df.ewm(alpha = alph, adjust = True).mean()
  return avg.iloc[-1].values[0]
                    
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
      #star_prev_ewma = prev_data[2]
              # Orders to be placed on exchange matching engine
    result = {}
    for product in state.order_depths: #order_depths is a dictinonary where the key is the product and the value is the order depth object
                  #each order depth is a dict where key is price and value is quantity
      order_depth: OrderDepth = state.order_depths[product]
                  # Initialize the list of Orders to be sent as an empty list
      orders: List[Order] = []
                  # Define a fair value for the PRODUCT. Might be different for each tradable item
                  # Note that this value of 10 is just a dummy value, you should likely change it!
      mean_reverting_star = False
      if product == 'STARFRUIT' and state.timestamp > 0:
        mom_avg = ewma(prev_data[0], star_look_window, prod = 'S')
          
      if len(order_depth.buy_orders) != 0 and product == 'STARFRUIT' and state.timestamp > 0:
                    
               #     star_prev_ewma.append(mom_avg)
                #    prev_data[2] = star_prev_ewma
               #     std_prev_ewma_lookback = len(star_prev_ewma) if len(star_prev_ewma) < 40 else 40
                  #  if std_prev_ewma_lookback != len(star_prev_ewma):
                #      std_prev_ewma = np.std(star_prev_ewma[-std_prev_ewma_lookback:-25])
                #   else:
                #      std_prev_ewma = np.std(star_prev_ewma[-std_prev_ewma_lookback:])

                #   if std_prev_ewma < .1 and len(star_prev_ewma) >8:
                    
                      #    mean_reverting_star = False

                  #  else:
                  #  mean_reverting_star = False
        best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                  #  prev_data[0].append((best_ask + best_bid)/2)
        if mean_reverting_star is False and best_ask < mom_avg:
                    # print("SELL", str(best_ask_amount) + "x", best_ask)
          orders.append(Order(product, best_ask, -best_ask_amount))

                  
      if len(order_depth.sell_orders) != 0 and product == 'STARFRUIT' and state.timestamp > 0:
        best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
        if mean_reverting_star is False and best_bid > mom_avg:
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
                

                  #  acceptable_price = 10000

                # print(product, acceptable_price)  # Participant should calculate this value
                  # All print statements output will be delivered inside test results
                 # if len(orders) > 0:
                 #     break

            # print("Acceptable price : " + str(acceptable_price))
            #  print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
            #  print(state.own_trades)
              # Order depth list come already sorted. 
              # We can simply pick first item to check first item to get best bid or offer
      if len(order_depth.sell_orders) != 0 and product == 'AMETHYSTS' and state.timestamp > 0:
                  #for offer in list(order_depth.sell_orders.items()):
                  # best_ask, best_ask_amount = offer[0], offer[1]
                  #best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
        for best_ask, best_ask_amount in order_depth.sell_orders.items():
          if best_ask and best_ask < acceptable_price:
                                        #print("j")

                          # In case the lowest ask is lower than our fair value,
                          # This presents an opportunity for us to buy cheaply
                            # The code below therefore sends a BUY order at the price level of the ask,
                            # with the same quantity
                            # We expect this order to trade with the sell order
                  #   print("BUY", str(-best_ask_amount) + "x", best_ask)
            orders.append(Order(product, best_ask, -best_ask_amount))
        
      if len(order_depth.buy_orders) != 0 and product == 'AMETHYSTS' and state.timestamp > 0:
                    #for offer in list(order_depth.sell_orders.items()):
                    #  best_ask = offer[0]
                    #  best_ask_amount = offer[1]
                    #best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
        for best_bid, best_bid_amount in order_depth.buy_orders.items():
              
          if best_bid and best_bid > acceptable_price:
                      # print("j")
                            # Similar situation with sell orders
                      #  print("SELL", str(best_bid_amount) + "x", best_bid)
            orders.append(Order(product, best_bid, -best_bid_amount))
      if product == 'AMETHYSTS' and state.timestamp == 0:
          prev_data[1].append((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0])/2)
      if product == 'AMETHYSTS' and state.timestamp > 0:
          prev_data[1].append((best_ask + best_bid)/2)
                    
      result[product] = orders
          # String value holding Trader state data required. 
          # It will be delivered as TradingState.traderData on next execution.
    traderData = str(pickle.dumps(prev_data), encoding = 'latin1')

          
          # Sample conversion request. Check more details below. 
    conversions = 1
    return result, conversions, traderData