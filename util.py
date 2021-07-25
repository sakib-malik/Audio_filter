import numpy as np


def dft_of_Hz(zeros, poles, samples=500):
    '''

    Parameters
    ----------
    zeros
    poles
    A
    N_M
    samples -> Number of samples for DFT

    Returns
    Computes DFT (Discrete) of Hz from its zeros and poles

    '''
    N_M = len(poles) - len(zeros)
    w = np.linspace(0, 2*np.pi, samples)
    H = (np.exp(1j*w)**N_M)
    for z in zeros:
        H *= (np.exp(1j*w) - z)
    for p in poles:
        H /= (np.exp(1j*w) - p)
    return H


def apply_filter(b, a, X):
    '''

    Parameters
    ----------
    b -> numerator coeff
    a -> denominator coeff
    X -> input signal

    Returns
    -------
    Output signal after filtering
    '''

    #          b[0] + b[1]z  + ... + b[M] z
    #     Y(z) = -------------------------------- X(z)
    #                      -1              -N
    #          a[0] + a[1]z  + ... + a[N] z

    zeros = np.poly1d(b).roots
    poles = np.poly1d(a).roots
    H = dft_of_Hz(zeros, poles, samples=len(X))
    Y = np.real(np.fft.ifft(np.fft.fft(X) * H))
    return (Y / (max(Y) - min(Y))) * (max(X) - min(X))

# EXAMPLES OF WORKING

# N = 100
# n = np.arange(N)
# x = np.sin(2 * np.pi * n / N)
# x_noise = x + np.random.normal(0, 0.05, len(x))
# from scipy import signal
# b, a = np.array([1, -1]) , np.array([2])   # HP
# b, a = np.array([1, 1]) , np.array([2])   # LP
# b, a = np.array([0.25, 0.25]) , np.array([1, -0.5]) # LP
# b, a = np.array([0.25, -0.25]) , np.array([1, -0.5]) # HP
# b, a = signal.butter(3, 0.05)

# y = apply_filter(b, a, x_noise)
# import matplotlib.pyplot as plt
# plt.plot(x_noise)
# plt.plot(y)
# plt.show()