#!/bin/bash

# Usage: bash fasttree.sh input.fasta output_tree.newick

INPUT_FILE=$1
OUTPUT_TREE=$2

# Check if parameters are provided
if [[ -z "$INPUT_FILE" || -z "$OUTPUT_TREE" ]]; then
  echo "Usage: bash $0 <input_fasta> <output_tree_file>"
  exit 1
fi

# Check if the input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Error: Input file '$INPUT_FILE' not found!"
  exit 1
fi

# Temporary alignment output file
ALIGN_FILE="temp_aligned.aln"

# Run MUSCLE for multiple sequence alignment
muscle -align "$INPUT_FILE" -output "$ALIGN_FILE"

# Run FastTree to build the phylogenetic tree
fasttree "$ALIGN_FILE" > "$OUTPUT_TREE"

# Optionally remove the temporary alignment file
rm "$ALIGN_FILE"

# Notify the user
echo "Tree saved to: $OUTPUT_TREE"
echo "You can visualize it at: https://www.chiplot.online/?#Bar"
