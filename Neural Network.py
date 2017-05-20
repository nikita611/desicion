# -*- coding: utf-8 -*-
import numpy as np
import random


def sigmoid(z):
    """
    Функция сигмоиды
    """
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """
    Производная сигмоиды
    """
    return sigmoid(z) * (1 - sigmoid(z))


def cost_function(network, test_data, onehot=True):
    """
    Наша функция оценки погрешностей
    В данном случае квадратичная
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
        Список ``sizes`` содержит количество нейронов в соответствующих слоях
        нейронной сети.
        Смещения и веса для нейронных сетей
        инициализируются случайными значениями, подчиняющимися стандартному нормальному
        распределению.
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
        Вычислить и вернуть выходную активацию нейронной сети
        при получении ``a`` на входе.
        """
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def update_mini_batch(self, mini_batch, eta):
        """
        Обновить веса и смещения нейронной сети, сделав шаг градиентного
        спуска на основе алгоритма обратного распространения ошибки, примененного
        к одному mini batch. Учесть штрафы за L1 и L2.
        ``mini_batch`` - список кортежей вида ``(x, y)``,
        ``eta`` - величина шага (learning rate).
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
        Возвращает кортеж ``(nabla_b, nabla_w)`` -- градиент целевой функции по всем параметрам сети.
        ``nabla_b`` и ``nabla_w`` -- послойные списки массивов ndarray,
        такие же, как self.biases и self.weights соответственно.
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x]  # список, хранящий все активации, слой за слоем
        zs = []  # список, хранящий все векторы сумматорной функции, слой за слоем

        # прямое распространение (forward pass)

        for b, w in zip(self.biases, self.weights):
            # посчитать активации
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        # обратное распространение (backward pass)
        delta = self.cost_derivative(activations[-1], y) * \
                sigmoid_prime(zs[-1])  # ошибка выходного слоя
        nabla_b[-1] = delta  # производная J по смещениям выходного слоя
        nabla_w[-1] = np.dot(delta, activations[-2].T)  # производная J по весам выходного слоя

        # Здесь l = 1 означает последний слой,
        # l = 2 - предпоследний и так далее.
        # используем тот факт, что в Python к переменной типа list
        # можно обращаться по негативному индексу.
        for l in range(2, self.num_layers):
            # дополнительные вычисления, чтобы легче записывалось
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l + 1].T, delta) * sigmoid_prime(zs[-l])  # ошибка на слое L-l
            nabla_b[-l] = delta  # производная J по смещениям L-l-го слоя
            nabla_w[-l] = np.dot(delta, activations[-l - 1].T)  # производная J по весам L-l-го слоя
        return nabla_b, nabla_w

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        """
        Обучить нейронную сеть, используя алгоритм стохастического
        (mini-batch) градиентного спуска. 
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
                print("Эпоха {0}: {1} / {2}".format(
                    j, success_tests, n_test))
            elif self.output:
                print("Эпоха {0} завершена".format(j))
        if test_data is not None:
            return success_tests / n_test

    def evaluate(self, test_data):
        """
        Вернуть количество тестовых примеров, для которых нейронная сеть
        возвращает правильный ответ
        """
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """
        Возвращает вектор частных производных (\partial C_x) / (\partial a) 
        целевой функции по активациям выходного слоя.
        """
        return (output_activations - y)
