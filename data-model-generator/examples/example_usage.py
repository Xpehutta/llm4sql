from src.data_model_generator import DataModelGenerator

if __name__ == "__main__":
    generator = DataModelGenerator()
    generator.create_sample_data_model()
    generator.load_data_model()
    dataset = generator.generate_dataset(num_queries=100)
    print(dataset.head())
