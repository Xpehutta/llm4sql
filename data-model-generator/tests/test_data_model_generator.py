import unittest
from src.data_model_generator import DataModelGenerator

class TestDataModelGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = DataModelGenerator()

    def test_create_sample_data_model(self):
        self.generator.create_sample_data_model(output_file="test_data_model.xlsx")
        self.assertTrue(pd.ExcelFile("test_data_model.xlsx"))

    def test_generate_synthetic_query(self):
        self.generator.load_data_model(excel_path="test_data_model.xlsx")
        query = self.generator.generate_synthetic_query()
        self.assertIsInstance(query, str)

if __name__ == "__main__":
    unittest.main()
