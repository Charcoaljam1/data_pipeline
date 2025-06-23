import yaml
import os

def load_config_file(filepath:str):
    """Helper to load a single YAML file"""

    try:
        with open(filepath,'r') as f:
            content = yaml.safe_load(f)
            return content if content is not None else {} # Ensure it returns a dict, not None for empty files
    except FileNotFoundError:
        print(f"Warning: Config file not found at '{filepath}'. Returning empty config.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in '{filepath}': {e}. Returning empty config.")
        return {}
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred loading config file '{filepath}': {e}. Returning empty config.")
        return {}


def get_pipeline_config(environment: str = "dev"):
    """Load the pipeline configuration based on the environment."""

    file_path_mapping = {
        "dev": "development.yaml",
        "staging": "staging.yaml",
        "prod": "production.yaml"
    }

    config_dir = "config"
    env_dir = "environments"
    service_dir = "services"
    env_filename = file_path_mapping.get(environment)
    

    env_filepath = os.path.join(config_dir, env_dir, env_filename)

    env_config = load_config_file(env_filepath)

    services = env_config.get('active_services',[])

    for service in services:
        service_filename = f"{service}.yaml"
        service_filepath = os.path.join(config_dir, service_dir, service_filename)
        env_config[f'{service}'] = load_config_file(service_filepath)

    return env_config