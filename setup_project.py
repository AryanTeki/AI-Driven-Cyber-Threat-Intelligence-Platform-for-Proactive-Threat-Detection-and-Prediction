import os
import shutil

def create_directory_structure():
    """Create the project directory structure"""
    directories = [
        'app',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/templates',
        'app/config',
        'app/auth',
        'app/utils',
        'app/monitoring',
        'app/ml',
        'app/integrations',
        'app/models',
        'reports',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file):
            open(init_file, 'a').close()

if __name__ == "__main__":
    create_directory_structure()
    print("Project structure created successfully!") 