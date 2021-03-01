'''

                            analysis.py              Current
                                 |                  /
        live -- broker.py -- brain.py -- requests.py
                    |            |                  \
                   past    technicals.py             Past
                          /             \
                          live          past

Within brain => press 1 or 2, 1 for live/paper 2 for backtest
'''
import anal
import broke
import req
import tech

type = int(input("1 => live, \n2 => paper, \n3 => backtester")

if type == 1:
    live()
if type == 2:
    paper()
if type == 3:
    backtester()

def live():
    return

def paper():
    for strategy in strategies:
        pass
    return

def backtester():
    return
