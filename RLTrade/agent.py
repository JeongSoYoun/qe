import numpy as np
import utils


class Agent:

    """
    STATE_DIM: State of Agent -> 주식 보유 비율 & 포트폴리오 가치
    TRADING_CHARGE: 수수료
    TRADING_TAX: 거래세

    portfolio_value = (balance) + (num_stocks)*(current_price)
    """

    STATE_DIM = 2
    TRADING_CHARGE = 0.00015
    TRADING_TAX = 0.0025
    ACTION_BUY = 0
    ACTION_SELL = 1
    ACTION_HOLD = 2
    ACTIONS = [ACTION_BUY, ACTION_SELL]
    NUM_ACTIONS = len(ACTIONS)

    def __init__(
        self,
        environment,
        min_trading_unit=1,
        max_trading_unit=2,
        delayed_reward_threshold=0.05,
    ):

        self.environment = environment
        self.min_trading_unit = min_trading_unit
        self.max_trading_unit = max_trading_unit
        self.delayed_reward_threshold = delayed_reward_threshold
        self.initial_balance = 0
        self.balance = 0
        self.num_stocks = 0
        self.portfolio_value = 0
        self.portfolio_value_base = 0
        self.num_buy = 0
        self.num_sell = 0
        self.num_hold = 0
        self.immediate_reward = 0
        self.profitloss = 0
        self.profitloss_base = 0
        self.exploration_base = 0

        # Variables that determine the state of Agent
        self.hold_ratio = 0
        self.portfolio_value_ratio = 0

    def reset(self):

        self.balance = self.initial_balance
        self.num_stocks = 0
        self.portfolio_value = self.initial_balance
        self.portfolio_value_base = self.initial_balance
        self.num_buy = 0
        self.num_sell = 0
        self.num_hold = 0
        self.immediate_reward = 0
        self.hold_ratio = 0
        self.portfolio_value_ratio = 0

    def reset_exploration(self):

        self.exploation_base = 0.5 + np.random.rand() / 2

    def set_balance(self, balance):

        """
        Initialize the balance to get profit-loss
        """

        self.initial_balance = balance

    def get_states(self):

        """
        hold_ratio: number of stocks holding / maximum number of stocks that you can hold
        portfolio_value_ratio: current portfolio value over base portfolio value
        """
        self.hold_ratio = self.num_stocks / int(
            self.portfolio_value / self.environment.get_price()
        )

        self.portfolio_value_ratio = self.portfolio_value / self.portfolio_value_base

    def decide_action(self, value, policy, eps):

        """
        eps: range(0,1)
        """
        confidence = 0
        prediction = policy

        if prediction is None:

            prediction = value

        if prediction is None:

            # If there is no action by Neural Network, explore
            eps = 1

        else:

            # if policy predict by NN and gives us same probabilty, that is
            # buy: 50 %, sell: 50 -> explore
            best_prediction = np.max(policy)
            if (policy == best_prediction).all():

                eps = 1

        if np.random.rand() < eps:

            exploration = True
            if np.random.rand() < self.exploration_base:

                action = self.ACTION_BUY

            else:

                action = np.random.randint(self.NUM_ACTIONS - 1) + 1

        else:

            exploration = False
            action = np.argmax(prediction)
            confidence = 0.5

            if policy is not None:
                confidence = prediction[action]

            elif value is not None:
                confidence = utils.sigmoid(prediction[action])

            return action, confidence, exploration

    def validate_action(self, action):

        """
        Check whether action is validated.
        For buying, we can't buy if there is not enough balance.
        For selling, we can't sell if there is no holding stocks
        """

        if action == Agent.ACTION_BUY:

            trading_cost = (
                self.environment.get_price()
                * (1 + self.TRADING_CHARGE)
                * self.min_trading_unit
            )

            if self.balance < trading_cost:

                return False

        elif action == Agent.ACTION_SELL:

            if self.num_stocks <= 0:

                return False

        return True

    def decide_trading_unit(self, confidence):

        """
        confidence: range(0,1). If it is closer to 1, we added more trading unit.
        Otherwise, no additional_trading.
        """

        trading_unit = self.max_trading_unit - self.min_trading_unit
        if np.isnan(confidence):

            return self.min_trading_unit

        additional_trading = max(min(int(confidence * trading_unit), trading_unit), 0)

        return self.min_trading_unit + additional_trading

    def act(self, action, confidence):

        """
        Act what agent has decided.
        action: [0: BUY, 1: SELL] decided by NN
        """

        if not self.validate_action(action):

            action = Agent.ACTION_HOLD

        self.immediate_reward = 0
        current_price = self.environment.get_price()
        buy_cost = current_price * (1 + self.TRADING_CHARGE)
        sell_cost = current_price * (1 - (self.TRADING_CHARGE + self.TRADING_TAX))

        # buy
        # trading_unit: at least min_trading_unit
        if action == Agent.ACTION_BUY:

            trading_unit = self.decide_trading_unit(confidence=confidence)
            balance = self.balance - (buy_cost * trading_unit)

            # if it exceeds balance...
            if balance < 0:

                trading_unit = max(
                    min(int(self.balance / buy_cost), self.max_trading_unit),
                    self.min_trading_unit,
                )

            total_buy_cost = buy_cost * trading_unit
            if total_buy_cost > 0:

                self.balance -= total_buy_cost
                self.num_stocks += trading_unit
                self.num_buy += 1

        # sell
        elif action == Agent.ACTION_SELL:

            trading_unit = self.decide_trading_unit(confidence=confidence)
            trading_unit = min(trading_unit, self.num_stocks)

            total_sell_cost = sell_cost * trading_unit
            if total_sell_cost > 0:

                self.balance += total_sell_cost
                self.num_stocks -= trading_unit
                self.num_sell += 1

        # hold
        elif action == Agent.ACTION_HOLD:

            """
            While holding, portfolio value would be changed, so we need to update our portfolio value.
            Here, we return whether our action was good/bad.

            portfolio_value_base: Base of the Portfolio value whenever we reach our delayed_reward_threshold.
            profit_loss_base: Base of the profit-loss when portfolio_value has updated.
            """

            self.num_hold += 1
            self.portfolio_value = self.balance + (current_price * self.num_stocks)
            self.profitloss = (
                self.portfolio_value - self.initial_balance
            ) / self.initial_balance

            self.immediate_reward = self.profitloss
            delayed_reward = 0

            self.profitloss_base = (
                self.portfolio_value - self.portfolio_value_base
            ) / self.portfolio_value_base

            if (
                self.profitloss_base > self.delayed_reward_threshold
                or self.profitloss_base < -self.delayed_reward_threshold
            ):

                self.portfolio_value_base = self.portfolio_value
                delayed_reward = self.immediate_reward
            else:

                delayed_reward = 0

            return delayed_reward, self.immediate_reward
