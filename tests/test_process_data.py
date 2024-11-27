import unittest
from src.process_data import parse_data

class TestDataParser(unittest.TestCase):
    def test_parsing(self):
        test_data = """Wygenerowane przez Trading 212 UK Ltd. 20 września 2024 o 21:00 (UTC).
Wplat PLN 0.00
Wyplaty PLN -3,000.00
Zrealizowane zyski/straty PLN 28.35
Niezrealizowane zyski i straty PLN 94.16
Dywidendy PLN 0.00
Odsetki „overnight” PLN 0.00
Wartosc konta ogolem PLN 11,288.47"""
        
        result = parse_data(test_data)
        self.assertEqual(result[0]['Date'], '2024-04-11')
        self.assertEqual(float(result[0]['Account_Value']), 5132.08)
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()