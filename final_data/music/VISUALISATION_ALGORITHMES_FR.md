# Guide de Visualisation pour les Algorithmes de Graphe

## Vue d'ensemble

Ce document explique **quelles visualisations sont nécessaires** pour chaque catégorie d'algorithmes décrite dans `README_ALGORITHMES.md`. Les visualisations permettent de **comparer les algorithmes** et de **comprendre leurs résultats**.

---

## Structure des Visualisations par Catégorie

### Catégorie I : Parcours de Graphe (BFS vs DFS)

#### 🎯 Objectif de la Visualisation

Montrer **l'ordre d'exploration** et **les niveaux de similarité** (hops) depuis les artistes écoutés par l'utilisateur.

#### 📊 Visualisations Requises

##### 1. Visualisation de l'Exploration (BFS/DFS)

**Ce qu'elle doit montrer** :
- **Nœuds de départ** : Artistes écoutés par l'utilisateur (couleur rouge, taille grande)
- **Niveaux d'exploration** : Nœuds colorés selon le hop level
  - Hop 0 (départ) : Rouge
  - Hop 1 : Orange (artistes directement similaires)
  - Hop 2 : Jaune (artistes à 2 hops)
  - Hop 3+ : Bleu clair
- **Arêtes** : Connexions entre artistes (via relation `similar_to`)
- **Ordre d'exploration** : Numéros sur les nœuds montrant l'ordre de visite (optionnel)

**Format de sortie** :
- Fichier : `algorithm_bfs_exploration.png` ou `algorithm_dfs_exploration.png`
- Taille : 16x12 pouces
- Légende : 
  - Rouge = Nœuds de départ
  - Orange = Hop 1 (artistes directement similaires)
  - Jaune = Hop 2
  - Bleu = Hop 3+
  - Épaisseur arête = Poids (connexion plus forte)

**Exemple de ce qu'on doit voir** :
```
[Beatles] (rouge, hop 0)
  ↓
[Queen, Stones, Led Zeppelin] (orange, hop 1)
  ↓
[Deep Purple, Black Sabbath] (jaune, hop 2)
```

##### 2. Visualisation Comparée BFS vs DFS

**Ce qu'elle doit montrer** :
- **Deux panneaux côte à côte** : BFS à gauche, DFS à droite
- **Même point de départ** : Mêmes artistes de départ
- **Différence d'exploration** : 
  - BFS : Exploration large (tous les voisins directs d'abord)
  - DFS : Exploration profonde (un chemin complet avant de revenir)

**Format de sortie** :
- Fichier : `comparison_bfs_vs_dfs.png`
- Deux sous-graphes côte à côte avec les mêmes couleurs de hop

##### 3. Statistiques d'Exploration

**Tableau à afficher** :
- Nombre de nœuds visités par hop
- Temps d'exécution
- Nombre de recommandations par niveau

---

### Catégorie II : Arbre Couvrant Minimum (Prim vs Kruskal)

#### 🎯 Objectif de la Visualisation

Montrer **la structure principale du graphe** (MST) et **les connexions les plus importantes** entre artistes.

#### 📊 Visualisations Requises

##### 1. Visualisation du MST (Prim/Kruskal)

**Ce qu'elle doit montrer** :
- **Nœuds de départ** : Artistes écoutés par l'utilisateur (rouge)
- **Arêtes du MST** : Seulement les arêtes qui font partie du MST (bleu foncé, épais)
- **Poids des arêtes** : Épaisseur proportionnelle au poids (plus épais = connexion plus forte)
- **Clusters** : Groupes d'artistes connectés dans le MST (peuvent être colorés différemment)
- **Recommandations** : Artistes dans le MST mais non écoutés (orange)

**Format de sortie** :
- Fichier : `algorithm_prim_mst.png` ou `algorithm_kruskal_mst.png`
- Taille : 16x12 pouces
- **Important** : Seulement les arêtes du MST, pas toutes les arêtes du graphe
- Légende :
  - Rouge = Nœuds de départ
  - Orange = Recommandations (dans MST)
  - Bleu clair = Autres nœuds du MST
  - Épaisseur arête = Poids (connexion plus forte)

**Exemple de ce qu'on doit voir** :
```
Cluster Rock:
  [Beatles] --(poids 8000)-- [Stones]
  [Beatles] --(poids 5000)-- [Queen]
  [Queen] --(poids 3000)-- [Led Zeppelin]

Cluster Pop:
  [Michael Jackson] --(poids 6000)-- [Madonna]
```

##### 2. Visualisation Comparée Prim vs Kruskal

**Ce qu'elle doit montrer** :
- **Deux panneaux côte à côte** : Prim à gauche, Kruskal à droite
- **Même MST** : Les deux doivent produire le même MST (même structure)
- **Différence d'approche** : 
  - Prim : Commence depuis un nœud, ajoute progressivement
  - Kruskal : Trie toutes les arêtes, ajoute par poids décroissant

**Format de sortie** :
- Fichier : `comparison_prim_vs_kruskal.png`
- Deux MST côte à côte (devraient être identiques)

##### 3. Visualisation des Clusters

**Ce qu'elle doit montrer** :
- **Groupes d'artistes** : Clusters identifiés dans le MST
- **Connexions inter-clusters** : Arêtes qui connectent différents clusters
- **Poids des connexions** : Pour comprendre la force des liens

**Format de sortie** :
- Fichier : `mst_clusters.png`
- Nœuds colorés par cluster

---

### Catégorie III : Plus Court Chemin (Dijkstra vs Bellman-Ford)

#### 🎯 Objectif de la Visualisation

Montrer **les chemins les plus courts** (connexions les plus fortes) depuis les artistes écoutés vers les autres artistes.

#### 📊 Visualisations Requises

##### 1. Visualisation des Chemins les Plus Courts (Dijkstra/Bellman-Ford)

**Ce qu'elle doit montrer** :
- **Nœuds de départ** : Artistes écoutés par l'utilisateur (rouge)
- **Distances** : Nœuds colorés selon la distance (plus proche = plus foncé vert)
- **Chemins les plus courts** : Arêtes en rouge épais montrant les chemins optimaux
- **Toutes les arêtes** : Arêtes du graphe en gris clair (pour contexte)
- **Labels de distance** : Distance affichée sur les nœuds recommandés

**Format de sortie** :
- Fichier : `algorithm_dijkstra_paths.png` ou `algorithm_bellman_ford_paths.png`
- Taille : 16x12 pouces
- Légende :
  - Rouge = Nœuds de départ
  - Vert (foncé → clair) = Distance depuis départ (plus foncé = plus proche)
  - Rouge épais = Chemins les plus courts
  - Gris clair = Autres arêtes du graphe

**Exemple de ce qu'on doit voir** :
```
[Beatles] (rouge, distance 0)
  ↓ (chemin rouge épais)
[Stones] (vert foncé, distance 0.000125)
  ↓ (chemin rouge épais)
[Queen] (vert moyen, distance 0.0002)
```

##### 2. Visualisation Comparée Dijkstra vs Bellman-Ford

**Ce qu'elle doit montrer** :
- **Deux panneaux côte à côte** : Dijkstra à gauche, Bellman-Ford à droite
- **Mêmes distances** : Les deux doivent produire les mêmes distances (pour poids positifs)
- **Mêmes chemins** : Les chemins les plus courts doivent être identiques

**Format de sortie** :
- Fichier : `comparison_dijkstra_vs_bellman_ford.png`
- Deux visualisations côte à côte avec les mêmes chemins

##### 3. Matrice de Distances (Optionnel)

**Ce qu'elle doit montrer** :
- **Tableau de distances** : Distance depuis chaque nœud de départ vers chaque artiste
- **Top recommandations** : Artistes avec les distances les plus courtes

**Format de sortie** :
- Fichier texte : `distances_matrix.txt` ou visualisation heatmap

---

## Structure des Fichiers de Sortie

### Organisation des Fichiers

```
final_data/music/
├── visualizations/
│   ├── parcours/
│   │   ├── bfs_exploration_user_0.png
│   │   ├── dfs_exploration_user_0.png
│   │   └── comparison_bfs_vs_dfs_user_0.png
│   ├── mst/
│   │   ├── prim_mst_user_0.png
│   │   ├── kruskal_mst_user_0.png
│   │   ├── comparison_prim_vs_kruskal_user_0.png
│   │   └── mst_clusters.png
│   └── shortest_path/
│       ├── dijkstra_paths_user_0.png
│       ├── bellman_ford_paths_user_0.png
│       └── comparison_dijkstra_vs_bellman_ford_user_0.png
```

---

## Spécifications Techniques

### Couleurs Standardisées

| Élément | Couleur | Usage |
|---------|---------|-------|
| Nœuds de départ | Rouge (`#FF0000`) | Artistes écoutés par l'utilisateur |
| Hop 1 (BFS/DFS) | Orange (`#FFA500`) | Artistes directement similaires |
| Hop 2 (BFS/DFS) | Jaune (`#FFFF00`) | Artistes à 2 hops |
| Hop 3+ (BFS/DFS) | Bleu clair (`#ADD8E6`) | Artistes à 3+ hops |
| Recommandations (MST) | Orange (`#FFA500`) | Artistes recommandés dans MST |
| Distance proche (Dijkstra) | Vert foncé (`#006400`) | Distance courte |
| Distance moyenne (Dijkstra) | Vert moyen (`#32CD32`) | Distance moyenne |
| Distance lointaine (Dijkstra) | Vert clair (`#90EE90`) | Distance longue |
| Chemins les plus courts | Rouge épais (`#FF0000`, width=2.5) | Chemins optimaux |
| Arêtes du graphe | Gris clair (`#D3D3D3`) | Contexte |
| Arêtes MST | Bleu foncé (`#00008B`) | Connexions du MST |

### Tailles de Nœuds

| Type de Nœud | Taille | Usage |
|--------------|--------|-------|
| Nœuds de départ | 600 | Artistes écoutés |
| Hop 1 / Recommandations | 450 | Artistes importants |
| Hop 2 | 350 | Artistes secondaires |
| Autres | 300 | Nœuds normaux |

### Épaisseur des Arêtes

- **Arêtes normales** : 0.5 - 1.0 (selon poids)
- **Chemins les plus courts** : 2.5 (fixe, rouge)
- **Arêtes MST** : 1.0 - 4.0 (selon poids, bleu foncé)

---

## Exemples de Commandes

### Générer les Visualisations pour BFS

```bash
python main.py --dataset music --algorithm bfs --user_id 0 --max_hops 3 --visualize
```

**Sorties attendues** :
- `visualizations/parcours/bfs_exploration_user_0.png`
- Nœuds colorés par hop level
- Arêtes montrant les connexions

### Générer les Visualisations pour DFS

```bash
python main.py --dataset music --algorithm dfs --user_id 0 --max_hops 3 --visualize
```

**Sorties attendues** :
- `visualizations/parcours/dfs_exploration_user_0.png`
- Même structure que BFS mais ordre d'exploration différent

### Comparer BFS vs DFS

```bash
python compare_algorithms.py --category parcours --user_id 0 --visualize
```

**Sorties attendues** :
- `visualizations/parcours/comparison_bfs_vs_dfs_user_0.png`
- Deux panneaux côte à côte

### Générer les Visualisations pour Prim

```bash
python main.py --dataset music --algorithm prim --user_id 0 --visualize
```

**Sorties attendues** :
- `visualizations/mst/prim_mst_user_0.png`
- Seulement les arêtes du MST
- Clusters d'artistes visibles

### Générer les Visualisations pour Dijkstra

```bash
python main.py --dataset music --algorithm dijkstra --user_id 0 --visualize
```

**Sorties attendues** :
- `visualizations/shortest_path/dijkstra_paths_user_0.png`
- Chemins les plus courts en rouge épais
- Nœuds colorés par distance

---

## Ce que Chaque Visualisation Doit Permettre

### Pour Comparer BFS vs DFS

✅ **Voir la différence d'ordre d'exploration**
- BFS : Tous les voisins directs d'abord (largeur)
- DFS : Un chemin complet avant de revenir (profondeur)

✅ **Comparer les recommandations**
- BFS : Artistes "proches" (hop 1, 2)
- DFS : Artistes sur des chemins spécifiques

### Pour Comparer Prim vs Kruskal

✅ **Vérifier que le MST est identique**
- Les deux algorithmes doivent produire le même MST
- Structure des connexions principales identique

✅ **Comprendre les clusters**
- Groupes d'artistes similaires
- Connexions entre clusters

### Pour Comparer Dijkstra vs Bellman-Ford

✅ **Vérifier que les distances sont identiques**
- Pour poids positifs, les deux doivent donner les mêmes résultats
- Chemins les plus courts identiques

✅ **Comprendre les connexions les plus fortes**
- Artistes avec les distances les plus courtes
- Chemins optimaux depuis les artistes écoutés

---

## Notes Importantes

1. **Pas de visualisation macro/micro** : On se concentre uniquement sur les résultats des algorithmes
2. **Une visualisation par algorithme** : Chaque algorithme génère sa propre visualisation
3. **Visualisations comparatives** : Pour chaque paire d'algorithmes, une visualisation côte à côte
4. **Couleurs cohérentes** : Utiliser les mêmes couleurs pour les mêmes concepts
5. **Légendes claires** : Chaque visualisation doit avoir une légende explicative

---

## Prochaines Étapes

1. **Implémenter les visualisations** dans `graph_visualizer.py`
2. **Intégrer dans `main.py`** pour générer automatiquement les visualisations
3. **Créer un script de comparaison** pour générer les visualisations comparatives
4. **Tester avec différents utilisateurs** pour valider les visualisations
