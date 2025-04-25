import time
import json
import csv
import unittest
from task1_1 import decode, encode  # Import both required functions


# Code to run the unitest file after the encode and decode function run.
def unitest_file_tests():
    """Code to run the unitest file"""
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='task1_1test.py')

    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


# Function to measure performance for Encode and Decode function with and without timing.
def measure_performance(rec_decoded, rec_encoded, output_csv):
    """Measure processing time for different batch sizes"""

    # Opening the Decoded record.
    with open(rec_decoded, "r", encoding="utf-8") as f:
        dec_records = json.load(f)["records_decoded"]

    # Opening the Encoded file.
    with open(rec_encoded, "r", encoding="utf-8") as f:
        enc_records = json.load(f)["records_encoded"]

    # Saving different batch size value in list for processing.
    batch_sizes = [100] + [i*1000 for i in range(1, 11)]
    results = []

    # Loop to get data for different batch size.
    for size in batch_sizes:
        batch1 = dec_records[:size]
        batch2 = enc_records[:size]
        
        # Measure without tests for passed decoded data to encode format
        start = time.time()
        [encode(record) for record in batch1]
        encode_function_without_testing = time.time() - start
        
        # Measure with tests for passed decoded data to encode format
        unitest_file_tests()
        encode_function_with_testing = time.time() - start

        # Measure without tests for passed encoded data to decode format
        start = time.time()
        [decode(record) for record in batch2]
        decode_function_without_testing = time.time() - start

        # Measure with tests for passed encoded data to decode format
        unitest_file_tests()
        decode_function_with_testing = time.time() - start

        # Appending results for the four column heading
        results.append({
            "num_records": size,
            "Encode Function without Testing": round(encode_function_without_testing, 8),
            "Encode Function with Testing": round(encode_function_with_testing, 8),
            "Decode Function without Testing": round(decode_function_without_testing, 8),
            "Decode Function with Testing": round(decode_function_with_testing, 8)
        })

    # Code to write the result in the CSV file.
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # Message to confirm that the data is stored in the CSV file.
    print(f"Performance results saved to {output_csv}")


if __name__ == "__main__":
    try:
        # Checking if the needed file to run the encode and decode function is available in the current path.
        with open("records_decoded.json", "r"):
            pass
        with open("records_encoded.json", "r"):
            pass
    except FileNotFoundError:
        print("Please complete Task 1 first to generate records_encoded.json and records_decoded.json")
        exit(1)

    # Running the performance function to generate the CSV file with data and used that data later to generate plot.
    measure_performance("records_decoded.json", "records_encoded.json", "performance_results.csv")

    try:
        # Importing necessary libraries
        import pandas as pd
        import matplotlib.pyplot as plt

        # Loading the CSV file.
        df = pd.read_csv("performance_results.csv")
        plt.figure(figsize=(10, 6))

        # Plotting the line based on the available data.
        plt.plot(df["num_records"], df["Encode Function without Testing"], label="Encode Without Tests", marker="o",
                 color='orange')
        plt.plot(df["num_records"], df["Encode Function with Testing"], label="Encode With Tests", marker="x",
                 color="green")
        plt.plot(df["num_records"], df["Decode Function without Testing"], label="Decode Without Tests", marker="+",
                 color='cyan')
        plt.plot(df["num_records"], df["Decode Function with Testing"], label="Decode With Tests", marker=".",
                 color="red")

        # Using necessary labels.
        plt.xlabel("Number of Records")
        plt.ylabel("Execution Time (seconds)")
        plt.title("MRZ Encoding Performance Comparison")
        plt.legend()
        plt.grid(True)

        # Saving the generated plot in the current directory with the name used below.
        plt.savefig("performance_plot.png")

        # Message to confirm that the plot was saved.
        print("Performance plot saved to performance_plot.png")
    except ImportError:
        print("Install pandas and matplotlib to generate performance plot:")
        print("pip install pandas matplotlib")
