import pandas as pd

# Create sample data model
def create_data_model_excel(output_file="data_model.xlsx"):
    # 1. Tables Sheet
    tables_data = [
        {"table_name": "customers", "description": "Customer information"},
        {"table_name": "orders", "description": "Sales orders"},
        {"table_name": "products", "description": "Product catalog"},
        {"table_name": "order_items", "description": "Order items details"},
        {"table_name": "suppliers", "description": "Supplier information"},
        {"table_name": "categories", "description": "Product categories"},
        {"table_name": "employees", "description": "Employee details"},
        {"table_name": "departments", "description": "Department details"},
        {"table_name": "locations", "description": "Location details"},
        {"table_name": "payments", "description": "Payment details"},
        {"table_name": "invoices", "description": "Invoice details"},
        {"table_name": "shipping_details", "description": "Shipping details"},
        {"table_name": "discounts", "description": "Discount details"},
        {"table_name": "promotions", "description": "Promotion details"},
        {"table_name": "reviews", "description": "Product reviews"},
        {"table_name": "feedbacks", "description": "Customer feedbacks"},
        {"table_name": "wishlists", "description": "Customer wishlists"},
        {"table_name": "shopping_carts", "description": "Shopping cart details"},
        {"table_name": "cart_items", "description": "Cart item details"},
        {"table_name": "inventory", "description": "Inventory details"},
        {"table_name": "sales", "description": "Sales details"},
        {"table_name": "returns", "description": "Return details"},
        {"table_name": "refunds", "description": "Refund details"},
        {"table_name": "taxes", "description": "Tax details"},
        {"table_name": "coupons", "description": "Coupon details"},
        {"table_name": "subscriptions", "description": "Subscription details"},
        {"table_name": "notifications", "description": "Notification details"},
        {"table_name": "user_roles", "description": "User role details"},
        {"table_name": "permissions", "description": "Permission details"},
        {"table_name": "audit_logs", "description": "Audit log details"},
        {"table_name": "contacts", "description": "Contact details"},
        {"table_name": "messages", "description": "Message details"},
        {"table_name": "chat_sessions", "description": "Chat session details"},
        {"table_name": "tickets", "description": "Support ticket details"},
        {"table_name": "ticket_comments", "description": "Ticket comment details"},
        {"table_name": "knowledge_base", "description": "Knowledge base articles"},
        {"table_name": "faq", "description": "Frequently asked questions"},
        {"table_name": "blog_posts", "description": "Blog post details"},
        {"table_name": "comments", "description": "Comment details"},
        {"table_name": "likes", "description": "Like details"},
        {"table_name": "followers", "description": "Follower details"},
        {"table_name": "activity_logs", "description": "Activity log details"},
        {"table_name": "settings", "description": "System settings"},
        {"table_name": "configurations", "description": "Configuration details"},
        {"table_name": "reports", "description": "Report details"},
        {"table_name": "dashboards", "description": "Dashboard details"},
        {"table_name": "widgets", "description": "Widget details"},
        {"table_name": "integrations", "description": "Integration details"}
    ]
    tables_df = pd.DataFrame(tables_data)
    
    # 2. Columns Sheet
    columns_data = [
        {"table_name": "customers", "column_name": "customer_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "customers", "column_name": "name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "customers", "column_name": "email", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "orders", "column_name": "order_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "orders", "column_name": "order_date", "data_type": "date", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "orders", "column_name": "customer_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "products", "column_name": "product_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "products", "column_name": "product_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "products", "column_name": "category_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        {"table_name": "products", "column_name": "supplier_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "order_items", "column_name": "order_item_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "order_items", "column_name": "order_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        {"table_name": "order_items", "column_name": "product_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        {"table_name": "order_items", "column_name": "quantity", "data_type": "int", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "order_items", "column_name": "price", "data_type": "decimal(10, 2)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "suppliers", "column_name": "supplier_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "suppliers", "column_name": "supplier_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "categories", "column_name": "category_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "categories", "column_name": "category_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "employees", "column_name": "employee_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "employees", "column_name": "first_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "employees", "column_name": "last_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "employees", "column_name": "department_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "departments", "column_name": "department_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "departments", "column_name": "department_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "locations", "column_name": "location_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "locations", "column_name": "address", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "locations", "column_name": "city", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "payments", "column_name": "payment_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "payments", "column_name": "amount", "data_type": "decimal(10, 2)", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "payments", "column_name": "order_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "invoices", "column_name": "invoice_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "invoices", "column_name": "invoice_date", "data_type": "date", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "invoices", "column_name": "order_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "shipping_details", "column_name": "shipping_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "shipping_details", "column_name": "tracking_number", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        {"table_name": "shipping_details", "column_name": "order_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "discounts", "column_name": "discount_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "discounts", "column_name": "discount_percent", "data_type": "decimal(5, 2)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "promotions", "column_name": "promotion_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "promotions", "column_name": "promotion_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "reviews", "column_name": "review_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "reviews", "column_name": "product_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        {"table_name": "reviews", "column_name": "rating", "data_type": "int", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "feedbacks", "column_name": "feedback_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "feedbacks", "column_name": "customer_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "wishlists", "column_name": "wishlist_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "wishlists", "column_name": "customer_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "shopping_carts", "column_name": "cart_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "shopping_carts", "column_name": "customer_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "cart_items", "column_name": "cart_item_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "cart_items", "column_name": "cart_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        {"table_name": "cart_items", "column_name": "product_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "inventory", "column_name": "inventory_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "inventory", "column_name": "product_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        {"table_name": "inventory", "column_name": "quantity", "data_type": "int", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "sales", "column_name": "sale_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "sales", "column_name": "product_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        {"table_name": "sales", "column_name": "quantity", "data_type": "int", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "returns", "column_name": "return_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "returns", "column_name": "order_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "refunds", "column_name": "refund_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "refunds", "column_name": "return_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "taxes", "column_name": "tax_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "taxes", "column_name": "tax_rate", "data_type": "decimal(5, 2)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "coupons", "column_name": "coupon_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "coupons", "column_name": "discount_amount", "data_type": "decimal(10, 2)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "subscriptions", "column_name": "subscription_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "subscriptions", "column_name": "customer_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "notifications", "column_name": "notification_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "notifications", "column_name": "message", "data_type": "text", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "user_roles", "column_name": "role_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "user_roles", "column_name": "role_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "permissions", "column_name": "permission_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "permissions", "column_name": "role_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "audit_logs", "column_name": "log_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "audit_logs", "column_name": "action", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "contacts", "column_name": "contact_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "contacts", "column_name": "name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "messages", "column_name": "message_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "messages", "column_name": "sender_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "chat_sessions", "column_name": "session_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "chat_sessions", "column_name": "participant_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "tickets", "column_name": "ticket_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "tickets", "column_name": "customer_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "ticket_comments", "column_name": "comment_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "ticket_comments", "column_name": "ticket_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "knowledge_base", "column_name": "article_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "knowledge_base", "column_name": "title", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "faq", "column_name": "faq_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "faq", "column_name": "question", "data_type": "text", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "blog_posts", "column_name": "post_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "blog_posts", "column_name": "author_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "comments", "column_name": "comment_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "comments", "column_name": "post_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "likes", "column_name": "like_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "likes", "column_name": "post_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "followers", "column_name": "follower_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "followers", "column_name": "user_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "activity_logs", "column_name": "activity_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "activity_logs", "column_name": "activity_type", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "settings", "column_name": "setting_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "settings", "column_name": "setting_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "configurations", "column_name": "config_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "configurations", "column_name": "config_value", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "reports", "column_name": "report_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "reports", "column_name": "report_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "dashboards", "column_name": "dashboard_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "dashboards", "column_name": "dashboard_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False},
        
        {"table_name": "widgets", "column_name": "widget_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "widgets", "column_name": "dashboard_id", "data_type": "int", "is_primary_key": False, "is_foreign_key": True},
        
        {"table_name": "integrations", "column_name": "integration_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
        {"table_name": "integrations", "column_name": "integration_name", "data_type": "varchar(255)", "is_primary_key": False, "is_foreign_key": False}
    ]
    columns_df = pd.DataFrame(columns_data)
    
    # 3. Relationships Sheet
    relationships_data = [
        {"source_table": "orders", "source_column": "customer_id", "target_table": "customers", "target_column": "customer_id"},
        {"source_table": "order_items", "source_column": "order_id", "target_table": "orders", "target_column": "order_id"},
        {"source_table": "order_items", "source_column": "product_id", "target_table": "products", "target_column": "product_id"},
        {"source_table": "products", "source_column": "category_id", "target_table": "categories", "target_column": "category_id"},
        {"source_table": "products", "source_column": "supplier_id", "target_table": "suppliers", "target_column": "supplier_id"},
        {"source_table": "employees", "source_column": "department_id", "target_table": "departments", "target_column": "department_id"},
        {"source_table": "payments", "source_column": "order_id", "target_table": "orders", "target_column": "order_id"},
        {"source_table": "invoices", "source_column": "order_id", "target_table": "orders", "target_column": "order_id"},
        {"source_table": "shipping_details", "source_column": "order_id", "target_table": "orders", "target_column": "order_id"},
        {"source_table": "reviews", "source_column": "product_id", "target_table": "products", "target_column": "product_id"},
        {"source_table": "feedbacks", "source_column": "customer_id", "target_table": "customers", "target_column": "customer_id"},
        {"source_table": "wishlists", "source_column": "customer_id", "target_table": "customers", "target_column": "customer_id"},
        {"source_table": "shopping_carts", "source_column": "customer_id", "target_table": "customers", "target_column": "customer_id"},
        {"source_table": "cart_items", "source_column": "cart_id", "target_table": "shopping_carts", "target_column": "cart_id"},
        {"source_table": "cart_items", "source_column": "product_id", "target_table": "products", "target_column": "product_id"},
        {"source_table": "inventory", "source_column": "product_id", "target_table": "products", "target_column": "product_id"},
        {"source_table": "sales", "source_column": "product_id", "target_table": "products", "target_column": "product_id"},
        {"source_table": "returns", "source_column": "order_id", "target_table": "orders", "target_column": "order_id"},
        {"source_table": "refunds", "source_column": "return_id", "target_table": "returns", "target_column": "return_id"},
        {"source_table": "subscriptions", "source_column": "customer_id", "target_table": "customers", "target_column": "customer_id"},
        {"source_table": "permissions", "source_column": "role_id", "target_table": "user_roles", "target_column": "role_id"},
        {"source_table": "messages", "source_column": "sender_id", "target_table": "customers", "target_column": "customer_id"},
        {"source_table": "chat_sessions", "source_column": "participant_id", "target_table": "customers", "target_column": "customer_id"},
        {"source_table": "tickets", "source_column": "customer_id", "target_table": "customers", "target_column": "customer_id"},
        {"source_table": "ticket_comments", "source_column": "ticket_id", "target_table": "tickets", "target_column": "ticket_id"},
        {"source_table": "blog_posts", "source_column": "author_id", "target_table": "employees", "target_column": "employee_id"},
        {"source_table": "comments", "source_column": "post_id", "target_table": "blog_posts", "target_column": "post_id"},
        {"source_table": "likes", "source_column": "post_id", "target_table": "blog_posts", "target_column": "post_id"},
        {"source_table": "followers", "source_column": "user_id", "target_table": "customers", "target_column": "customer_id"},
        {"source_table": "widgets", "source_column": "dashboard_id", "target_table": "dashboards", "target_column": "dashboard_id"}
    ]
    relationships_df = pd.DataFrame(relationships_data)
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        tables_df.to_excel(writer, sheet_name="Tables", index=False)
        columns_df.to_excel(writer, sheet_name="Columns", index=False)
        relationships_df.to_excel(writer, sheet_name="Relationships", index=False)
    
    print(f"Data model created successfully: {output_file}")
