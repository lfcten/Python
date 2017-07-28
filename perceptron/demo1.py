#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time     : 2017/7/28 9:26
@Author   : Danxiyang
@File     : demo1.py
@Software : PyCharm
"""
import numpy as np
import matplotlib.pyplot as plt


# train matrix
def get_train_data():
    M1 = np.random.random((100, 2))
    M11 = np.column_stack((M1, np.ones(100)))
    M2 = np.random.random((100, 2)) - 1
    M22 = np.column_stack((M2, np.ones(100) * (-1)))
    MA = np.vstack((M11, M22))
    MA = np.column_stack((MA, np.arange(200)))
    plt.plot(M1[:, 0], M1[:, 1], 'ro')
    plt.plot(M2[:, 0], M2[:, 1], 'go')
    min_x = np.min(M2)
    max_x = np.max(M1)
    x = np.linspace(min_x, max_x, 100)
    return MA, x


def get_gram(MA):
    length = len(MA)
    GRAM = np.empty(shape=(length, length))
    for i in range(length):
        for j in range(length):
            GRAM[i, j] = np.dot(MA[i, :2], MA[j, :2])
    return GRAM


def func(alpha, b, xi, yi, yN, index, GRAM):
    pa1 = alpha * yN
    pa2 = GRAM[:, index]
    return yi * (np.dot(pa1, pa2) + b)


def train(MA, alpha, b, GRAM, yN):
    for sample in MA:
        xi = sample[:2]
        yi = sample[-2]
        index = int(sample[-1])
        if func(alpha, b, xi, yi, yN, index, GRAM) <= 0:
            alpha[index] += n
            b += n * yi
            train(MA, alpha, b, GRAM, yN)

    return alpha, b


def plot_classify(w, b, x, rate0):
    y = (w[0] * x + b)/((-1) * w[1])
    plt.plot(x, y)
    plt.title("Accuracy = " + str(rate0))


# def get_test_data():
#     M = np.random.random((50, 2))
#     plt.plot(M[:, 0], M[:, 1], '*y')
#     return M


# def classify(w, b, test_i):
#     if np.sign(np.dot(w, test_i) + b)==1:
#         return 1
#     else:
#         return 0


# def test(w, b, test_data):
#     right_count = 0
#     for test_i in test_data:
#         classx = classify(w, b, test_i)
#         if classx == 1:
#             right_count += 1
#     return right_count / len(test_data)


if __name__ == "__main__":
    MA, x = get_train_data()
    # test_data = get_test_data()
    GRAM = get_gram(MA)
    yN = MA[:, 2]
    xN = MA[:, :2]
    alpha = [0] * 200
    b = 0
    n = 1
    rate0 = 0
    # for i in np.linspace(0.01, 1, 100):
    n = 0.5
    alpha, b = train(MA, alpha, b, GRAM, yN)
    # alphap = np.column_stack((alpha * yN, alpha * yN))
    # w = sum(alphap * xN)
    w = np.dot(alpha * yN, xN)
    # print(w)
    # rate = test(w, b, test_data)
    # if rate > rate0:
    #     rate0 = rate
    #     w0 = w
    #     b0 = b
    # plot_classify(w0, b0, x, rate0)
    plot_classify(w, b, x, rate0=1.0)
    plt.show()
