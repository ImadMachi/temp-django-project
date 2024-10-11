# Guide d'Installation du Projet BlueEye

## Aperçu de la Structure du Projet

```
BLUESKY_PROJECT/
├── agents/                  # Scripts d'agents personnalisés
├── bluesky_core/            # Répertoire principal du projet Django
├── financial_data/          # Application Django pour les données financières
├── frontend/                # Application frontend React
│   ├── src/
│   │   ├── components/
│   │   │   ├── Charts.js
│   │   │   └── FinancialTableSimulation.jsx
│   │   └── ...
│   ├── package.json
│   └── ...
├── venv/                    # Environnement virtuel Python
├── .gitignore
├── manage.py                # Script de gestion Django
├── requirements.txt         # Dépendances Python
└── ...
```

## Installation du Backend (Django)

1. Clonez le dépôt ou assurez-vous d'avoir les fichiers du projet :

   ```bash
   git clone <url_du_dépôt>
   cd BLUESKY_PROJECT
   ```

2. Créez et activez un environnement virtuel :

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Installez les dépendances Python :

   ```bash
   pip install -r requirements.txt
   ```

4. Créez un fichier `.env` à la racine du projet :

   ```
   GOOGLE_API_KEY=votre_clé_secrète_ici
   ```

5. Mettez à jour `bluesky_core/settings.py` si nécessaire :

   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.mysql",
           "NAME": "bluesky",
           "USER": "root",
           "PASSWORD": "",
           "HOST": "localhost",
           "PORT": "3306",
       }
   }
   ```

6. Démarrez le serveur de développement Django :
   ```bash
   python manage.py runserver
   ```

## Installation du Frontend (React)

1. Naviguez vers le répertoire frontend :

   ```bash
   cd frontend
   ```

2. Installez les dépendances Node.js :

   ```bash
   npm install
   ```

3. Installez les dépendances spécifiques :

   ```bash
   npm install chartjs-adapter-date-fns date-fns @ant-design/icons antd axios
   ```

4. Démarrez le serveur de développement React :
   ```bash
   npm start
   ```

## Configuration Supplémentaire

1. **CORS** : Assurez-vous que le fichier `settings.py` de Django est configuré pour autoriser les requêtes du frontend.
2. **Fichiers statiques** : Exécutez `python manage.py collectstatic` si vous déployez en production.

## Exécution du Projet

1. Démarrez le backend Django :

   ```bash
   python manage.py runserver
   ```

2. Dans un nouveau terminal, démarrez le frontend React :
   ```bash
   cd frontend
   npm start
   ```

## Dépannage

- Pour les problèmes MySQL : Vérifiez l'état du serveur et les identifiants dans `settings.py`.
- Pour les packages manquants : Réexécutez `pip install -r requirements.txt` ou `npm install`.
- Pour les problèmes de cache npm : Exécutez `npm cache clean --force`.
- Vérifiez les sorties de console des deux serveurs pour identifier les erreurs éventuelles.
