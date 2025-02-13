import pandas as pd
import random
from faker import Faker

class DataModelGenerator:
    def __init__(self, seed=42):
        self.fake = Faker()
        self.seed = seed
        random.seed(seed)
        self.data_model = None

    def load_data_model(self, excel_path="data_model.xlsx"):
        """Load data model from Excel file with expected structure"""
        try:
            data_model = {
                'tables': pd.read_excel(excel_path, sheet_name='Tables'),
                'columns': pd.read_excel(excel_path, sheet_name='Columns'),
                'relationships': pd.read_excel(excel_path, sheet_name='Relationships')
            }
        except ValueError as e:
            print(f"Error loading data model: {e}")
            return None
        
        # Check if required columns exist in each sheet
        for sheet_name, df in data_model.items():
            if sheet_name == 'tables' and 'table_name' not in df.columns:
                print(f"'table_name' column missing in 'Tables' sheet.")
                return None
            elif sheet_name == 'columns' and ('table_name' not in df.columns or 'column_name' not in df.columns or 'data_type' not in df.columns):
                print(f"Missing required columns in 'Columns' sheet.")
                return None
            elif sheet_name == 'relationships' and ('source_table' not in df.columns or 'target_table' not in df.columns or 'source_column' not in df.columns or 'target_column' not in df.columns):
                print(f"Missing required columns in 'Relationships' sheet.")
                return None
        
        self.data_model = data_model
        return True

    def generate_synthetic_query(self, num_joins=2, num_conditions=2):
        """Generate a synthetic SQL query based on the data model"""
        if self.data_model is None:
            raise ValueError("Data model not loaded. Call load_data_model() first.")
        
        # Randomly select base table
        base_table = random.choice(self.data_model['tables']['table_name'].tolist())
        
        # Get related tables
        relationships = self.data_model['relationships'][
            self.data_model['relationships']['source_table'] == base_table
        ]
        
        # Select joins
        selected_joins = relationships.sample(min(num_joins, len(relationships)))
        
        # Generate SELECT clause
        use_all_columns = random.choice([True, False])
        
        if use_all_columns:
            select_clause = "*"
        else:
            columns = self.data_model['columns'][
                self.data_model['columns']['table_name'] == base_table
            ]['column_name'].tolist()
            select_clause = ', '.join(columns)
        
        # Generate JOIN clauses
        join_clauses = []
        for _, join in selected_joins.iterrows():
            join_type = random.choice(['', 'LEFT'])
            join_clause = (
                f"{join_type} JOIN {join['target_table']} "
                f"ON {base_table}.{join['source_column']} = "
                f"{join['target_table']}.{join['target_column']}"
            )
            join_clauses.append(join_clause)
        
        # Generate WHERE conditions
        involved_tables = [base_table] + selected_joins['target_table'].tolist()
        all_columns = self.data_model['columns'][
            self.data_model['columns']['table_name'].isin(involved_tables)
        ]
        
        where_conditions = []
        for _ in range(num_conditions):
            col = all_columns.sample(1).iloc[0]
            condition = self._generate_column_condition(col)
            where_conditions.append(condition)
        
        # Assemble query
        query = f"SELECT {select_clause}\n"
        query += f"FROM {base_table}\n"
        if join_clauses:
            query += '\n'.join(join_clauses) + '\n'
        if where_conditions:
            query += f"WHERE {' AND '.join(where_conditions)};"
        else:
            query += ";"
        
        return query

    def _generate_column_condition(self, col):
        """Generate realistic condition based on column type"""
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
        r_list = []
        for q in queries:
            r = random.choice([1, 2])
            parts = q.split("\n")
            input_part = ' '.join(parts[:r])
            output_part = ' '.join(parts[r:])
            input_lst.append(input_part)
            output_lst.append(output_part)
            r_list.append(r)

        queries = pd.DataFrame({"queries": queries})
        dataset = pd.DataFrame({"input": input_lst, "output": output_lst, "group":r_list})
        
        return dataset, queries

# Example usage:
# generator = DataModelGenerator()
# generator.load_data_model()
# dataset, queries = generator.generate_dataset(num_queries=5000)
