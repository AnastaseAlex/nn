#!/usr/bin/env python
### Script to run a complete experiment

## Import libraries
import datatools
import os
reload(datatools)
from datatools import load_dataset, plot_images, plot_compare, load_sequence
from keras.models import Sequential  
from keras.layers.core import Dense, Activation, Flatten  
from keras.layers.recurrent import SimpleRNN, LSTM

import numpy as np

import matplotlib.pyplot as plt

plt.close("all")

# Data preparation
n_prev = 24
hor = 6
Xtmp = load_dataset(linnum=[44,55,66,77,88,99,110,121])
X = np.sum(Xtmp,axis=1)

#normalisation
mu = np.mean(X.flatten())
sigma = np.std(X.flatten())

X = (X - mu)/sigma
nt,nx,ny = X.shape
X = X.reshape([nt,nx*ny])
Xapp,yapp = load_sequence(X,n_prev=n_prev,hor=hor)



# Model Definition
in_out_neurons = nx*ny
nhid = 200

model = Sequential()

model.add(LSTM(input_dim=in_out_neurons,output_dim=nhid,return_sequences=False))
#model.add(SimpleRNN(input_dim=in_out_neurons,output_dim=nhid,return_sequences=False))
# parent args
#keras.layers.recurrent.Recurrent(weights=None, return_sequences=False, go_backwards=False, stateful=False, unroll=False, consume_less='cpu', input_dim=None, input_length=None)
# heir args
#keras.layers.recurrent.SimpleRNN(output_dim, init='glorot_uniform', inner_init='orthogonal', activation='tanh', W_regularizer=None, U_regularizer=None, b_regularizer=None, dropout_W=0.0, dropout_U=0.0)
model.add(Dense(input_dim=nhid,output_dim=in_out_neurons))
model.add(Activation("linear"))

model.compile(loss="mean_squared_error",optimizer="rmsprop")

model.fit(Xapp,yapp,batch_size=32,nb_epoch=20,validation_split=0.05)
y_predict = model.predict(Xapp)

#plot_compare(yapp.reshape([-1,7,7]),y_predict.reshape([-1,7,7]),[50,1000,5500,7000,11000])

# Save nn
outdir = '../data/nn_rec2'
modelname = 'rnn.json'
weights = 'weights.h5'
data =  'data.npz'

json_string = model.to_json()
open(os.path.join(outdir,modelname),'w').write(json_string)
model.save_weights(os.path.join(outdir,weights),overwrite=True)
np.savez(os.path.join(outdir,data),Xapp=Xapp,yapp=yapp)
