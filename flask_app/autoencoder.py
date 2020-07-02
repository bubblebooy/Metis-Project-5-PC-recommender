from keras.models import Model
from keras.layers import Input, Dense, Dropout
from keras.optimizers import Adam

def create_autoencoder(weights = None):
    inputs = Input(shape=(43,))
    # x = Dropout(0)(inputs)
    x = Dense(30 , activation = "relu")(inputs)
    x = Dense(25 , activation = "relu")(x)
    x = Dense(20 , activation = "relu")(x)
    x = Dense(25 , activation = "relu")(x)
    x = Dense(30 , activation = "relu")(x)
    x = Dense(60 , activation = "relu")(x)
    x = Dense(120 , activation = "relu")(x)

    out_reg = Dense(15 , activation = "linear", name = 'out_reg')(x)
    out_log = Dense(13 , activation = "sigmoid", name = 'out_log')(x)
    out_series = Dense(9 , activation = "softmax", name = 'out_series')(x)
    out_motherboard = Dense(5 , activation = "softmax", name = 'out_motherboard')(x)
    model = Model(inputs=inputs, outputs=[out_reg, out_log, out_series, out_motherboard]) #
    model.compile(optimizer=Adam(), #learning_rate=0.0001
                      loss=['mean_squared_error','binary_crossentropy','categorical_crossentropy','categorical_crossentropy']) #
    if weights is not None:
        model.load_weights(weights)
    return model
