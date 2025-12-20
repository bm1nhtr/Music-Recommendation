# Framework de Graphe de Connaissances

Un framework pour l'analyse et la visualisation de graphes de connaissances, avec support pour l'application d'algorithmes graphiques classiques.

## 📚 Documentation des Algorithmes

Pour une documentation complète des algorithmes implémentés, consultez **[README_ALGORITHMES.md](README_ALGORITHMES.md)**.

**Algorithmes disponibles :**
- **Parcours de graphe** : BFS, DFS
- **Arbre couvrant de poids minimum** : Prim, Kruskal
- **Plus court chemin** : Dijkstra
- **Plus courts chemins avancés** : Bellman-Ford

### 📊 Guide de Visualisation

Pour comprendre **quelles visualisations sont nécessaires** pour chaque catégorie d'algorithmes et comment les interpréter, consultez **[final_data/music/VISUALISATION_ALGORITHMES_FR.md](final_data/music/VISUALISATION_ALGORITHMES_FR.md)**.

Ce guide explique :
- Les visualisations requises pour chaque algorithme (BFS, DFS, Prim, Kruskal, Dijkstra, Bellman-Ford)
- Comment comparer les algorithmes dans chaque catégorie
- Les spécifications techniques (couleurs, tailles, formats)

## Vue d'ensemble

Ce projet implémente un modèle de recommandation qui utilise un graphe de connaissances pour améliorer les recommandations. Le modèle propage les préférences utilisateur à travers le graphe en utilisant des mécanismes d'attention multi-hops.


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

Pour créer un dataset réduit directement pendant le preprocessing (18 users, 18 artists par défaut):

```bash
cd src
python preprocess.py --dataset music --reduce --max_users 18 --max_artists 18
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

**Note importante** : Pour les visualisations spécifiques aux algorithmes (BFS, DFS, Prim, Kruskal, Dijkstra, Bellman-Ford), consultez le **[Guide de Visualisation](final_data/music/VISUALISATION_ALGORITHMES_FR.md)** qui explique en détail quelles visualisations sont nécessaires pour chaque catégorie d'algorithmes.

**Visualisations de base (actuelles):**

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


Voir `final_data/music/DATA_EXPLANATION_FR.md` pour plus de détails sur le format des données.

