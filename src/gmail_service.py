import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

class GmailService:
    """Service wrapper for Gmail API operations"""

    def __init__(self, credentials: Credentials):
        """Initialize the Gmail service with authorized credentials"""
        if not credentials or not credentials.valid:
            raise ValueError("Invalid or missing credentials")
        self.service = build('gmail', 'v1', credentials=credentials)
        self.user_id = 'me'

    def get_user_email(self) -> str:
        """Get authenticated user's email address"""
        try:
            profile = self.service.users().getProfile(userId=self.user_id).execute()
            return profile.get('emailAddress', '')
        except HttpError as e:
            print(f"Error getting user profile: {e}")
            return ""

    async def list_recent_emails(self, max_results=10) -> list[dict]:
        """List recent emails from inbox"""
        try:
            # Get message list
            results = self.service.users().messages().list(
                userId=self.user_id,
                labelIds=['INBOX'],
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            if not messages:
                return []

            # Get details for each message
            email_list = []
            for msg in messages:
                msg_data = self.service.users().messages().get(
                    userId=self.user_id,
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['Subject', 'From']
                ).execute()

                # Extract headers
                headers = msg_data.get('payload', {}).get('headers', [])
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '[No Subject]')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), '[No Sender]')

                email_list.append({
                    'id': msg_data['id'],
                    'threadId': msg_data.get('threadId'),
                    'subject': subject,
                    'from': sender,
                    'snippet': msg_data.get('snippet', '')
                })

            return email_list

        except HttpError as e:
            print(f"Error listing emails: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    async def get_email(self, mail_id: str) -> dict:
        """Get full content of a specific email"""
        try:
            message = self.service.users().messages().get(
                userId=self.user_id,
                id=mail_id,
                format='full'
            ).execute()

            # Extract headers and content
            payload = message.get('payload', {})
            headers = payload.get('headers', [])
            
            email_data = {
                'id': message['id'],
                'threadId': message.get('threadId'),
                'snippet': message.get('snippet'),
                'subject': '',
                'from': '',
                'to': '',
                'date': '',
                'body': ''
            }

            # Process headers
            for header in headers:
                name = header.get('name', '').lower()
                value = header.get('value', '')
                if name in ['subject', 'from', 'to', 'date']:
                    email_data[name] = value

            # Extract body
            if payload.get('parts'):
                part = self._find_part_by_mimetype(payload['parts'], 'text/plain')
                if not part:
                    part = self._find_part_by_mimetype(payload['parts'], 'text/html')
                
                if part and part.get('body', {}).get('data'):
                    email_data['body'] = base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8')
            elif payload.get('body', {}).get('data'):
                email_data['body'] = base64.urlsafe_b64decode(
                    payload['body']['data']
                ).decode('utf-8')

            # Use snippet if body extraction failed
            if not email_data['body']:
                email_data['body'] = email_data['snippet']

            return email_data

        except HttpError as e:
            print(f"Error reading email {mail_id}: {e}")
            return {'error': str(e), 'id': mail_id}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {'error': str(e), 'id': mail_id}

    async def send_email(self, sender: str, recipient: str, subject: str, body: str) -> dict:
        """Send an email"""
        try:
            message = MIMEText(body)
            message['to'] = recipient
            message['from'] = sender
            message['subject'] = subject

            encoded_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('utf-8')

            sent_message = self.service.users().messages().send(
                userId=self.user_id,
                body={'raw': encoded_message}
            ).execute()

            return {
                'status': 'success',
                'message_id': sent_message['id']
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _find_part_by_mimetype(self, parts: list, mimetype: str) -> dict:
        """Recursively search message parts for specific MIME type"""
        for part in parts:
            if part.get('mimeType') == mimetype:
                return part
            if part.get('parts'):
                found = self._find_part_by_mimetype(part['parts'], mimetype)
                if found:
                    return found
        return {}
