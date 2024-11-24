# Create and activate virtual environment using uv
uv venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -r requirements.txt

# Run the conversion script
python convert_csv_to_env.py

# Deactivate virtual environment
deactivate 