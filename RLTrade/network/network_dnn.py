
from tensorflow.python.keras.layers.core import Dropout
from tensorflow.python.keras.layers.normalization.batch_normalization import BatchNormalization
from network import Network
from tensorflow.python.keras.backend import set_session
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import Model 
from tensorflow.keras.layers import Input, Dense
import tensorflow as tf
import numpy as np

graph = tf.compat.v1.get_default_graph()
session = tf.compat.v1.Session()

class DNN(Network):

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        with graph.as_default():

            if session is not None:
                set_session(session = session)
                
            input = None
            output = None

            if self.shared_network is None:

                input = Input((self.input_dim, ))
                output = self.get_network(input = input).output

            else: 

                input = self.shared_network.input
                output = self.shared_network.output

            output = Dense (

                self.output_dim, 
                activation = self.activation,
                kernel_initializer = 'random_normal'

            )(output)
            
            self.model = Model(input,output)
            
            # Configures the model for training
            self.model.compile(
                
                optimizer = SGD(learning_rate = self.lr),
                loss = self.loss
            )
    
    @staticmethod
    def get_network(input, dropout_ratio = 0.1):
        
        output = Dense(256, activation = "sigmoid", kernel_initializer = "random_normal")(input)
        output = BatchNormalization()(output)
        output = Dropout(dropout_ratio)(output)
        output = Dense(128, activation = "sigmoid", kernel_initializer = "random_normal")(output)
        output = BatchNormalization()(output)
        output = Dropout(dropout_ratio)(output)
        output = Dense(64, activation = "sigmoid", kernel_initializer = "random_normal")(output)
        output = BatchNormalization()(output)
        output = Dropout(dropout_ratio)(output)
        output = Dense(32, activation = "sigmoid", kernel_initializer = "random_normal")(output)
        output = BatchNormalization()(output)
        output = Dropout(dropout_ratio)(output)

        return Model(input,output)

    def train(self, input, label):

        input = np.array(input).reshape((-1, self.input_dim))

        return super().train(input,label)

    def predict(self, sample):

        sample = np.array(sample).reshape((1,self.input_dim))

        return super().predict(input = sample)

if __name__ == "__main__":

    dnn = DNN()
    print(dnn.model)