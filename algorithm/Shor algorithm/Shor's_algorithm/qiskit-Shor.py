#import packages we need
from qiskit import Aer, transpile, assemble
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np

def c_Uamod15(a, p):
    U = QuantumCircuit(4)# concatenate U-factors to form U^p
    for iteration in range(p):
        if a in [2,13]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [7,8]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a in [4, 11]:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = "{0}^{1} mod {2}".format(a, p, N)
    c_U = U.control()
    return c_U
# inverse QFT
def qft_dagger(n):
    qc = QuantumCircuit(n)
    for q in range(n//2):
        qc.swap(q, n-q-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc

# Initialize registers and the quantum circuit
n_work = 4 # L
a=7;N=15
n_control = 2 * n_work + 1 # 2*L+1
c = QuantumRegister(n_control, name='c')
w = QuantumRegister(n_work, name='w')
cl = ClassicalRegister(n_control, name='cl')
qc = QuantumCircuit(c, w, cl)
# Initialize control qubits
for q in range(n_control):
    qc.h(q)
# Populate work register with state |1>
qc.x(n_control)
# Controlled-U^p operations formed by concatenation
for k in range(n_control):
    qc.append(c_Uamod15(a, 2**k),[k] + [i+n_control for i in range(n_work)])
# Inverse-QFT
qc.append(qft_dagger(n_control), range(n_control))
# Measure control register
qc.measure(c, cl)

# simulate
aer_sim = Aer.get_backend('aer_simulator')
t_qc = transpile(qc, aer_sim)
obj = assemble(t_qc)
results = aer_sim.run(obj, shots=1024).result()
counts = results.get_counts()
plot_histogram(counts, title='N = {0} a = {1}'.format(N, a), figsize=(6,8))
plt.show()