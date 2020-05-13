import tensorflow as tf
import numpy as np

N = 39
TRAIN_DATA_SIZE = 5


class RecommendationModel(tf.keras.Model):

    def __init__(self):
        super(RecommendationModel, self).__init__()
        self.input_layer = tf.keras.layers.Dense(N, input_shape=[1, N])
        self.middle_layer1 = tf.keras.layers.Dense(N * 2, activation='relu')
        self.middle_layer2 = tf.keras.layers.Dense(N * 3, activation='relu')
        self.middle_layer3 = tf.keras.layers.Dense(N * 5, activation='relu')
        self.output_layer = tf.keras.layers.Dense(1)

    def call(self, inputs):
        x = self.input_layer(inputs)
        x = self.middle_layer1(x)
        x = self.middle_layer2(x)
        x = self.middle_layer3(x)
        x = self.output_layer(x)
        return x


def get_new_model(weights):
    model = RecommendationModel()
    model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
                  loss='mae',
                  metrics=['mse'])
    model.fit([[1 for _ in range(N)]], [1], epochs=1, batch_size=1)

    if len(weights) > 1:
        converted_weights = [np.array(x) for x in weights]
        model.set_weights(converted_weights)

    return model


def get_ratings(json_weights, data):
    model = get_new_model(json_weights)
    return model.predict(data, batch_size=1)


def train_model(json_weights, data_in, data_out):
    model = get_new_model(json_weights)
    model.fit(data_in, data_out, epochs=1, batch_size=1)
    return [x.tolist() for x in model.get_weights()]
