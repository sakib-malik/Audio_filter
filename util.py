import numpy as np


def dft_of_Hz(zeros, poles, A = 1, samples=500):
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
    N_M = len(zeros) - len(poles)
    w = np.linspace(0, 2*np.pi, samples)
    H = A * np.exp(1j*w)**N_M
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
    Y = np.fft.ifft(np.fft.fft(X) * H)
    return Y

from scipy import signal
b, a = signal.butter