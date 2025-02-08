import pandas as pd
import random
from faker import Faker

class DataModelGenerator:
    def __init__(self, seed=42):
        self.fake = Faker()
        self.seed = seed
        random.seed(seed)
        self.data_model = None

    def create_sample_data_model(self, output_file="data_model.xlsx"):
        """Create a sample data model and save it to an Excel file."""
        # Tables Sheet
        tables_data = [
            {"table_name": "customers", "description": "Customer information"},
            # ... (other table entries as provided in the original code)
        ]
        tables_df = pd.DataFrame(tables_data)
        
        # Columns Sheet
        columns_data = [
            {"table_name": "customers", "column_name": "customer_id", "data_type": "int", "is_primary_key": True, "is_foreign_key": False},
            # ... (other column entries as provided in the original code)
        ]
        columns_df = pd.DataFrame(columns_data)
        
        # Relationships Sheet
        relationships_data = [
            {"source_table": "orders", "source_column": "customer_id", "target_table": "customers", "target_column": "customer_id"},
            # ... (other relationship entries as provided in the original code)
        ]
        relationships_df = pd.DataFrame(relationships_data)
        
        # Create Excel file with multiple sheets
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            tables_df.to_excel(writer, sheet_name="Tables", index=False)
            columns_df.to_excel(writer, sheet_name="Columns", index=False)
            relationships_df.to_excel(writer, sheet_name="Relationships", index=False)
        
        print(f"Data model created successfully: {output_file}")

    def load_data_model(self, excel_path="data_model.xlsx"):
        """Load the data model from an Excel file."""
        try:
            data_model = {
                'tables': pd.read_excel(excel_path, sheet_name='Tables'),
                'columns': pd.read_excel(excel_path, sheet_name='Columns'),
                'relationships': pd.read_excel(excel_path, sheet_name='Relationships')
            }
        except Exception as e:
            print(f"Error loading data model: {e}")
            return False
        
        required_columns = {
            'tables': ['table_name'],
            'columns': ['table_name', 'column_name', 'data_type'],
            'relationships': ['source_table', 'source_column', 'target_table', 'target_column']
        }
        for sheet, cols in required_columns.items():
            if not all(col in data_model[sheet].columns for col in cols):
                print(f"Missing required columns in {sheet} sheet.")
                return False
        
        self.data_model = data_model
        return True

    def generate_synthetic_query(self, num_joins=2, num_conditions=2):
        """Generate a synthetic SQL query based on the loaded data model."""
        if self.data_model is None:
            raise ValueError("Data model not loaded. Call load_data_model() first.")
        
        # Base table selection
        base_table = random.choice(self.data_model['tables']['table_name'].tolist())
        
        # Select related tables for joins
        relationships = self.data_model['relationships'][self.data_model['relationships']['source_table'] == base_table]
        selected_joins = relationships.sample(min(num_joins, len(relationships))) if not relationships.empty else pd.DataFrame()
        
        # SELECT clause
        if random.choice([True, False]):
            select_clause = "*"
        else:
            columns = self.data_model['columns'][self.data_model['columns']['table_name'] == base_table]['column_name'].tolist()
            select_clause = ', '.join(columns)
        
        # JOIN clauses
        join_clauses = []
        for _, join in selected_joins.iterrows():
            join_type = random.choice(['INNER', 'LEFT', 'RIGHT'])
            join_clause = (f"{join_type} JOIN {join['target_table']} ON {base_table}.{join['source_column']} = "
                           f"{join['target_table']}.{join['target_column']}")
            join_clauses.append(join_clause)
        
        # WHERE conditions
        involved_tables = [base_table] + selected_joins['target_table'].tolist()
        all_columns = self.data_model['columns'][self.data_model['columns']['table_name'].isin(involved_tables)]
        where_conditions = [self._generate_column_condition(col) for _, col in all_columns.sample(min(num_conditions, len(all_columns))).iterrows()]
        
        # Assemble query
        query = f"SELECT {select_clause}\nFROM {base_table}"
        if join_clauses:
            query += "\n" + "\n".join(join_clauses)
        if where_conditions:
            query += f"\nWHERE {' AND '.join(where_conditions)};"
        else:
            query += ";"
        return query

    def _generate_column_condition(self, col):
        """Generate a realistic condition for a column (private helper method)."""
        col_name = f"{col['table_name']}.{col['column_name']}"
        data_type = col['data_type'].lower()
        
        if data_type in ['int', 'number']:
            value = random.randint(1, 1000)
            operator = random.choice(['>', '<', '=', '!='])
            return f"{col_name} {operator} {value}"
        elif data_type in ['varchar', 'text']:
            if random.random() > 0.5:
                return f"{col_name} LIKE '%{self.fake.word()}%'"
            else:
                values = [f"'{self.fake.word()}'" for _ in range(3)]
                return f"{col_name} IN ({', '.join(values)})"
        elif data_type == 'date':
            start = self.fake.date_between(start_date='-5y', end_date='today')
            end = self.fake.date_between(start_date=start, end_date='today')
            return f"{col_name} BETWEEN '{start}' AND '{end}'"
        else:
            return f"{col_name} = {random.choice([True, False])}"

    def generate_dataset(self, num_queries=5000, num_joins=2, num_conditions=2):
        """Generate a dataset of synthetic queries split into input/output pairs."""
        queries = [self.generate_synthetic_query(num_joins, num_conditions) for _ in range(num_queries)]
        
        input_lst = []
        output_lst = []
        for q in queries:
            r = random.choice([1, 2])
            parts = q.split("\n")
            input_part = ' '.join(parts[:r])
            output_part = ' '.join(parts[r:])
            input_lst.append(input_part)
            output_lst.append(output_part)

        queries = pd.DataFrame({"queries": queries})
        dataset = pd.DataFrame({"input": input_lst, "output": output_lst})
        
        return dataset, queries

# Example usage:
# generator = DataModelGenerator()
# generator.create_sample_data_model()
# generator.load_data_model()
# dataset, queries = generator.generate_dataset(num_queries=5000)
# print(dataset.head())
