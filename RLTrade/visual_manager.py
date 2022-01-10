
import threading
import numpy as np
import matplotlib.pyplot as plt

plt.switch_backend('agg')

from mplfinance.original_flavor import candlestick_ohlc
from agent import Agent