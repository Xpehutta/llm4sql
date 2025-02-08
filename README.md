### Data Model:

1. **Tables**:
   - Added a variety of new tables such as `employees`, `departments`, `locations`, `payments`, `invoices`, `shipping_details`, `discounts`, `promotions`, `reviews`, `feedbacks`, `wishlists`, `shopping_carts`, `cart_items`, `inventory`, `sales`, `returns`, `refunds`, `taxes`, `coupons`, `subscriptions`, `notifications`, `user_roles`, `permissions`, `audit_logs`, `contacts`, `messages`, `chat_sessions`, `tickets`, `ticket_comments`, `knowledge_base`, `faq`, `blog_posts`, `comments`, `likes`, `followers`, `activity_logs`, `settings`, `configurations`, `reports`, `dashboards`, `widgets`, and `integrations`.

2. **Columns**:
   - Each table has its own set of columns with appropriate data types.
   - Primary keys are marked with `is_primary_key=True`.
   - Foreign keys are marked with `is_foreign_key=True`.

3. **Relationships**:
   - Defined relationships between tables based on foreign key constraints. For example, `orders` references `customers` via `customer_id`, `order_items` references `orders` via `order_id`, and so on.

This data model provides a richer structure for generating synthetic SQL queries, allowing for more complex joins and conditions.

### Required Excel File Structure:

1. **Tables Sheet** (`Tables` worksheet):
```csv
table_name   | description
-------------|-------------
customers    | Customer information
orders       | Sales orders
products     | Product catalog
```

2. **Columns Sheet** (`Columns` worksheet):
```csv
table_name | column_name | data_type | is_primary_key | is_foreign_key
-----------|-------------|-----------|----------------|---------------
customers  | customer_id | int       | True           | False
customers  | name        | varchar   | False          | False
orders     | order_id    | int       | True           | False
orders     | customer_id | int       | False          | True
```

3. **Relationships Sheet** (`Relationships` worksheet):
```csv
source_table | source_column | target_table | target_column
-------------|---------------|--------------|--------------
orders       | customer_id   | customers    | customer_id
```

### Example Generated Query:
```sql
SELECT customer_id, name
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
WHERE customers.name LIKE '%smith%' 
  AND orders.order_date BETWEEN '2021-03-15' AND '2023-08-22';
```

### Features:
1. **Realistic Data Generation**:
   - Numeric ranges based on column types
   - Realistic date ranges
   - Context-aware string patterns

2. **Query Complexity Control**:
   - `num_joins`: Control number of JOIN clauses
   - `num_conditions`: Control WHERE clause complexity

3. **Data Model Awareness**:
   - Respects primary/foreign key relationships
   - Follows table/column data types
   - Maintains referential integrity

4. **Variety Generation**:
   - Multiple JOIN types (INNER, LEFT, RIGHT)
   - Different comparison operators
   - Various condition patterns (LIKE, IN, BETWEEN)
  



# Technical Overview

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

---

## 2. **Dataset and Tokenization**
### Mathematical Description
- Input-output pairs $(x, y)$ are tokenized into sequences.
- Construct full text as $z = x \to y$ (separator token $\to$).
- Tokenization and padding:

  $z_{\text{tokens}} = \text{Tokenizer}(z), \quad z_{\text{padded}} = \text{PadOrTruncate}(z_{\text{tokens}}, L)$

### Why It Works Well
- Fixed sequence length $L$ simplifies batch processing.
- The separator token clarifies input-output boundaries for the model.

---

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

---

## 4. **Batch Processing**
### Mathematical Description
- Input tensor shape: $[B, L]$ for batch size $B$ and sequence length $L$.
- Batch-averaged loss:

   ![Loss Function](https://latex.codecogs.com/svg.image?\mathcal{L}_{\mathcal{B}}(\theta)&space;=&space;\frac{1}{B&space;\cdot&space;L}&space;\sum_{b=1}^B&space;\sum_{t=1}^L&space;\ell(\hat{y}_{b,t},&space;y_{b,t}))


### Why It Works Well
- GPU parallelism accelerates batch computations.
- Larger batches stabilize gradient estimates.

---

## 5. **Loss Function**
### Mathematical Description
- Cross-entropy loss for token prediction:

  $\ell(\hat{y}_t, y_t) = -\log P(y_t \mid \hat{y}_t)$
  
- Sequence loss:

  $\mathcal{L}(\theta) = \frac{1}{L} \sum_{t=1}^L \ell(\hat{y}_t, y_t)$

### Why It Works Well
- Directly optimizes token prediction accuracy.
- Suitable for autoregressive language modeling.

---

## 6. **Device Management**
### Mathematical Description
- GPU computation time dominates:

  $T_{\text{GPU}} \ll T_{\text{CPU}}$

### Why It Works Well
- GPUs excel at parallel matrix operations critical for neural networks.
- Efficient hardware utilization speeds up training.



### 1. **Why BERT Works Well for Semantic Similarity**

#### a. **Understanding BERT Embeddings**
BERT (Bidirectional Encoder Representations from Transformers) is a deep learning model that generates contextualized embeddings for words or sentences. These embeddings capture semantic meaning by considering the context in which words appear.

- **Contextualization**: Unlike traditional word embeddings like Word2Vec or GloVe, which assign a single vector to each word regardless of its context, BERT generates different vectors for the same word depending on its surrounding words.
- **Deep Learning Architecture**: BERT uses a transformer-based architecture with multiple layers of self-attention mechanisms, enabling it to capture long-range dependencies and complex relationships between words.

For example:
- The word "bank" in "river bank" vs. "bank account" will have different embeddings in BERT because the context determines its meaning.

#### b. **Sentence Embeddings**
When we use BERT for sentence-level tasks, the embeddings represent the entire sentence as a single vector. This vector encodes the semantic meaning of the sentence, including the relationships between words.

- **Pooling Techniques**: Common methods to generate sentence embeddings from BERT include:
  - **Mean Pooling**: Average the embeddings of all tokens in the sentence.
  - **CLS Token**: Use the embedding of the special `[CLS]` token, which is often fine-tuned for specific tasks.
  - **Max Pooling**: Take the maximum value across dimensions for all tokens.

These embeddings are high-dimensional (typically 768 dimensions for BERT-base), capturing rich semantic information.

---

### 2. **Why Cosine Similarity Works Great**

Cosine similarity measures the cosine of the angle between two vectors in a multi-dimensional space. It is widely used for comparing text embeddings because:

#### a. **Definition of Cosine Similarity**
Given two vectors $\mathbf{A}$ and $\mathbf{B}$ in $n$-dimensional space, cosine similarity is defined as:

$\text{cosine\_similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$

Where:
- $\mathbf{A} \cdot \mathbf{B}$: Dot product of $\mathbf{A}$ and $\mathbf{B}$.
- $\|\mathbf{A}\|$: Magnitude (or norm) of $\mathbf{A}$, calculated as $\sqrt{\sum_{i=1}^n A_i^2}$.

#### b. **Properties of Cosine Similarity**
1. **Range**: Cosine similarity values range from -1 to 1:
   - $1$: Vectors are identical (perfect alignment).
   - $0$: Vectors are orthogonal (no similarity).
   - $-1$: Vectors are diametrically opposite.
2. **Invariance to Vector Length**: Cosine similarity is unaffected by the magnitude of the vectors, focusing only on their direction. This makes it ideal for comparing normalized embeddings like those produced by BERT.

#### c. **Why Cosine Similarity Works Well with BERT Embeddings**
1. **Semantic Alignment**: BERT embeddings encode semantic meaning, so semantically similar sentences tend to have vectors pointing in similar directions in the embedding space. Cosine similarity effectively captures this alignment.
2. **Normalization**: BERT embeddings are typically L2-normalized, meaning their magnitudes are close to 1. This ensures that cosine similarity directly reflects the angular distance between vectors, without being influenced by differences in magnitude.

---

### 3. **Mathematical Details of Why BERT + Cosine Similarity Works**

#### a. **BERT Embeddings Capture Semantic Meaning**
Let’s consider two sentences:
- $S_1 = \text{"I love programming"}$
- $S_2 = \text{"Programming is fun"}$

BERT generates embeddings $\mathbf{E}_1$ and $\mathbf{E}_2$ for these sentences. If $S_1$ and $S_2$ are semantically similar, their embeddings will point in similar directions in the embedding space.

#### b. **Cosine Similarity Measures Angular Distance**
The cosine similarity between $\mathbf{E}_1$ and $\mathbf{E}_2$ is:

$\text{cosine\_similarity}(\mathbf{E}_1, \mathbf{E}_2) = \frac{\mathbf{E}_1 \cdot \mathbf{E}_2}{\|\mathbf{E}_1\| \|\mathbf{E}_2\|}$

If $\mathbf{E}_1$ and $\mathbf{E}_2$ are close in direction (small angle between them), the dot product $\mathbf{E}_1 \cdot \mathbf{E}_2$ will be large, resulting in a high cosine similarity value.

#### c. **Example Calculation*
Assume $\mathbf{E}_1 = [0.5, 0.8, 0.2]$ and $\mathbf{E}_2 = [0.4, 0.9, 0.1]$:

1. **Dot Product**:

   $\mathbf{E}_1 \cdot \mathbf{E}_2 = (0.5 \times 0.4) + (0.8 \times 0.9) + (0.2 \times 0.1) = 0.2 + 0.72 + 0.02 = 0.94$

3. **Magnitudes**:

   $\|\mathbf{E}_1\| = \sqrt{0.5^2 + 0.8^2 + 0.2^2} = \sqrt{0.25 + 0.64 + 0.04} = \sqrt{0.93} \approx 0.964$

   $\|\mathbf{E}_2\| = \sqrt{0.4^2 + 0.9^2 + 0.1^2} = \sqrt{0.16 + 0.81 + 0.01} = \sqrt{0.98} \approx 0.990$

4. **Cosine Similarity**:
   
   $\text{cosine\_similarity}(\mathbf{E}_1, \mathbf{E}_2) = \frac{0.94}{0.964 \times 0.990} \approx \frac{0.94}{0.954} \approx 0.985$

This high value indicates strong similarity between $ S_1 $ and $ S_2 $.

---

### 4. **Comparison with Other Methods**

#### a. **TF-IDF vs. BERT**
- **TF-IDF**: Captures term frequency and inverse document frequency but lacks semantic understanding. For example, "car" and "vehicle" would not be considered similar under TF-IDF.
- **BERT**: Encodes semantic meaning, so "car" and "vehicle" would have similar embeddings.

#### b. **Euclidean Distance vs. Cosine Similarity**
- **Euclidean Distance**: Measures absolute distance between vectors. However, it can be sensitive to vector magnitude, making it less suitable for normalized embeddings.
- **Cosine Similarity**: Focuses on direction rather than magnitude, making it more robust for comparing semantic embeddings.

---

### 5. **Conclusion**

Using **Sentence Embeddings (BERT)** and **Cosine Similarity** works great:
1. **BERT Embeddings** capture rich semantic meaning by leveraging contextualized representations.
2. **Cosine Similarity** effectively measures the alignment of these embeddings, focusing on direction rather than magnitude.

