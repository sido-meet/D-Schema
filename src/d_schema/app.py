from omegaconf import DictConfig, OmegaConf
import os
import sys
from hydra import initialize_config_dir, compose

# Use importlib.resources for robust path finding
if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

from .db_parser import DatabaseParser
from .structures import DatabaseSchema
from .generators.ddl_schema.generator import DDLSchemaGenerator
from .generators.m_schema.generator import MSchemaGenerator
from .generators.mac_sql_schema.generator import MacSQLSchemaGenerator
from .generators.profile_report.generator import ProfileReportGenerator

# A mapping from generator names to their classes
GENERATOR_CLASSES = {
    "ddl": DDLSchemaGenerator,
    "m_schema": MSchemaGenerator,
    "mac_sql": MacSQLSchemaGenerator,
    "profile_report": ProfileReportGenerator,
}

def run_generator(db_structure: DatabaseSchema, output_path: str, generator_cfg: DictConfig):
    """
    Initializes and runs a single generator based on its configuration.
    """
    # Convert the generator config to a standard python dict
    generator_params = OmegaConf.to_container(generator_cfg, resolve=True)
    gen_name = generator_params.pop("name")

    if gen_name not in GENERATOR_CLASSES:
        print(f"Warning: Generator '{gen_name}' not found. Skipping.")
        return

    print(f"Running generator: {gen_name}...")
    generator_class = GENERATOR_CLASSES[gen_name]

    # Pass the generator-specific config to its constructor
    generator_instance = generator_class(schema=db_structure, **generator_params)
    
    schema_content = generator_instance.generate_schema()
    
    # Define a unique output filename for each generator
    if gen_name == "ddl":
        output_filename = "schema.ddl"
    elif gen_name == "m_schema":
        output_filename = "schema.mschema"
    elif gen_name == "mac_sql":
        output_filename = "schema.macsql"
    elif gen_name == "profile_report":
        output_filename = "profile_report.md"
    else:
        output_filename = f"schema.{gen_name}.txt"

    file_path = os.path.join(output_path, output_filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(schema_content)
        
    print(f"Generator {gen_name} finished. Output written to {file_path}")

def main():
    """
    Main application entry point using programmatic Hydra initialization.
    This version handles a single generator run at a time.
    """
    # Find the absolute path to the config directory within the package
    config_path_ref = importlib_resources.files('d_schema') / 'config'
    
    with config_path_ref as config_path:
        # Initialize Hydra and compose the configuration
        with initialize_config_dir(config_dir=str(config_path), job_name="d_schema_app"):
            cfg = compose(config_name="config", overrides=sys.argv[1:])

            print("Starting D-Schema with configuration:")
            print(OmegaConf.to_yaml(cfg))

            # Determine if profiling is needed based on the selected generator
            should_profile = cfg.generator.name == 'profile_report'

            print(f"\nParsing database structure... (Profiling enabled: {should_profile}, Samples: {cfg.num_samples})")
            parser = DatabaseParser(cfg.db_url)
            db_structure = parser.parse(profile=should_profile, num_samples=cfg.num_samples)
            print("Database parsed successfully.")

            os.makedirs(cfg.output_path, exist_ok=True)
            
            run_generator(db_structure, cfg.output_path, cfg.generator)

if __name__ == "__main__":
    main()