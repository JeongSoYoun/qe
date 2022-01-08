# Reinforcement Learning Trade
# Agent Environment


class Environment:

    """
    chart_data
    """

    def __init__(self, chart_data=None):

        self.chart_data = chart_data
        self.observation = None
        self.idx = -1

    def reset(self):

        self.observation = None
        self.idx = -1

    def observe(self):

        if len(self.chart_data) > self.idx + 1:

            self.idx += 1
            self.observation = self.chart_data.iloc[self.idx]

            return self.observation

        return None

    def get_price(self):

        if self.observation is not None:

            return self.observation.Close

        return None

    def set_chart_data(self, chart_data):

        self.chart_data = chart_data
