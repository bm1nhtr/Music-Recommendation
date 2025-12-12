# Algorithmes de Graphe pour Système de Recommandation Musicale

## Vue d'ensemble

Ce projet implémente un système de recommandation musicale basé sur un **graphe de connaissances** construit à partir des **patterns d'écoute** (nombre d'écoutes) des utilisateurs. Le graphe permet d'appliquer différents algorithmes classiques pour découvrir des artistes similaires et générer des recommandations personnalisées.

## 🎯 Objectif de Comparaison

Ce projet implémente **6 algorithmes** organisés en **3 catégories** pour permettre une **comparaison systématique** :

| Catégorie | Algorithmes | Task Commun | Critères de Comparaison |
|-----------|-------------|-------------|------------------------|
| **I. Parcours de Graphe** | BFS, DFS | Explorer le graphe depuis les artistes écoutés | Ordre d'exploration, profondeur vs largeur |
| **II. Arbre Couvrant Minimum** | Prim, Kruskal | Construire un MST pour identifier les connexions principales | Efficacité, approche (greedy local vs global) |
| **III. Plus Court Chemin** | Dijkstra, Bellman-Ford | Trouver les chemins les plus courts (connexions les plus fortes) | Gestion des poids, complexité |

**Important** : Chaque paire d'algorithmes dans la même catégorie résout **exactement le même problème** mais avec des approches différentes, permettant une comparaison équitable.

## Structure du Graphe

### Entités

Le graphe contient deux types d'entités :

- **Artistes** : Indices `0` à `n_artists - 1`
- **Utilisateurs** : Indices `n_artists` à `n_artists + n_users - 1`

### Relations

Le graphe utilise **4 types de relations** basées sur les patterns d'écoute :

| Relation ID | Nom | Direction | Description |
|-------------|-----|-----------|-------------|
| 0 | `listened_to` | `user → artist` | Un utilisateur a écouté un artiste (poids = nombre d'écoutes) |
| 1 | `listened_by` | `artist → user` | Relation inverse de `listened_to` |
| 2 | `similar_to` | `artist → artist` | Deux artistes sont similaires (poids = nombre d'utilisateurs ayant écouté les deux) |
| 3 | `similar_from` | `artist → artist` | Relation inverse de `similar_to` |

### Format du Fichier KG

```
head_entity \t relation_id \t tail_entity
```

**Exemple :**
```
1000    0    45    # User 1000 a écouté l'artiste 45
45      1    1000  # L'artiste 45 est écouté par le user 1000
45      2    67    # L'artiste 45 est similaire à l'artiste 67
67      3    45    # L'artiste 67 est similaire à l'artiste 45 (inverse)
```

---

## I. Parcours de Graphe : BFS vs DFS

### 🎯 Task Commun

**Problème à résoudre** : Explorer le graphe depuis les artistes que l'utilisateur a déjà écoutés pour découvrir des artistes similaires à différentes distances.

**Input** : Liste des artistes écoutés par l'utilisateur (nœuds de départ)

**Output** : Liste des artistes recommandés, organisés par niveau de similarité (hops)

**Critères de comparaison** :
- Ordre d'exploration (largeur vs profondeur)
- Nombre de nœuds visités
- Temps d'exécution
- Qualité des recommandations (artistes proches vs connexions profondes)

---

### 1. BFS (Breadth-First Search) - Parcours en Largeur

#### Principe

BFS explore le graphe niveau par niveau, en visitant d'abord tous les voisins directs avant de passer au niveau suivant.

#### Application dans la Recommandation

**Objectif** : Trouver des artistes similaires à différentes distances (hops) depuis les artistes que l'utilisateur a déjà écoutés.

**Algorithme** :
```
1. Initialiser avec les artistes écoutés par l'utilisateur (niveau 0)
2. Pour chaque niveau (hop) :
   - Visiter tous les voisins directs (via relation similar_to)
   - Ajouter les artistes non visités au niveau suivant
3. Recommandations = artistes aux niveaux 1, 2, 3...
```

**Avantages** :
- Trouve les artistes les plus proches en premier
- Exploration systématique par niveau de similarité
- Idéal pour découvrir des artistes "proches" des préférences actuelles

**Exemple** :
```
User a écouté: [The Beatles, Pink Floyd]
  ↓
BFS Hop 1: [Led Zeppelin, Queen, The Rolling Stones]
  ↓
BFS Hop 2: [Deep Purple, Black Sabbath, The Who]
  ↓
Recommandations: Artistes par ordre de proximité
```

#### Complexité
- **Temps** : O(V + E) où V = nombre de nœuds, E = nombre d'arêtes
- **Espace** : O(V) pour la file d'attente

---

### 2. DFS (Depth-First Search) - Parcours en Profondeur

#### Principe

DFS explore le graphe en allant le plus loin possible le long d'une branche avant de revenir en arrière.

#### Application dans la Recommandation

**Objectif** : Explorer des chemins spécifiques dans le graphe pour découvrir des connexions profondes entre artistes.

**Algorithme** :
```
1. Initialiser avec les artistes écoutés par l'utilisateur
2. Pour chaque artiste de départ :
   - Explorer récursivement tous les chemins possibles
   - Marquer les nœuds visités
   - Recommander les artistes découverts
```

**Avantages** :
- Découvre des connexions profondes et spécifiques
- Utile pour explorer des genres musicaux particuliers
- Moins de mémoire que BFS (récursion)

**Exemple** :
```
User a écouté: [Jazz Artist A]
  ↓
DFS explore: A → B → C → D (chemin profond)
  ↓
Recommandations: Artistes D, E, F (connexions profondes)
```

#### Complexité
- **Temps** : O(V + E)
- **Espace** : O(V) pour la pile de récursion

---

### 📊 Comparaison BFS vs DFS

| Critère | BFS | DFS |
|---------|-----|-----|
| **Ordre d'exploration** | Niveau par niveau (largeur) | Chemin complet avant de revenir (profondeur) |
| **Première découverte** | Artistes les plus proches (hop 1) | Artistes sur un chemin spécifique |
| **Mémoire** | O(V) - file d'attente | O(V) - pile de récursion |
| **Meilleur pour** | Découvrir artistes proches | Explorer des genres musicaux spécifiques |
| **Recommandations** | Artistes par niveau de similarité | Artistes avec connexions profondes |
| **Exemple** | Hop 1: [Queen, Stones], Hop 2: [Deep Purple] | Chemin: Beatles → Queen → Led Zeppelin → Deep Purple |

**Quand utiliser BFS** : Pour des recommandations générales, découvrir des artistes "proches" des préférences actuelles.

**Quand utiliser DFS** : Pour explorer des chemins spécifiques, découvrir des connexions profondes dans un genre musical particulier.

---

## II. Arbre Couvrant de Poids Minimum : Prim vs Kruskal

### 🎯 Task Commun

**Problème à résoudre** : Construire un arbre couvrant minimum (MST) pour identifier les connexions les plus importantes entre artistes dans le graphe.

**Input** : Graphe complet avec poids (nombre de co-listens entre artistes)

**Output** : Arbre couvrant minimum contenant les connexions les plus fortes (poids maximum)

**Critères de comparaison** :
- Efficacité algorithmique
- Approche (greedy local vs global)
- Temps d'exécution
- Structure du MST résultant

### 3. Algorithme de Prim

#### Principe

Prim construit un arbre couvrant minimum en ajoutant progressivement les arêtes de poids minimum qui connectent de nouveaux nœuds à l'arbre.

#### Application dans la Recommandation

**Objectif** : Identifier la structure principale du graphe et découvrir les connexions les plus importantes entre artistes.

**Algorithme** :
```
1. Commencer avec un artiste de départ (ou un ensemble d'artistes écoutés)
2. Construire un MST en ajoutant les arêtes de poids maximum (connexions les plus fortes)
3. Recommandations = artistes dans le MST mais non écoutés par l'utilisateur
```

**Avantages** :
- Identifie les connexions les plus significatives
- Réduit le graphe à sa structure essentielle
- Utile pour comprendre les clusters d'artistes

**Exemple** :
```
MST révèle:
- Cluster Rock: [Beatles, Stones, Queen, Led Zeppelin]
- Cluster Pop: [Michael Jackson, Madonna, Prince]
- Cluster Jazz: [Miles Davis, John Coltrane]

User a écouté: [Beatles, Stones]
→ Recommandations: [Queen, Led Zeppelin] (même cluster dans MST)
```

#### Complexité
- **Temps** : O(E log V) avec heap binaire, O(V²) avec matrice d'adjacence
- **Espace** : O(V)

---

### 4. Algorithme de Kruskal

#### Principe

Kruskal construit un MST en triant toutes les arêtes par poids et en les ajoutant une par une si elles ne créent pas de cycle.

#### Application dans la Recommandation

**Objectif** : Similaire à Prim, mais avec une approche différente qui peut être plus efficace sur des graphes denses.

**Algorithme** :
```
1. Trier toutes les arêtes par poids décroissant (connexions les plus fortes)
2. Initialiser une structure Union-Find
3. Pour chaque arête (dans l'ordre) :
   - Si elle ne crée pas de cycle, l'ajouter au MST
4. Recommandations = artistes dans le MST
```

**Avantages** :
- Plus efficace sur graphes denses
- Approche globale (considère toutes les arêtes)
- Utile pour identifier des communautés d'artistes

**Exemple** :
```
Toutes les arêtes triées:
- (Beatles, Stones): poids 8000
- (Beatles, Queen): poids 5000
- (Queen, Led Zeppelin): poids 3000
  ↓
MST construit avec les connexions les plus fortes
→ Recommandations basées sur la structure du MST
```

#### Complexité
- **Temps** : O(E log E) pour le tri + O(E α(V)) pour Union-Find ≈ O(E log E)
- **Espace** : O(V) pour Union-Find

---

### 📊 Comparaison Prim vs Kruskal

| Critère | Prim | Kruskal |
|---------|------|---------|
| **Approche** | Greedy local (commence depuis un nœud) | Greedy global (trie toutes les arêtes) |
| **Structure de données** | Min-heap (ou matrice d'adjacence) | Union-Find + tri des arêtes |
| **Complexité** | O(E log V) avec heap, O(V²) avec matrice | O(E log E) |
| **Meilleur pour** | Graphes denses (beaucoup d'arêtes) | Graphes clairsemés (peu d'arêtes) |
| **Dépendance du point de départ** | Oui (commence depuis un nœud spécifique) | Non (considère toutes les arêtes) |
| **MST résultant** | Peut varier selon le point de départ | Toujours le même (si poids uniques) |
| **Exemple** | Commence depuis Beatles, ajoute progressivement | Trie toutes les arêtes, ajoute par poids décroissant |

**Quand utiliser Prim** : 
- Graphe dense (beaucoup d'arêtes)
- On veut un MST qui commence depuis un artiste spécifique
- On a une représentation en matrice d'adjacence

**Quand utiliser Kruskal** :
- Graphe clairsemé (peu d'arêtes)
- On veut un MST global indépendant du point de départ
- On veut identifier des communautés d'artistes

**Note** : Pour notre graphe de recommandation, les deux algorithmes produisent le même MST (même structure de connexions principales), mais avec des approches différentes.

---

## III. Plus Court Chemin : Dijkstra vs Bellman-Ford

### 🎯 Task Commun

**Problème à résoudre** : Trouver les chemins les plus courts depuis les artistes écoutés par l'utilisateur vers tous les autres artistes, où la distance représente la force de connexion (distance courte = connexion forte).

**Input** : 
- Graphe avec poids (nombre de co-listens)
- Nœuds sources : artistes écoutés par l'utilisateur

**Output** : 
- Distances depuis les sources vers tous les autres artistes
- Recommandations : artistes avec les distances les plus courtes (connexions les plus fortes)

**Critères de comparaison** :
- Gestion des poids (positifs vs négatifs)
- Complexité temporelle
- Robustesse
- Efficacité selon la densité du graphe

### 5. Algorithme de Dijkstra

#### Principe

Dijkstra trouve le chemin le plus court depuis un nœud source vers tous les autres nœuds dans un graphe pondéré avec poids positifs.

#### Application dans la Recommandation

**Objectif** : Trouver les artistes ayant les connexions les plus fortes (chemins les plus courts) depuis les artistes écoutés par l'utilisateur.

**Algorithme** :
```
1. Initialiser les distances depuis les artistes écoutés (distance = 0)
2. Utiliser une file de priorité (min-heap)
3. Pour chaque nœud :
   - Extraire le nœud avec la distance minimale
   - Mettre à jour les distances des voisins
   - Distance = 1 / poids (plus le poids est élevé, plus la distance est courte)
4. Recommandations = artistes avec les distances les plus courtes
```

**Avantages** :
- Utilise les poids réels (nombre d'écoutes, co-listening)
- Trouve les connexions les plus significatives
- Recommandations de haute qualité

**Exemple** :
```
User a écouté: [The Beatles]
  ↓
Dijkstra calcule les distances:
- Beatles → Queen: distance = 1/5000 = 0.0002
- Beatles → Rolling Stones: distance = 1/8000 = 0.000125
  ↓
Recommandation: Rolling Stones (distance la plus courte = connexion la plus forte)
```

#### Complexité
- **Temps** : O((V + E) log V) avec heap binaire, O(V²) avec matrice
- **Espace** : O(V)

**Note** : Dans notre graphe, les poids représentent la force de connexion (plus élevé = plus similaire), donc on utilise `distance = 1 / poids` pour que les connexions fortes aient une distance courte.

---

## IV. Plus Courts Chemins Avancés

### 6. Algorithme de Bellman-Ford

#### Principe

Bellman-Ford trouve les plus courts chemins depuis un nœud source vers tous les autres nœuds, même avec des poids négatifs, et détecte les cycles de poids négatif.

#### Application dans la Recommandation

**Objectif** : Similaire à Dijkstra, mais peut gérer des cas où les poids peuvent être négatifs (par exemple, si on utilise des scores de similarité négatifs pour certains cas).

**Algorithme** :
```
1. Initialiser les distances depuis la source (0 pour source, ∞ pour autres)
2. Relaxer toutes les arêtes V-1 fois :
   - Pour chaque arête (u, v) avec poids w:
     - Si distance[v] > distance[u] + w:
       - distance[v] = distance[u] + w
3. Vérifier les cycles de poids négatif (relaxation supplémentaire)
4. Recommandations = artistes avec distances les plus courtes
```

**Avantages** :
- Gère les poids négatifs
- Détecte les cycles de poids négatif
- Plus robuste que Dijkstra dans certains cas

**Exemple** :
```
User a écouté: [Artiste A]
  ↓
Bellman-Ford calcule les distances même avec poids négatifs possibles
  ↓
Recommandations basées sur les chemins les plus courts
```

#### Complexité
- **Temps** : O(V × E)
- **Espace** : O(V)

**Note** : Moins efficace que Dijkstra pour notre cas (poids positifs), mais utile si on veut gérer des cas spéciaux.

---

### 📊 Comparaison Dijkstra vs Bellman-Ford

| Critère | Dijkstra | Bellman-Ford |
|---------|----------|--------------|
| **Poids supportés** | Uniquement positifs | Positifs et négatifs |
| **Complexité** | O((V + E) log V) avec heap | O(V × E) |
| **Structure de données** | Min-heap (priority queue) | Tableau simple |
| **Détection de cycles négatifs** | Non | Oui |
| **Efficacité** | Plus rapide (graphes denses) | Plus lent mais plus robuste |
| **Meilleur pour** | Graphes avec poids positifs uniquement | Graphes avec poids négatifs possibles |
| **Initialisation** | Distance source = 0, autres = ∞ | Même |
| **Relaxation** | Une fois par nœud (greedy) | V-1 fois toutes les arêtes |
| **Exemple** | User → Beatles → Queen (distance: 0.0002) | Même résultat, mais vérifie aussi cycles négatifs |

**Quand utiliser Dijkstra** :
- ✅ **Notre cas principal** : Graphe avec poids positifs uniquement (nombre de co-listens)
- Plus efficace et plus rapide
- Recommandations de haute qualité

**Quand utiliser Bellman-Ford** :
- Graphe avec poids négatifs possibles (scores de similarité négatifs)
- Besoin de détecter des cycles de poids négatif
- Validation et robustesse

**Note** : Pour notre graphe de recommandation (poids = nombre de co-listens, toujours positifs), **Dijkstra est recommandé** car plus efficace. Bellman-Ford est utile pour des cas spéciaux ou pour validation.

---

### 7. Algorithme de Floyd-Warshall (Optionnel - Analyse Globale)

#### Principe

Floyd-Warshall trouve les plus courts chemins entre **toutes les paires** de nœuds dans un graphe, même avec des poids négatifs (mais pas de cycles négatifs).

#### Application dans la Recommandation

**Objectif** : Calculer la similarité entre toutes les paires d'artistes et identifier les chemins de connexion les plus courts dans tout le graphe.

**Algorithme** :
```
1. Initialiser une matrice de distances D[i][j] = poids de l'arête (i,j) ou ∞
2. Pour chaque nœud intermédiaire k :
   - Pour chaque paire (i, j) :
     - D[i][j] = min(D[i][j], D[i][k] + D[k][j])
3. Recommandations = artistes avec distances minimales depuis les artistes écoutés
```

**Avantages** :
- Calcule toutes les paires de plus courts chemins en une fois
- Utile pour analyser la structure globale du graphe
- Identifie les connexions indirectes entre artistes

**Exemple** :
```
Matrice de distances calculée pour toutes les paires:
- Beatles → Queen: distance directe = 0.0002
- Beatles → Led Zeppelin: via Queen = 0.0002 + 0.0003 = 0.0005
  ↓
Recommandations basées sur toutes les connexions possibles
```

#### Complexité
- **Temps** : O(V³)
- **Espace** : O(V²) pour la matrice de distances

**Note** : Plus coûteux que Dijkstra, mais calcule toutes les paires en une fois. Utile pour des analyses globales.

---

## 📊 Tableau Comparatif Global

### Vue d'ensemble de tous les algorithmes

| Algorithme | Catégorie | Objectif Principal | Complexité Temps | Complexité Espace | Meilleur Pour |
|------------|-----------|-------------------|------------------|-------------------|---------------|
| **BFS** | Parcours | Exploration par niveau | O(V + E) | O(V) | Découvrir artistes proches |
| **DFS** | Parcours | Exploration en profondeur | O(V + E) | O(V) | Chemins spécifiques |
| **Prim** | MST | MST (structure principale) | O(E log V) | O(V) | Clusters d'artistes (graphes denses) |
| **Kruskal** | MST | MST (approche globale) | O(E log E) | O(V) | Communautés d'artistes (graphes clairsemés) |
| **Dijkstra** | Plus court chemin | Plus court chemin (source unique) | O((V+E) log V) | O(V) | Recommandations qualité (poids positifs) |
| **Bellman-Ford** | Plus court chemin | Plus court chemin (poids négatifs) | O(V × E) | O(V) | Cas spéciaux, validation |
| **Floyd-Warshall** | Plus court chemin | Plus courts chemins (toutes paires) | O(V³) | O(V²) | Analyse globale (optionnel) |

### Comparaison par Catégorie

#### Catégorie I : Parcours de Graphe

| Critère | BFS | DFS |
|---------|-----|-----|
| **Task** | Explorer depuis artistes écoutés | Explorer depuis artistes écoutés |
| **Approche** | Largeur (niveau par niveau) | Profondeur (chemin complet) |
| **Complexité** | O(V + E) | O(V + E) |
| **Recommandations** | Artistes par hop (1, 2, 3...) | Artistes sur chemins profonds |
| **Avantage** | Découvre les plus proches d'abord | Découvre connexions spécifiques |

#### Catégorie II : Arbre Couvrant Minimum

| Critère | Prim | Kruskal |
|---------|------|---------|
| **Task** | Construire MST | Construire MST |
| **Approche** | Greedy local (depuis un nœud) | Greedy global (toutes arêtes) |
| **Complexité** | O(E log V) | O(E log E) |
| **Meilleur pour** | Graphes denses | Graphes clairsemés |
| **Avantage** | Efficace sur graphes denses | Indépendant du point de départ |

#### Catégorie III : Plus Court Chemin

| Critère | Dijkstra | Bellman-Ford |
|---------|----------|--------------|
| **Task** | Plus court chemin depuis sources | Plus court chemin depuis sources |
| **Poids** | Positifs uniquement | Positifs et négatifs |
| **Complexité** | O((V+E) log V) | O(V × E) |
| **Détection cycles** | Non | Oui |
| **Avantage** | Plus rapide (notre cas) | Plus robuste |

---

## Utilisation Pratique

### Préparation des Données

```bash
# 1. Préparer le graphe depuis les données brutes
cd src
python preprocess.py --dataset music --reduce --max_users 50 --max_artists 100
```

### Exécution et Comparaison des Algorithmes

#### Comparaison BFS vs DFS

```bash
# Exécuter BFS
python main.py --dataset music --algorithm bfs --user_id 0 --max_hops 3

# Exécuter DFS
python main.py --dataset music --algorithm dfs --user_id 0 --max_hops 3

# Comparer les résultats : nombre de nœuds visités, temps, recommandations
```

#### Comparaison Prim vs Kruskal

```bash
# Exécuter Prim
python main.py --dataset music --algorithm prim --user_id 0

# Exécuter Kruskal
python main.py --dataset music --algorithm kruskal --user_id 0

# Comparer : temps d'exécution, structure du MST, clusters identifiés
```

#### Comparaison Dijkstra vs Bellman-Ford

```bash
# Exécuter Dijkstra
python main.py --dataset music --algorithm dijkstra --user_id 0

# Exécuter Bellman-Ford
python main.py --dataset music --algorithm bellman_ford --user_id 0

# Comparer : temps d'exécution, distances calculées, recommandations
```

### Script de Comparaison Automatique

```bash
# Comparer tous les algorithmes d'une catégorie
python compare_algorithms.py --category parcours --user_id 0
python compare_algorithms.py --category mst --user_id 0
python compare_algorithms.py --category shortest_path --user_id 0
```

### Visualisation

```bash
# 3. Visualiser le graphe et les résultats
python main.py --dataset music --visualize --max_nodes 100
```

---

## 🎯 Stratégie de Comparaison

### Comment Comparer les Algorithmes

Pour chaque catégorie, les algorithmes résolvent **exactement le même problème** mais avec des approches différentes :

1. **Parcours (BFS vs DFS)** :
   - **Input identique** : Liste des artistes écoutés par l'utilisateur
   - **Output comparable** : Liste des artistes recommandés
   - **Différence** : Ordre d'exploration (largeur vs profondeur)
   - **Métriques** : Nombre de nœuds visités, temps d'exécution, qualité des recommandations

2. **MST (Prim vs Kruskal)** :
   - **Input identique** : Graphe complet avec poids
   - **Output comparable** : MST avec les connexions principales
   - **Différence** : Approche algorithmique (local vs global)
   - **Métriques** : Temps d'exécution, structure du MST, efficacité selon densité

3. **Plus Court Chemin (Dijkstra vs Bellman-Ford)** :
   - **Input identique** : Graphe avec poids, nœuds sources
   - **Output comparable** : Distances et chemins les plus courts
   - **Différence** : Gestion des poids, complexité
   - **Métriques** : Temps d'exécution, robustesse, qualité des recommandations

### Métriques de Comparaison

Pour chaque paire d'algorithmes, comparer :
- ⏱️ **Temps d'exécution** : Mesurer le temps réel
- 💾 **Utilisation mémoire** : Espace utilisé
- 🎯 **Qualité des recommandations** : Pertinence des artistes recommandés
- 📊 **Couverture** : Nombre de nœuds visités/explorés
- 🔍 **Structure découverte** : Clusters, chemins, connexions

---

## Exemples de Cas d'Usage

### Cas 1 : Découverte d'Artistes Proches (BFS vs DFS)

**Scénario** : Un utilisateur aime The Beatles et veut découvrir des artistes similaires.

**Solution BFS** : Explore niveau par niveau depuis The Beatles.
- Hop 1 : The Rolling Stones, Queen, Led Zeppelin
- Hop 2 : Deep Purple, Black Sabbath, The Who
- **Avantage** : Découvre les plus proches d'abord

**Solution DFS** : Explore en profondeur depuis The Beatles.
- Chemin 1 : Beatles → Queen → Led Zeppelin → Deep Purple
- Chemin 2 : Beatles → Stones → The Who → The Kinks
- **Avantage** : Découvre des connexions profondes dans un genre

**Comparaison** :
- BFS : Recommandations générales, artistes "proches"
- DFS : Recommandations spécialisées, chemins spécifiques

### Cas 2 : Identification de Clusters (Prim vs Kruskal)

**Scénario** : Comprendre la structure du graphe et identifier des communautés d'artistes.

**Solution Prim** : Construit MST depuis un artiste de départ (ex: Beatles).
- Commence depuis Beatles
- Ajoute progressivement : Stones, Queen, Led Zeppelin
- **Avantage** : Efficace sur graphes denses, MST centré sur point de départ

**Solution Kruskal** : Construit MST en triant toutes les arêtes.
- Trie toutes les arêtes par poids
- Ajoute les connexions les plus fortes : (Beatles, Stones), (Queen, Led Zeppelin)...
- **Avantage** : MST global, indépendant du point de départ

**Résultat commun** :
- Cluster Rock : [Beatles, Stones, Queen, Led Zeppelin]
- Cluster Pop : [Michael Jackson, Madonna, Prince]
- Recommandations : Artistes dans le même cluster

**Comparaison** :
- Prim : Plus rapide sur graphes denses, dépend du point de départ
- Kruskal : Plus adapté aux graphes clairsemés, MST global

### Cas 3 : Recommandations de Haute Qualité (Dijkstra vs Bellman-Ford)

**Scénario** : Trouver les artistes ayant les connexions les plus fortes depuis The Beatles.

**Solution Dijkstra** : Utilise min-heap pour trouver les chemins les plus courts.
- The Beatles → The Rolling Stones (poids: 8000, distance: 0.000125)
- The Beatles → Queen (poids: 5000, distance: 0.0002)
- **Avantage** : Plus rapide (O((V+E) log V)), efficace pour poids positifs

**Solution Bellman-Ford** : Relaxe toutes les arêtes V-1 fois.
- Même résultat : The Rolling Stones (distance: 0.000125)
- **Avantage** : Plus robuste, détecte cycles négatifs, gère poids négatifs

**Résultat commun** :
- Recommandation : The Rolling Stones (connexion la plus forte)

**Comparaison** :
- Dijkstra : **Recommandé pour notre cas** (poids positifs uniquement), plus rapide
- Bellman-Ford : Utile pour validation, cas spéciaux avec poids négatifs

### Cas 4 : Analyse Globale (Floyd-Warshall - Optionnel)

**Scénario** : Analyser toutes les connexions possibles entre artistes.

**Solution** : Floyd-Warshall calcule les distances entre toutes les paires.

**Résultat** :
- Matrice complète de similarité entre tous les artistes
- Identification de chemins de connexion indirects
- Recommandations basées sur l'analyse globale

---

## Structure du Code

```
src/
├── graph_loader.py          # Chargement du graphe
├── graph_visualizer.py      # Visualisation
├── graph_algorithms.py      # Implémentation des algorithmes
├── preprocess.py            # Construction du graphe
└── main.py                  # Point d'entrée principal
```

---

## Notes Techniques

### Poids des Arêtes

Dans notre graphe :
- **Relations User-Artist** : Poids = nombre d'écoutes
- **Relations Artist-Artist** : Poids = nombre d'utilisateurs ayant écouté les deux artistes

### Conversion Distance/Poids

Pour Dijkstra et autres algorithmes de plus court chemin :
- **Distance** = `1 / poids` (plus le poids est élevé, plus la connexion est forte, donc distance courte)
- Cela permet d'utiliser les algorithmes de plus court chemin pour trouver les connexions les plus fortes

### Filtrage des Relations

Les algorithmes peuvent être appliqués sur :
- **Toutes les relations** : Exploration complète
- **Relations spécifiques** : Par exemple, seulement `similar_to` pour les recommandations artiste-artiste

---

## Références

- **Introduction to Algorithms** (Cormen, Leiserson, Rivest, Stein)
- **Algorithm Design** (Kleinberg, Tardos)
- **NetworkX Documentation** : https://networkx.org/

---

## Auteur

Projet développé dans le cadre du cours d'Algorithmes de Graphes (S5-Algo).

---

## Licence

Ce projet est à des fins éducatives.
