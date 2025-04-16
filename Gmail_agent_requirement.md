# Creating a PydanticAI Agent for Gmail

This document outlines the basic steps to create a PydanticAI agent designed to interact with Gmail, including defining tools to read and send emails.

## 1. Define Agent Dependencies (Optional but Recommended)

If your tools need access to things like API clients or authentication details, define a class (often a `dataclass`) to hold them.

**Authentication Handling:**
*   Before initializing the `GmailClient`, your application should implement logic to handle authentication.
*   **Check for Existing Token:** Look for a stored, valid access token (e.g., in a file, environment variable, or secure storage).
*   **OAuth2 Flow:** If no valid token exists, initiate the OAuth2 authorization flow to obtain user consent and generate a new access token and potentially a refresh token.
*   **Store Token:** Securely store the obtained token(s) for future use.
*   The authenticated client or the access token itself should be part of the dependencies passed to the agent.

```python
from dataclasses import dataclass
# Hypothetical Gmail service client and auth function
from your_gmail_library import GmailClient, authenticate_gmail

@dataclass
class GmailAgentDependencies:
    gmail_client: GmailClient # This client should be pre-authenticated
    user_email: str

# Example (outside the agent definition):
def setup_dependencies():
    # 1. Check for existing token or run OAuth2 flow
    credentials = authenticate_gmail() # This function handles token check/OAuth2
    # 2. Initialize client with credentials
    gmail_client = GmailClient(credentials=credentials)
    user_email = gmail_client.get_user_email() # Get user's email via client
    return GmailAgentDependencies(gmail_client=gmail_client, user_email=user_email)

# deps = setup_dependencies() # Call this before running the agent
```

## 2. Initialize the Agent

Create an instance of the `Agent` class. Specify:
*   A language model (e.g., 'openai:gpt-4o').
*   The `result_type` (what kind of final output you expect, e.g., `str` for a summary, or a custom Pydantic model).
*   The `deps_type` if you defined dependencies in step 1.
*   A `system_prompt` to instruct the agent on its role (e.g., "You are a helpful Gmail assistant.").

```python
from pydantic_ai import Agent

gmail_agent = Agent(
    'openai:gpt-4o', # Or any other supported model
    deps_type=GmailAgentDependencies,
    system_prompt="You are a helpful Gmail assistant. Use the provided tools to read and send emails when requested."
    # result_type=str # Or a more specific model if needed
)
```

## 3. Define Tools

Tools are functions the agent can call. Use the `@gmail_agent.tool` decorator if the tool needs dependencies, or `@gmail_agent.tool_plain` if it doesn't.

### Tool 1: Read Email by ID

This tool allows the agent to fetch the content of a specific email.

```python
from pydantic_ai import RunContext

@gmail_agent.tool
async def read_mail_by_id(ctx: RunContext[GmailAgentDependencies], mail_id: str) -> str:
    """
    Reads the content of a specific email using its unique ID.

    Args:
        mail_id: The unique identifier of the email to read.
    """
    # The gmail_client in ctx.deps is already authenticated
    email_content = await ctx.deps.gmail_client.get_email(mail_id)
    # Process content if needed (e.g., extract body)
    return f"Content of email {mail_id}: {email_content['body']}" # Simplified example
```
*   **Explanation:** The agent uses this tool when asked to retrieve information from a specific email. It needs the `mail_id` to know which email to fetch. The function uses the **authenticated** `gmail_client` (provided via dependencies) to interact with the actual Gmail API. It returns the email's content as a string.

### Tool 2: Send Email

This tool allows the agent to compose and send an email.

```python
from pydantic import EmailStr

@gmail_agent.tool
async def send_mail(ctx: RunContext[GmailAgentDependencies], to: EmailStr, subject: str, body: str) -> str:
    """
    Sends an email to the specified recipient with the given subject and body.

    Args:
        to: The email address of the recipient.
        subject: The subject line of the email.
        body: The main content/message of the email.
    """
    # The gmail_client in ctx.deps is already authenticated
    send_status = await ctx.deps.gmail_client.send(
        sender=ctx.deps.user_email,
        recipient=to,
        subject=subject,
        body=body
    )
    return f"Email sent to {to} with subject '{subject}'. Status: {send_status}" # Simplified example
```
*   **Explanation:** The agent uses this tool when asked to send an email. It needs the recipient's address (`to`), the `subject`, and the `body` of the message. It uses the **authenticated** `gmail_client` to handle the actual sending process via the Gmail API. It returns a confirmation message.

## 4. Run the Agent

Use the agent's `run` or `run_sync` method, providing the user's request and the **pre-configured, authenticated dependencies**.

```python
import asyncio
# Assume setup_dependencies() is defined as above and handles auth
deps = setup_dependencies()

async def main():
    # Example: Ask agent to read a specific email
    result_read = await gmail_agent.run("Read the email with ID '123xyz'", deps=deps)
    print(result_read.data)

    # Example: Ask agent to send an email
    result_send = await gmail_agent.run(
        "Send an email to example@test.com with subject 'Meeting Follow-up' and body 'Hi, just following up on our meeting.'",
        deps=deps
    )
    print(result_send.data)

# asyncio.run(main()) # Uncomment to run
```

This structure provides a foundation for building a PydanticAI agent capable of interacting with Gmail using defined tools. Remember to replace placeholder code like `your_gmail_library` and `GmailClient` with actual implementations for interacting with the Gmail API (e.g., using Google's official client libraries) and handling OAuth2 authentication.
