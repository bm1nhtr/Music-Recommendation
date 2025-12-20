# Résolution du Problème de Cache - Nodes Incorrects

## 🔴 Problème

Lorsque vous relancez le preprocessing avec des paramètres différents (ex: `--max_users 30 --max_artists 30`), les statistiques peuvent afficher un nombre incorrect de nodes (ex: 80 au lieu de 60).

**Symptômes** :
- Metadata indique `n_entities=60` (correct)
- Mais les statistiques affichent `Nombre de nœuds: 80` (incorrect)
- Le fichier `kg_final.txt` contient bien 60 nodes, mais le loader lit 80

## 🔍 Cause

Le problème vient du **fichier cache** `kg_final.npy` qui contient les données de l'ancien preprocessing. Le code dans `graph_loader.py` charge d'abord le fichier `.npy` s'il existe, au lieu de relire le fichier `.txt` mis à jour.

```python
# Dans graph_loader.py ligne 69-70
if os.path.exists(kg_file + '.npy'):
    kg_np = np.load(kg_file + '.npy')  # ← Lit l'ancien cache
```

## ✅ Solution Rapide

### ⚡ Solution Automatique (Recommandée)

**Le système détecte et corrige automatiquement les problèmes de cache !**

Lorsque vous lancez `python main.py`, le système :
1. Vérifie si `kg_final.txt` a été modifié après le cache `.npy` (comparaison de timestamp)
2. Vérifie si le nombre d'entités dans le cache correspond aux métadonnées
3. **Supprime automatiquement le cache obsolète** si nécessaire
4. Régénère le cache depuis le fichier `.txt` mis à jour

**Vous n'avez plus besoin de supprimer manuellement le cache !** 🎉

### Option Manuelle (Si nécessaire)

Si vous voulez forcer la régénération du cache manuellement :

```bash
# Windows PowerShell
Remove-Item final_data\music\kg_final.npy
Remove-Item final_data\music\ratings_final.npy

# Linux/Mac
rm final_data/music/kg_final.npy
rm final_data/music/ratings_final.npy
```

Puis relancer votre script. Le fichier `.npy` sera régénéré automatiquement avec les bonnes données.

## 🛡️ Prévention

### ✅ Méthode Automatique (Recommandée - Déjà Implémentée)

Le système gère automatiquement la cohérence du cache :

1. **Détection automatique** : Le système vérifie la cohérence à chaque chargement
2. **Correction automatique** : Le cache obsolète est supprimé et régénéré automatiquement
3. **Aucune action requise** : Vous pouvez simplement lancer vos scripts normalement

**Workflow recommandé** :
```bash
# 1. Relancer le preprocessing (si vous changez les paramètres)
cd src
python preprocess.py --dataset music --reduce --max_users 30 --max_artists 30

# 2. Utiliser les données (le cache sera automatiquement géré)
python main.py --dataset music --visualize
```

### Méthode Manuelle (Si vous voulez forcer la régénération)

Si vous voulez forcer la suppression du cache avant le preprocessing :

```bash
# 1. Supprimer le cache
Remove-Item final_data\music\kg_final.npy
Remove-Item final_data\music\ratings_final.npy

# 2. Relancer le preprocessing
cd src
python preprocess.py --dataset music --reduce --max_users 30 --max_artists 30
```

### Vérification de Cohérence (Optionnel)

Pour vérifier manuellement la cohérence (le système le fait déjà automatiquement) :

```python
from src.graph_loader import load_kg

n_entity, n_relation, kg, metadata = load_kg('final_data', 'music')

expected = metadata.get('n_artists_actual', 0) + metadata.get('n_users_actual', 0)
if n_entity != expected:
    print(f"⚠️ Incohérence détectée: n_entity={n_entity}, attendu={expected}")
    print("💡 Le système devrait avoir corrigé cela automatiquement")
```

## 📝 Note Technique

Le fichier `.npy` est créé pour **accélérer le chargement** (plus rapide que lire un fichier texte). 

**Gestion automatique** : Le système détecte maintenant automatiquement quand `kg_final.txt` change (via comparaison de timestamp) et régénère le cache si nécessaire. Vous n'avez plus besoin de supprimer manuellement le cache.

**Comment ça marche** :
1. Le système compare le timestamp de `kg_final.txt` avec celui de `kg_final.npy`
2. Si `.txt` est plus récent → cache supprimé et régénéré
3. Si les métadonnées ne correspondent pas → cache supprimé et régénéré
4. Sinon → cache réutilisé (reproducibility garantie)

---

## ✅ Solution Automatique (Implémentée)

Le système détecte maintenant automatiquement les incohérences et régénère le cache :

1. **Vérification de timestamp** : Si `kg_final.txt` a été modifié après le cache `.npy`, le cache est automatiquement supprimé
2. **Vérification de metadata** : Si le nombre d'entités dans le cache ne correspond pas aux métadonnées, le cache est régénéré
3. **Reproducibility** : Si les fichiers n'ont pas changé, le cache est réutilisé pour garantir la cohérence

Vous n'avez plus besoin de supprimer manuellement le cache - le système le fait automatiquement !

---

## 🔐 Vérification d'Intégrité et Reproducibility

### Problème : Comment garantir que deux personnes avec les mêmes paramètres ont les mêmes données ?

Lorsque vous travaillez en équipe, il est important de garantir que tous les membres obtiennent exactement les mêmes données après le preprocessing, même sur des machines différentes.

### Solution : Checksums (Hashes SHA256)

Le système calcule automatiquement des **checksums SHA256** pour les fichiers `kg_final.txt` et `ratings_final.txt` lors du preprocessing. Ces checksums sont sauvegardés dans `dataset_metadata.txt`.

#### Comment ça fonctionne

1. **Lors du preprocessing** :
   ```bash
   python preprocess.py --dataset music --reduce --max_users 30 --max_artists 50
   ```
   - Le système calcule automatiquement les hash SHA256 de `kg_final.txt` et `ratings_final.txt`
   - Les hash sont sauvegardés dans `dataset_metadata.txt` :
     ```
     kg_file_hash=abc123def456...
     ratings_file_hash=789xyz012...
     ```

2. **Lors du chargement** :
   ```bash
   python main.py --dataset music
   ```
   - Le système compare automatiquement les hash des fichiers actuels avec ceux dans metadata
   - Si les hash correspondent → ✅ Reproducibility garantie
   - Si les hash ne correspondent pas → ❌ Les fichiers ont été modifiés ou corrompus

3. **Vérification manuelle** :
   ```bash
   python main.py --dataset music --verify
   ```
   - Vérifie uniquement l'intégrité sans charger les données
   - Affiche un rapport détaillé de vérification

#### Exemple de sortie

**Cas 1 : Données valides (reproducibility garantie)**
```
✅ [VERIFICATION] Fichier KG valide (hash: abc123def4567890...)
✅ [VERIFICATION] Fichier Ratings valide (hash: 789xyz0123456789...)
✅ [VERIFICATION] Tous les fichiers sont valides - Reproducibility garantie!
```

**Cas 2 : Données invalides**
```
❌ [VERIFICATION] Fichier KG INVALIDE!
   Hash actuel:   abc123def4567890...
   Hash attendu:  xyz789abc0123456...
   → Les données ne correspondent pas aux métadonnées
❌ [VERIFICATION] Certains fichiers sont invalides - Reproducibility NON garantie!
```

### Workflow pour Travail en Équipe

#### Sur la machine du premier développeur :

1. **Préprocesser les données** :
   ```bash
   cd src
   python preprocess.py --dataset music --reduce --max_users 30 --max_artists 50
   ```

2. **Vérifier que tout est correct** :
   ```bash
   python main.py --dataset music --verify
   ```

3. **Commit dans git** :
   ```bash
   git add final_data/music/kg_final.txt
   git add final_data/music/ratings_final.txt
   git add final_data/music/dataset_metadata.txt
   git commit -m "Add preprocessed data with checksums"
   git push
   ```
   
   ⚠️ **Important** : Ne commitez PAS les fichiers `.npy` (ils sont déjà dans `.gitignore`)

#### Sur la machine du deuxième développeur :

1. **Récupérer les fichiers** :
   ```bash
   git pull
   ```

2. **Vérifier l'intégrité** :
   ```bash
   cd src
   python main.py --dataset music --verify
   ```

3. **Si la vérification réussit** :
   - ✅ Les données sont identiques
   - ✅ Reproducibility garantie
   - Vous pouvez utiliser les données en toute confiance

4. **Si la vérification échoue** :
   - ❌ Les fichiers ont été modifiés ou corrompus
   - **Solution** : Relancez le preprocessing avec les mêmes paramètres :
     ```bash
     python preprocess.py --dataset music --reduce --max_users 30 --max_artists 50
     ```

### Avantages

1. **Détection automatique** : Le système détecte automatiquement si les fichiers ont été modifiés
2. **Reproducibility garantie** : Même hash = même données, même sur des machines différentes
3. **Pas de comparaison manuelle** : Plus besoin de comparer les fichiers ligne par ligne
4. **Sécurité** : Détecte les corruptions de fichiers ou modifications accidentelles

### Notes Techniques

- **Algorithme de hash** : SHA256 (cryptographiquement sûr)
- **Performance** : Le calcul du hash est rapide même pour les gros fichiers (lecture par chunks de 4KB)
- **Compatibilité** : Les anciens datasets sans checksums affichent un avertissement mais fonctionnent toujours
- **Cache** : Les fichiers `.npy` ne sont pas vérifiés (ils sont régénérés automatiquement depuis `.txt`)

---

**Dernière mise à jour** : Ajout du système de checksums pour garantir la reproducibility entre différentes machines

