import unittest
import os
from xlsx_to_csv import xlsx_to_csv, find_all_xlsx, change_ext_to_csv

class TestXlsxToCsv(unittest.TestCase):
    def setUp(self):
        self.excel_path = os.path.join(
            os.path.dirname(__file__), 'test-data', 'test.xlsx')
        self.csv_path = os.path.join(
            os.path.dirname(__file__), 'test-data', 'test.csv')
        self.tmp_path = os.path.join(
            os.path.dirname(__file__), 'test-data', 'tmp.csv')
    
    def test_glob(self):
        test_xlsx_list = find_all_xlsx(os.path.dirname(__file__))
        self.assertEqual(test_xlsx_list, [self.excel_path])

    def test_name_conversion(self):
        self.assertEqual(change_ext_to_csv(self.excel_path), self.csv_path)

    def test_conversion(self):
        xlsx_to_csv(self.excel_path, self.tmp_path)
        with open(self.csv_path) as csv_file:
            with open(self.tmp_path) as tmp_file:
                self.assertEqual(csv_file.read(),
                         tmp_file.read())

    def tearDown(self):
        if os.path.exists(self.tmp_path):
            os.remove(self.tmp_path)


if __name__ == "__main__":
    unittest.main()
