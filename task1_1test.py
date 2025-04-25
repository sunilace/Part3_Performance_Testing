import unittest
from unittest.mock import patch
from task1_1 import check_digit, encode_mrz, decode, hardware_scan, database_query


class MTTDtest(unittest.TestCase):
    # Mock function
    @patch("task1_1.hardware_scan")
    def test_mock_hardware(self, mock_scan):
        mock_scan.return_value = "MOCK_SCANNED_DATA"
        result = mock_scan()
        mock_scan.assert_called_once()
        self.assertEqual(result, "MOCK_SCANNED_DATA")

    # Mock function
    @patch("task1_1.database_query")
    def test_mock_database_query(self, mock_db):
        expected_result = {"passport_number": "123456789"}
        mock_db.return_value = expected_result
        test_query = "SELECT * FROM passports"
        result = mock_db(test_query)
        mock_db.assert_called_once_with(test_query)
        self.assertEqual(result, expected_result)

    # Dummy data for later use.
    def setUp(self):
        self.standard_data = {
            "document_type": "P",
            "issuing_country": "UTO",
            "last_name": "DOE",
            "first_name": "JOHN",
            "passport_number": "123456789",
            "nationality": "UTO",
            "birth_date": "900101",
            "sex": "M",
            "expiry_date": "250101",
            "personal_number": "1234567890"
        }
        self.standard_lines = (
            "P<UTODOE<<JOHN<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",
            "1234567892UTO9001011M25010161234567890<<<<<5"
        )

    # Test case for valid check digit input
    def test_check_digit_valid_input(self):
        self.assertEqual(check_digit("L898902C3"), 0)
        self.assertEqual(check_digit("W45896745"), 2)

    # Test case for invalid check digit input
    def test_check_digit_invalid_input(self):
        self.assertNotEqual(check_digit("W45896745"), 5)
        self.assertNotEqual(check_digit("L898902C3"), 1)

    # Test case for valid MRZ encoding
    def test_encode_mrz_valid(self):
        info = {
            "document_type": 'P',
            "issuing_country": "UTO",
            "last_name": "GUPTA",
            "first_name": "SUNIL VIRENDRA",
            "passport_number": "W45896745",
            "nationality": "UTO",
            "birth_date": "900101",
            "sex": "M",
            "expiry_date": "250101",
            "personal_number": "ZE184226B",
        }
        encoded_mrz = encode_mrz(info)
        self.assertEqual(encoded_mrz,
                         'P<UTOGUPTA<<SUNIL<VIRENDRA<<<<<<<<<<<<<<<<<<\nW458967452UTO9001011M2501016ZE184226B<<<<<<4')

    def test_encode_mrz_missing_fields(self):
        # Three test cases to check if any fields are missing then system raising ValueError.
        incomplete_info = {
            # Document type missing
            "issuing_country": "UTO",
            "last_name": "GUPTA",
            "first_name": "SUNIL VIRENDRA",
            "passport_number": "W45896745",
            "nationality": "UTO",
            "birth_date": "900101",
            "sex": "M",
            "expiry_date": "250101",
            "personal_number": "ZE184226B",
        }
        with self.assertRaises(ValueError):
            encode_mrz(incomplete_info)

        incomplete_info = {
            # Given name missing
            "document_type": 'P',
            "issuing_country": "UTO",
            "last_name": "GUPTA",
            "passport_number": "W45896745",
            "nationality": "UTO",
            "birth_date": "900101",
            "sex": "M",
            "expiry_date": "250101",
            "personal_number": "ZE184226B",
        }
        with self.assertRaises(ValueError):
            encode_mrz(incomplete_info)

        incomplete_info = {
            # Personal no missing
            "document_type": 'P',
            "issuing_country": "UTO",
            "last_name": "GUPTA",
            "first_name": "SUNIL VIRENDRA",
            "passport_number": "W45896745",
            "nationality": "UTO",
            "birth_date": "900101",
            "sex": "M",
            "expiry_date": "250101",
        }
        with self.assertRaises(ValueError):
            encode_mrz(incomplete_info)

    # Checking values decode properly based on given two lines.
    def test_decode_valid(self):
        line1, line2 = self.standard_lines
        parsed = decode(line1+";"+line2)
        line1 = parsed['line1']
        line2 = parsed['line2']

        self.assertEqual(line1["issuing_country"], "UTO")
        self.assertEqual(line1["last_name"], "DOE")
        self.assertEqual(line1["given_name"], "JOHN")
        self.assertEqual(line2["passport_number"], "123456789")
        self.assertEqual(line2["country_code"], "UTO")
        self.assertEqual(line2["birth_date"], "900101")
        self.assertEqual(line2["sex"], "M")
        self.assertEqual(line2["expiration_date"], "250101")
        self.assertEqual(line2["personal_number"], "1234567890")

    # Test case for invalid MRZ parsing
    def test_decode_invalid(self):
        # Test case with incomplete MRZ data
        line1_incomplete = "PUTO<<DOE<<JOHN<<<<<<<<<<"
        line2_incomplete = "123456789UTO900101M250101"
        self.assertEqual(decode(line1_incomplete+";"+line2_incomplete), "Invalid Passport Details")


if __name__ == "__main__":
    unittest.main()
