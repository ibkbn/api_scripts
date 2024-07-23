#! /usr/bin/env python3

import logging
import ibapi
import time
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.execution import Execution
from ibapi.order import Order

class TestApp(EWrapper, EClient):


    def __init__(self):
        EWrapper.__init__(self)
        EClient.__init__(self, self)
        self.dataframe = {}

    def error(self, reqId: int, errorCode: int, errorString: str,
              advansedOrderreject=""):
        super().error(reqId, errorCode, errorString, advansedOrderreject)
        error_message = f'Error id: {reqId}, Error code: {errorCode}, ' \
                        + f'Msg: {errorString}'
        print(error_message)
       
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        logging.debug(f"Next valid ID is set to {orderId}")
        self.nextValidOrderId = orderId # Snippet 1
        print(self.nextValidOrderId)
        self.start()

    def openOrder(self, orderId, contract, order, orderState):
        print("Open Order: ", orderId, contract, order)

    def orderStatus(self, orderId, status, filled, remaining,
            avgFillPrice, permid, parentId, lastFillPrice, 
            clientId, whyHeld, mktCapPrice):
        print(f"Order Status: id: {orderId}, status: {status}," +\
                f"filled: {filled}, remaining: {remaining}," +\
                f"avgFillPrice: {avgFillPrice}, permid: {permid}," +\
                f"parentId: {parentId}, lastFillPrice: {lastFillPrice}," +\
                f"clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def placeAdjustedOrder(self):

        contract = Contract()

        contract.symbol = "BMW"
        contract.exchange = "SMART"
        contract.currency = "EUR"
        contract.secType = 'STK'

        order = Order()

        order.action = 'BUY'
        order.orderType = 'MKT'
        order.totalQuantity = 1
#        order.auxPrice = 108.55 
        order.tif = 'DAY'

        adjusted = Order()
        adjusted.parentId = order.orderId
        adjusted.orderId = order.orderId + 1
        adjusted.action = "BUY"
        adjusted.tif = "DAY"
        adjusted.totalQuantity = 2
        adjusted.triggerPrice = 175
        adjusted.adjustedOrderType = "TRAIL LMT"
        adjusted.adjustedStopLimitPrice = 105.6
        adjusted.lmtPriceOffset = 1
        adjusted.auxPrice = 3

        orders = [order, adjusted]

        orderid = self.nextValidOrderId
        
        for order in orders:
            self.placeOrder(orderid, contract, order)

    def start(self):

        contract = Contract()

        contract.symbol = "BMW"
        contract.exchange = "SMART"
        contract.currency = "EUR"
        contract.secType = 'STK'

        order = Order()

        order.action = 'BUY'
        order.orderType = 'MKT'
        order.totalQuantity = 1
#        order.auxPrice = 108.55 
        order.tif = 'DAY'

        self.placeOrder(self.nextValidOrderId, contract, order)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    try:
        app = TestApp()
        app.connect('192.168.43.222', 7496, clientId=0)
        print(f'{app.serverVersion()} --- {app.twsConnectionTime().decode()}')
        print(f'ibapi version: ', ibapi.__version__)
#        Timer(5, app.stop).start()
        app.run()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
