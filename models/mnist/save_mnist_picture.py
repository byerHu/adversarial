import keras

from keras.datasets import mnist

import matplotlib.pyplot as plt
(X_train,y_train),(X_test,y_test) = mnist.load_data()

for i in range(20):
    plt.imshow(X_train[i],cmap='gray')
    plt.savefig('./mnist_pic'+str(i)+'.jpg')
