import numpy as np
import pandas as pd
import os


class DFS:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        

    def read_file(self, dataset,file_path):
        full_path = os.path.join(self.root_dir, dataset,file_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File {full_path} does not exist.")
        return pd.read_csv(full_path)

    def write_file(self, file_path, data_frame):
        full_path = os.path.join(self.root_dir, file_path)
        data_frame.to_csv(full_path, index=False)

    def get_root_dir(self):
        return self.root_dir
