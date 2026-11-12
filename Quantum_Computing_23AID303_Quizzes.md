# 23AID303 Quantum Computing & Algorithms — Evaluated Quizzes & Question Bank

This document compiles all questions, answer options, verified correct answers, and detailed explanations from the three evaluated assessments:
1. **Continuous Evaluation 2 (CE 2)** — Grover’s Algorithm, Shor’s Algorithm, QFT
2. **Continuous Evaluation 3 (CE 3)** — NISQ Era, VQA, VQE, Parameter-Shift Rule
3. **Part A: Final Project Review Subject Viva** — Fundamentals, Qiskit, Quantum Gates, Measurements

---

# Assessment 1: Continuous Evaluation 2 (CE 2)
**Topics:** Grover's Algorithm, Shor's Algorithm, Quantum Fourier Transform (QFT)  
**Total Questions:** 17

---

### Q1. Grover's Speedup
* **Type:** True / False
* **Question:** Grover's algorithm gives an exponential speedup over classical unstructured search.
* **Options:**
  * True
  * False
* **Correct Answer:** **False**
* **Explanation:** Grover's algorithm provides a **quadratic speedup** ($O(\sqrt{N})$ compared to classical $O(N)$). Algorithms like Shor's provide exponential speedup, but Grover's search is provably optimal at quadratic speedup.

---

### Q2. Basis Representation Dimension
* **Type:** Multiple Choice (MCQ)
* **Question:** A quantum state $|\psi\rangle$ is represented using 32 computational basis states. How many states are required in the Fourier basis to represent the same quantum state?
* **Options:**
  * A) 5
  * B) 16
  * C) 32
  * D) 64
* **Correct Answer:** **C) 32**
* **Explanation:** The Quantum Fourier Transform (QFT) is an orthonormal change of basis within the Hilbert space. The dimensionality of the state space does not change; a state in a 32-dimensional Hilbert space requires exactly 32 basis states in any complete orthonormal basis, including the Fourier basis.

---

### Q3. Ancilla Preparation in Grover's Algorithm
* **Type:** Fill in the Blanks
* **Question:** In the Grover circuit, the ancilla is prepared in $|-\rangle$ by applying $X$ and then ______.
* **Accepted Answers:** `H` / `Hadamard` / `Hadamard Gate` / `Hadamard (H)`
* **Correct Answer:** **H (Hadamard)**
* **Explanation:** An ancilla qubit initialized in $|0\rangle$ is flipped by $X$ to $|1\rangle$. Applying a Hadamard gate produces $H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} = |-\rangle$, which enables phase kickback during oracle evaluation ($(-1)^{f(x)}$).

---

### Q4. Role of QFT in Shor's Algorithm
* **Type:** Multiple Choice (MCQ)
* **Question:** In Shor’s algorithm for integer factorization, at which stage is the Quantum Fourier Transform (QFT) primarily used?
* **Options:**
  * A) To extract the periodicity of the function
  * B) To initialize all qubits into the $|0\rangle$ state
  * C) To perform modular exponentiation
  * D) To perform the final classical factorization
* **Correct Answer:** **A) To extract the periodicity of the function**
* **Explanation:** Shor's algorithm maps factoring to order-finding (period finding of $f(x) = a^x \pmod N$). The inverse QFT transforms the periodic state in the first register into sharp probability peaks corresponding to multiples of $1/r$, allowing the period $r$ to be extracted.

---

### Q5. Optimal Grover Iterations for $N = 64$
* **Type:** Multiple Choice (MCQ)
* **Question:** For $N = 64$ with one marked item, the optimal number of Grover iterations is:
* **Options:**
  * A) 4
  * B) 6
  * C) 8
  * D) 16
* **Correct Answer:** **B) 6**
* **Explanation:** The optimal number of iterations is given by $R \approx \frac{\pi}{4}\sqrt{N} = \frac{\pi}{4}\sqrt{64} = \frac{\pi}{4} \times 8 \approx 2\pi \approx 6.28$. Rounding to the nearest integer yields **6**.

---

### Q6. Reflection Operator
* **Type:** Multiple Choice (MCQ)
* **Question:** The operator that reflects a vector about the line spanned by a unit vector $|u\rangle$ is $R_u =$ ______.
* **Options:**
  * A) $2|u\rangle\langle u| - I$
  * B) $2\langle u|u\rangle - I$
  * C) $2|0\rangle\langle 0| - I$
  * D) $H(2|u\rangle\langle u| - I)H$
* **Correct Answer:** **A) $2|u\rangle\langle u| - I$**
* **Explanation:** An elementary reflection across the subspace spanned by $|u\rangle$ preserves components parallel to $|u\rangle$ ($(2 - 1)|u\rangle = |u\rangle$) and negates orthogonal components ($(0 - 1)|u^\perp\rangle = -|u^\perp\rangle$), which is expressed as $2|u\rangle\langle u| - I$.

---

### Q7. Modular Exponentiation in Shor's Algorithm
* **Type:** Multiple Choice (MCQ)
* **Question:** In a quantum circuit implementing Shor’s algorithm, which part of the circuit is responsible for performing modular exponentiation?
* **Options:**
  * A) Hadamard gates
  * B) QFT Block
  * C) Measurement gates
  * D) The Oracle
* **Correct Answer:** **D) The Oracle**
* **Explanation:** The quantum oracle $U_f$ computes $|x\rangle|0\rangle \to |x\rangle|a^x \pmod N\rangle$, implementing the reversible modular exponentiation circuit.

---

### Q8. Quantum vs Classical Steps in Shor's Algorithm
* **Type:** Multiple Choice (MCQ)
* **Question:** In Shor's algorithm, which step actually needs the quantum computer?
* **Options:**
  * A) Computing $\gcd(a, N)$
  * B) Order-finding
  * C) Continued-fraction expansion
  * D) Checking that $a$ and $N$ are coprime
* **Correct Answer:** **B) Order-finding**
* **Explanation:** $\gcd(a, N)$, coprimality checks, and continued-fraction expansion are all efficiently solvable in polynomial time on a classical computer using Euclid's algorithm. Only **order-finding** (finding the period $r$ of $a^x \pmod N$) is computationally hard classically and requires the quantum routine.

---

### Q9. Success Probability with Over-Iteration in Grover's
* **Type:** True / False
* **Question:** In Grover's algorithm, running more iterations than the optimal number always increases the success probability.
* **Options:**
  * True
  * False
* **Correct Answer:** **False**
* **Explanation:** Grover's algorithm acts as a geometric rotation in a 2D subspace. Continuing iterations past the optimal point $\theta \approx \pi/2$ causes the state vector to rotate past the marked state, decreasing the success probability (over-rotation).

---

### Q10. Ancilla Qubits to Factor $N = 15$
* **Type:** Fill in the Blanks
* **Question:** How many ancilla qubits are needed to factor $N = 15$?
* **Accepted Answers:** `4` / `Four` / `Four (4)` / `4 (Four)`
* **Correct Answer:** **4**
* **Explanation:** To hold the values of $a^x \pmod{15}$, the register must hold numbers up to $N-1 = 14$. The number of qubits required is $n = \lceil \log_2(15) \rceil = 4$ qubits ($2^4 = 16 > 15$).

---

### Q11. Period Calculation in Shor's Algorithm
* **Type:** Fill in the Blanks
* **Question:** The period of the function $f(p) = g^p \pmod N$ given $g = 8$ and $N = 15$ is ______.
* **Accepted Answers:** `4` / `Four`
* **Correct Answer:** **4**
* **Explanation:** Evaluate successive powers modulo 15:
  * $8^0 \equiv 1 \pmod{15}$
  * $8^1 \equiv 8 \pmod{15}$
  * $8^2 = 64 \equiv 4 \pmod{15}$
  * $8^3 = 32 \equiv 2 \pmod{15}$
  * $8^4 = 16 \equiv 1 \pmod{15}$
  The sequence repeats every 4 powers, so the period $r = 4$.

---

### Q12. Grover Probability for $N = 4$
* **Type:** Multiple Choice (MCQ)
* **Question:** For $N = 4$ with one marked item, the success probability after one Grover iteration is:
* **Options:**
  * A) 25%
  * B) 50%
  * C) 75%
  * D) 100%
* **Correct Answer:** **D) 100%**
* **Explanation:** For $N = 4$ (2 qubits), the rotation angle per Grover step is $\theta = 2\arcsin(1/\sqrt{4}) = 2\arcsin(1/2) = \pi/3$. The initial state is at angle $\pi/6$. A single rotation advances the angle to $\pi/6 + \pi/3 = \pi/2$, exactly aligning the state with the marked state. Thus, the probability is $\sin^2(\pi/2) = 1.0$ (100%).

---

### Q13. Verification of Continued Fractions in Shor's
* **Type:** True / False
* **Question:** In Shor's algorithm to factorize 15, we proceed with a guess value $g = 8$. Suppose the measurement gives the output $M = 8$, and $2^n = 16$ where $n$ is the number of ancilla qubits. The continued-fraction candidate for $r$ will definitely pass the verification ($a^r \pmod N = 1$).
* **Options:**
  * True
  * False
* **Correct Answer:** **False**
* **Explanation:** With $M = 8$ and $2^n = 16$, the fraction is $M/2^n = 8/16 = 1/2$. The continued fraction expansion yields denominator candidate $r' = 2$. However, $8^2 \pmod{15} = 64 \pmod{15} = 4 \ne 1$. Because $r'$ is a factor of the true period ($r=4$) rather than the full period, the verification fails.

---

### Q14. Output of QFT on Periodic Register
* **Type:** Multiple Choice (MCQ)
* **Question:** A 4-qubit register holds an equal superposition of $p = 1, 5, 9, 13$. After the QFT, the possible measurement outcomes are:
* **Options:**
  * A) {0, 4, 8, 12}
  * B) {1, 5, 9, 13}
  * C) {0, 2, 4, …, 14}
  * D) All 16 values, equally likely
* **Correct Answer:** **A) {0, 4, 8, 12}**
* **Explanation:** For a 4-qubit system ($N = 16$), the state has period $r = 4$ (values spaced by 4: $1, 1+4, 1+8, 1+12$). The discrete Fourier transform of a periodic train with period $r$ yields peaks at multiples of $N/r = 16/4 = 4$, which are $\{0, 4, 8, 12\}$. The offset $p=1$ introduces a global linear phase shift that does not affect measurement probabilities.

---

### Q15. Oracle Marking "101" and "111"
* **Type:** Multiple Choice (MCQ)
* **Question:** Assume three search qubits and an ancilla $q_3$ that is already prepared in $|-\rangle$. Which code excerpt marks exactly the two states "101" and "111"?
* **Options:**
  * A) `qc.mcx([0, 1, 2], 3)`
  * B) `qc.ccx(0, 1, 3)`
  * C) `qc.ccx(0, 2, 3)`
  * D) `qc.ccx(1, 2, 3)`
* **Correct Answer:** **C) qc.ccx(0, 2, 3)**
* **Explanation:** The binary representations are $|q_2 q_1 q_0\rangle = |101\rangle$ and $|111\rangle$. In both target states, $q_2 = 1$ and $q_0 = 1$, while $q_1$ can be either $0$ or $1$ (don't care). Controlling on qubits 0 and 2 flips the phase on both $|101\rangle$ and $|111\rangle$ via the $|-\rangle$ target.

---

### Q16. Parity Oracle for $a + b$ Even
* **Type:** Multiple Choice (MCQ)
* **Question:** Which circuit writes $f(a, b) = 1$ (when $a + b$ is even) onto the ancilla $q_4$? Setup: $a = (q_1 q_0)$ and $b = (q_3 q_2)$, with $q_0$ and $q_2$ as least significant bits. Ancilla $q_4$ starts in $|0\rangle$.
* **Options:**
  * A [Correct]
  * B
  * C
  * D
* **Correct Answer:** **A**
* **Explanation:** The sum of two integers $a + b$ is even if and only if their least significant bits have the same parity: $q_0 \oplus q_2 = 0$. Therefore, $f(a, b) = \overline{q_0 \oplus q_2} = X(q_0 \oplus q_2)$. The circuit applies CNOTs from $q_0$ and $q_2$ into the target, followed/preceded by an $X$ gate (or initializing $q_4$ in $|1\rangle$), corresponding to Circuit A.

---

### Q17. 3-Qubit QFT Circuit
* **Type:** Multiple Choice (MCQ)
* **Question:** Which circuit correctly implements the 3-qubit QFT?
* **Options:**
  * A) Quantum Circuit A
  * B) Both Quantum Circuit B and C
  * C) Quantum Circuit C
  * D) Quantum Circuit B and D
* **Correct Answer:** **C) Quantum Circuit C**
* **Explanation:** A standard 3-qubit QFT requires Hadamard on $q_0$, controlled-$R_2$ ($S$) from $q_1$, controlled-$R_3$ ($T$) from $q_2$, followed by Hadamard on $q_1$, controlled-$R_2$ from $q_2$, Hadamard on $q_2$, and a final SWAP between $q_0$ and $q_2$. Circuit C implements this sequence correctly with proper gate orientations.

---
---

# Assessment 2: Continuous Evaluation 3 (CE 3)
**Topics:** NISQ Era, Variational Quantum Algorithms (VQA), VQE, Parameter-Shift Rule  
**Total Questions:** 20

---

### Q1. Quantum Resources vs. Noise
* **Type:** Multiple Choice (MCQ)
* **Question:** Which of the following correctly describes the role of superposition, entanglement, and decoherence in quantum computing?
* **Options:**
  * A) Superposition and entanglement are undesirable, while decoherence is useful.
  * B) Superposition and entanglement are quantum resources, while decoherence is undesirable.
  * C) All three are essential resources for quantum computation.
  * D) Decoherence enhances the stability and performance of qubits.
* **Correct Answer:** **B) Superposition and entanglement are quantum resources, while decoherence is undesirable.**
* **Explanation:** Superposition and entanglement enable computational speedups and quantum parallelism. Decoherence is the unwanted loss of quantum coherence caused by environmental coupling.

---

### Q2. Meaning of NISQ
* **Type:** True / False
* **Question:** NISQ era stands for "Noisy Immediate-Scale Quantum"
* **Options:**
  * True
  * False
* **Correct Answer:** **False**
* **Explanation:** NISQ stands for **Noisy Intermediate-Scale Quantum**, coined by John Preskill in 2018.

---

### Q3. Why NISQ Devices are "Noisy"
* **Type:** Multiple Choice (MCQ)
* **Question:** Why are NISQ quantum computers considered “noisy”?
* **Options:**
  * A) Because decoherence, gate errors, and measurement errors can accumulate during computation
  * B) Because quantum gates are completely random
  * C) Because qubits cannot be entangled
  * D) Because qubits exist in superposition
* **Correct Answer:** **A) Because decoherence, gate errors, and measurement errors can accumulate during computation**

---

### Q4. Noise Percentage Estimation
* **Type:** Multiple Choice (MCQ)
* **Question:** Calculate approximately what percentage of measurements amounts to noise?
* **Options:**
  * A) 10 %
  * B) 15 %
  * C) 85 %
  * D) 50 %
* **Correct Answer:** **B) 15 %**

---

### Q5. Factors Influencing Quantum Volume
* **Type:** True / False
* **Question:** Quantum Volume depends not only on the number of qubits but also on factors such as gate errors, measurement errors, crosstalk, and qubit connectivity. Therefore, simply increasing the number of qubits does not necessarily increase the Quantum Volume.
* **Options:**
  * True
  * False
* **Correct Answer:** **True**
* **Explanation:** Quantum Volume measures the largest square circuit depth and width that can be successfully executed with low error rates. Adding low-fidelity or poorly connected qubits decreases or stagnates Quantum Volume.

---

### Q6. Parameter-Shift Rule Evaluations
* **Type:** Multiple Choice (MCQ)
* **Question:** For a VQA with 100 trainable parameters, if the parameter-shift rule is used to calculate the gradient of every parameter, how many circuit evaluations are required for one optimization step, excluding the original circuit evaluation?
* **Options:**
  * A) 200
  * B) 100
  * C) 10,000
  * D) 300
* **Correct Answer:** **A) 200**
* **Explanation:** The parameter-shift rule evaluates $\frac{\partial \langle H \rangle}{\partial \theta_i} = \frac{\langle H \rangle_{\theta_i + \pi/2} - \langle H \rangle_{\theta_i - \pi/2}}{2}$. Each parameter requires 2 shifted evaluations. For $P = 100$ parameters: $2 \times 100 = 200$ circuit evaluations.

---

### Q7. Multiplicative Observable Dependence
* **Type:** Multiple Choice (MCQ)
* **Question:** For the two-qubit circuit consisting of $R_y(\theta_1)$ and $R_y(\theta_2)$, which observable depends on both parameters multiplicatively?
* **Options:**
  * A) $ZI$
  * B) $IZ$
  * C) $ZI + IZ$
  * D) $ZZ$
* **Correct Answer:** **D) ZZ**
* **Explanation:** For unentangled single-qubit rotations starting in $|00\rangle$, $\langle ZI \rangle = \cos\theta_1$ and $\langle IZ \rangle = \cos\theta_2$. The joint expectation value factors as $\langle ZZ \rangle = \langle Z \rangle_1 \langle Z \rangle_2 = \cos(\theta_1)\cos(\theta_2)$, which depends multiplicatively on both parameters.

---

### Q8. Expectation Value Calculation
* **Type:** Multiple Choice (MCQ)
* **Question:** [Expectation value of orthogonal state / observable]
* **Options:**
  * A) 1
  * B) -1
  * C) 0
  * D) 1/2
* **Correct Answer:** **C) 0**

---

### Q9. Quantity Minimized in VQE
* **Type:** Multiple Choice (MCQ)
* **Question:** In the VQE, which quantity is minimized by the classical optimizer?
* **Options:**
  * A) Qubit count
  * B) Measurement probability
  * C) Expectation value of the Hamiltonian
  * D) Expectation value of the Z operator
* **Correct Answer:** **C) Expectation value of the Hamiltonian**
* **Explanation:** By the Rayleigh-Ritz variational principle, $\langle \psi(\vec{\theta})|H|\psi(\vec{\theta})\rangle \ge E_0$. The classical optimizer updates $\vec{\theta}$ to minimize this expectation value to approximate ground state energy $E_0$.

---

### Q10. Parameterized Trial Circuit Name
* **Type:** Descriptive / One-Word
* **Question:** What is the name given to the parameterized quantum circuit used to prepare the trial quantum state in VQE? (Answer in 1 word)
* **Expected Answer:** **Ansatz**

---

### Q11. Physical Quantity of VQE Cost Function
* **Type:** Descriptive
* **Question:** What quantity does the VQE cost function represent?
* **Expected Keywords:** **Energy / Expectation value of Hamiltonian / Energy error**
* **Explanation:** The cost function evaluates the expected ground state energy of the target physical system represented by the Hamiltonian $\langle H \rangle$.

---

### Q12. Measurement Results vs. Eigenvalues
* **Type:** True / False
* **Question:** Every possible measurement result of an observable must lie between its smallest and largest eigenvalues, but need not itself be an eigenvalue.
* **Options:**
  * True
  * False
* **Correct Answer:** **False**
* **Explanation:** According to the postulates of quantum mechanics, the outcome of any projective measurement of an observable **must be strictly one of its eigenvalues**. It is the *expectation value* (mean of many measurements) that lies between the smallest and largest eigenvalues.

---

### Q13. Probability Sum Invariant
* **Type:** True / False
* **Question:** In the two-qubit $R_y$ circuit, the probabilities of the four computational-basis states need not sum to one.
* **Options:**
  * True
  * False
* **Correct Answer:** **False**
* **Explanation:** Quantum states are normalized unit vectors ($\langle\psi|\psi\rangle = 1$), meaning total probability across all mutually exclusive basis states $\sum_i P(i)$ must strictly equal 1.

---

### Q14. Hybrid Nature of VQE
* **Type:** True / False
* **Question:** VQE completely eliminates the need for a classical computer once the quantum circuit has been constructed.
* **Options:**
  * True
  * False
* **Correct Answer:** **False**
* **Explanation:** VQE is an inherently hybrid quantum-classical algorithm. The classical computer is permanently in the loop to execute the parameter optimization routines (COBYLA, SPSA, Adam).

---

### Q15. Molecular Hamiltonian Representation
* **Type:** Fill in the Blanks
* **Question:** The qubit Hamiltonian obtained after transforming the molecular Hamiltonian is expressed as a sum of ______ strings.
* **Accepted Answers:** `Pauli` / `pauli`
* **Correct Answer:** **Pauli**
* **Explanation:** Transformations such as Jordan-Wigner or Bravyi-Kitaev map fermionic annihilation/creation operators into linear combinations of tensor products of Pauli matrices: $H = \sum_j c_j P_j$ where $P_j \in \{I, X, Y, Z\}^{\otimes n}$.

---

### Q16. Two-Qubit $R_y$ at $\theta_1 = \theta_2 = 0$
* **Type:** Multiple Choice (MCQ)
* **Question:** In a 2 qubit $R_y$ circuit, if $\theta_1 = \theta_2 = 0$, which computational-basis state is obtained with probability 1?
* **Options:**
  * A) $|00\rangle$
  * B) $|01\rangle$
  * C) $|10\rangle$
  * D) $|11\rangle$
* **Correct Answer:** **A) $|00\rangle$**
* **Explanation:** $R_y(0) = \begin{pmatrix} \cos 0 & -\sin 0 \\ \sin 0 & \cos 0 \end{pmatrix} = I$. Qubits initialized in $|00\rangle$ remain in $|00\rangle$ with probability 1.

---

### Q17. Optimization Loop in VQA
* **Type:** Multiple Choice (MCQ)
* **Question:** Which statement best describes the optimization loop in a VQA?
* **Options:**
  * A) The quantum computer updates parameters while the classical computer measures observables
  * B) The classical computer prepares the quantum state and the quantum computer performs optimization
  * C) Both computers independently minimize the cost function
  * D) The quantum computer evaluates the cost function and the classical computer updates the parameters
* **Correct Answer:** **D) The quantum computer evaluates the cost function and the classical computer updates the parameters**

---

### Q18. Importance of Shallow Ansätze for NISQ
* **Type:** Multiple Choice (MCQ)
* **Question:** Why are shallow ansätze particularly important for NISQ devices?
* **Options:**
  * A) They eliminate the need for classical optimization
  * B) They guarantee the global minimum of the cost function
  * C) They reduce the effect of limited coherence time and decoherence
  * D) They require more entangling gates to improve expressibility
* **Correct Answer:** **C) They reduce the effect of limited coherence time and decoherence**
* **Explanation:** NISQ hardware has short coherence times ($T_1, T_2$) and high gate error rates. Shallow circuits finish execution before decoherence destroys quantum information.

---

### Q19. Limitations of VQE
* **Type:** Multiple Choice (MCQ)
* **Question:** Which of the following is NOT listed as a limitation of VQE?
* **Options:**
  * A) Measurement overhead
  * B) Barren plateaus
  * C) Dependence on ansatz choice
  * D) Elimination of decoherence
* **Correct Answer:** **D) Elimination of decoherence**
* **Explanation:** VQE does *not* eliminate decoherence (it suffers from it). Measurement overhead, barren plateaus (vanishing gradients), and ansatz dependency are well-known limitations.

---

### Q20. Observable Terms in Hamiltonian
* **Type:** Multi-Choice / Select All That Apply
* **Question:** Select all observable terms corresponding to the system:
* **Options:**
  * A) $ZII$ [Correct]
  * B) $IIZ$ [Correct]
  * C) $IZI$
  * D) $III$
* **Correct Answer:** **A ($ZII$) and B ($IIZ$)**

---
---

# Assessment 3: Part A — Final Project Review Subject Viva
**Topics:** Quantum Fundamentals, Gates, Measurement, Qiskit  
**Total Questions:** 15

---

### Q1. Purpose of Quantum Gates
* **Type:** Multiple Choice (MCQ)
* **Question:** What is the purpose of quantum gates in quantum computing?
* **Options:**
  * A) To entangle qubits
  * B) To collapse superposition
  * C) To manipulate qubits
  * D) To measure qubit states
* **Correct Answer:** **C) To manipulate qubits**
* **Explanation:** Quantum gates perform controlled unitary transformations to manipulate the amplitudes and phases of quantum states.

---

### Q2. Entanglement Measurement Speed
* **Type:** Multiple Choice (MCQ)
* **Question:** When two particles are entangled and it is observed that one has its spin up, how long does it take for the other’s spin to be down?
* **Options:**
  * A) However long it takes light to travel between them
  * B) 1 nanosecond
  * C) Instantaneously
  * D) 1 microsecond
* **Correct Answer:** **C) Instantaneously**
* **Explanation:** Wavefunction collapse across entangled systems occurs instantaneously upon measurement regardless of spatial separation (non-local quantum correlation).

---

### Q3. Classical vs. Quantum Logic Gates
* **Type:** Multiple Choice (MCQ)
* **Question:** A fundamental difference between classical and quantum logic gates is that:
* **Options:**
  * A) Quantum gates are irreversible like classical AND gates.
  * B) Quantum gates are reversible unitary transformations.
  * C) Quantum gates destroy data upon measurement.
  * D) Quantum gates require no energy.
* **Correct Answer:** **B) Quantum gates are reversible unitary transformations.**
* **Explanation:** Conservation of probability dictates that closed quantum evolution is governed by unitary operators ($U^\dagger U = I$), making all quantum gates reversible.

---

### Q4. Characteristics of NISQ-Era Computers
* **Type:** Multiple Choice (MCQ)
* **Question:** What is a characteristic of NISQ-era quantum computers?
* **Options:**
  * A) Large number of qubits with perfect coherence
  * B) High error rates and limited number of qubits
  * C) Error-corrected and fault-tolerant
  * D) Infinite computational capacity
* **Correct Answer:** **B) High error rates and limited number of qubits**
* **Explanation:** NISQ machines typically possess 50–1000 qubits without full fault-tolerant quantum error correction (QEC), meaning they have significant gate and measurement noise.

---

### Q5. Definition of Quantum Volume
* **Type:** Multiple Choice (MCQ)
* **Question:** What does quantum volume measure?
* **Options:**
  * A) The physical size of a quantum computer
  * B) The overall computational power of a quantum computer considering qubits, connectivity, and gate errors
  * C) The number of classical bits a quantum computer can store
  * D) The number of qubits only
* **Correct Answer:** **B) The overall computational power of a quantum computer considering qubits, connectivity, and gate errors**

---

### Q6. Probabilistic Nature of Quantum Computing
* **Type:** Multiple Choice (MCQ)
* **Question:** Classical computation is deterministic, while quantum computation is often probabilistic because:
* **Options:**
  * A) Quantum systems are error-free.
  * B) Measurement collapses a superposition into a single outcome with certain probabilities.
  * C) Quantum computers use binary logic gates.
  * D) Quantum computers cannot store information.
* **Correct Answer:** **B) Measurement collapses a superposition into a single outcome with certain probabilities.**
* **Explanation:** By Born's rule, measurement projects the continuous state vector into one of the eigenstates, with probability proportional to the squared amplitude $|\alpha|^2$.

---

### Q7. Measurement Probability Calculation
* **Type:** Multiple Choice (MCQ)
* **Question:** A qubit is in the state $|\psi\rangle = \frac{\sqrt{3}}{2}|0\rangle + \frac{1}{2}|1\rangle$. If it is measured in the computational basis, what is the probability of obtaining $|1\rangle$?
* **Options:**
  * A) 1/2
  * B) $\sqrt{3}/2$
  * C) 3/4
  * D) 1/4
* **Correct Answer:** **D) 1/4**
* **Explanation:** $P(|1\rangle) = |\langle 1 | \psi \rangle|^2 = \left|\frac{1}{2}\right|^2 = \frac{1}{4} = 0.25$.

---

### Q8. Superposition State Count on $n$ Qubits
* **Type:** Multiple Choice (MCQ)
* **Question:** A register of $n$ qubits is prepared by applying $H$ to each qubit initialized in $|0\rangle$. How many computational basis states appear with nonzero amplitude?
* **Options:**
  * A) $2^n$
  * B) $n$
  * C) $n^2$
  * D) $n^n$
* **Correct Answer:** **A) $2^n$**
* **Explanation:** $H^{\otimes n}|0\rangle^{\otimes n} = \frac{1}{\sqrt{2^n}}\sum_{x=0}^{2^n-1}|x\rangle$, creating a uniform superposition containing all $2^n$ computational basis states.

---

### Q9. Distinguishing $|+\rangle$ from a Mixed State
* **Type:** Multiple Choice (MCQ)
* **Question:** How can the superposition $|+\rangle$ be experimentally distinguished from a classical 50/50 mixture of $|0\rangle$ and $|1\rangle$?
* **Options:**
  * A) Measure twice and compare outcomes
  * B) They cannot be distinguished by any measurement
  * C) Measure in the computational (Z) basis
  * D) Apply $H$, then measure in the $Z$ basis
* **Correct Answer:** **D) Apply H, then measure in the Z basis**
* **Explanation:**
  * Measuring directly in the $Z$ basis yields 50% $|0\rangle$ and 50% $|1\rangle$ for both states.
  * Applying $H$ first: $H|+\rangle = |0\rangle$ (yields outcome 0 with 100% probability). For the classical 50/50 mixture, $H$ transforms $|0\rangle \to |+\rangle$ and $|1\rangle \to |-\rangle$, which still measures as 0 and 1 each with 50% probability.

---

### Q10. Surface of the Bloch Sphere
* **Type:** Multiple Choice (MCQ)
* **Question:** What do the points on the surface of the Bloch sphere represent?
* **Options:**
  * A) Pure states of a single qubit
  * B) Entangled states of two qubits
  * C) Only the states $|0\rangle$ and $|1\rangle$
  * D) Mixed states of multiple qubits
* **Correct Answer:** **A) Pure states of a single qubit**
* **Explanation:** Points on the surface ($r = 1$) represent single-qubit pure states ($|\psi\rangle$). Points inside the sphere ($r < 1$) represent mixed states ($\rho$).

---

### Q11. Estimating $\langle Z \rangle$ Expectation Value
* **Type:** Multiple Choice (MCQ)
* **Question:** A circuit is run for 1000 shots and measured in the $Z$ basis. The results are 700 outcomes of 0 and 300 outcomes of 1. What is the estimated $\langle Z \rangle$?
* **Options:**
  * A) 0.3
  * B) 0.4
  * C) -0.3
  * D) 0.7
* **Correct Answer:** **B) 0.4**
* **Explanation:** Since $Z|0\rangle = +1|0\rangle$ and $Z|1\rangle = -1|1\rangle$, the expectation value is:
  $$\langle Z \rangle = (+1) \cdot P(0) + (-1) \cdot P(1) = \frac{700 - 300}{1000} = \frac{400}{1000} = 0.4$$

---

### Q12. Molecule Ground State on NISQ
* **Type:** Multiple Choice (MCQ)
* **Question:** A pharma startup has access only to a noisy 50-qubit NISQ device. They want to estimate the ground-state energy of a small molecule such as LiH. Which approach is most suitable?
* **Options:**
  * A) Grover's algorithm
  * B) Variational Quantum Eigensolver (VQE)
  * C) Shor's Algorithm
  * D) Quantum GAN
* **Correct Answer:** **B) Variational Quantum Eigensolver**
* **Explanation:** VQE is the leading algorithm designed specifically for noisy intermediate-scale quantum devices to compute ground-state molecular energies with shallow circuits.

---

### Q13. Identity Function Bit Oracle
* **Type:** Multiple Choice (MCQ)
* **Question:** A bit oracle acts as $U_f|x\rangle|y\rangle = |x\rangle|y \oplus f(x)\rangle$. Which circuit implements $U_f$ for the 1-bit identity function $f(x) = x$?
* **Options:**
  * A) A CNOT with $y$ as control and $x$ as target
  * B) No gates at all (the identity circuit)
  * C) A single $X$ gate on the target qubit $y$
  * D) A CNOT with $x$ as control and $y$ as target
* **Correct Answer:** **D) A CNOT with x as control and y as target**
* **Explanation:** For $f(x) = x$, the oracle transformation is $|x\rangle|y\rangle \to |x\rangle|y \oplus x\rangle$. This is the exact definition of a CNOT gate where $x$ is the control qubit and $y$ is the target qubit.

---

### Q14. Qiskit Measurement Indexing
* **Type:** Multiple Choice (MCQ)
* **Question:** In `qc = QuantumCircuit(5, 5)`, which line measures the 5th qubit and stores the result in the 5th classical bit?
* **Options:**
  * A) `qc.measure(5, 5)`
  * B) `qc.measure(qubit=5)`
  * C) `qc.measure(4, 4)`
  * D) `qc.measure_all(5)`
* **Correct Answer:** **C) qc.measure(4, 4)**
* **Explanation:** Python and Qiskit use 0-based indexing. For a 5-qubit and 5-bit circuit, the valid indices are $0, 1, 2, 3, 4$. The 5th item is at index 4.

---

### Q15. Qiskit Bitstring Ordering (Endianness)
* **Type:** Multiple Choice (MCQ)
* **Question:** A 3-qubit circuit runs `qc.x(0)` and then `qc.measure_all()`. On an ideal simulator, which bitstring appears in the counts?
* **Options:**
  * A) 001
  * B) 100
  * C) 010
  * D) 000
* **Correct Answer:** **A) 001**
* **Explanation:** Qiskit orders bitstrings in little-endian format: $|q_{n-1} \dots q_1 q_0\rangle$. Flipping qubit 0 (`qc.x(0)`) puts qubit 0 in state $|1\rangle$, while qubits 1 and 2 remain $|0\rangle$. The resulting measurement bitstring is read right-to-left as `001`.
