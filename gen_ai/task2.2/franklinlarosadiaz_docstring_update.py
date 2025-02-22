#CS 472 
#NSHE ID: 5004634201     Franklin La Rosa Diaz
#Refactored code from ChatGPT
def get_valid_filename():
    """
    Prompts the user for a valid filename and checks if the file exists
    and is accessible. Repeatedly asks the user for a filename until
    a valid file is provided.
    
    Returns:
        str: A valid filename provided by the user.
    """
    while True:
        # Ask the user to input the file name
        fname = input("Enter the file name: \n")
        try:
            # Try to open the file to check if it exists and is accessible
            with open(fname, 'r'):
                print("File accepted. Loading...\n")
                return fname  # Return the valid filename
        except IOError:
            # Handle the error if the file cannot be accessed
            print("File not accessible. Try again.\n")

def transcribe_dna_to_rna(dna_sequence):
    """
    Converts a given DNA sequence to its RNA equivalent by replacing 
    'T' (thymine) with 'U' (uracil).

    Args:
        dna_sequence (str): A string representing a DNA sequence.
    
    Returns:
        str: A string representing the RNA sequence with 'T' replaced by 'U'.
    """
    return dna_sequence.replace('T', 'U')  # Replace 'T' with 'U'

def read_file_and_transcribe(fname):
    """
    Reads a DNA sequence file, processes each line by transcribing 
    it into RNA, and returns a list of RNA sequences.

    Args:
        fname (str): The name of the file containing the DNA sequences.
    
    Returns:
        list: A list of RNA sequences (strings), one for each line in the file.
    """
    with open(fname, 'r') as iFile:
        # Use list comprehension to read each line, strip newlines, and transcribe DNA to RNA
        return [transcribe_dna_to_rna(line.strip()) for line in iFile]

# Main Program Execution
# Step 1: Get a valid filename from the user
filename = get_valid_filename()

# Step 2: Read the file and transcribe the DNA sequences to RNA
rna_sequences = read_file_and_transcribe(filename)

# Step 3: Output the resulting RNA sequences, one per line
for rna_seq in rna_sequences:
    print(rna_seq)
