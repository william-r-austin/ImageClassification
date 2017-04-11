import numpy as np
np.random.seed(123)

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from matplotlib import pyplot as plt

from keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()


model = Sequential()

model.add(Dense(units = 64, input_dim = 100))
model.add(Activation('relu'))
model.add(Dense(units = 10))
model.add(Activation('softmax'))


model.compile(loss = 'categorical_crossentropy',
              optimizer = 'sgd',
              metrics = ['accuracy'])

model.fit(X_train, y_train, epochs = 5, batch_size = 32)

loss_and_metrics = model.evaluate(X_test, y_test, batch_size = 128)

# print ("len = " + str(X_train.sh))
# plt.imshow(X_train[0])


random_state = np.random.RandomState(19680801)
X = random_state.randn(10000)

fig, ax = plt.subplots()
ax.hist(X, bins = 25, normed = True)
x = np.linspace(-5, 5, 1000)
ax.plot(x, 1 / np.sqrt(2 * np.pi) * np.exp(-(x ** 2) / 2), linewidth = 4)
ax.set_xticks([])
ax.set_yticks([])
fig.savefig("C:/Users/William/histogram_frontpage.png", dpi = 25)  # results in 160x120 px image
