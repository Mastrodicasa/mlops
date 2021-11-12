import logging

from keras.datasets import fashion_mnist
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from tensorflow.keras.optimizers import SGD

logger = logging.getLogger()


class CNNFashion:
    """
    This class creates a CNN that is able to predict the class of fashion images.

    If the images + labels are not given, the ones in keras.datasets will be used.

    Attributes:
        model: None before training, CNN model after
    """

    def __init__(self):
        self.model = None

    @staticmethod
    def __check_input(train_x, train_y):
        """
        Checks the inputs to make sure they can be used to train/ test the model.

        :param train_x: Matrix of images
        :param train_y: Labels
        :return: Boolean: True if the inputs respect the conditions, False if not
        """
        try:
            assert train_x.shape[1:] == (28, 28, 1)
            assert train_x.shape[0] == train_y.shape[0]
            return True
        except AssertionError:
            return False

    def __check_is_fitted(self):
        """
        Checks if the class has a model loaded.

        :return: Boolean: True if a model is present, False if not
        """
        if self.model is None:
            print("Run fit before running predict")
            return False
        else:
            return True

    @staticmethod
    def __reshape_dataset(train_x, train_y):
        try:
            # reshape dataset to have a single channel
            train_x = train_x.reshape((train_x.shape[0], 28, 28, 1))
            # one hot encode target values
            train_y = to_categorical(train_y)
            return train_x, train_y
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": "failed", "message": str(e)}

    @staticmethod
    def prep_pixels(train_x):
        """
        Scale the pixels from a 0-255 range to the 0-1 range.

        :param train_x: Matrix of images
        :return train_norm: Matrix of normalised images
        """
        try:
            # convert from integers to floats
            train_norm = train_x.astype('float32')
            # normalize to range 0-1
            train_norm = train_norm / 255.0
            # return normalized images
            return train_norm
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": "failed", "message": str(e)}

    @staticmethod
    def define_model():
        """Defines the CNN model"""
        try:
            model = Sequential()
            model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
            model.add(MaxPooling2D((2, 2)))
            model.add(Flatten())
            model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
            model.add(Dense(10, activation='softmax'))
            # compile model
            opt = SGD(lr=0.01, momentum=0.9)
            model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
            return model
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": "failed", "message": str(e)}

    def fit(self, train_x=None, train_y=None):
        try:
            # if no data given, default to load keras dataset
            if train_x is None or train_y is None:
                (train_x, train_y), (test_x, test_y) = fashion_mnist.load_data()
            else:
                pass

            # reshape train_x and train_y
            train_x, train_y = self.__reshape_dataset(train_x, train_y)
            self.__check_input(train_x, train_y)

            # prepare pixel data
            train_x = self.prep_pixels(train_x)

            # define model
            model = self.define_model()
            # fit model
            model.fit(train_x, train_y, epochs=10, batch_size=32, verbose=0)
            # save model
            self.model = model
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": "failed", "message": str(e)}

    def evaluate(self, test_x, test_y):
        try:
            # Check if the model was trained
            self.__check_is_fitted()

            # reshape train_x and train_y
            test_x, test_y = self.__reshape_dataset(test_x, test_y)
            self.__check_input(test_x, test_y)

            # prepare pixel data
            test_x = self.prep_pixels(test_x)
            _, acc = self.model.evaluate(test_x, test_y, verbose=0)
            return [_, acc]
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": "failed", "message": str(e)}

    def predict(self, test_x):
        try:
            self.__check_is_fitted()
            # reshape test_x
            test_x = test_x.reshape((test_x.shape[0], 28, 28, 1))
            # prepare pixel data
            test_x = self.prep_pixels(test_x)
            predictions = self.model.predict(test_x)
            return predictions
        except Exception as e:
            logger.error(e, exc_info=True)
            return {"result": "failed", "message": str(e)}

#
# (trainX, trainY), (testX, testY) = fashion_mnist.load_data()
#
# print(trainX.shape)
# print(type(trainX))
# print(type(trainY))
# print(trainY.shape)
# print(testX.shape)
# print(testY.shape)
# cf = CNNFashion()
# cf.fit()
# _, acc = cf.evaluate(testX, testY)
# print(_)
# print(acc)
# #print('> %.3f' % (acc * 100.0))
# print(cf.predict(testX))
#
# print("Second")
# cf.fit(trainX, trainY)
# _, acc = cf.evaluate(testX, testY)
# print(_)
# print(acc)
# #print('> %.3f' % (acc * 100.0))
# print(cf.predict(testX))
#
#




