import tensorflow as tf

N = 39

class recommendation_model(tf.keras.Model):

    def __init__(self):
        super(recommendation_model, self).__init__()
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

def get_new_model():
    model = recommendation_model()
    model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
              loss='mae',
              metrics=['mse'])
    model.fit([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]],[1], epochs=1, batch_size=1)
    return model

def prepare_data(data):
    return data

def get_ratings(jsonWeights, data):
    model = get_new_model()

    model.set_weights(jsonWeights)
    p_data = prepare_data(data)
    return model.predict(p_data, batch_size=1)