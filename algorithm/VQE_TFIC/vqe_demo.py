import numpy as np
from quafu import QuantumCircuit, simulate
import matplotlib.pyplot as plt

"""
A minimum working example of variational quantum eigen-solver 
for ground-state energy of TFIC model.
"""


def apply_ansatz(qc, n, paras):
    """
    Prepare the ansatz state
    |psi>=U|0>
    """
    for i in range(n):
        qc.rx(i, paras[i])

    for i in range(n // 2):
        qc.cnot(2 * i, (2 * i + 1) % n)

    for i in range(n // 2):
        qc.cnot((2 * i + 1), (2 * i + 2) % n)


def inverse_ansatz(qc, n, paras):
    """
    <psi|=<0|U^+
    """
    for i in range(n // 2):
        qc.cnot((2 * i + 1), (2 * i + 2) % n)

    for i in range(n // 2):
        qc.cnot(2 * i, (2 * i + 1) % n)

    for i in range(n):
        qc.rx(i, -paras[i])


def eval_zz(n, paras, i):
    """
    Evaluate <psi|Z_i Z_{i+1}|psi>
    """
    qc = QuantumCircuit(n)

    apply_ansatz(qc, n, paras)
    qc.barrier()

    qc.z(i)
    qc.z((i + 1) % n)

    qc.barrier()
    inverse_ansatz(qc, n, paras)

    qc.measure()

    simu_res = simulate(qc, output='state_vector')
    expectation = simu_res.state_vector[0]
    assert np.isreal(expectation), 'expectation is not real'

    return expectation.real


def eval_x(n, paras, i):
    """
    Evaluate <psi|X_i|psi>
    """
    qc = QuantumCircuit(n)

    apply_ansatz(qc, n, paras)
    qc.barrier()

    qc.x(i)

    qc.barrier()
    inverse_ansatz(qc, n, paras)

    qc.measure()

    simu_res = simulate(qc, output='state_vector')
    expectation = simu_res.state_vector[0]
    assert abs(expectation.imag) < 1e-15, f'expectation is not real: {expectation}'

    return expectation.real


def exact_e_gs(n: int, h: float):
    """
    Exact result of ground-state energy of transverse Ising chain
    with h > 0 and under PBC.
    """
    ks = np.pi / n * np.arange(-(n - 1) + n % 2, n + 1, 2)
    es = (1 + h ** 2 - 2 * h * np.cos(ks)) ** 0.5
    return - np.sum(es)


def metropolis_vqe(n: int, h: float, opt_steps: int = 1000, verbose: bool = False):
    # init
    energy = 0
    records = []
    paras = np.random.random(n) * np.pi
    if verbose:
        print('initial paras:', paras)

    # hyper parameters
    lr = 0.05
    t = 0.2

    for k in range(opt_steps):
        # make a movement
        d_paras = lr * np.random.randn(n)
        paras_p = (paras + d_paras) % np.pi
        energy_p = 0

        # evaluate expectation
        for i in range(n):
            energy_p -= eval_zz(n, paras_p, i)
            energy_p -= h * eval_x(n, paras_p, i)

        # optimize using Metropolis scheme
        de = energy_p - energy
        _ = np.random.random()
        if k == 0:
            energy = energy_p
            records.append(energy)
            continue
        if _ < np.exp(-de/t):
            paras = paras_p
            energy = energy_p
        if verbose:
            print(f'{k}-th step, delta_e={de:3}, energy={energy:3}')
        records.append(energy)
    return records, paras


if __name__ == '__main__':
    spin_num = 5
    h = 1
    step_num = 2000
    e_exact = exact_e_gs(spin_num, h)
    energy_records, paras_final = metropolis_vqe(n=spin_num, h=h, opt_steps=step_num, verbose=True)
    print('final paras:', paras_final)

    plt.plot(range(step_num), energy_records)
    plt.plot([0, step_num], [e_exact] * 2)
    plt.text(0, e_exact, f'Eg(exact)={e_exact:.3f}', va='bottom', ha='left')
    plt.title('TFIC-QVE by Metropolis Optimization')
    plt.ylabel('energy')
    plt.xlabel('steps')
    plt.savefig('TFIC-QVE by Metropolis Optimization.png', dpi=300)
