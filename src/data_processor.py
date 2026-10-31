import pandas as pd
import os

def process_onet_data(data_directory: str, occupation_filename: str, unified_file_names: list[str]) -> pd.DataFrame:
    """
    Reads O*NET data from various files within a specified directory and merges them into a single DataFrame.

    This function first reads the occupation titles. Then, for each specified
    unified format file, it extracts element-specific data (ID, Name, Importance,
    Level, N) and dynamically creates new columns for each element associated
    with an O*NET-SOC Code. Finally, it merges all this data into a single
    comprehensive DataFrame.

    Args:
        data_directory (str): The path to the directory where all the O*NET .txt files are located.
        occupation_filename (str): The filename of the "Occupation Data.txt" file (e.g., "Occupation Data.txt").
        unified_file_names (list[str]): A list of base filenames (e.g., "Skills",
                                        "Work Activities") for files that are in
                                        the "unified format". The script will
                                        append ".txt" to these names.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the merged occupation and
                      unified format data. Returns an empty DataFrame if
                      the initial occupation data file cannot be read.
    """

    # Construct the full path for the occupation data file
    occupation_filepath = os.path.join(data_directory, occupation_filename)

    # 1. Read Occupation Data
    try:
        # Read only the necessary columns: "O*NET-SOC Code" and "Title"
        occupation_df = pd.read_csv(
            occupation_filepath,
            sep='\t',  # Data is tab-separated
            usecols=["O*NET-SOC Code", "Title"],
            encoding='utf-8' # O*NET files are typically UTF-8 encoded
        )
        print(f"Successfully loaded occupation data from '{occupation_filepath}'.")
    except FileNotFoundError:
        print(f"Error: Occupation Data file not found at '{occupation_filepath}'. Please ensure the file exists.")
        return pd.DataFrame() # Return an empty DataFrame on error
    except Exception as e:
        print(f"Error reading '{occupation_filepath}': {e}")
        return pd.DataFrame()

    # Initialize the final DataFrame with the occupation data.
    # This DataFrame will be progressively merged with data from unified files.
    final_df = occupation_df.copy()

    # 2. Process Unified Format Files
    for file_name_base in unified_file_names:
        # Construct the full path for the current unified file
        unified_filepath = os.path.join(data_directory, f"{file_name_base}.txt")
        print(f"Attempting to process unified format file: '{unified_filepath}'...")

        try:
            unified_df = pd.read_csv(
                unified_filepath,
                sep='\t',
                encoding='utf-8'
            )
            print(f"Successfully loaded unified data from '{unified_filepath}'.")
        except FileNotFoundError:
            print(f"Warning: Unified format file not found at '{unified_filepath}'. Skipping this file.")
            continue # Skip to the next file if this one is not found
        except Exception as e:
            print(f"Error reading '{unified_filepath}': {e}. Skipping this file.")
            continue

        # Filter the unified DataFrame to include only the columns necessary for processing.
        # This improves performance and clarity.
        unified_df_relevant = unified_df[[
            "O*NET-SOC Code", "Element ID", "Element Name", "Scale ID", "Data Value", "N"
        ]].copy()

        # List to store processed rows for the current unified file.
        # Each dictionary in this list will represent a row for a specific O*NET-SOC Code.
        processed_rows_for_current_file = []

        # Iterate through each unique O*NET-SOC Code found in the initial
        # occupation data. This ensures that our final DataFrame contains
        # all occupations, even if they don't have entries in a specific unified file.
        for soc_code in occupation_df["O*NET-SOC Code"].unique():
            # Filter data for the current O*NET-SOC Code from the unified file
            soc_data = unified_df_relevant[unified_df_relevant["O*NET-SOC Code"] == soc_code]

            # If no data exists for this SOC code in the current unified file,
            # append a basic row with just the SOC code to maintain its presence
            # in the merged DataFrame. Other columns will be NaN.
            if soc_data.empty:
                processed_rows_for_current_file.append({"O*NET-SOC Code": soc_code})
                continue

            # Group the filtered data by "Element ID". This is crucial because
            # "Importance" (IM) and "Level" (LV) values are provided for the same
            # "Element ID" in separate rows.
            grouped_by_element = soc_data.groupby("Element ID")

            # Initialize a dictionary to build the row for the current SOC code.
            # It starts with the O*NET-SOC Code itself.
            current_soc_row = {"O*NET-SOC Code": soc_code}
            element_counter = 1 # Counter for dynamic column naming (e.g., "Skill 1", "Skill 2")

            # Iterate through each unique Element ID found for the current SOC code.
            for element_id, element_group in grouped_by_element:
                # Element Name and N value are generally consistent across 'IM' and 'LV' scales
                element_name = element_group["Element Name"].iloc[0]
                n_value = element_group["N"].iloc[0]

                # Extract Importance (IM) and Level (LV) values.
                # Use .iloc[0] to get the scalar value from the filtered Series.
                # Use .empty check to handle cases where 'IM' or 'LV' might be missing.
                importance_value = element_group[element_group["Scale ID"] == "IM"]["Data Value"].iloc[0] \
                                   if not element_group[element_group["Scale ID"] == "IM"].empty else None
                level_value = element_group[element_group["Scale ID"] == "LV"]["Data Value"].iloc[0] \
                              if not element_group[element_group["Scale ID"] == "LV"].empty else None

                # Dynamically create column names based on the file's base name and element counter.
                current_soc_row[f"{file_name_base} Element ID {element_counter}"] = element_id
                current_soc_row[f"{file_name_base} Element Name {element_counter}"] = element_name
                current_soc_row[f"{file_name_base} Importance Data Value {element_counter}"] = importance_value # Changed header
                current_soc_row[f"{file_name_base} Level Data Value {element_counter}"] = level_value # Changed header
                current_soc_row[f"{file_name_base} N {element_counter}"] = n_value

                element_counter += 1 # Increment the counter for the next element

            # Add the constructed row for the current SOC code to the list
            processed_rows_for_current_file.append(current_soc_row)

        # Convert the list of dictionaries (each representing an SOC code's data
        # for the current unified file) into a DataFrame.
        # Pandas will automatically handle columns that are not present in all
        # dictionaries by filling them with NaN (Not a Number).
        current_file_processed_df = pd.DataFrame(processed_rows_for_current_file)

        # Merge the processed data from the current unified file with the
        # main final_df. A 'left' merge ensures all original occupations
        # from 'occupation_df' are retained.
        final_df = pd.merge(
            final_df,
            current_file_processed_df,
            on="O*NET-SOC Code",
            how="left"
        )
        print(f"Finished merging data from '{unified_filepath}'.")

    return final_df

# --- Example Usage ---
# IMPORTANT: Before running, ensure you have your O*NET data files in the
# specified directory.

# You can create dummy files for testing purposes by uncommenting the function call below.
# This function will create sample .txt files if they don't already exist.
# def create_dummy_files(directory="."):
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#     if not os.path.exists(os.path.join(directory, "Occupation Data.txt")):
#         with open(os.path.join(directory, "Occupation Data.txt"), "w", encoding="utf-8") as f:
#             f.write("O*NET-SOC Code\tTitle\n")
#             f.write("11-1011.00\tChief Executives\n")
#             f.write("15-1132.00\tSoftware Developers, Applications\n")
#             f.write("17-2051.00\tCivil Engineers\n") # Added for testing missing data in Skills.txt

#     if not os.path.exists(os.path.join(directory, "Skills.txt")):
#         with open(os.path.join(directory, "Skills.txt"), "w", encoding="utf-8") as f:
#             f.write("O*NET-SOC Code\tElement ID\tElement Name\tScale ID\tData Value\tN\tStandard Error\tLower CI Bound\tUpper CI Bound\tRecommend Suppress\tNot Relevant\tDate\tDomain Source\n")
#             f.write("11-1011.00\t1.A.1.a\tActive Listening\tIM\t4.5\t100\t0.1\t4.3\t4.7\tN\tN\t07/2023\tO*NET\n")
#             f.write("11-1011.00\t1.A.1.a\tActive Listening\tLV\t6.0\t100\t0.1\t5.8\t6.2\tN\tN\t07/2023\tO*NET\n")
#             f.write("11-1011.00\t1.A.1.b\tSpeaking\tIM\t4.0\t100\t0.1\t3.8\t4.2\tN\tN\t07/2023\tO*NET\n")
#             f.write("11-1011.00\t1.A.1.b\tSpeaking\tLV\t5.5\t100\t0.1\t5.3\t5.7\tN\tN\t07/2023\tO*NET\n")
#             f.write("15-1132.00\t1.A.1.c\tComplex Problem Solving\tIM\t4.8\t120\t0.1\t4.6\t5.0\tN\tN\t07/2023\tO*NET\n")
#             f.write("15-1132.00\t1.A.1.c\tComplex Problem Solving\tLV\t6.5\t120\t0.1\t6.3\t6.7\tN\tN\t07/2023\tO*NET\n")
#             f.write("15-1132.00\t1.A.1.d\tCritical Thinking\tIM\t4.7\t120\t0.1\t4.5\t4.9\tN\tN\t07/2023\tO*NET\n")
#             f.write("15-1132.00\t1.A.1.d\tCritical Thinking\tLV\t6.2\t120\t0.1\t6.0\t6.4\tN\tN\t07/2023\tO*NET\n")
#             f.write("15-1132.00\t1.A.1.e\tActive Learning\tIM\t4.2\t120\t0.1\t4.0\t4.4\tN\tN\t07/2023\tO*NET\n")
#             f.write("15-1132.00\t1.A.1.e\tActive Learning\tLV\t5.8\t120\t0.1\t5.6\t6.0\tN\tN\t07/2023\tO*NET\n")


#     if not os.path.exists(os.path.join(directory, "Work Activities.txt")):
#         with open(os.path.join(directory, "Work Activities.txt"), "w", encoding="utf-8") as f:
#             f.write("O*NET-SOC Code\tElement ID\tElement Name\tScale ID\tData Value\tN\tStandard Error\tLower CI Bound\tUpper CI Bound\tRecommend Suppress\tNot Relevant\tDate\tDomain Source\n")
#             f.write("11-1011.00\t4.A.1.a.1\tCommunicating with Supervisors, Peers, or Subordinates\tIM\t4.0\t95\t0.1\t3.8\t4.2\tN\tN\t07/2023\tO*NET\n")
#             f.write("11-1011.00\t4.A.1.a.1\tCommunicating with Supervisors, Peers, or Subordinates\tLV\t5.0\t95\t0.1\t4.8\t5.2\tN\tN\t07/2023\tO*NET\n")
#             f.write("15-1132.00\t4.A.4.a.1\tThinking Creatively\tIM\t4.3\t110\t0.1\t4.1\t4.5\tN\tN\t07/2023\tO*NET\n")
#             f.write("15-1132.00\t4.A.4.a.1\tThinking Creatively\tLV\t5.8\t110\t0.1\t5.6\t6.0\tN\tN\t07/2023\tO*NET\n")
#             f.write("17-2051.00\t4.A.2.a.1\tInterpreting the Meaning of Information for Others\tIM\t4.1\t80\t0.1\t3.9\t4.3\tN\tN\t07/2023\tO*NET\n")
#             f.write("17-2051.00\t4.A.2.a.1\tInterpreting the Meaning of Information for Others\tLV\t5.5\t80\t0.1\t5.3\t5.7\tN\tN\t07/2023\tO*NET\n")

# # Example: Create dummy files in a 'data' subdirectory
# # create_dummy_files(directory="data")

# Define the directory where your O*NET data files are located.
# Replace 'your_data_folder' with the actual path to your data.
# For example, if your files are in a folder named 'onet_data' in the same directory as the script:
# data_folder_path = "onet_data"
# If your files are in the current directory:
data_folder_path = "." # Use '.' for the current directory

occupation_data_file = "Occupation Data.txt"
unified_data_files = ["Skills", "Abilities", "Knowledge", "Work Activities"] # Add more file names (without .txt) as needed

# Call the function to process the data, passing the data_folder_path
processed_onet_data = process_onet_data(data_folder_path, occupation_data_file, unified_data_files)

# Display the first few rows of the processed data to verify
if not processed_onet_data.empty:
    print("\n--- Processed O*NET Data (First 5 Rows) ---")
    print(processed_onet_data.head().to_string())

    # Optional: Display info about the DataFrame to see columns and non-null counts
    print("\n--- Processed O*NET Data Info ---")
    processed_onet_data.info()

    # Export the result to a CSV file for further analysis
    output_csv_filename = "processed_onet_data.csv"
    processed_onet_data.to_csv(output_csv_filename, index=False, encoding='utf-8')
    print(f"\nProcessed data saved to '{output_csv_filename}'")
else:
    print("\nNo data was processed. Please check file paths and content.")
