# Algorithmes de Graphe pour Système de Recommandation Musicale

## Vue d'ensemble

Ce projet implémente un système de recommandation musicale basé sur un **graphe de connaissances** construit à partir des **patterns d'écoute** (nombre d'écoutes) des utilisateurs. Le graphe permet d'appliquer différents algorithmes classiques pour découvrir des artistes similaires et générer des recommandations personnalisées.

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

## I. Parcours de Graphe

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

## II. Arbre Couvrant de Poids Minimum (MST)

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

## III. Plus Court Chemin

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

### 7. Algorithme de Floyd-Warshall

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

## Comparaison des Algorithmes

| Algorithme | Objectif Principal | Complexité Temps | Complexité Espace | Meilleur Pour |
|------------|-------------------|------------------|-------------------|---------------|
| **BFS** | Exploration par niveau | O(V + E) | O(V) | Découvrir artistes proches |
| **DFS** | Exploration en profondeur | O(V + E) | O(V) | Chemins spécifiques |
| **Prim** | MST (structure principale) | O(E log V) | O(V) | Clusters d'artistes |
| **Kruskal** | MST (approche globale) | O(E log E) | O(V) | Communautés d'artistes |
| **Dijkstra** | Plus court chemin (source unique) | O((V+E) log V) | O(V) | Recommandations qualité |
| **Bellman-Ford** | Plus court chemin (poids négatifs) | O(V × E) | O(V) | Cas spéciaux |
| **Floyd-Warshall** | Plus courts chemins (toutes paires) | O(V³) | O(V²) | Analyse globale |

---

## Utilisation Pratique

### Préparation des Données

```bash
# 1. Préparer le graphe depuis les données brutes
cd src
python preprocess.py --dataset music --reduce --max_users 50 --max_artists 100
```

### Exécution des Algorithmes

```bash
# 2. Appliquer un algorithme spécifique
python main.py --dataset music --algorithm bfs --user_id 0 --max_hops 2
python main.py --dataset music --algorithm dijkstra --user_id 0
python main.py --dataset music --algorithm prim --user_id 0
```

### Visualisation

```bash
# 3. Visualiser le graphe et les résultats
python main.py --dataset music --visualize --max_nodes 100
```

---

## Exemples de Cas d'Usage

### Cas 1 : Découverte d'Artistes Proches (BFS)

**Scénario** : Un utilisateur aime The Beatles et veut découvrir des artistes similaires.

**Solution** : BFS explore le graphe niveau par niveau depuis The Beatles.

**Résultat** :
- Hop 1 : The Rolling Stones, Queen, Led Zeppelin
- Hop 2 : Deep Purple, Black Sabbath, The Who
- Recommandations : Artistes par ordre de proximité

### Cas 2 : Recommandations de Haute Qualité (Dijkstra)

**Scénario** : Trouver les artistes ayant les connexions les plus fortes.

**Solution** : Dijkstra utilise les poids (nombre de co-listens) pour trouver les chemins les plus courts.

**Résultat** :
- The Beatles → The Rolling Stones (poids: 8000, distance: 0.000125)
- The Beatles → Queen (poids: 5000, distance: 0.0002)
- Recommandation : The Rolling Stones (connexion la plus forte)

### Cas 3 : Identification de Clusters (Prim/Kruskal)

**Scénario** : Comprendre la structure du graphe et identifier des communautés d'artistes.

**Solution** : MST révèle les connexions les plus importantes.

**Résultat** :
- Cluster Rock : [Beatles, Stones, Queen, Led Zeppelin]
- Cluster Pop : [Michael Jackson, Madonna, Prince]
- Recommandations : Artistes dans le même cluster

### Cas 4 : Analyse Globale (Floyd-Warshall)

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
