import csv
import tensorflow as tf
import numpy as np 

def modeltrain():

    train_features = []
    train_labels = []
    test_features = []
    test_labels = []

    file = open("ACC_train_movement.csv")
    csvreader = csv.reader(file)
    for row in csvreader:
        if len(row)==3:
            train_features.append( [ int(row[0]), int(row[1]), int(row[2]) ] )
            train_labels.append([1])

    file = open("ACC_train_nomovement.csv")
    csvreader = csv.reader(file)
    for row in csvreader:
        if len(row)==3:
            train_features.append( [ int(row[0]), int(row[1]), int(row[2]) ] )
            train_labels.append([0])

    file = open("ACC_test_movement.csv")
    csvreader = csv.reader(file)
    for row in csvreader:
        if len(row)==3:
            test_features.append( [ int(row[0]), int(row[1]), int(row[2]) ] )
            test_labels.append([1])

    file = open("ACC_test_nomovement.csv")
    csvreader = csv.reader(file)
    for row in csvreader:
        if len(row)==3:
            test_features.append( [ int(row[0]), int(row[1]), int(row[2]) ] )
            test_labels.append([0])



    train_features = np.array(train_features)
    train_labels = np.array(train_labels)
    test_features = np.array(test_features)
    test_labels = np.array(test_labels)

    
    model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(input_shape=(3,)),
    tf.keras.layers.Dense(units=100, activation='tanh'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(units=2, activation='Softmax')
    ])

    predictions = model(train_features).numpy()
    predictions

    tf.nn.softmax(predictions).numpy()

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)

    loss_fn(train_labels, predictions).numpy()

    model.compile(optimizer='adam',
                loss=loss_fn,
                metrics=['accuracy'])

    model.fit(train_features, train_labels, epochs=10)

    model.evaluate(test_features,  test_labels, verbose=2)

    #model.save(filepath="models")

    tf.saved_model.save(model, "trainedmodel")

    
modeltrain()