import json
from typing import List, Dict
import zlib


# 0. Check digit function using CRC32
def check_digit(string):
    crc32_val = zlib.crc32(string.encode('utf-8')) & 0xFFFFFFFF
    remainder = crc32_val % 10
    return remainder


# 1. To validate country code
def validate_country_code(code):
    valid_3letter = ["USA", "CAN", "GBR", "DEU", "FRA", "IND", "CHN", "JPN", "AUS", "BRA", "RUS", "ZAF", "MEX", "ITA",
                     "ESP", "KOR", "NGA", "ARG", "EGY", "TUR", "UNO", "EUE", "XOM", "XPO", "UNA", "UNK", "XXA", "XXB",
                     "XXC", "XXX", "GBD", "GBN", "GBO", "GBP", "GBS", "D<<", "ZIM", "BAH", "ADM", "AON", "AVA", "AZA",
                     "BUR", "ELM", "CSM", "SGY", "IPA", "IMR", "IVR", "KRL", "LAN", "MRC", "NAT", "NRR", "NVA", "NDK",
                     "ICN", "PBC", "FKJ", "SNC", "SAS", "SBR", "SON", "TIN", "UEU", "DRG", "WSV", "WUR", "YAT", "ZNX",
                     "GML", "MAY", "BLG", "RNZ", "CDR", "AAR", "ABE", "AEN", "AGE", "ANI", "AMI", "ASR", "ASH", "ASP",
                     "ASV", "ATI", "ATO", "AST", "RSA", "BAR", "BAU", "BEC", "BRR", "BRK", "CAD", "CGD", "CAM", "CRN",
                     "CCO", "CEN", "CET", "CLV", "COR", "DSC", "DNB", "DES", "DGM", "DSL", "DKJ", "DCK", "ESV", "RUE",
                     "EDP", "EGN", "EGR", "ELD", "ENR", "ESX", "ESE", "FFK", "FLA", "FLR", "FOR", "GLS", "GDN", "HAK",
                     "HBD", "HRA", "HSI", "IKO", "IDH", "IUS", "JUC", "JUP", "JUS", "KNZ", "KTH", "KLT", "KDR", "KOH",
                     "KRT", "KSJ", "KOS", "LST", "LDL", "LEG", "LHM", "LEV", "LYG", "LNG", "LQN", "LDW", "LDN", "LYT",
                     "MTA", "MTH", "MCA", "MKN", "MIL", "MGN", "MIS", "MON", "NAV", "NDL", "NKV", "NEI", "NFC", "NPV",
                     "NRZ", "RUB", "NST", "SCY", "NWP", "NLL", "NDL", "NSE", "NCT", "NRT", "NOS", "OCC", "NVR", "NVN",
                     "ORI", "OSK", "OVR", "PCM", "PRV", "PIN", "PLU", "PLA", "PMP", "PSH", "PPN", "PSF", "QUE", "QSL",
                     "RND", "RNK", "REV", "REY", "URM", "ROS", "RVA", "RDV", "SIV", "SAL", "SDS", "SDO", "SEY", "SHC",
                     "SHR", "SRW", "SVU", "SKJ", "SVT", "SLI", "SGV", "SYZ", "SRH", "STM", "STR", "SUB", "SUN", "SDM",
                     "SWV", "TAM", "TER", "THD", "TNA", "TOD", "TNT", "TRV", "TCR", "UBQ", "UBR", "USW", "UOR", "VRS",
                     "VHM", "VLS", "VDP", "WLN", "WAM", "WSP", "WEG", "WNH", "WYV", "YDR", "YUX", "AMZ", "LBY", "MDN",
                     "MAH", "MGW", "SAT", "UNT", "USI", "RKS", "ANT", "NTZ", "UTO", "IAO", "XCC", "XIM", "XBA", "XCE",
                     "XCO", "XEC", "XPO", "XES", "XMP", "XOM", "XDC", ]
    valid_2letter = {'EU', 'DE', 'KS', 'FR', 'CN', 'UN', 'AN', 'NT', 'UT', 'IA'}
    if code in valid_3letter or code in valid_2letter:
        return True
    else:
        return False


# 2. Complete encode_mrz function implementation
def encode_mrz(info: dict) -> str:
    """Core function for MRZ encoding"""
    required_fields = ['first_name', 'last_name', 'passport_number', 'nationality', 'birth_date', 'sex', 'expiry_date',
                     'personal_number', 'document_type', 'issuing_country']
    
    # Check for required fields. If not present then return ValueError
    missing_fields = [field for field in required_fields if field not in info]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Set default values
    info.setdefault('document_type', 'P')  # 'P' for passport by default
    info.setdefault('sex', '<')  # Default sex marker

    # Process special characters in names
    def sanitize(text):
        """Convert spaces and hyphens to '<' and ensure uppercase"""
        return text.upper().replace(" ", "<").replace("-", "<")
    
    # Build line 1
    line1 = (
        f"{info['document_type']}<{info['issuing_country']}"
        f"{sanitize(info['last_name'])}<<{sanitize(info['first_name'])}"
    ).ljust(44, "<")  # Pad to 44 characters with '<'
    
    # Build line 2
    passport_num = info['passport_number'].ljust(9, "<")[:9]  # Ensure 9 chars
    personal_num = info['personal_number'].ljust(14, "<")[:14]  # Ensure 14 chars
    
    line2 = (
        f"{passport_num}"f"{check_digit(passport_num)}"
        f"{info['nationality']}"
        f"{info['birth_date']}"f"{check_digit(info['birth_date'])}"
        f"{info['sex']}"
        f"{info['expiry_date']}"f"{check_digit(info['expiry_date'])}"
        f"{personal_num}"
    ).ljust(43, "<") + f"{check_digit(personal_num)}"
    
    return f"{line1}\n{line2}"


# 3. Record Loading functions
def load_records(input_file: str) -> List[Dict]:
    """Load records from JSON file"""
    with open(input_file, "r", encoding='utf-8') as f:
        data = json.load(f)
    if "records_decoded" in data:
        return data["records_decoded"]
    elif "records_encoded" in data:
        return data["records_encoded"]


def encode(record: Dict) -> str:
    """Encode a single record"""
    line1_data = record["line1"]
    line2_data = record["line2"]
    
    # Prepare data for encode_mrz
    mrz_data = {
        "document_type": "P",
        "issuing_country": line1_data["issuing_country"],
        "last_name": line1_data["last_name"],
        "first_name": line1_data["given_name"],
        "passport_number": line2_data["passport_number"],
        "nationality": line2_data["country_code"],
        "birth_date": line2_data["birth_date"],
        "sex": line2_data["sex"],
        "expiry_date": line2_data["expiration_date"],
        "personal_number": line2_data.get("personal_number", "")  # Handle possible missing values
    }
    
    encoded = encode_mrz(mrz_data)
    return encoded.replace("\n", ";")  # Replace newline with semicolon


def process_records_encoding(input_file: str, output_file: str):
    """Process all records and save encoded output"""
    decoded_records = load_records(input_file)
    encoded_records = [encode(record) for record in decoded_records]
    
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump({"records_encoded": encoded_records}, f, indent=2)


# Decoding function.
def decode(line):
    line = line.split(";")
    line1 = line[0]
    line2 = line[-1]

    # If less then 44 charcters then return as invalid details.
    if len(line1) != 44 or len(line2) != 44:
        return f"Invalid Passport Details"

    # Separate dictionary to store data in proper format.
    d1 = {}
    d2 = {}

    # make a dict to simplify filling d1 and d2 dictionary.
    dict = {
        "document_type": line1[0],
        "issuing_country": line1[2:5],
        "last_name": line1[5:line1.find("<<")],
        "first_name": line1[line1.find("<<") + 2:].replace("<", " ").strip(),
        "passport_number": line2[0:9],
        "passport_number_cd": line2[9],
        "nationality": line2[10:13],
        "birth_date": line2[13:19],
        "birth_date_cd": line2[19],
        "sex": line2[20],
        "expiry_date": line2[21:27],
        "expiry_date_cd": line2[27],
        "personal_number": line2[28:-1].replace("<", "").strip(),
        "personal_number_cd": line2[-1]
    }

    d1["issuing_country"] = dict["issuing_country"]
    d1["last_name"] = dict['last_name']
    d1['given_name'] = dict['first_name']
    d2['passport_number'] = dict['passport_number']
    d2['country_code'] = dict['nationality']
    d2['birth_date'] = dict['birth_date']
    d2['sex'] = dict['sex']
    d2['expiration_date'] = dict['expiry_date']
    d2['personal_number'] = dict['personal_number']

    # Return the record in proper decode format.
    return {'line1': d1, 'line2': d2}


def process_records_decoding(input_file: str, output_file: str):
    """Process all records and save encoded output"""
    encoded_records = load_records(input_file)
    decoded_records = [decode(record) for record in encoded_records]

    with open(output_file, "w", encoding='utf-8') as f:
        json.dump({"records_decoded": decoded_records}, f, indent=2)


def hardware_scan() -> str:
    """Simulate hardware device scanning (placeholder for unit testing)."""
    pass  # Actual implementation would return device data, e.g., "SCANNED_DATA"


def database_query() -> Dict:
    """Simulate database access (placeholder for unit testing)."""
    pass  # Actual implementation would return query results, e.g., {"id": 123}


if __name__ == "__main__":
    try:
        process_records_encoding("records_decoded.json", "records_encoded_prog.json")
        print("Encoding completed. Results saved to records_encoded_prog.json")
        process_records_decoding("records_encoded.json", "records_decoded_prog.json")
        print("Decoding completed. Results saved to records_encoded_prog.json")
    except Exception as e:
        print(f"Processing failed: {e}")
        import traceback
        traceback.print_exc()
