---
# Data Modeling
---

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

