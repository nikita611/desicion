# -*- coding: utf-8 -*-
import numpy as np
import random


def sigmoid(z):
    """
    ������� ��������
    """
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """
    ����������� ��������
    """
    return sigmoid(z) * (1 - sigmoid(z))


def cost_function(network, test_data, onehot=True):
    """
    ���� ������� ������ ������������
    � ������ ������ ������������
    """
    c = 0
    for example, y in test_data:
        if not onehot:
            y = np.eye(3, 1, k=-int(y))
        yhat = network.feedforward(example)
        c += np.sum((y - yhat) ** 2)
    return c / len(test_data)


class RegularizedNetwork:
    def __init__(self, sizes, output=True, l1=0, l2=0):
        """
        ������ ``sizes`` �������� ���������� �������� � ��������������� �����
        ��������� ����.
        �������� � ���� ��� ��������� �����
        ���������������� ���������� ����������, �������������� ������������ �����������
        �������������.
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.output = output
        self.l1 = l1
        self.l2 = l2
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """
        ��������� � ������� �������� ��������� ��������� ����
        ��� ��������� ``a`` �� �����.
        """
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def update_mini_batch(self, mini_batch, eta):
        """
        �������� ���� � �������� ��������� ����, ������ ��� ������������
        ������ �� ������ ��������� ��������� ��������������� ������, ������������
        � ������ mini batch. ������ ������ �� L1 � L2.
        ``mini_batch`` - ������ �������� ���� ``(x, y)``,
        ``eta`` - �������� ���� (learning rate).
        """

        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]

        eps = eta / len(mini_batch)
        self.weights = [w - eps * nw - self.l1 * np.sign(w) - self.l2 * w for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - eps * nb for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """
        ���������� ������ ``(nabla_b, nabla_w)`` -- �������� ������� ������� �� ���� ���������� ����.
        ``nabla_b`` � ``nabla_w`` -- ��������� ������ �������� ndarray,
        ����� ��, ��� self.biases � self.weights ��������������.
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x]  # ������, �������� ��� ���������, ���� �� �����
        zs = []  # ������, �������� ��� ������� ����������� �������, ���� �� �����

        # ������ ��������������� (forward pass)

        for b, w in zip(self.biases, self.weights):
            # ��������� ���������
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        # �������� ��������������� (backward pass)
        delta = self.cost_derivative(activations[-1], y) * \
                sigmoid_prime(zs[-1])  # ������ ��������� ����
        nabla_b[-1] = delta  # ����������� J �� ��������� ��������� ����
        nabla_w[-1] = np.dot(delta, activations[-2].T)  # ����������� J �� ����� ��������� ����

        # ����� l = 1 �������� ��������� ����,
        # l = 2 - ������������� � ��� �����.
        # ���������� ��� ����, ��� � Python � ���������� ���� list
        # ����� ���������� �� ����������� �������.
        for l in range(2, self.num_layers):
            # �������������� ����������, ����� ����� ������������
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].T, delta) * sigmoid_prime(zs[-l])  # ������ �� ���� L-l
            nabla_b[-l] = delta  # ����������� J �� ��������� L-l-�� ����
            nabla_w[-l] = np.dot(delta, activations[-l - 1].T)  # ����������� J �� ����� L-l-�� ����
        return nabla_b, nabla_w

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        """
        ������� ��������� ����, ��������� �������� ���������������
        (mini-batch) ������������ ������. 
        """
        if test_data is not None: n_test = len(test_data)
        n = len(training_data)
        success_tests = 0
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k + mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data is not None and self.output:
                success_tests = self.evaluate(test_data)
                print("����� {0}: {1} / {2}".format(
                    j, success_tests, n_test))
            elif self.output:
                print("����� {0} ���������".format(j))
        if test_data is not None:
            return success_tests / n_test

    def evaluate(self, test_data):
        """
        ������� ���������� �������� ��������, ��� ������� ��������� ����
        ���������� ���������� �����
        """
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """
        ���������� ������ ������� ����������� (\partial C_x) / (\partial a) 
        ������� ������� �� ���������� ��������� ����.
        """
        return (output_activations - y)
