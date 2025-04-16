# Guide des Outils

## Structure des Outils de l'Agent

### 1. GmailService
Le service principal qui gère les interactions avec l'API Gmail.

#### Méthodes principales :
- `list_recent_emails(max_results=10)`: Liste les emails récents
- `get_email(mail_id)`: Récupère un email spécifique
- `send_email(sender, recipient, subject, body)`: Envoie un email

### 2. EmailInfo
Modèle de données pour les informations d'email.

```python
class EmailInfo:
    id: str
    subject: str
    sender: str
    snippet: str
```

### 3. GmailAgent
Agent principal utilisant l'API Gemini pour le traitement en langage naturel.

#### Commandes disponibles:
- "List my X most recent emails"
- "Read the email with ID 'xxx'"
- "Send an email to 'xxx' with subject 'xxx' and body 'xxx'"

## Architecture

```
src/
├── gmail_agent.py  # Agent principal et outils
├── gmail_auth.py   # Gestion de l'authentification
└── gmail_service.py # Services Gmail
```
