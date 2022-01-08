
import threading
from tensorflow.keras.layers import Input
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

graph = tf.compat.v1.get_default_graph()
session = tf.compat.v1.Session()

class Network:

    """
    In A3C, we need to use multi-thread, so to prevent collapsing between thread, we need Lock class.
    graph: Space where Neural Network is defined.
    session: Space where Neural Netowrk is excuted.
    """

    lock = threading.Lock()

    def __init__(
        self,
        input_dim = 0,
        output_dim = 0,
        lr = 0.001,
        shared_network = None,
        activation = "sigmoid",
        loss = "mse",
    ):

        self.input_dim = input_dim
        self.output_dim = output_dim
        self.lr = lr
        self.shared_network = shared_network
        self.activation = activation
        self.loss = loss
        self.model = None

    def predict(self, input):

        with self.lock:
            with graph.as_default():
                if session is not None:
                    set_session(session=session)

                return self.model.predict(input).flatten()

    def train(self, input, label):

        loss = 0.0
        with self.lock:
            with graph.as_default():
                if session is not None:
                    set_session(session=session)

                loss = self.model.train_on_batch(x=input, y=label)

        return loss

    def save_weights(self, path):

        if path is not None and self.model is not None:

            self.model.save_weights(filepath=path, overwrite=True)

    def load_weights(self, path):

        if path is not None and self.model is not None:

            self.model.load_weights(filepath=path)

    @classmethod
    def get_shared_network(cls, network="dnn", num_steps=1, input_dim=0):

        """
        Each of the NN(DNN,LSTM,CNN) has 'get_network' method
        """
        with graph.as_default():

            if session is not None:

                set_session(session=session)

            if network == "dnn":
                return cls.get_newtwork(Input(input_dim, ))

            elif network == "lstm":
                return cls.get_network(Input((num_steps, input_dim)))

            elif network == "cnn":
                return cls.get_network(Input((1, num_steps, input_dim)))
