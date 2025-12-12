"""
Module pour charger et construire le graphe de connaissances
Séparé du code ML/recommendation pour se concentrer sur les algorithmes graph classiques
"""
import collections
import os
import numpy as np


def load_dataset_metadata(dataset_path, dataset_name='music'):
    """
    Charger les métadonnées du dataset
    
    Returns:
        dict: Métadonnées du dataset ou None si pas de fichier
    """
    metadata_file = os.path.join(dataset_path, dataset_name, 'dataset_metadata.txt')
    if not os.path.exists(metadata_file):
        return None
    
    metadata = {}
    with open(metadata_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                # Convertir les valeurs booléennes et numériques
                if value.lower() == 'true':
                    metadata[key] = True
                elif value.lower() == 'false':
                    metadata[key] = False
                else:
                    try:
                        metadata[key] = int(value)
                    except ValueError:
                        metadata[key] = value
    return metadata


def load_kg(dataset_path, dataset_name='music', use_small=False):
    """
    Charger le graphe de connaissances depuis un fichier
    
    Args:
        dataset_path: Chemin vers le dossier final_data (ex: '../final_data')
        dataset_name: Nom du dataset (ex: 'music')
        use_small: Si True, utilise kg_final_small.txt au lieu de kg_final.txt (déprécié, utilise metadata)
    
    Returns:
        tuple: (n_entity, n_relation, kg, metadata)
            - n_entity: Nombre d'entités
            - n_relation: Nombre de relations
            - kg: Dictionnaire {head: [(tail, relation), ...]}
            - metadata: Dictionnaire avec métadonnées du dataset
    """
    print('Lecture du fichier KG ...')
    
    # Charger les métadonnées
    metadata = load_dataset_metadata(dataset_path, dataset_name)
    
    # Si metadata existe et indique filtered, on utilise le dataset filtré
    # Sinon, on utilise use_small flag (pour compatibilité)
    if metadata and metadata.get('filtered', False):
        print('Dataset filtré détecté depuis les métadonnées')
    
    suffix = '_small' if use_small else ''
    kg_file = os.path.join(dataset_path, dataset_name, f'kg_final{suffix}')
    
    if os.path.exists(kg_file + '.npy'):
        kg_np = np.load(kg_file + '.npy')
    else:
        kg_np = np.loadtxt(kg_file + '.txt', dtype=np.int32)
        np.save(kg_file + '.npy', kg_np)
    
    n_entity = len(set(kg_np[:, 0]) | set(kg_np[:, 2]))
    n_relation = len(set(kg_np[:, 1]))
    
    kg = construct_kg(kg_np)
    
    # Mettre à jour metadata avec les valeurs réelles
    if metadata is None:
        metadata = {}
    metadata['n_entity'] = n_entity
    metadata['n_relation'] = n_relation
    metadata['type'] = 'filtered' if metadata.get('filtered', False) else 'full'
    
    print(f'Graphe de connaissances chargé: {n_entity} entités, {n_relation} relations')
    return n_entity, n_relation, kg, metadata


def construct_kg(kg_np):
    """
    Construire la structure du graphe depuis un array numpy
    
    Args:
        kg_np: Array numpy de shape (n_triples, 3) avec [head, relation, tail]
    
    Returns:
        Dictionnaire {head: [(tail, relation), ...]}
    """
    print('Construction du graphe de connaissances ...')
    kg = collections.defaultdict(list)
    for head, relation, tail in kg_np:
        kg[head].append((tail, relation))
    return kg


def load_ratings(dataset_path, dataset_name='music', use_small=False):
    """
    Charger les ratings utilisateur-item (optionnel, pour analyse)
    
    Args:
        dataset_path: Chemin vers le dossier final_data
        dataset_name: Nom du dataset
        use_small: Si True, utilise ratings_final_small.txt au lieu de ratings_final.txt (déprécié)
    
    Returns:
        Array numpy de shape (n_ratings, 3) avec [user_id, item_id, label]
    """
    print('Lecture du fichier de ratings ...')
    
    # Vérifier metadata pour savoir si dataset est filtré
    metadata = load_dataset_metadata(dataset_path, dataset_name)
    
    suffix = '_small' if use_small else ''
    rating_file = os.path.join(dataset_path, dataset_name, f'ratings_final{suffix}')
    
    if os.path.exists(rating_file + '.npy'):
        rating_np = np.load(rating_file + '.npy')
    else:
        rating_np = np.loadtxt(rating_file + '.txt', dtype=np.int32)
        np.save(rating_file + '.npy', rating_np)
    
    print(f'Ratings chargés: {rating_np.shape[0]} interactions')
    return rating_np


def get_user_history(ratings_np):
    """
    Extraire l'historique des utilisateurs depuis les ratings
    
    Args:
        ratings_np: Array numpy avec [user_id, item_id, label]
    
    Returns:
        Dictionnaire {user_id: [item_id, ...]} avec seulement les interactions positives (label=1)
    """
    user_history = collections.defaultdict(list)
    
    for user_id, item_id, label in ratings_np:
        if label == 1:  # Seulement les interactions positives
            user_history[user_id].append(item_id)
    
    return user_history

