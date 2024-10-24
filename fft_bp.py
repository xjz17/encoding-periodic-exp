import os
import pandas as pd
from algorithm import *
from typing import Callable
import time
# Assuming the encode and decode functions are already defined as follows:
# encode: function that takes data and path, returns a tuple of size and time
# decode: function that takes a path and returns data
# def period_encode_param(data, path):
#     # Simulation of the encoding process
#     encoded_size = len(data) * 2  # hypothetical compression
#     encoding_time = 0.01 * len(data)  # hypothetical time
#     return (encoded_size, encoding_time)

# def period_decode(path):
#     # Simulation of the decoding process
#     return [1, 2, 3]  # just a dummy return

def process_files(root_dir):
    exp_data = {
        "folder": [],
        "file": [],
        "compress_ratio": [],
        "encoding_time": []
    }

    # Traverse through directories and files
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                df = pd.read_csv(file_path)
                # len = df.shape[0]

                # Ensure the file has at least two columns
                if df.shape[1] < 1:
                    continue
                

                data = df.iloc[:, 1].tolist()  # get data from the second column
                if len(data) < 1:
                    continue 
                result_path = "result.bin"  # path to save the encoded data

                # Encode data
                result, encoding_time = period_encode_param(data, result_path)
                compress_ratio = result / (len(data) * 4)  # assuming each int is 4 bytes
                compress_ratio = 1/compress_ratio
                encoding_time = encoding_time*1000000000/len(data)

                # Store results
                exp_data['folder'].append(subdir)
                exp_data['file'].append(file)
                exp_data['compress_ratio'].append(compress_ratio)
                exp_data['encoding_time'].append(encoding_time)



                # Print results (optional)
                print(f"Processed {file} in {subdir}: Compression Ratio = {compress_ratio}, Encoding Time = {encoding_time}")

    # Save experiment data to CSV
    exp_data_df = pd.DataFrame(data=exp_data)
    root_csv_dir = "/Users/xiaojinzhao/Documents/GitHub/encoding-outlier/icde0802/supply_experiment/R3O2_compare_compression/compression_ratio/fft"
    exp_data_df.to_csv(os.path.join(root_csv_dir, "compression_results.csv"), index=False)

# Specify the root directory containing 'tran_data' /Users/xiaojinzhao/Documents/GitHub/encoding-outlier/trans_data
root_dir = "/Users/xiaojinzhao/Documents/GitHub/encoding-outlier/trans_data"
# root_dir = "/Users/xiaojinzhao/Documents/GitHub/encoding-outlier/icde0802/supply_experiment/R3O2_compare_compression/data"
process_files(root_dir)
