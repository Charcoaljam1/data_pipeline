import yaml

def open_yaml(filepath:str):
    """Helper to load a single YAML file."""
    try:
        with open(filepath, 'r') as f:
            content = yaml.safe_load(f)
            return content if content is not None else {}
    except FileNotFoundError:
        print(f"Warning: YAML file not found at '{filepath}'. Returning empty dictionary.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in '{filepath}': {e}. Returning empty config.")
        return {}
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred loading config file '{filepath}': {e}. Returning empty config.")
        return {}



from pathlib import Path

def config_getter(environment:str = "development") -> dict:
    """
    Loads and merges configuration files based on the environment.
    
    Args:
        environment (str): The name of the environment (e.g., 'development', 'staging', 'production').
                           Defaults to 'development'.
    Returns:
        dict: A merged dictionary containing the full pipeline configuration.
    """

    config_mapping = {
        'development':'development.yaml',
        'staging':'staging.yaml',
        'production': 'production.yaml'
    }

    # The name of the directories
    CONFIG_DIR = Path('config')
    ENV_DIR = 'environments'
    SERVICE_DIR = 'services'

    # Load the base configuration
    base_config_dir = CONFIG_DIR / 'base.yaml'
    full_config = open_yaml(base_config_dir)

    env = config_mapping.get(environment)


    if not env:
        pass # Raise an error here. Fail fast and quickly

    config_path = CONFIG_DIR / ENV_DIR / env
    env_overrides = open_yaml(config_path) 

    full_config.update(env_overrides)

    if 'services' not in full_config:
        full_config['services'] = {}

    # Get the configuration for the necessary services
    active_services = full_config.get('active_services',[])
    for service in active_services:
        service_filename = f'{service}.yaml'
        serv_path = CONFIG_DIR / SERVICE_DIR / service_filename
        full_config['services'][service] = open_yaml(serv_path)

    return full_config