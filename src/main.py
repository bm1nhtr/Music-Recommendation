"""
Point d'entrée principal pour les algorithmes graph classiques
"""
import argparse
import os
from dfs import DFS
from graph_loader import load_kg, load_ratings, get_user_history
from graph_visualizer import visualize_graph_structure, visualize_all_relations, print_graph_statistics


# Configuration par défaut
DATA_PATH = '../final_data'  # Chemin vers les données traitées
RAW_DATA_PATH = '../rawdata'  # Chemin vers les données brutes
DEFAULT_DATASET = 'music'


def main():
    parser = argparse.ArgumentParser(description='Graph Algorithms: BFS, Dijkstra, Prim')
    parser.add_argument('--dataset', type=str, default=DEFAULT_DATASET,
                       help='Dataset name (e.g., music, movie, product)')
    parser.add_argument('--algorithm', type=str, default='bfs',
                       choices=['bfs', 'dijkstra', 'prim'],
                       help='Algorithme à utiliser')
    parser.add_argument('--max_hops', type=int, default=2,
                       help='Nombre maximum de hops pour BFS')
    parser.add_argument('--user_id', type=int, default=0,
                       help='ID de l\'utilisateur à analyser')
    parser.add_argument('--visualize', action='store_true',
                       help='Visualiser le graphe')
    parser.add_argument('--max_nodes', type=int, default=100,
                       help='Nombre maximum de nœuds à visualiser')
    parser.add_argument('--use_small', action='store_true',
                       help='Utiliser le dataset réduit (kg_final_small.txt)')
    
    args = parser.parse_args()
    
    # # Charger le graphe (retourne maintenant metadata aussi)
    # print(f"Chargement du graphe pour le dataset: {args.dataset}")
    n_entity, n_relation, kg, metadata = load_kg(DATA_PATH, args.dataset, use_small=args.use_small)
    
    # # Utiliser metadata pour déterminer le type de dataset
    # if metadata:
    #     dataset_type_str = "FILTRÉ" if metadata.get('type') == 'filtered' else "COMPLET"
    #     print(f"Type de dataset détecté: {dataset_type_str}")
    #     if metadata.get('filtered'):
    #         print(f"  - Paramètres de filtrage:")
    #         print(f"    * Max users demandé: {metadata.get('max_users_requested', 'N/A')}")
    #         print(f"    * Max artists demandé: {metadata.get('max_artists_requested', 'N/A')}")
    #         print(f"  - Valeurs réelles après filtrage:")
    #         print(f"    * Users réels: {metadata.get('n_users_actual', 'N/A')}")
    #         print(f"    * Artists réels: {metadata.get('n_artists_actual', 'N/A')}")
    # else:
    #     # Fallback si pas de metadata
    #     is_filtered = args.use_small or n_entity < 500
    #     metadata = {
    #         'type': 'filtered' if is_filtered else 'full',
    #         'n_entity': n_entity,
    #         'n_relation': n_relation
    #     }
    
    # # Créer info dataset pour la visualisation
    # dataset_info = {
    #     'type': metadata.get('type', 'full'),
    #     'n_entity': n_entity,
    #     'n_relation': n_relation,
    #     **metadata  # Inclure toutes les métadonnées
    # }
    
    # # Afficher les statistiques du graphe
    # print_graph_statistics(kg, dataset_info)
    
    # # Charger les ratings (optionnel)
    # try:
    #     ratings = load_ratings(DATA_PATH, args.dataset, use_small=args.use_small)
    #     user_history = get_user_history(ratings)
    #     print(f"Ratings chargés pour {len(user_history)} utilisateurs")
    # except Exception as e:
    #     print(f"Impossible de charger les ratings: {e}")
    #     user_history = {}
    
    # # Visualiser le graphe si demandé
    # if args.visualize:
    #     print("\n=== Génération des visualisations ===")
        
    #     output_dir = f'../final_data/{args.dataset}'
    #     os.makedirs(output_dir, exist_ok=True)
        
    #     # 1. Visualisation de la structure générale
    #     print("\n1. Visualisation de la structure générale du graphe...")
    #     visualize_graph_structure(kg, 
    #                              output_file=os.path.join(output_dir, 'graph_structure.png'),
    #                              dataset_info=dataset_info,
    #                              max_nodes=args.max_nodes)
        
    #     # 2. Visualisations par type de relation
    #     print("\n2. Visualisations par type de relation...")
    #     visualize_all_relations(kg, 
    #                            output_dir=output_dir,
    #                            dataset_info=dataset_info,
    #                            max_nodes=args.max_nodes)
    
    #TODO: Implement the algorithm
    # Les algorithmes qu'on a fait : BFS, Dijkstra, Prim, etc...
    test = DFS(DATA_PATH)
    print(f"DFS initialized with root directory: {test.get_root_dir()}")
    df = test.read_file(DEFAULT_DATASET,"kg_final.txt")
    print(f"Data read from file:\n{df.head()}")
    print(n_entity, n_relation)
    print(kg)


if __name__ == '__main__':
    main()
