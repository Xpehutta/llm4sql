---
# Training Results Summary
---


### **Epoch 1**
- **Training Loss**: `0.1687`
- **Training Duration**: `954.77 seconds`
- **Validation Loss**: `0.1677`
- **ROUGE-L-SQL F1 Score**: `0.4067`
- **Total Epoch Duration**: `1723.02 seconds`


### **Epoch 2**
- **Training Loss**: `0.1655`
- **Training Duration**: `953.36 seconds`
- **Validation Loss**: `0.1664`
- **ROUGE-L-SQL F1 Score**: `0.4392`
- **Total Epoch Duration**: `1721.41 seconds`


### **Epoch 3**
- **Training Loss**: `0.1640`
- **Training Duration**: `952.15 seconds`
- **Validation Loss**: `0.1664`
- **ROUGE-L-SQL F1 Score**: `0.4497`
- **Total Epoch Duration**: `1720.05 seconds`


### **Overall Training Duration**
- **Total Time**: `5164.47 seconds` (~86 minutes)


### Key Observations:
- The **training loss** decreased consistently across epochs, indicating model improvement.
- The **ROUGE-L-SQL F1 Score** improved from `0.4067` in Epoch 1 to `0.4497` in Epoch 3, reflecting better performance on the validation set.
- The total duration for all three epochs was approximately **86 minutes**.



---
# Technical Overview of Fine-tuning
---

## 1. **LoRA (Low-Rank Adaptation)**
### Mathematical Description
- LoRA reduces trainable parameters by adding low-rank matrices to the original weights.
- Let $W \in \mathbb{R}^{d \times d}$ be the original weight matrix.
- Introduce two small matrices $A \in \mathbb{R}^{d \times r}$ and $B \in \mathbb{R}^{r \times d}$ where $r \ll d$.
- The updated weight matrix becomes:
  
  $W_{\text{new}} = W + AB$
  
- During fine-tuning, only $A$ and $B$ are updated, reducing parameters from $d^2$ to $2dr$.

### Why It Works Well
- Low-rank updates minimize catastrophic forgetting of pre-trained knowledge.
- A scaling factor $\alpha$ controls the update impact:

  $W_{\text{new}} = W + \frac{\alpha}{r} AB$
  
  This balances task-specific adaptation and stability.


## 2. **Dataset and Tokenization**
### Mathematical Description
- Input-output pairs $(x, y)$ are tokenized into sequences.
- Construct full text as $z = x \to y$ (separator token $\to$).
- Tokenization and padding:

  $z_{\text{tokens}} = \text{Tokenizer}(z), \quad z_{\text{padded}} = \text{PadOrTruncate}(z_{\text{tokens}}, L)$

### Why It Works Well
- Fixed sequence length $L$ simplifies batch processing.
- The separator token clarifies input-output boundaries for the model.


## 3. **Training Loop**
#### Mathematical Description:
- The training loop minimizes the loss function $\mathcal{L}(\theta)$, where $\theta$ represents the trainable parameters (i.e., $A$ and $B$ in LoRA).
- For each batch $\mathcal{B} $, the loss is computed as:

 ![Equation](https://latex.codecogs.com/svg.image?\mathcal{L}_{\mathcal{B}}(\theta)&space;=&space;\frac{1}{|\mathcal{B}|}&space;\sum_{(x,&space;y)&space;\in&space;\mathcal{B}}&space;\ell(x,&space;y;&space;\theta))
  
  where $\ell(x, y; \theta)$ is the per-sample loss (e.g., cross-entropy loss for language modeling).
- Gradients are computed using backpropagation:

  $\nabla_\theta \mathcal{L}_{\mathcal{B}}(\theta)$
  
- Parameters are updated using AdamW optimization:

  $\theta \leftarrow \theta - \eta \cdot \nabla_\theta \mathcal{L}_{\mathcal{B}}(\theta)$
  
  where $\eta$ is the learning rate.

### Why It Works Well
- AdamW combines adaptive learning rates and weight decay.
- Fine-tuning only LoRA parameters reduces memory and speeds training.


## 4. **Batch Processing**
### Mathematical Description
- Input tensor shape: $[B, L]$ for batch size $B$ and sequence length $L$.
- Batch-averaged loss:

   ![Loss Function](https://latex.codecogs.com/svg.image?\mathcal{L}_{\mathcal{B}}(\theta)&space;=&space;\frac{1}{B&space;\cdot&space;L}&space;\sum_{b=1}^B&space;\sum_{t=1}^L&space;\ell(\hat{y}_{b,t},&space;y_{b,t}))


### Why It Works Well
- GPU parallelism accelerates batch computations.
- Larger batches stabilize gradient estimates.


## 5. **Loss Function**
### Mathematical Description
- Cross-entropy loss for token prediction:

  $\ell(\hat{y}_t, y_t) = -\log P(y_t \mid \hat{y}_t)$
  
- Sequence loss:

  $\mathcal{L}(\theta) = \frac{1}{L} \sum_{t=1}^L \ell(\hat{y}_t, y_t)$

### Why It Works Well
- Directly optimizes token prediction accuracy.
- Suitable for autoregressive language modeling.


## 6. **Device Management**
### Mathematical Description
- GPU computation time dominates:

  $T_{\text{GPU}} \ll T_{\text{CPU}}$

### Why It Works Well
- GPUs excel at parallel matrix operations critical for neural networks.
- Efficient hardware utilization speeds up training.


---
# Metrics of SQL similarity
---

### **1. Normalization**  
**Goal:** Standardize queries to ignore superficial differences (aliases, literals, formatting).  
**How it works:**  
- Uses `sqlglot` to parse the query into an Abstract Syntax Tree (AST).  
- Applies `remove_aliases_and_literals` to:  
  - Strip aliases (e.g., `customers AS c` → `customers`).  
  - Replace literals (e.g., `'2023-01-01'` → `?`).  
- Converts the AST back to standardized SQL (consistent formatting).  

**Example:**  
```sql
-- Original Query
SELECT c.name FROM customers AS c WHERE c.id = 123;

-- Normalized Query
SELECT name FROM customers WHERE id = ?;
```


### **2. AST Similarity**  
**Goal:** Compare the structural similarity of queries using their ASTs.  
**How it works:**  
- Converts the AST into a string of node class names (e.g., `Select From Join Where`).  
- Uses **Levenshtein distance** (edit distance) to compare these strings.  
- Normalizes the distance by the maximum string length to get a score between 0 (dissimilar) and 1 (identical).  

**Why it works:**  
- Ignores aliases/literals (due to normalization).  
- Captures structural patterns (e.g., joins, filters, groupings).  


### **3. Component Similarity**  
**Goal:** Compare shared components (tables, columns, conditions) using **Jaccard similarity**.  
**How it works:**  
- Extracts components from the AST:  
  - **Tables**: `customers`, `orders`  
  - **Columns**: `name`, `total`  
  - **Conditions**: `orders.date > ?`  
- Computes Jaccard index for each component:  
  ```
  similarity = (intersection of components) / (union of components)
  ```  

**Why it works:**  
- Identifies overlaps in critical elements (e.g., shared tables/columns).  
- Useful for detecting partial similarities (e.g., same tables but different filters).  


### **4. Combined Score**  
A weighted average of:  
- `AST similarity (40%)`  
- `Table similarity (30%)`  
- `Column similarity (20%)`  
- `Condition similarity (10%)`  

This allows customizable prioritization of structural vs. component similarities.


### **Key Insights**  
1. **Robust to Formatting:** Normalization removes formatting noise (aliases, spacing, capitalization).  
2. **Semantic Understanding:** AST comparisons capture logical structure, not just text.  
3. **Flexibility:** Component weights can be adjusted based on use case (e.g., prioritize tables over conditions).  
4. **Tradeoffs:**  
   - **AST similarity** is strict but may miss semantic equivalences (e.g., `WHERE a = b` vs `WHERE b = a`).  
   - **Component similarity** is lenient but may over-simplify complex logic.  


### **Example Output**  
For the provided `query1` and `query2`:  
- **Normalized Queries** become structurally identical (aliases removed, literals replaced).  
- **AST Similarity**: High (~1.0).  
- **Component Similarities**:  
  - Tables: 1.0 (both use `customers`, `orders`).  
  - Columns: 1.0 (`name`, `total`).  
  - Conditions: Lower due to different dates (`?` vs `?` after normalization).  


### **Use Cases**  
- Plagiarism detection in SQL queries.  
- Identifying redundant queries in a codebase.  
- Detecting similar queries for performance optimization.  


