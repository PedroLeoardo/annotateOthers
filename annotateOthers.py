import argparse
import pandas as pd

def annotate_others(input_file, output_file, output_format="tsv"):
    # Open the input file and create a dataframe named 'df'
    # The file is read with tab (\t) as the delimiter, and columns are named as "Chrom", "Position", and "Coverage"
    with open(input_file) as tsvfile:
        df = pd.read_csv(tsvfile, delimiter="\t", names=["Chrom", "Position", "Coverage"])

    # Empty dictionary to be filled with information to be added to the output file
    # Dictionary keys are strings starting with "ID=other-" followed by a number
    # Dictionary values are lists with information about "Chrom", "annotateOthers", "others", start, end, '.', '.', '0', and the corresponding ID
    D = {}
    count_id = 0  # Counter used to create the ID for each new entry

    # Loop through the dataframe df to find regions with coverage 0
    i = 0
    while i <= df.shape[0] - 1:
        if i > df.shape[0] - 1:
            break
        current_line = df.iloc[i]  # Get the current line from the dataframe
        if current_line[2] == 0:  # Check if coverage is 0
            i = i + 1  # Move to the next line
            if i > df.shape[0] - 1:
                break
            next_line = df.iloc[i]  # Get the next line from the dataframe
            while (current_line[0] == next_line[0]) and (next_line[2] == 0):  # Loop to find the last line with coverage 0
                i = i + 1
                if i > df.shape[0] - 1:
                    break
                next_line = df.iloc[i]
            end_line = df.iloc[i - 1]  # The last line with coverage 0
            if current_line[1] == end_line[1]:  # Check if the start is equal to the end
                pass
            else:  # If the start is not equal to the end, create a new entry in the dictionary
                count_id = count_id + 1
                id_string = 'ID=other-' + str(count_id)  # Create the corresponding ID
                # Add information for the new entry to the dictionary
                D[id_string] = [current_line[0], 'annotateOthers', 'others', int(current_line[1]), int(end_line[1]), '.', '.', '0', id_string]
        else:  # If coverage is not 0, move to the next line
            i = i + 1
            if i > df.shape[0] - 1:
                break

    # Create a new dataframe from the filled dictionary
    annotated_DF = pd.DataFrame.from_dict(D, orient='index')

    # Save the new dataframe as an output file with tab delimiter (\t) or BED9 format
    # The dataframe index is not included in the output file
    if output_format.lower() == "bed9":
        annotated_DF.to_csv(output_file, index=False, sep='\t', header=False)
    else:
        annotated_DF.to_csv(output_file, index=False, sep='\t')

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Annotate regions with zero coverage as 'others'")
    parser.add_argument("-i", "--input", help="Input TSV file", required=True)
    parser.add_argument("-o", "--output", help="Output file", required=True)
    parser.add_argument("-f", "--format", help="Output format (default is TSV, supports 'tsv' or 'bed9')", default="tsv")
    args = parser.parse_args()

    # Call the annotate_others function with the provided input and output file paths
    annotate_others(args.input, args.output, args.format)
