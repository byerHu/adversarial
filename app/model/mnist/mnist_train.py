import keras
from keras.datasets import mnist
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Activation,Dropout
from keras.utils import np_utils


# 数据准备
(X_train, y_train),(X_test,y_test) = mnist.load_data()
print(X_train.shape)
print(X_test.shape)
# 将二位数据变成一维数据
X_train = X_train.reshape(len(X_train),-1)
X_test = X_test.reshape(len(X_test),-1)
# 对数据进行归一化处理 uint不能有负数,我们先转为float类型 归一化的方式很多
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train = (X_train - 127) / 127
X_test = (X_test - 127) / 127

# One-hot encoding
nb_classes = 10
y_train = np_utils.to_categorical(y_train,nb_classes)
y_test = np_utils.to_categorical(y_test,nb_classes)

# 搭建网络
model = Sequential()

model.add(Dense(512, input_shape=(784,), kernel_initializer='he_normal'))
model.add(Activation('relu'))
model.add(Dropout(0.2))

model.add(Dense(512, kernel_initializer='he_normal'))
model.add(Activation('relu'))
model.add(Dropout(0.2))

model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
model.fit(X_train,y_train,epochs=20,batch_size=64,verbose=1,validation_split=0.05)

model.save('mnist_h5')
loss,accuracy = model.evaluate(X_test,y_test)

print('Test loss:',loss)
print('Test accuracy:',accuracy)



