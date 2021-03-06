'''
Implement with PoC base
The base source code:
 A logistic regression learning algorithm example using TensorFlow library.
 Code: https://github.com/aymericdamien/TensorFlow-Examples/blob/master/examples/2_BasicModels/logistic_regression.py
'''

from framework import BaseTask
from framework import Context
from typing import Any

import warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

# Import mnist data
from tensorflow.examples.tutorials.mnist import input_data

from framework import BaseTask

class Task(BaseTask):
    """
    Concrete task class.
    """

    def __init__(self, context: Context) -> None:
        super().__init__(context)

    def execute(self) -> Any:
        self.learning_rate = self.args.learning_rate
        self.training_epochs = self.args.training_epochs
        self.batch_size = self.args.batch_size
        self.display_step = self.args.display_step


        """
        Concrete execute method.

        Notes
        -----
        1. Logging:
            You can output logs with `self.context.logger`.
            (e.g.) self.context.logger.debug("logging output")
        2. Env var:
            You can access to environment variables with `self.context.config`.
            (e.g.) self.context.config.get("KEY")
        3. Command Line Arguments:
            You can access to arguments through `self.args` after set your arguments
            through `set_arguments` method.
            (e.g.) self.args.model_path
        4. File Path:
            You can get absolute path under `data` directory by `self.context.file.get_path`.
            Please put your files (data set or any necessary files) under `data` directory.
            (e.g.) self.context.file.get_path('sample.csv')
        """

        # Logger
        logger = self.context.logger

        # Parameters
        learning_rate = self.args.learning_rate
        training_epochs = self.args.training_epochs
        batch_size = self.args.batch_size
        display_step = self.args.display_step

        # Download dataset to /data/tmp
        mnist = input_data.read_data_sets(self.context.file.get_path("tmp"), one_hot=True)

        # tf Graph Input
        x = tf.placeholder(tf.float32, [None, 784])  # mnist data image of shape 28*28=784
        y = tf.placeholder(tf.float32, [None, 10])  # 0-9 digits recognition => 10 classes

        # Set model weights
        W = tf.Variable(tf.zeros([784, 10]))
        b = tf.Variable(tf.zeros([10]))

        # Construct model
        pred = tf.nn.softmax(tf.matmul(x, W) + b)  # Softmax

        # Minimize error using cross entropy
        cost = tf.reduce_mean(-tf.reduce_sum(y * tf.log(pred), reduction_indices=1))
        # Gradient Descent
        optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

        # Initialize the variables (i.e. assign their default value)
        init = tf.global_variables_initializer()

        # Start training
        with tf.Session() as sess:

            # Run the initializer
            sess.run(init)

            # Training cycle
            for epoch in range(training_epochs):
                avg_cost = 0.
                total_batch = int(mnist.train.num_examples / batch_size)
                # Loop over all batches
                for i in range(total_batch):
                    batch_xs, batch_ys = mnist.train.next_batch(batch_size)
                    # Run optimization op (backprop) and cost op (to get loss value)
                    _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs,
                                                                  y: batch_ys})
                    # Compute average loss
                    avg_cost += c / total_batch
                # Display logs per epoch step
                if (epoch + 1) % display_step == 0:
                    #logger.info("Epoch: %04d cost=", epoch + 1, "{:.9f}".format(avg_cost))
                    msg = "Epoch: " + str(epoch + 1) + "cost= " + "{:.9f}".format(avg_cost)
                    logger.info(msg)

            logger.info("Optimization Finished!")

            # Test model
            correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
            # Calculate accuracy
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            #logger.info("Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))
            msg = "Accuracy: " + str(accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))
            logger.info(msg)

    def set_arguments(self, parser) -> None:
        """
        Set your command line arguments if necessary.

        Notes
        -----
        Adding command line arguments.
        (e.g.) `parser.add_argument('--model', dest="model_path", help='set model path')`
        """

        learning_rate = 0.01
        training_epochs = 25
        batch_size = 100
        display_step = 1

        parser.add_argument('--learning_rate', dest="learning_rate", default=learning_rate, help='set learning rate')
        parser.add_argument('--training_epochs', dest="training_epochs", default=training_epochs, help='set training epochs')
        parser.add_argument('--batch_size', dest="batch_size", default=batch_size, help='set batch size')
        parser.add_argument('--display_step', dest="display_step", default=display_step, help='set display step')

