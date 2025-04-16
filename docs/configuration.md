# Configuration de l'Agent Gmail

## Prérequis
- Python 3.8 ou supérieur
- Un compte Google avec Gmail
- Les identifiants OAuth2 de Google Cloud Platform

## Configuration initiale

### 1. Configuration des credentials Google

1. Créez un projet sur Google Cloud Platform
2. Activez l'API Gmail
3. Créez des identifiants OAuth2
4. Téléchargez le fichier credentials.json
5. Placez credentials.json dans le dossier `credentials/`

### 2. Variables d'environnement

Créez un fichier `.env` à la racine du projet avec :
```
GEMINI_API_KEY=votre_clé_api_gemini
```

### 3. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 4. Premier lancement

Lors du premier lancement, le script ouvrira automatiquement une fenêtre de navigateur pour l'authentification OAuth2. Une fois autorisé, un fichier token.json sera créé dans le dossier credentials/.
