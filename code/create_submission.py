import os
import zipfile

def create_submission():
    # List of files to include in the submission
    files_to_include = [
        'Robot.py',
        'sample_path.py',
        'calculated_path.csv',
        'ground_truth_path.csv',
        'sample_path_plot.png'  # Assuming the student saved their plot with this name
    ]

    # Prompt for Andrew ID and name the zip file accordingly
    andrew_id = input("Enter your andrew ID: ").strip()
    zip_filename = f"{andrew_id}_hw3.zip"

    # Create a zip file
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file} to the submission zip.")
            else:
                print(f"Warning: {file} not found and not included in the submission.")

    print(f"\nSubmission zip created: {zip_filename}")
    print("Please upload this file to Gradescope.")

if __name__ == "__main__":
    create_submission()