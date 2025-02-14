
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
