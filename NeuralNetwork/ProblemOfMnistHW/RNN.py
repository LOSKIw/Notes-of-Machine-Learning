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
model.add(tf.keras.layers.SimpleRNN(
    units=50,
    batch_input_shape=(None, 28, 28)))
model.add(tf.keras.layers.Dense(10, activation = 'softmax'))
model.summary()
model.compile(loss = 'categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=100,
          epochs = 2,
          steps_per_epoch=10,
          verbose=1,
          validation_data=(x_test, y_test),
          validation_steps=10)

score = model.evaluate(x_test, y_test, verbose=0,steps=10)
print('Test score:', score[0])
print('Test accuracy:', score[1])
input()
