# Gestion d’un Tournoi d’Échecs – Projet Python (OpenClassrooms)

Ce projet est une application développée en Python permettant de gérer un tournoi d’échecs en ligne de commande.  
Elle fonctionne **entièrement hors ligne**, conformément aux exigences du projet.

L’application permet de :
- créer un tournoi et jouer tous les rounds ;
- reprendre un tournoi existant à partir de son état sauvegardé ;
- générer différents rapports (joueurs, tournois, rounds, matchs).

Le projet respecte une architecture **MVC** afin de séparer clairement :
- les affichages (**views**) ;
- les données (**models**) ;
- la logique métier (**controllers**).

---

## Prérequis

Avant d'utiliser le programme, vous devez disposer de :

- **Python 3.10 ou version supérieure** ;
- Un environnement virtuel recommandé (`venv`) ;
- `pip` pour installer les dépendances ;
- Les outils de qualité de code (pour le rapport flake8) :
  - `flake8`
  - `flake8-html`

---

## Structure du projet

Depuis le dossier `CODE/` :

```text
CODE/
 ├── controllers/               # Logique métier : création/reprise de tournoi, matchs, rapports…
 │    ├── controller.py
 │    ├── controller_match.py
 │    ├── controller_round.py
 │    ├── controller_tournament.py
 │    ├── creation_tournoi.py        # Création d’un nouveau tournoi
 │    ├── reprise_tournoi.py         # Reprise d’un tournoi existant
 │    ├── generer_rapport.py         # Génération des rapports
 │    └── …
 ├── models/                    # Classes Player, Match, Round, Tournament
 │    ├── model.py
 │    ├── model_match.py
 │    ├── model_round.py
 │    ├── model_tournament.py
 │    └── …
 ├── views/                     # Affichage et saisies utilisateur (menus, messages…)
 │    ├── view.py               # Menu principal
 │    ├── view_creation_tournoi.py
 │    ├── view_reprise_tournoi.py
 │    ├── view_report.py
 │    └── …
 ├── flake-report/              # Rapport HTML généré par flake8-html (sans erreur)
 ├── data_base_players.json     # Base de données des joueurs
 ├── data_base_tournament.json  # Base de données des tournois
 ├── main.py                    # Point d’entrée de l’application
 ├── .flake8                    # Configuration flake8
 ├── .gitignore                 # Fichiers ignorés par Git
 └── venv/                      # Environnement virtuel (local, non nécessaire sur GitHub)
```

> Les fichiers `data_base_players.json` et `data_base_tournament.json` sont **remplis automatiquement** par le programme au fur et à mesure de l’utilisation.  
> S’ils sont vides au départ, ce n’est pas un problème.

---

## Lancer le programme

Depuis la racine du projet (`CODE/`), exécuter :

```bash
python main.py
```

Le programme affiche alors le menu principal :

```text
1 - Créer un tournoi
2 - Reprendre un tournoi
3 - Générer un rapport
```

### Exemple d’utilisation simple

- **Créer un tournoi**  
  1. Choisir `1 - Créer un tournoi`.  
  2. Saisir les informations du tournoi (nom, lieu, dates…).  
  3. Indiquer le nombre de joueurs (pair et ≥ 2).  
  4. Créer les joueurs un par un.  
  5. Lancer les rounds, choisir les vainqueurs ou les matchs nuls, suivre l’affichage du classement.

- **Reprendre un tournoi**  
  1. Choisir `2 - Reprendre un tournoi`.  
  2. Saisir le nom d’un tournoi déjà enregistré.  
  3. Le programme reconstruit les rounds et propose de continuer les matchs restants jusqu’à la fin du tournoi.

- **Générer un rapport**  
  1. Choisir `3 - Générer un rapport`.  
  2. Un sous-menu de rapports s’affiche (joueurs, tournois, rounds/matchs d’un tournoi, etc.).  
  3. Suivre les instructions pour afficher les informations souhaitées.

Toutes les interactions se font en ligne de commande, par saisie de numéros et de textes.

---

## 🔧 Générer un rapport flake8-html

Le projet inclut un dossier **flake-report/** généré avec flake8-html.  
Il doit contenir un rapport **sans aucune erreur** de peluchage.

Pour générer ou régénérer un rapport flake8-html à partir de la racine du projet (`CODE/`) :

```bash
flake8 --format=html --htmldir=flake-report
```

Si des erreurs sont détectées, corriger le code puis relancer la commande jusqu’à ce que le rapport indique 0 erreur.

---

## 📦 Dépendances

Les principales dépendances sont :

- Python 3.x
- flake8
- flake8-html
- tinydb

Un fichier `requirements.txt` est fourni, les installer avec :

```bash
pip install -r requirements.txt
```

Sinon, installation minimale :

```bash
pip install flake8 flake8-html tinydb
```

---

## 🎯 Objectif pédagogique

- Mettre en place et utiliser une architecture logicielle **MVC** ;
- Manipuler des classes Python (joueurs, matchs, rounds, tournois) ;
- Gérer des entrées utilisateur en ligne de commande ;
- Structurer un projet logiciel complet et maintenable ;
- Respecter **PEP 8** et vérifier le code avec **flake8** et **flake8-html**.

