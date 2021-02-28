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
import analysis
import broker
import requests
import technicals
