from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import jsonpickle as jp

class Trader:
    def run(self, state: TradingState):
        result = {}
        for product in state.order_depths: 
            order_depth: OrderDepth = state.order_depths[product]

            orders: List[Order] = []

            # All print statements output will be delivered inside test results
            print("Acceptable price : " + "the best available price")
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))

            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                print("BUY", str(-best_ask_amount) + "x", best_ask)
                orders.append(Order(product, best_ask, -best_ask_amount))

    
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                print("SELL", str(best_bid_amount) + "x", best_bid)
                orders.append(Order(product, best_bid, -best_bid_amount))
            
            # want the key to be the product and the result to be the orders we want to do with that product
            result[product] = orders
    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "shell_max" 
        
		    # Sample conversion request. Check more details below. 
                # KEEP THIS SET EQUAL TO NONE --> WE ARE NOT THAT SWEATY
        conversions = None 
        
        return result, conversions, traderData