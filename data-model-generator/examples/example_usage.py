from src.data_model_generator import DataModelGenerator

if __name__ == "__main__":
    generator = DataModelGenerator()
    generator.load_data_model()
    dataset, queries = generator.generate_dataset(num_queries=5000)
    print(dataset.head())
    print(queries.head())
