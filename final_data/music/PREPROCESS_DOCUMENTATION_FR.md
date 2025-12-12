# Documentation Complète du Préprocessing - Dataset Music

## Vue d'ensemble

Le module `preprocess.py` transforme les données brutes du dataset Last.fm en un graphe de connaissances structuré, prêt pour l'application d'algorithmes graphiques (BFS, DFS, Prim, Kruskal, Dijkstra, Bellman-Ford).

## Objectif

Construire un **graphe de connaissances** basé sur les **patterns d'écoute** (nombre d'écoutes) plutôt que sur les tags, permettant une analyse plus directe des préférences utilisateur et l'application d'algorithmes graphiques classiques.

---

## Schéma d'ensemble

```
FICHIERS DE DONNÉES BRUTES (Input)          FICHIERS TRAITÉS (Output)
───────────────────────────────             ─────────────────────────

user_artists.dat                            ratings_final.txt
├─ userID \t artistID \t weight    →       ├─ user_id \t artist_id \t label
└─ Exemple: 2 \t 51 \t 13883               └─ Exemple: 0 \t 45 \t 1

user_artists.dat                            kg_final.txt
├─ userID \t artistID \t weight    →       ├─ head \t relation \t tail \t weight
└─ Exemple: 2 \t 51 \t 13883               └─ Exemple: 100 \t 0 \t 0 \t 13883

artists.dat
└─ id \t name \t url
```

**Note importante** : Le graphe de connaissances est maintenant construit à partir des **patterns d'écoute** (nombre d'écoutes) et non plus des tags.

---

## Structure des Données d'Entrée

### Fichiers Requis (dans `rawdata/music/`)

1. **`artists.dat`**
   - Format : `id \t name \t url \t pictureURL`
   - Contenu : Liste de tous les artistes du dataset
   - Exemple : `51 \t The Beatles \t http://... \t http://...`

2. **`user_artists.dat`**
   - Format : `userID \t artistID \t weight`
   - Contenu : Interactions utilisateur-artiste avec nombre d'écoutes
   - Exemple : `2 \t 51 \t 13883` (User 2 a écouté The Beatles 13,883 fois)

---

## Processus de Préprocessing

### Étape 1 : Lecture et Mapping des Artistes

**Objectif** : Créer un mapping des IDs d'artistes vers des indices consécutifs (0, 1, 2, ...)

**Processus** :
```python
1. Lire artists.dat
2. Pour chaque artiste :
   - Extraire l'ID
   - Assigner un index consécutif (0, 1, 2, ...)
   - Créer mapping : artist_id2index[raw_id] = index
```

**Résultat** :
- `artist_id2index` : Dictionnaire {raw_artist_id: index}
- Indices : 0 à `n_artists - 1`

**Exemple** :
```
Raw IDs: 51, 55, 56, 65, ...
Mapped:  0,  1,  2,  3,  ...
```

---

### Étape 2 : Conversion en Ratings

**Objectif** : Créer le fichier `ratings_final.txt` avec les interactions utilisateur-artiste

**Input**: `user_artists.dat`
```
userID	artistID	weight
2	51	13883
2	52	11690
2	53	11351
```

#### 2.1. Lecture des Interactions

```python
Lire user_artists.dat :
- user_id : ID utilisateur brut
- artist_id : ID artiste brut
- weight : Nombre d'écoutes (listening count)
```

#### 2.2. Calcul du Seuil (Threshold)

```python
1. Collecter tous les weights
2. Calculer la médiane : threshold = median(all_weights)
3. Utiliser ce seuil pour classifier positive/négative
```

**Exemple** :
```
Weights: [13883, 8983, 6152, 3579, 3301, ...]
Médiane: 1234.0
→ Weight >= 1234 : label = 1 (positive)
→ Weight < 1234 : label = 0 (négative)
```

#### 2.3. Remapping des IDs Utilisateur

```python
1. Identifier tous les utilisateurs uniques
2. Créer mapping : user_id2index[raw_user_id] = index
3. Indices : 0, 1, 2, ... (consécutifs)
```

#### 2.4. Écriture de `ratings_final.txt`

**Format** : `user_idx \t artist_idx \t label`

**Contenu** :
- **Ratings positifs** : Toutes les interactions avec `weight >= threshold`
- **Ratings négatifs** : Échantillonnage aléatoire d'artistes non écoutés (pour équilibrer)

**Output**: `ratings_final.txt`
```
user_id	artist_id	label
0	45	1      ← L'utilisateur 0 a écouté l'artiste 45 (positive)
0	46	1      ← L'utilisateur 0 a écouté l'artiste 46 (positive)
0	100	0      ← L'utilisateur 0 n'a pas écouté l'artiste 100 (échantillon négatif)
```

---

### Étape 3 : Construction du Graphe de Connaissances

**Objectif** : Créer `kg_final.txt` avec les relations basées sur les patterns d'écoute

**Input**: `user_artists.dat` (même fichier que l'étape 1)

#### 3.1. Mapping des Entités

**Structure** :
- **Artistes** : Indices `0` à `n_artists - 1`
- **Utilisateurs** : Indices `n_artists` à `n_artists + n_users - 1`

**Exemple** :
```
Si n_artists = 100, n_users = 50 :
- Artistes : 0-99
- Utilisateurs : 100-149
```

#### 3.2. Relations User-Artist (Approach 2)

**Type de Relations** :
- `listened_to` (ID: 0) : `user → artist`
- `listened_by` (ID: 1) : `artist → user` (relation inverse)

**Calcul du Poids** :
```python
weight = nombre_d_écoutes  # Directement depuis user_artists.dat
```

**Processus** :
```python
1. Relire user_artists.dat
2. Pour chaque ligne (user_id, artist_id, weight) :
   - Convertir en indices : user_idx, artist_idx
   - Calculer user_entity_idx = n_artists + user_idx
   - Créer relation : (user_entity_idx, artist_idx, weight)
```

**Exemple** :
```
User 2 (raw) → User 0 (index) → Entity 100 (n_artists=100)
Artist 51 (raw) → Artist 0 (index)
Weight: 13883

Relations créées :
- 100 → 0 (listened_to, weight=13883)
- 0 → 100 (listened_by, weight=13883)
```

**Format dans kg_final.txt** :
```
head_entity \t relation_id \t tail_entity \t weight
100 \t 0 \t 0 \t 13883
0 \t 1 \t 100 \t 13883
```

#### 3.3. Relations Artist-Artist (Approach 3)

**Type de Relations** :
- `similar_to` (ID: 2) : `artist1 → artist2`
- `similar_from` (ID: 3) : `artist2 → artist1` (relation inverse)

**Calcul du Poids** :
```python
weight = nombre_d_utilisateurs_ayant_écouté_les_deux_artistes
```

**Processus** :

##### Étape 3.3.1 : Construire le Mapping Artist-Users

```python
artist_users = {
    artist_idx: {user_idx: weight, ...}
}

Pour chaque relation user-artist :
    artist_users[artist_idx][user_idx] = weight
```

**Exemple** :
```
Artist 0 (Beatles) : {user0: 13883, user1: 5000, user2: 2000}
Artist 1 (Stones) : {user0: 10000, user1: 3000}
```

##### Étape 3.3.2 : Calculer la Similarité (Co-listening)

```python
Pour chaque utilisateur :
    1. Trouver tous les artistes qu'il a écoutés
    2. Créer des connexions entre TOUTES les paires d'artistes
    3. Incrémenter le compteur pour chaque paire

artist_similarity[(artist1, artist2)] += 1
```

**Exemple** :
```
User 0 a écouté : [Beatles (0), Stones (1), Queen (2)]

Paires créées :
- (0, 1) : Beatles-Stones → count += 1
- (0, 2) : Beatles-Queen → count += 1
- (1, 2) : Stones-Queen → count += 1

Si User 1 a aussi écouté Beatles et Stones :
- (0, 1) : Beatles-Stones → count = 2
```

##### Étape 3.3.3 : Filtrer par Seuil Minimum

```python
min_co_listens = 2  # Seuil minimum de co-écoutes

Pour chaque paire (artist1, artist2) :
    Si count >= min_co_listens :
        Créer relation avec weight = count
```

**Exemple** :
```
(Beatles, Stones) : count = 5 → Créer relation (weight=5)
(Beatles, Queen) : count = 3 → Créer relation (weight=3)
(Stones, Queen) : count = 1 → Ignorer (count < 2)
```

**Format dans kg_final.txt** :
```
0 \t 2 \t 1 \t 5    # Beatles → Stones (similar_to, 5 users)
1 \t 3 \t 0 \t 5    # Stones → Beatles (similar_from, 5 users)
0 \t 2 \t 2 \t 3    # Beatles → Queen (similar_to, 3 users)
2 \t 3 \t 0 \t 3    # Queen → Beatles (similar_from, 3 users)
```

---

## Format du Fichier de Sortie : `kg_final.txt`

### Structure

```
head_entity \t relation_id \t tail_entity \t weight
```

### Types de Relations

| Relation ID | Nom | Direction | Poids |
|-------------|-----|-----------|-------|
| 0 | `listened_to` | `user → artist` | Nombre d'écoutes |
| 1 | `listened_by` | `artist → user` | Nombre d'écoutes (identique à listened_to) |
| 2 | `similar_to` | `artist → artist` | Nombre d'utilisateurs ayant écouté les deux |
| 3 | `similar_from` | `artist → artist` | Nombre d'utilisateurs (identique à similar_to) |

### Exemple Complet

```
# Relations User-Artist
100    0    0    13883    # User 100 a écouté artiste 0 (13,883 fois)
0      1    100  13883    # Artiste 0 est écouté par user 100 (13,883 fois)

# Relations Artist-Artist
0      2    1    5        # Artiste 0 similaire à artiste 1 (5 users)
1      3    0    5        # Artiste 1 similaire à artiste 0 (5 users)
0      2    2    3        # Artiste 0 similaire à artiste 2 (3 users)
2      3    0    3        # Artiste 2 similaire à artiste 0 (3 users)
```

---

## Comment exécuter le preprocessing

### Option 1: Prétraitement complet

```bash
cd src
python preprocess.py --dataset music
```

### Option 2: Prétraitement avec réduction (recommandé pour tests)

```bash
cd src
python preprocess.py --dataset music --reduce --max_users 50 --max_artists 100
```

**Sortie console** (exemple avec réduction):
```
Filtrage des données brutes: max 50 utilisateurs, 100 artistes...
Données originales: 5000 interactions
Sélection: 50 utilisateurs, 100 artistes
Fichier filtré: 450 interactions
Prétraitement du dataset music...
Lecture des artistes...
100 artistes trouvés
Conversion des interactions utilisateur-artiste en ratings...
Seuil de poids utilisé: 1234.00 pour les ratings positifs
Nombre d'utilisateurs: 50
Nombre d'items (artistes): 100
Construction du graphe de connaissances à partir des patterns d'écoute...
  - Construction des relations User-Artist...
    450 relations User-Artist créées
  - Construction des relations Artist-Artist (similarité pondérée)...
    250 relations Artist-Artist créées (seuil: 2 co-écoutes)
Graphe de connaissances créé:
  - Nombre d'entités: 150 (100 artistes + 50 utilisateurs)
  - Nombre de relations: 4
    * listened_to/listened_by: 900 triplets
    * similar_to/similar_from: 500 triplets
  - Nombre total de triplets KG: 1400
Terminé!
```

---

## Mapping des IDs

### IDs Utilisateur
- **Brut**: 2, 3, 4, 5, ... (non consécutifs)
- **Traité**: 0, 1, 2, 3, ... (consécutifs à partir de 0)

### IDs Artiste  
- **Brut**: 51, 52, 53, ... (non consécutifs)
- **Traité**: 0, 1, 2, 3, ... (consécutifs à partir de 0)

### IDs Entité dans le KG
- **Artistes**: 0 → `n_artists - 1`
- **Utilisateurs**: `n_artists` → `n_artists + n_users - 1`

**Exemple** :
```
Si n_artists = 100, n_users = 50 :
- Artistes : 0-99
- Utilisateurs : 100-149
```

---

## Calcul des Poids

### Poids pour Relations User-Artist

**Source** : Directement depuis `user_artists.dat`, colonne `weight`

**Valeur** : Nombre d'écoutes (listening count)

**Exemple** :
```
user_artists.dat: 2 \t 51 \t 13883
→ weight = 13883 (User 2 a écouté l'artiste 51, 13,883 fois)
```

### Poids pour Relations Artist-Artist

**Source** : Calculé à partir du co-listening

**Valeur** : Nombre d'utilisateurs ayant écouté les deux artistes

**Processus** :
1. Pour chaque utilisateur, identifier tous les artistes qu'il a écoutés
2. Créer des connexions entre toutes les paires d'artistes pour cet utilisateur
3. Compter le nombre d'utilisateurs pour chaque paire
4. Filtrer avec seuil minimum (`min_co_listens = 2`)

**Exemple** :
```
User 0 a écouté : [Beatles, Stones, Queen]
User 1 a écouté : [Beatles, Stones]
User 2 a écouté : [Beatles, Queen]

Paires et compteurs :
- (Beatles, Stones) : 2 users (User 0, User 1) → weight = 2
- (Beatles, Queen) : 2 users (User 0, User 2) → weight = 2
- (Stones, Queen) : 1 user (User 0) → Ignoré (count < 2)
```

---

## Paramètres de Filtrage

### Option `--reduce`

Permet de créer un sous-ensemble du dataset pour les tests et visualisations.

**Processus** :
1. Analyser `user_artists.dat` pour identifier les utilisateurs et artistes les plus actifs
2. Sélectionner les `max_users` utilisateurs avec le plus d'interactions
3. Sélectionner les `max_artists` artistes avec le plus d'écoutes totales
4. Filtrer toutes les données pour ne garder que ces sélections

**Exemple** :
```bash
python preprocess.py --dataset music --reduce --max_users 50 --max_artists 100
```

**Résultat** :
- Dataset réduit avec ~50 users et ~100 artists
- Plus facile à visualiser et tester
- Les valeurs réelles peuvent être légèrement inférieures aux max demandés

---

## Métadonnées Sauvegardées

Le fichier `dataset_metadata.txt` contient :

```
filtered=true/false
max_users_requested=50          # Si filtered=true
max_artists_requested=100       # Si filtered=true
n_users_actual=46               # Valeur réelle après filtrage
n_artists_actual=98             # Valeur réelle après filtrage
n_entities=144                  # n_artists + n_users
n_relations=4                   # Nombre de types de relations
n_kg_triples=1234               # Nombre total de triplets
```

---

## Statistiques Générées

Après le preprocessing, les statistiques suivantes sont affichées :

```
Prétraitement du dataset music...
Lecture des artistes...
100 artistes trouvés
Conversion des interactions utilisateur-artiste en ratings...
Seuil de poids utilisé: 1234.00 pour les ratings positifs
Nombre d'utilisateurs: 50
Nombre d'items (artistes): 100
Construction du graphe de connaissances à partir des patterns d'écoute...
  - Construction des relations User-Artist...
    500 relations User-Artist créées
  - Construction des relations Artist-Artist (similarité pondérée)...
    250 relations Artist-Artist créées (seuil: 2 co-écoutes)
Graphe de connaissances créé:
  - Nombre d'entités: 150 (100 artistes + 50 utilisateurs)
  - Nombre de relations: 4
    * listened_to/listened_by: 1000 triplets
    * similar_to/similar_from: 500 triplets
  - Nombre total de triplets KG: 1500
```

---

## Pourquoi le preprocessing est nécessaire?

1. **Standardisation du format** : Les données brutes ont plusieurs formats → standardisation en format simple
2. **Remapping des IDs** : Les IDs dans les données brutes ne sont pas consécutifs → remapping en 0, 1, 2... pour faciliter le traitement
3. **Création d'échantillons négatifs** : Les données brutes n'ont que des interactions positives → besoin d'échantillons négatifs pour l'entraînement
4. **Construction du Graphe de Connaissances** : À partir des patterns d'écoute → créer une structure de graphe avec relations et poids pour les algorithmes graphiques

---

## Différences avec l'Ancien Processus (Tags)

| Aspect | Ancien (Tags) | Nouveau (Patterns d'Écoute) |
|--------|---------------|------------------------------|
| **Source** | `user_taggedartists.dat` | `user_artists.dat` |
| **Entités** | Artistes + Tags | Artistes + Utilisateurs |
| **Relations** | `has_tag`, `tagged_by` | `listened_to`, `listened_by`, `similar_to`, `similar_from` |
| **Poids** | Non utilisé | Nombre d'écoutes / Co-listening count |
| **Complexité** | Basée sur tags explicites | Basée sur comportement d'écoute |

---

## Utilisation des Poids dans les Algorithmes

Les poids sont essentiels pour les algorithmes suivants :

### Pour Dijkstra et Bellman-Ford

Les poids sont utilisés pour calculer les distances :
```python
distance = 1 / weight  # Plus le poids est élevé, plus la distance est courte
```

**Explication** :
- Poids élevé = connexion forte = distance courte
- Permet d'utiliser les algorithmes de plus court chemin pour trouver les connexions les plus fortes

### Pour Prim et Kruskal

Les poids sont utilisés directement pour construire le MST :
- Arêtes avec poids élevé = connexions importantes
- Le MST contient les connexions les plus significatives

### Pour BFS et DFS

Les poids ne sont pas utilisés directement dans l'algorithme, mais peuvent être affichés pour information lors de la visualisation.

---

## Notes Techniques

### Performance

- **Complexité** : O(U × A²) où U = nombre d'utilisateurs, A = nombre d'artistes
- **Bottleneck** : Calcul des relations Artist-Artist (co-listening)
- **Optimisation** : Utilisation de `defaultdict` et structures de données efficaces

### Limitations

- **Seuil de co-listening** : `min_co_listens = 2` par défaut
  - Augmenter pour réduire le nombre de relations (moins de bruit, mais moins de connexions)
  - Diminuer pour plus de connexions (mais plus de bruit)

- **Mémoire** : Pour de très grands datasets, considérer le filtrage (`--reduce`)

---

## Exemple d'Exécution

```bash
cd src
python preprocess.py --dataset music --reduce --max_users 50 --max_artists 100
```

**Sortie attendue** :
```
Filtrage des données brutes: max 50 utilisateurs, 100 artistes...
Données originales: 5000 interactions
Sélection: 50 utilisateurs, 100 artistes
Fichier filtré: 450 interactions
Prétraitement du dataset music...
[... statistiques ...]
Terminé!
```

---

## Fichiers Générés

Après le preprocessing, les fichiers suivants sont créés dans `final_data/music/` :

1. **`ratings_final.txt`** : Interactions utilisateur-artiste (format: `user_id \t artist_id \t label`)
2. **`kg_final.txt`** : Graphe de connaissances avec relations et poids (format: `head \t relation \t tail \t weight`)
3. **`dataset_metadata.txt`** : Métadonnées du dataset (type, taille, paramètres de filtrage)
4. **`user_artists.dat.backup`** : Sauvegarde du fichier original (si filtrage activé)

---

## Validation

Pour valider le preprocessing :

1. **Vérifier les statistiques** : Nombre d'entités, relations, triplets
2. **Vérifier les poids** : Doivent être > 0 pour toutes les relations
3. **Vérifier le mapping** : Les indices doivent être consécutifs (0, 1, 2, ...)
4. **Vérifier les relations** : Chaque relation doit avoir sa relation inverse
5. **Vérifier le format** : `kg_final.txt` doit avoir 4 colonnes (head, relation, tail, weight)

---

## Références

- Dataset Last.fm : http://www.last.fm
- Format des données brutes : Voir `rawdata/music/readme.txt`
