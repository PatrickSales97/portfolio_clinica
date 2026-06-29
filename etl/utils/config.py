import os

PROJECT_ROOT = '/app'

def get_data_path(rel_path):
    return os.path.join(PROJECT_ROOT, 'data', rel_path)