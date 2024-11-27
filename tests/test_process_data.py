import unittest
from src.process_data import parse_data, preformat
class TestDataParser(unittest.TestCase):
    def test_parsing(self):
        test_data = """Wygenerowane przez Trading 212 UK Ltd. 9 maja 2024 o 21:00 (UTC).
Wpłat PLN 0.00
Wypłaty PLN 0.00
Zrealizowane zyski/straty PLN 49.37
Niezrealizowane zyski i straty PLN 588.86
Dywidendy PLN 0.00
Odsetki „overnight” PLN -9.25
Wartość konta ogółem PLN 13,018.59"""
        
        result = parse_data(preformat(test_data))
        self.assertEqual(result[0]['Date'], '2024-09-01')
        self.assertEqual(float(result[0]['Account_Value']), 11.896)
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()
