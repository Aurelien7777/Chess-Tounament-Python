# **Gestion d’un Tournoi d’Échecs – Projet Python (OpenClassrooms)**



Ce projet est une application développée en Python permettant de gérer un tournoi d’échecs en ligne de commande.  
Elle fonctionne **entièrement hors ligne**, conformément aux exigences du projet OpenClassrooms.  
L’objectif est de créer des joueurs, organiser les matchs et les tournois, mettre à jour les scores et sauvegarder l’état du tournoi.

Le projet respecte une architecture **MVC** afin de séparer clairement :

* les affichages (**views**) ;
* les données (**models**) ;
* la logique métier (**controllers**).

---

## 🛠️ **Prérequis**

Avant d'utiliser le programme, vous devez disposer de :

* **Python 3.10 ou version supérieure** ;
* Un environnement virtuel recommandé (`venv`) ;
* `pip` pour installer les dépendances ;
* Les outils de qualité de code suivants (pour le rapport flake8) :

  * `flake8`
  * `flake8-html`

---

## 📁 **Structure du projet**

```text
CODE/
 ├── controllers/               # Logique métier : création des joueurs, matchs, tournois, reprise, rapports…
 ├── models/                    # Classes Player, Match, Round, Tournament
 ├── views/                     # Fonctions d’affichage et récupération de saisies utilisateur
 ├── tournaments/               # Données liées aux tournois (si utilisées)
 ├── flake-report/              # Rapport HTML généré par flake8-html (sans erreur)
 ├── data\_base\_players.json     # Base de données des joueurs
 ├── data\_base\_tournament.json  # Base de données des tournois
 ├── main.py                    # Point d’entrée de l’application
 ├── .flake8                    # Configuration flake8
 ├── .gitignore                 # Fichiers ignorés par Git
 ├── README.md                  # Documentation du projet
 └── venv/                      # Environnement virtuel (local, non indispensable dans le dépôt)
```

---

## ▶️ **Lancer le programme**



Depuis la racine du projet (`CODE/`), exécuter :

```bash
python main.py
```

Le programme affiche alors le menu principal suivant :

```text
1 - Créer joueur
2 - Créer match
3 - Créer tournoi
4 - Reprendre un tournoi
5 - Générer un rapport
```



### **Exemple d’utilisation simple**



* Choisir `1 - Créer joueur` pour ajouter un nouveau joueur :  
  le programme demande le nom, le prénom, la date de naissance, etc.
* Choisir ensuite `3 - Créer tournoi` pour créer un tournoi, définir son nom, son lieu, ses dates…
* Utiliser `2 - Créer match` et/ou `4 - Reprendre un tournoi` pour gérer la suite des matchs et rounds.
* L’option `5 - Générer un rapport` permet de produire un rapport sur les données du tournoi (joueurs, classements, etc.), selon la logique implémentée dans les contrôleurs.

Toutes les interactions se font en ligne de commande, par saisie de numéros et de textes.

---

## 🔧 **Générer un rapport flake8-html**



Le projet inclut un dossier **flake-report/** généré avec flake8-html.  
Il doit contenir un rapport **sans aucune erreur** de peluchage.

Pour générer ou régénérer un rapport flake8-html à partir de la racine du projet :

```bash
flake8 --format=html --htmldir=flake-report
```

Si des erreurs sont détectées, corriger le code puis relancer la commande jusqu’à ce que le rapport indique 0 erreur.

---

## 📦 **Dépendances**

Les principales dépendances sont :

* Python 3.x
* flake8
* flake8-html

Si un fichier `requirements.txt` est fourni, les installer avec :

```bash
pip install -r requirements.txt
```

---

## 🎯 **Objectif pédagogique**

* Mettre en place et utiliser une architecture logicielle **MVC** ;
* Manipuler des classes Python (joueurs, matchs, rounds, tournois) ;
* Gérer des entrées utilisateur en ligne de commande ;
* Structurer un projet logiciel complet et maintenable ;
* Respecter **PEP 8** et vérifier le code avec **flake8** et **flake8-html**.
