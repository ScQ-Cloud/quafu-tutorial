import matplotlib.pyplot as plt
import numpy as np

from quafu import QuantumCircuit, Task, simulate

def iqft(qc, n):
    """
    inverse quantum Fourier transform, apply the adjoint operator
    in the original quantum Fourier transform circuit in reverse order.
    """

    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)  # swap before rotate
    for i in range(n):
        for k in range(i):
            qc.cp(n - k - 1, n - 1 - i, -np.pi * (2 ** (k - i)))  # in reverse order
        qc.h(n - i - 1)
    return qc


def mix(qc, n):
    """
    mix into the uniform superposition state
    """
    for qubit in range(n):
        qc.h(qubit)
    return qc


def pe_test():  # just for test
    qc2 = QuantumCircuit(6)
    qc2.x(5)
    mix(qc2, 5)
    angle = 2 * np.pi / 3
    repetitions = 1
    for help_qubit in range(5):
        for i in range(repetitions):
            qc2.cp(help_qubit, 5, angle)
        repetitions *= 2
    qc2.barrier([0, 1, 2, 3, 4, 5])
    iqft(qc2, 5)
    qc2.barrier([0, 1, 2, 3, 4, 5])
    qc2.measure([0, 1, 2, 3, 4])
    qc2.draw_circuit(width=0)
    simu_res2 = simulate(qc2, output='probabilities')
    simu_res2.plot_probabilities()
    plt.show()


def controlledu(qc, a=7):
    for help_qubit in range(9):
        ctrl=8-help_qubit
        for iteration in range(2 ** help_qubit):
            if a in [2, 13]:
                qc.fredkin(ctrl, 9, 10)
                qc.fredkin(ctrl, 10, 11)
                qc.fredkin(ctrl, 11, 12)
            if a in [7, 8]:
                qc.fredkin(ctrl, 11, 12)
                qc.fredkin(ctrl, 10, 11)
                qc.fredkin(ctrl, 9, 10)
            if a in [4, 11]:
                qc.fredkin(ctrl, 9, 11)
                qc.fredkin(ctrl, 10, 12)
            if a in [7, 11, 13]:
                for q in range(4):
                    qc.cx(ctrl, 9 + q)


def controlledu_test():  ##just for test
    qct = QuantumCircuit(13)
    for z in range(9):
        qct.x(z)
    qct.x(12)
    controlledu(qct)
    qct.measure([9, 10, 11, 12])
    qct.draw_circuit(width=1)
    simu_res_test = simulate(qct, output='probabilities')
    simu_res_test.plot_probabilities(full=False)
    plt.show()

N = 15
a = 7
x = 7
n = 13
# pe_test()
#controlledu_test()
qpe = QuantumCircuit(n)
qpe.x(n - 1)  # prepare |1> state in the second register
mix(qpe, n - 4)
controlledu(qpe)  # controlled U
iqft(qpe, n - 4)
qpe.measure(list(range(n - 4)))
qpe.draw_circuit(width=1)
simu_res = simulate(qpe, output='state_vector')
print(simu_res.state_vector)
plt.show()
