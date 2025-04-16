# Import standard libraries
from dataclasses import dataclass
from typing import List, Union
import os
import json

# Import third-party libraries
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

# Import local modules
from .gmail_auth import authenticate_gmail
from .gmail_service import GmailService

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Models
class EmailInfo(BaseModel):
    """Email information model"""
    id: str
    subject: str = "[No Subject]"
    sender: str = "[No Sender]"
    snippet: str = ""

@dataclass
class GmailAgentDependencies:
    """Dependencies for Gmail agent tools"""
    gmail_client: GmailService
    user_email: str

# Agent setup
def setup_dependencies() -> GmailAgentDependencies:
    """Initialize Gmail client and authentication"""
    credentials = authenticate_gmail()
    gmail_service = GmailService(credentials=credentials)
    user_email = gmail_service.get_user_email()
    return GmailAgentDependencies(
        gmail_client=gmail_service,
        user_email=user_email
    )

# Initialize Gemini provider and model
gemini_provider = GoogleGLAProvider(api_key=GEMINI_API_KEY)
gemini_model = GeminiModel('gemini-2.0-flash', provider=gemini_provider)

# Initialize the Agent with simple data handling
gmail_agent = Agent(
    model=gemini_model,
    deps_type=GmailAgentDependencies,
    system_prompt=(
        "You are a Gmail assistant. Return email information in a clear format."
    ),
    result_type=str  # Simplifié à str pour éviter les problèmes de schéma
)

@gmail_agent.tool
async def list_emails(ctx: RunContext[GmailAgentDependencies], count: int = 10, subject: str = None, sender: str = None) -> str:
    """Lists the most recent emails from the inbox."""
    try:
        print(f"Fetching {count} recent emails...")
        emails_data = await ctx.deps.gmail_client.list_recent_emails(max_results=count)
        if not emails_data:
            return "[]"  # Retourne une liste JSON vide

        # Apply filters
        filtered_emails = emails_data
        if subject:
            filtered_emails = [email for email in filtered_emails if subject.lower() in email.get('subject', '').lower()]
        if sender:
            filtered_emails = [email for email in filtered_emails if sender.lower() in email.get('from', '').lower()]

        # Formater la réponse en liste JSON de dictionnaires
        formatted_emails = []
        for email in filtered_emails:
            formatted_emails.append({
                'id': email.get('id'),
                'subject': email.get('subject'),
                'from': email.get('from'),
                'snippet': email.get('snippet') # Include snippet
            })

        return json.dumps(formatted_emails)  # Retourne une chaîne JSON

    except Exception as e:
        print(f"Error in list_emails: {str(e)}")
        return f"Error: {e}"

@gmail_agent.tool
async def read_mail_by_id(ctx: RunContext[GmailAgentDependencies], mail_id: str) -> str:
    """Gets the full content of a specific email by its ID and extracts sender and subject."""
    try:
        email_data = await ctx.deps.gmail_client.get_email(mail_id)
        if 'error' in email_data:
            print(f"Error reading email: {email_data['error']}")
            return f"Error: {email_data['error']}"

        # Extract sender, subject, and body
        sender = email_data.get('from', '[No Sender]')
        subject = email_data.get('subject', '[No Subject]')
        body = email_data.get('body', '[No Content]')
        snippet = email_data.get('snippet', '[No Snippet]')

        # Return the email details in the original language
        return f"Subject: {subject}\nFrom: {sender}\nSnippet: {snippet}\nBody: {body}"

    except Exception as e:
        print(f"Error reading email {mail_id}: {str(e)}")
        return f"Error: {e}"

@gmail_agent.tool
async def send_mail(
    ctx: RunContext[GmailAgentDependencies],
    to: EmailStr = None,
    subject: str = None,
    body: str = None
) -> str:
    """Send an email using the authenticated account"""
    try:
        if not to:
            return "What recipient email address should I use?"
        if not subject:
            return "What subject should I use for the email?"
        if not body:
            return "What body should I use for the email?"
        
        result = await ctx.deps.gmail_client.send_email(
            sender=ctx.deps.user_email,
            recipient=to,
            subject=subject,
            body=body
        )
        if result.get('status') == 'success':
            return f"Message sent successfully. ID: {result.get('message_id')}"
        return f"Failed to send email: {result.get('error', 'Unknown error')}"
    except Exception as e:
        return f"Error sending email: {e}"

@gmail_agent.tool
async def search_emails_by_date(ctx: RunContext[GmailAgentDependencies], date: str) -> str:
    """Searches for emails received on a specific date (YYYY-MM-DD)."""
    try:
        print(f"Searching for emails received on {date}...")
        query = f"date:{date}"
        results = ctx.deps.gmail_client.service().users().messages().list(
            userId='me', q=query, maxResults=10  # Adjust maxResults as needed
        ).execute()
        messages = results.get('messages', [])

        if not messages:
            return f"No emails found on {date}."

        email_list = []
        for msg in messages:
            msg_data = ctx.deps.gmail_client.service().users().messages().get(
                userId='me', id=msg['id'], format='metadata',
                metadataHeaders=['Subject', 'From']
            ).execute()
            headers = msg_data.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '[No Subject]')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), '[No Sender]')
            email_list.append(f"ID: {msg_data['id']}, Subject: {subject}, From: {sender}")

        return f"Emails received on {date}:\n" + "\n".join(email_list)

    except Exception as e:
        print(f"Error in search_emails_by_date: {e}")
        return f"Error: {e}"