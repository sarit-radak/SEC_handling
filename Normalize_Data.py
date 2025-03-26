import pandas as pd
import glob

# Folder path containing the Excel files
folder_path = '/Users/sradak/'

# Initialize separate dictionaries for A280 and A214 data
data_280 = {}

# Loop through all Excel files in the folder
for file in glob.glob(f"{folder_path}/*.xlsx"):
    # Read the Excel file
    df = pd.read_excel(file)

    # Extract the filename without the path and extension
    file_name = file.split('/')[-1].split('.')[0]

    # Extract A280 columns and drop rows where either value is missing
    df_280 = df.iloc[1:, [0, 1]].dropna()
    df_280.columns = ['ml', 'mAU']

    # Save extracted data into dictionaries
    data_280[file_name] = df_280

# Merge all A280 data
merged_280 = None
for file_name, df in data_280.items():
    if merged_280 is None:
        merged_280 = df.rename(columns={'mAU': f'mAU_{file_name}'})
    else:
        merged_280 = pd.merge(
            merged_280,
            df.rename(columns={'mAU': f'mAU_{file_name}'}),
            on='ml',
            how='outer'
        )

# Sort merged DataFrames by 'ml'
merged_280['ml'] = pd.to_numeric(merged_280['ml'], errors='coerce')
merged_280 = merged_280.sort_values(by='ml')

# Save the merged data to Excel files
merged_280.to_excel(f"{folder_path}/merged_280.xlsx", index=False)
