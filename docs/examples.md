# Exemples d'Utilisation

## 1. Lister et Répondre aux Emails Récents

```python
# Initialisation
agent_deps = setup_dependencies()

# Liste des 2 derniers emails
list_result = await gmail_agent.run("List my 2 most recent emails", deps=agent_deps)

# Extraire et lire le premier email
id_match = re.search(r'ID: ([a-f0-9]+)', list_result.data)
if id_match:
    email_id = id_match.group(1)
    read_result = await gmail_agent.run(f"Read the email with ID '{email_id}'", deps=agent_deps)
```

## 2. Envoi d'un Nouvel Email

```python
# Envoi simple
send_prompt = "Send an email to 'recipient@example.com' with the subject 'Hello' and the body 'Test message'"
send_result = await gmail_agent.run(send_prompt, deps=agent_deps)
```

## 3. Workflow Complet
```python
async def process_emails():
    # 1. Liste des emails
    list_result = await gmail_agent.run("List my 3 most recent emails", deps=agent_deps)
    
    # 2. Lecture du premier email
    id_match = re.search(r'ID: ([a-f0-9]+)', list_result.data)
    if id_match:
        email_id = id_match.group(1)
        read_result = await gmail_agent.run(f"Read the email with ID '{email_id}'", deps=agent_deps)
        
        # 3. Réponse automatique
        if "urgent" in read_result.data.lower():
            sender = extract_sender(read_result.data)
            subject = extract_subject(read_result.data)
            send_prompt = f"Send an email to '{sender}' with the subject 'Re: {subject}' and the body 'Message reçu, je traite cela en urgence.'"
            await gmail_agent.run(send_prompt, deps=agent_deps)
```
