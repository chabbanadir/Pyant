import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']
TOKEN_PATH = 'credentials/token.json'
CREDENTIALS_PATH = 'credentials/credentials.json'

def authenticate_gmail():
    """Handles Gmail API authentication using OAuth2.

    Checks for existing token, refreshes if necessary, or runs the
    OAuth2 flow to get new credentials.

    Returns:
        google.oauth2.credentials.Credentials: The authorized credentials.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatiy when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except json.JSONDecodeError:
            print(f"Error reading {TOKEN_PATH}. Starting OAuth flow.")
            creds = None
        except ValueError as e:
            print(f"Error loading credentials from {TOKEN_PATH}: {e}. Starting OAuth flow.")
            creds = None


    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing access token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"Failed to refresh token: {e}. Starting new OAuth flow.")
                # If refresh fails, force re-authentication
                if os.path.exists(TOKEN_PATH):
                    os.remove(TOKEN_PATH)
                creds = None # Ensure we run the flow below
        else:
             # Only run the flow if creds are truly missing or unrefreshable
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"Credentials file not found at {CREDENTIALS_PATH}. "
                    "Please download it from Google Cloud Console and place it there."
                )
            print("No valid credentials found or token expired. Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            # Specify a fixed port or let it choose dynamically
            # Using port 0 lets the system choose an available port
            # Using a fixed port like 8080 requires registering http://localhost:8080/ in Google Cloud Console
            fixed_port = 8080
            print(f"Starting local server for OAuth flow on port {fixed_port}...")
            creds = flow.run_local_server(port=fixed_port)

        # Save the credentials for the next run
        if creds:
            print(f"Saving credentials to {TOKEN_PATH}")
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        else:
             print("Failed to obtain credentials.")


    if not creds or not creds.valid:
         raise Exception("Failed to obtain valid Gmail credentials.")

    print("Authentication successful.")
    return creds

if __name__ == '__main__':
    # Example of how to use it:
    try:
        credentials = authenticate_gmail()
        print("Credentials obtained successfully.")
        # You can now use these credentials to build the Gmail service
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
