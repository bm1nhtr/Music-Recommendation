# Framework de Graphe de Connaissances

Un framework pour l'analyse et la visualisation de graphes de connaissances, avec support pour l'application d'algorithmes graphiques classiques.

## 📚 Documentation des Algorithmes

Pour une documentation complète des algorithmes implémentés, consultez **[README_ALGORITHMES.md](README_ALGORITHMES.md)**.

**Algorithmes disponibles :**
- **Parcours de graphe** : BFS, DFS
- **Arbre couvrant de poids minimum** : Prim, Kruskal
- **Plus court chemin** : Dijkstra
- **Plus courts chemins avancés** : Bellman-Ford, Floyd-Warshall

## Vue d'ensemble

Ce projet implémente un modèle de recommandation qui utilise un graphe de connaissances pour améliorer les recommandations. Le modèle propage les préférences utilisateur à travers le graphe en utilisant des mécanismes d'attention multi-hops.

## Structure du Projet

```
├── src/
│   ├── graph_loader.py      # Chargement et construction du graphe + métadonnées
│   ├── graph_visualizer.py  # Visualisation macro/micro avec légendes
│   ├── main.py              # Point d'entrée principal
│   ├── preprocess.py        # Prétraitement avec option de réduction
│   └── data_loader.py       # (Legacy - pour référence)
├── rawdata/                 # Données brutes (ignoré par git)
│   └── {dataset}/           # (ex: music)
│       ├── artists.dat
│       ├── user_artists.dat
│       └── ...
├── final_data/              # Données traitées
│   └── {dataset}/           # (ex: music)
│       ├── ratings_final.txt       # Interactions utilisateur-item
│       ├── kg_final.txt            # Graphe de connaissances
│       ├── dataset_metadata.txt    # Métadonnées (type, taille, paramètres)
│       ├── graph_macro.png         # Visualisation macro (vue d'ensemble)
│       └── graph_micro_user_X.png  # Visualisation micro (utilisateur)
└── README.md
```

## Format des Données

### Fichier Ratings (`ratings_final.txt`)
Format: `user_id \t item_id \t label`
- `label`: 1 pour interaction positive, 0 pour interaction négative

### Fichier Graphe de Connaissances (`kg_final.txt`)
Format: `head_entity \t relation \t tail_entity`
- Les entités et relations doivent être des indices entiers

## Installation

### Packages requis

- numpy >= 1.14.5
- networkx >= 2.5 (pour la visualisation)
- matplotlib >= 3.3.0 (pour la visualisation)


## Utilisation

### 1. Préparer vos données

#### Données brutes (RAW)
Placez dans `rawdata/{nom_dataset}/`:
- Fichiers `.dat` originaux (ex: `artists.dat`, `user_artists.dat`, etc.)
- **Note**: Ces fichiers sont ignorés par git (voir `.gitignore`)

#### Données traitées (PROCESSED)
Générées automatiquement dans `final_data/{nom_dataset}/`:
- `ratings_final.txt`: Interactions utilisateur-item (format: `user_id \t item_id \t label`)
- `kg_final.txt`: Triplets du graphe de connaissances (format: `head \t relation \t tail`)
- `dataset_metadata.txt`: Métadonnées du dataset (type, taille réelle, paramètres)

#### Distinction RAW vs FILTERED
- **RAW**: Données brutes originales (peuvent être très volumineuses)
- **FILTERED**: Sous-ensemble créé avec `--reduce` (plus petit, pour tests/visualisation)
  - Les valeurs réelles peuvent être inférieures aux max demandés
  - Exemple: demander 50 users peut donner 46 users réels (selon les données disponibles)

### 2. Visualiser le graphe

Voir la section "Visualiser le graphe" ci-dessous pour plus de détails.


## Prétraitement des données Music

### Option 1: Prétraitement avec réduction automatique (RECOMMANDÉ)

Pour créer un dataset réduit directement pendant le preprocessing (50 users, 100 artists par défaut):

```bash
cd src
python preprocess.py --dataset music --reduce --max_users 50 --max_artists 100
```

**Avantages:**
- Une seule commande, pas besoin de scripts séparés
- Le fichier original est automatiquement sauvegardé (`.backup`)
- Le graph créé sera petit (environ 50-100 entités) et facile à visualiser
- Les métadonnées sont sauvegardées dans `dataset_metadata.txt` pour synchronisation avec `main.py`

### Option 2: Prétraitement complet

Pour prétraiter toutes les données brutes:

```bash
cd src
python preprocess.py --dataset music
```

### Résultat du preprocessing

Le preprocessing convertit depuis `rawdata/music/`:
- `user_artists.dat` → `final_data/music/ratings_final.txt` (interactions utilisateur-artiste)
- `user_taggedartists.dat` → `final_data/music/kg_final.txt` (graphe de connaissances artiste-tag)
- `dataset_metadata.txt` → Métadonnées du dataset (type, taille, paramètres de filtrage)

### Visualiser le graphe

```bash
python main.py --dataset music --visualize
```

**Le script génère automatiquement 2 visualisations:**

1. **Vue MACRO** (`graph_macro.png`):
   - Visualisation complète du dataset filtré
   - Vue d'ensemble de la structure du graphe
   - Légende: Nœuds (Entités), Arêtes (Relations), Type de dataset

2. **Vue MICRO** (`graph_micro_user_X.png`):
   - Visualisation du sous-graphe de l'utilisateur avec le plus de connexions
   - Vue détaillée des relations d'un utilisateur spécifique
   - Légende: Nœud de départ (User/Item), Nœuds connectés, Relations

**Fonctionnalités:**
- Détection automatique du type de dataset (COMPLET/FILTRÉ) via `dataset_metadata.txt`
- Synchronisation entre `preprocess.py` et `main.py`
- Sélection automatique de l'utilisateur le plus connecté pour la vue micro
- Légendes claires pour comprendre la structure du graphe

**Options de visualisation:**
```bash
# Limiter le nombre de nœuds affichés
python main.py --dataset music --visualize --max_nodes 200

# Spécifier un utilisateur particulier
python main.py --dataset music --visualize --user_id 5
```

Voir `final_data/music/DATA_EXPLANATION_FR.md` pour plus de détails sur le format des données.

