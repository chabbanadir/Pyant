# Fonctionnalités Principales

## 1. Liste des Emails
L'agent peut lister les emails récents de votre boîte de réception.

### Utilisation
```python
# Liste les 5 derniers emails
list_result = await gmail_agent.run("List my 5 most recent emails", deps=agent_deps)
```

### Informations retournées
- ID de l'email
- Expéditeur
- Sujet
- Aperçu du contenu
- ID du thread

## 2. Lecture d'Email
Permet de lire le contenu complet d'un email spécifique.

### Utilisation
```python
# Lecture d'un email avec son ID
read_result = await gmail_agent.run(f"Read the email with ID 'email_id'", deps=agent_deps)
```

### Informations retournées
- Expéditeur complet
- Destinataire
- Date
- Sujet
- Corps du message
- Pièces jointes (si présentes)

## 3. Envoi d'Email
Permet d'envoyer de nouveaux emails ou de répondre à des emails existants.

### Utilisation
```python
# Envoi d'un nouvel email
send_prompt = f"Send an email to 'recipient@example.com' with the subject 'Test' and the body 'Hello'"
send_result = await gmail_agent.run(send_prompt, deps=agent_deps)
```

### Fonctionnalités
- Envoi d'emails simples
- Réponses automatiques
- Support des sujets avec préfixe "Re:"
- Confirmation de l'envoi avec ID du message
