import os
from convert_csv_to_env import load_lastpass_creds

# Load credentials
if load_lastpass_creds():
    # Access credentials as environment variables
    some_service_username = os.getenv('SOME_SERVICE_USERNAME')
    some_service_password = os.getenv('SOME_SERVICE_PASSWORD')
    
    # Use credentials in your automation
    # ... 