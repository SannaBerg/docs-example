from google.oauth2 import service_account
import google.auth.transport.requests

# Replace with your key filename
KEY_FILE = "exampledocumentation-a7cd2db89434.json"

# Define the required scope for the Google Analytics Data API
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

# Load credentials and refresh to get access token
credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=SCOPES
)
request = google.auth.transport.requests.Request()
credentials.refresh(request)

# Print the access token
print(credentials.token)