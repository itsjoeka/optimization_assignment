<h1 align="center"> Optimal Assignment of ECG Technicians Units to Electricity Faults Across Multi-Town Service Areas: A Case Study of Hohoe Operations Department </h1>

## Table of Contents
- [Project Overview](#Project-Overview)
- [Objectives](#Objectives)
- [Mathematical Formulation](#Mathematical-Formulation)
- [Acknowledgment](#Acknowledgment)
- [Team](#Team)
- [References](#References)
  
## Project Overview


## Objectives
1. **Efficiency** – minimizing total travel time
2. **Equity** – ensuring Far-zone towns do not wait excessively longer than Near-zone towns

## Mathematical Formulation
### **Defining the Sets**

#### **Set 1: Technician Groups**

* **Notation:** ( I )
* **Definition:**
$I = {1, 2, 3, 4, 5}$

* **Meaning:** Five technician groups, each group containing **three technicians who always move together**.

| Group | Description             |
| ----- | ----------------------- |
| 1     | Group 1 (3 technicians) |
| 2     | Group 2 (3 technicians) |
| 3     | Group 3 (3 technicians) |
| 4     | Group 4 (3 technicians) |
| 5     | Group 5 (3 technicians) |

---

#### **Set 2: Faults**

* **Notation:** ( $J$ )
* **Definition:**
$J = {1, 2, \ldots, 15}$

* **Meaning:** 15 faults reported in a given day.

---

#### **Set 3: Zones**

* **Notation:** ( $Z$ )
* **Definition:**
$Z = {\text{Near}, \text{Far}}$

**Zone definitions:**

* **Near:** Towns ≤ 20 km from Hohoe
* **Far:** Towns > 20 km from Hohoe

---

### **Defining Parameters**

#### **1. Travel Time**

* **Notation:** ( $t_j$ )
* Time to travel from the Hohoe office to fault ( $j$ ).
* Obtained from [ECG Towns Dataset](dataset/ecg_towns_dataset.csv)

---

#### **2. Repair Time**

* **Notation:** ( $r_j$ )

| Fault Type                    | Repair Time (hrs) |
| ------------------------------| ----------------- |
| Transformer installation      | 4.0               |
| Transformer maintenance       | 0.75              |
| Cable joining and termination | 0.33              |
| Network line extension        | 2.0               |
| Pole replacement              | 1.0               |
| Vegetation control            | 4.0               |

---

#### **3. Zone of Fault**

* **Notation:** ( $z_j$ )
* Either **Near** or **Far**.

---

#### **4. Group Capacity**

* **Notation:** ( $Q_i$ )
* Maximum number of faults a group can handle per shift.

$$
Q_i = 3 \quad \forall i \in I
$$

---

#### **5. Shift Duration**

* **Notation:** ( $H$ )
$$
H = 8 \text{ hours}
$$

---

#### **6. Equity Tolerance**

* **Notation:** ( $\theta$ )
    * $\theta = 1.7$
Far-zone average response time should be **no more than 50% greater** than Near-zone average response time.

---

### **7. Objective Weights**

* **Notation:** ( $\alpha$, $\beta$ )
$$
\alpha + \beta = 1
$$

---

### **Decision Variables**

#### **Assignment Variable**

* **Notation:** $x_{ij}$
* Binary decision:
    * $x_{ij} = 1$ if group *i* IS assigned to fault *j*
    * $x_{ij} = 0$ if group *i* is NOT assigned to fault *j*

Total variables = ( 5 $$\times$$ 15 = 75 )

---

#### **Helper Variables**

* **Average response time for each zone:**
    * $R_{\text{Near}}, \quad R_{\text{Far}}$

---

### **The Objective Function**

#### **Full Multi-Objective Function**

$$
\min Z = \alpha \cdot \left( \sum_{i=1}^{5} \sum_{j=1}^{15} t_j \cdot x_{ij} \right)
;+; \beta \cdot (R_{\text{Far}} - R_{\text{Near}})
$$

---

#### **Efficiency Component**

$$
\text{Total Travel Time} = \sum_{i=1}^{5} \sum_{j=1}^{20} t_j x_{ij}
$$

---

#### **Equity Component**

$$
R_{\text{Near}} =
\frac{\sum_{j : z_j = \text{Near}} t_j \left(\sum_{i=1}^{5} x_{ij}\right)}
{\text{Number of Near faults}}
$$

$$
R_{\text{Far}} =
\frac{\sum_{j : z_j = \text{Far}} t_j \left(\sum_{i=1}^{5} x_{ij}\right)}
{\text{Number of Far faults}}
$$

---

#### **Simplified Starting Objective (Recommended for Implementation First)**

$$
\min Z =
\sum_{i=1}^{5} \sum_{j=1}^{15} t_j \cdot x_{ij}
$$

Add the equity term later once the base model works.

---

#### **Summary**

| Component         | Description                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| Sets              | Technician groups, faults, zones                                         |
| Parameters        | Travel time, repair time, zone, capacity, shift length, equity tolerance |
| Decision Variable | Binary assignment of groups to faults                                    |
| Objective         | Minimize travel time + zone inequity                                     |

---


### Model Constraints

Main Constraints used in the **Technician Group Fault Assignment Optimization Model

---

#### **Constraint 1 — Coverage**

**Every fault must be assigned to exactly one technician group.**

#### **Formulation**

$$
\sum_{i=1}^{5} x_{ij} = 1, \quad \forall j \in J
$$

**Interpretation**

For each fault ( $j$ ), exactly one of the variables
( $x_{1j}$, $x_{2j}$, $x_{3j}$, $x_{4j}$, $x_{5j}$ ) must be 1.


---

#### **Constraint 2 — Capacity**

**Each group can handle at most 3 faults per shift.**

#### **Formulation**

$$
\sum_{j=1}^{15} x_{ij} \leq Q_i, \quad \forall i \in I
$$

With ( $Q_i = 3$ ):
$\sum_{j=1}^{15} x_{ij} \leq 3, \quad \forall i$

**Interpretation**

The number of faults assigned to each group ( $i = 1,2,3,4,5$ ) must be ≤ 3.

**5 constraints** (one per group)

---

#### **Constraint 3 — Time Feasibility**

#### **Formulation**

$$
\sum_{j=1}^{20} (t_j + r_j) x_{ij} \leq H, \quad \forall i \in I
$$

With ( $H = 8$ ):
$\sum_{j=1}^{20} (t_j + r_j) x_{ij} \leq 8$

**Interpretation**

For each group, sum the total time required for its assigned faults. This must be ≤ 8 hours.

**5 constraints** (one per group)

---

#### **Constraint 4 — Equity**

#### **Formulation**

$$
R_{\text{Far}} \leq \theta \cdot R_{\text{Near}}
$$

Where ( $\theta = 1.7$ ), and:

$$
R_{\text{Near}} =
\frac{\sum_{j : z_j = Near} t_j}{\sum_{j : z_j = Near} 1}
$$

$$
R_{\text{Far}} =
\frac{\sum_{j : z_j = Far} t_j}{\sum_{j : z_j = Far} 1}
$$

---

#### **Implementation**

Let:

* ( $N_{Near}$ ) = number of Near-zone faults
* ( $N_{Far}$ ) = number of Far-zone faults

Then:

$$
\frac{\sum_{j: z_j = Far} t_j}{N_{Far}}
\le
1.7 \cdot
\frac{\sum_{j: z_j = Near} t_j}{N_{Near}}
$$

Or fully linearized:

$$
\sum_{j: z_j = Far} t_j
\le
1.7 \cdot \frac{N_{Far}}{N_{Near}}
\cdot
\sum_{j: z_j = Near} t_j
$$


# Acknowledgment
Hohoe Electricity Company of Ghana and Abdul Haliq.

# Team
- Jonathan Kalami
- Sally Gli
- Tayyiba Amartey
- Dr. Ali Abubakar
- Dr. Bright Owusu

# References
