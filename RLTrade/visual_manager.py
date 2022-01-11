
from mplfinance.original_flavor import candlestick_ohlc
from agent import Agent
import threading
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as data_manager

lock = threading.Lock()

class Visual_Manager:

    COLORS = ['r', 'b', 'g']

    def __init__(self, vnet=False):

        self.canvas = None
        self.fig = None
        self.axes = None
        self.title = ''

    def chart_canvas(self, chart_data, title):

        """
            Settings for canvas of entire chart
            Day chart is common part regardless of the epoch, I have initialized it here.
        """

        self.title = title
        with lock:

            self.fig, self.axes = plt.subplots (

                nrows=5,
                ncols=1,
                facecolor='w',
                sharex=True
            )

        for ax in self.axes:

            ax.get_xaxis().get_major_formatter().set_scientific(False)
            ax.get_yaxis().get_major_formatter().set_scientific(False)
            ax.yaxis.tick_right()

        # Chart 1 - Day Chart
        self.axes[0].set_ylabel('Env')
        x = np.arange(len(chart_data))
        ohlc = np.hstack(
            (
                x.reshape(-1,1),
                np.array(chart_data)[:, 0:-1]
            )
        )
        candlestick_ohlc (

            ax=self.axes[0],
            quotes=ohlc,
            colorup='r',
            colordown='b'
        )
        ax = self.axes[0].twinx()
        volume = np.array(chart_data)[:,-1].tolist()
        ax.bar(x, volume, color='b', alpha=0.3)

        plt.title(self.title)
        plt.show()

    def plot(
        self,
        epoch_str=None,
        num_epochs=None,
        epsilon=None,
        action_list=None,
        actions=None,
        num_stocks=None,
        values=[],
        policies=[],
        exps=None,
        lr_idxes=None,
        initial_balance=None,
        pvs=None
    ):

        """
            args:
                - epsilon: exploration rate
                - action_list: What agent can do [Buy, Sell]
                - actions: What agent has done
                - num_stocks: Number of stocks holding
                - values: Output of value by NN
                - policies: Output of policy by NN
                - exps: List of whether explores or not
                - lr_idxes: Learning location
                - pvs: List of portfolio values
        """
        with lock:

            x = np.arange(len(actions))
            actions = np.array(actions)
            values = np.array(values)
            policies = np.array(policies)
            pvs_base = np.zeros(len(actions)) + initial_balance

        # Chart 2 - Status of Agent: Actions & Number of Stocks
        # (('Buy','r'),('Sell','b'))
        for (action, color) in zip(action_list, self.COLORS):
            for i in x[actions == action]:

                self.axes[1].axvline(i, color=color, alpha=0.1)

        # plot number of stocks holding
        self.axes[1].plot(x, num_stocks, '-k')


if __name__ == '__main__':

    visual_manager = Visual_Manager()
    df = data_manager.get_data_yahoo('AAPL', start='2021-01-01', end='2022-01-01')
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    print(df)
    visual_manager.chart_canvas(chart_data=df, title='Agent Status')