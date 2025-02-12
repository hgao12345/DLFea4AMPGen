# Step 1: Perform multiple sequence alignment in MEGA11 to create '13aa.seq.align.fas'
# Ensure the alignment file '13aa.seq.align.fas' is generated and aligned before proceeding.

# Step 2: Install FastTree using Conda (ensure you are in the correct environment)
# Activate your Conda environment if not already done
conda install -c bioconda fasttree

# Step 3: Build the evolutionary tree using FastTree and save it in Newick format
fasttree 13aa.seq.align.fas > tree_align.newick

# Step 4: Visit the website to visualize the plot
# https://www.chiplot.online/?#Bar

