# Annotation Script: annotateOthers

## Overview

The `annotateOthers` script is designed to read information from a TSV file containing details about contigs, their positions, and coverages. A coverage value of zero is assigned to regions without any matching. The script identifies empty intersections (zero coverage) and annotates them as "others."

## Usage

1. **Input Data:** Prepare a TSV genome coverage file with information about contigs, positions, and coverages.

2. **Run the Script:**
   ```bash
   python annotateOthers.py -i input_file.tsv -o output_file.tsv -f [tsv or bed6]

## Options
- Specify the input TSV file using the -i flag.
- Specify the output file with the -o flag.
- The script also supports saving in BED9 format using the -f bed9 flag.
