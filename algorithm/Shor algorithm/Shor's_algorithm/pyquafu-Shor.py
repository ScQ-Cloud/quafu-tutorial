print(bin(10)[2:])
#import packages we need
from quafu import QuantumCircuit,Task,simulate
import numpy as np
import matplotlib.pyplot as plt

def iqft(qc,n): #inverse quantum Fourier transform, apply the adjoint operator in the original quantum Fourier transform circuit in reverse order.
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1) #swap before rotate
    for i in range(n):
        for k in range(i):
            qc.cp(n-k-1,n-1-i,-np.pi*(2**(k-i))) #in reverse order
        qc.h(n-i-1)
    return qc

def mix(qc,n):
    for qubit in range(n):
        qc.h(qubit)##mix into the uniform superposition state
    return qc

def controlledu(qc,x=7):
    for ctrl in range(8):
        for iteration in range(2**ctrl):
            if a in [2, 13]:
                qc.fredkin(ctrl,9,10)
                qc.fredkin(ctrl,10,11)
                qc.fredkin(ctrl,11,12)
            if a in [7,8]:
                qc.fredkin(ctrl, 11, 12)
                qc.fredkin(ctrl, 10, 11)
                qc.fredkin(ctrl, 9, 10)
            if a in [4, 11]:
                qc.fredkin(ctrl, 9, 11)
                qc.fredkin(ctrl, 10, 12)
            if a in [7, 11, 13]:
                for q in range(4):
                    qc.cx(ctrl,9+q)
N=15;a=7;x=7;n=13
qpe=QuantumCircuit(n)
for i in range(4):
    qpe.swap(i,8-i)
for i in range(2):
    qpe.swap(9+i,12-i)
qpe.x(n-1)  # prepare |1> state in the second register
mix(qpe,n-1)
controlledu(qpe)# controlled U
qpe.barrier(list(range(n)))
iqft(qpe, n-1)
qpe.barrier(list(range(n)))
qpe.measure(list(range(n-1)))
qpe.draw_circuit(width=1)
simu_res = simulate(qpe, output='probabilities')
simu_res.plot_probabilities(full=False)
plt.show()
