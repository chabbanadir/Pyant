# Guide de Dépannage

## Problèmes Courants et Solutions

### 1. Problèmes d'Authentification

#### Erreur : "Invalid Credentials"
- Vérifiez que le fichier `credentials.json` est présent dans le dossier `credentials/`
- Supprimez `token.json` et relancez le programme pour une nouvelle authentification
- Assurez-vous que l'API Gmail est activée dans votre projet Google Cloud

#### Erreur : "Token has expired"
- Le token sera automatiquement rafraîchi
- Si le problème persiste, supprimez `token.json` et relancez le programme

### 2. Problèmes de Liste d'Emails

#### Erreur : "No emails found"
- Vérifiez que votre boîte de réception n'est pas vide
- Vérifiez les permissions de l'application dans les paramètres Google

#### Format de réponse incorrect
- Assurez-vous que le paramètre `max_results` est un nombre positif
- Vérifiez que l'API retourne bien les données au format attendu

### 3. Problèmes d'Envoi d'Emails

#### Erreur : "Invalid recipient"
- Vérifiez le format de l'adresse email
- Assurez-vous que l'adresse existe

#### Erreur : "Rate limit exceeded"
- Respectez les limites de l'API Gmail
- Attendez quelques minutes avant de réessayer

### 4. Problèmes de l'Agent Gemini

#### Erreur : "API Key not found"
- Vérifiez que la variable d'environnement GEMINI_API_KEY est définie
- Vérifiez que la clé API est valide

#### Erreur : "Model not responding"
- Vérifiez votre connexion internet
- Réessayez la requête
- Assurez-vous que le service Gemini est disponible

### 5. Commandes de Diagnostic

```python
# Vérifier l'état de l'authentification
print(agent_deps.gmail_client.get_user_email())

# Tester la connexion à l'API Gmail
list_result = await gmail_agent.run("List my 1 most recent emails", deps=agent_deps)

# Vérifier les permissions
print(agent_deps.gmail_client.service.users().getProfile(userId='me').execute())
```

### 6. Contact et Support

Pour des problèmes plus complexes :
- Consultez la [documentation de l'API Gmail](https://developers.google.com/gmail/api)
- Vérifiez les [quotas de l'API](https://console.cloud.google.com/apis/dashboard)
- Consultez les [logs dans Google Cloud Console](https://console.cloud.google.com/logs)

## Maintenance

### Mise à jour régulière
```bash
pip install --upgrade google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Nettoyage des tokens
```bash
rm credentials/token.json  # En cas de problèmes d'authentification
```
