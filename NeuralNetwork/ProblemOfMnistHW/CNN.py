import tensorflow as tf
mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

print('Integer-valued labels:')
print(y_train[:10])

y_train = tf.one_hot(y_train, 10)
y_test = tf.one_hot(y_test, 10)

print('One-hot labels:')
print(y_train[:10])

model=tf.keras.models.Sequential()
model.add(tf.keras.layers.Conv2D(filters = 16, kernel_size = 2, padding = 'same', activation = 'relu',input_shape = (28, 28, 1)))
model.add(tf.keras.layers.MaxPool2D(pool_size = 2))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Conv2D(filters = 64, kernel_size = 2, padding = 'same', activation = 'relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(500, activation = 'relu'))
model.add(tf.keras.layers.Dense(10, activation = 'softmax'))

model.summary()

model.compile(loss = 'categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
print(x_train.shape)
print(x_test.shape)
model.fit(x_train, y_train,
          batch_size=1,
          steps_per_epoch=100,
          epochs = 5,
          verbose=1,
          validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
input()
