from src.data_model_generator import DataModelGenerator
from model.data_model_generator import create_data_model_excel

if __name__ == "__main__":
    create_data_model_excel()
    generator = DataModelGenerator()
    generator.load_data_model()
    dataset, queries = generator.generate_dataset(num_queries=5000)
    print(dataset.head())
    print(queries.head())
