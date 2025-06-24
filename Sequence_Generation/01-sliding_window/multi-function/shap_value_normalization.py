import argparse
import os

# ---- Argument parsing ----
parser = argparse.ArgumentParser(description="Normalize and merge SHAP value files (global min-max).")
parser.add_argument('--input_files', nargs='+', required=True, help='List of SHAP input text files')
parser.add_argument('--output_dir', type=str, required=True, help='Directory to save normalized and merged outputs')
args = parser.parse_args()

input_files = args.input_files
output_dir = args.output_dir
os.makedirs(output_dir, exist_ok=True)
base_names = [os.path.splitext(os.path.basename(f))[0] for f in input_files]


# ---- Step 1: Read all data ----
def read_all_data(file_list):
    all_data = []
    for f in file_list:
        with open(f, 'r', encoding='utf-8') as fh:
            lines = fh.readlines()
            data = [[-float(x) for x in line.strip().split(", ")] for line in lines]
            all_data.append(data)
    return all_data


all_data = read_all_data(input_files)  # List of N files × List of rows × List of values

# ---- Step 2: Compute global max positive and max negative values ----
flat_values = [x for file_data in all_data for row in file_data for x in row]
max_pos = max((x for x in flat_values if x > 0), default=1.0)
max_neg = max((-x for x in flat_values if x < 0), default=1.0)


# ---- Step 3: Global normalization ----
def normalize_value(x):
    if x > 0:
        return x / max_pos
    elif x < 0:
        return x / max_neg
    else:
        return 0.0


normalized_all = [
    [[normalize_value(x) for x in row] for row in file_data]
    for file_data in all_data
]


# ---- Step 4: Write normalized results for each file ----
for name, norm_data in zip(base_names, normalized_all):
    out_path = os.path.join(output_dir, f"normalized_{name}.txt")
    with open(out_path, "w", encoding="utf-8") as fw:
        for row in norm_data:
            fw.write(', '.join(map(str, row)) + '\n')


# ---- Step 5: Compute and write merged (summed) results ----
with open(os.path.join(output_dir, "all_model_mean.txt"), "w", encoding="utf-8") as fw:
    for rows in zip(*normalized_all):  # Each round 'rows' is one row from each file
        added = [sum(vals) for vals in zip(*rows)]
        fw.write(', '.join(map(str, added)) + '\n')
