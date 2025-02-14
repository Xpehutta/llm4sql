
---
## DataModelGenerator Class
---

### Approach
1. **Class Initialization**: The class will initialize necessary components like Faker for generating fake data and set a random seed for reproducibility.
2. **Data Model Creation**: A method will generate an Excel file with predefined tables, columns, and relationships.
3. **Data Model Loading**: Another method will load the data model from the Excel file into the class instance.
4. **Query Generation**: A method will generate synthetic SQL queries using the loaded data model, considering the number of joins and conditions specified.
5. **Dataset Generation**: This method will generate a dataset of synthetic queries, split into input and output parts for each query.


### Explanation
- **Initialization**: The `DataModelGenerator` class initializes with a seed for reproducibility and sets up Faker for generating fake data.
- **Data Model Creation**: The `create_sample_data_model` method generates an Excel file with predefined tables, columns, and relationships.
- **Data Model Loading**: The `load_data_model` method reads the Excel file and validates its structure, storing it in the instance.
- **Query Generation**: The `generate_synthetic_query` method constructs SQL queries based on the data model, including joins and conditions.
- **Dataset Generation**: The `generate_dataset` method creates a dataset by splitting each query into input (initial part) and output (remaining part) to facilitate training models for query completion or generation tasks.

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
   - Multiple JOIN types ('', LEFT)
   - Different comparison operators
   - Various condition patterns (LIKE, IN, BETWEEN)



---
## SQLRougeL Class
---

### Approach
1. **Class Definition**: Create a class `SQLRougeL` that will contain all the necessary methods.
2. **Helper Methods**:
   - **Tokenization**: Convert SQL queries into tokens using regular expressions to identify SQL keywords, identifiers, operators, and punctuation.
   - **LCS Calculation**: Compute the length of the longest common subsequence between two token lists using dynamic programming.
3. **Main Method**: Calculate the ROUGE-L-SQL score by utilizing the tokenizer and LCS functions to determine precision, recall, and F1 score between a generated SQL query and a reference query.


### Explanation
1. **Class Initialization**: The `SQLRougeL` class is defined without an initializer since no instance variables are needed.
2. **Static Methods**:
   - `_sql_tokenizer`: Converts an SQL query into a list of tokens by normalizing the query and using regular expressions to identify SQL components.
   - `_lcs`: Uses dynamic programming to compute the length of the longest common subsequence between two lists of tokens.
3. **Main Method**:
   - `rouge_l_sql`: Takes two SQL queries (generated and reference), tokenizes them, computes the LCS length, and calculates precision, recall, and F1 score to return the ROUGE-L-SQL metrics.

The provided code implements a custom ROUGE-L metric tailored for SQL queries, combining methodological adaptations for SQL syntax and mathematical foundations of sequence alignment. Below is a breakdown of its methodological and mathematical rationale:


### **Methodological Insights**
1. **SQL-Specific Tokenization**:
   - **Normalization**: Converts queries to lowercase and collapses whitespace to handle stylistic variations (e.g., `SELECT` vs `select`).
   - **Pattern-Based Splitting**: Uses regex to tokenize SQL into:
     - **Keywords** (e.g., `SELECT`, `FROM`),
     - **Identifiers** (e.g., table/column names like `customer_id`),
     - **Operators** (e.g., `=`, `>`),
     - **Punctuation** (e.g., commas, parentheses).
   - This ensures structural elements (e.g., clauses) are preserved, while ignoring irrelevant formatting differences.

2. **Longest Common Subsequence (LCS)**:
   - **Order-Aware Comparison**: LCS identifies the longest sequence of tokens that appear in the same order (not necessarily contiguously) in both the generated and reference queries.
   - **Robust to Partial Matches**: Handles variations like reordered conditions in `WHERE` clauses (e.g., `WHERE a=1 AND b=2` vs `WHERE b=2 AND a=1` will partially match).

3. **ROUGE-L Adaptation**:
   - **Precision/Recall/F1**: Computes:
     - **Precision**: `LCS Length / Generated Query Length` (avoids over-cluttering),
     - **Recall**: `LCS Length / Reference Query Length` (ensures coverage),
     - **F1 Score**: Balances the two.
   - These metrics align with the goals of SQL generation: producing concise, accurate queries (precision) that include all necessary components (recall).


### **Mathematical Insights**
1. **Dynamic Programming for LCS**:
   - The LCS algorithm uses a 2D matrix `dp` where `dp[i][j]` represents the LCS length of the first `i` tokens of the generated query and first `j` tokens of the reference query.
   - Recurrence Relation:
     ```
     dp[i][j] = dp[i-1][j-1] + 1              if tokens match
                max(dp[i-1][j], dp[i][j-1])   otherwise
     ```
   - Time Complexity: \(O(mn)\), where \(m\) and \(n\) are token counts of the two queries.

2. **F1 Score Calculation**:
   - Harmonic mean of precision (\(P\)) and recall (\(R\)):
$$
F_1 = \frac{2PR}{P + R}
$$
   - Penalizes extreme imbalances (e.g., high recall but low precision).


### **Why It Works Well for SQL**
1. **Structure Preservation**:
   - Tokenization captures SQL’s hierarchical structure (e.g., `SELECT` followed by column names, `FROM` followed by tables).
   - LCS rewards correct ordering of clauses (e.g., `SELECT` before `FROM`).

2. **Invariance to Irrelevant Variations**:
   - Case insensitivity and whitespace normalization ignore stylistic differences.
   - Operators/punctuation are treated as distinct tokens, ensuring comparisons are syntax-aware.

3. **Balanced Evaluation**:
   - F1 score discourages overly verbose or incomplete queries.


### **Limitations and Considerations**
- **Semantic Equivalence**: LCS does not account for semantically equivalent but syntactically different queries (e.g., `WHERE a=1 AND b=2` vs `WHERE b=2 AND a=1`).
- **Complex SQL Constructs**: The tokenizer may miss advanced features (e.g., `WITH` clauses, window functions), depending on the regex patterns.
- **Token Granularity**: Identifier names are tokenized as single units, so typos (e.g., `custmer_id` vs `customer_id`) are penalized harshly.


### **Conclusion**
This approach is suitable for tasks where **structural similarity** (clauses, keywords, identifiers) is more critical than semantic equivalence. It provides a robust, interpretable metric for evaluating SQL generation systems, aligning with the syntactic rigor required for valid SQL. For deeper semantic validation, additional checks (e.g., query execution equivalence) would be needed.

---
## SQLSimilarity Class
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
