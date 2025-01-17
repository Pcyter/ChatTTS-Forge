import argparse
import os
import dotenv
from fastapi import FastAPI

from modules.api.api_setup import (
    process_api_args,
    process_model_args,
    setup_api_args,
    setup_model_args,
    setup_uvicon_args,
)
from modules.api.app_config import app_description, app_title, app_version
from modules import config
from modules.utils.torch_opt import configure_torch_optimizations

dotenv.load_dotenv(
    dotenv_path=os.getenv("ENV_FILE", ".env.api"),
)
parser = argparse.ArgumentParser(
    description="Start the FastAPI server with command line arguments"
)
setup_api_args(parser)
setup_model_args(parser)
setup_uvicon_args(parser)

args = parser.parse_args()

app = FastAPI(
    title=app_title,
    description=app_description,
    version=app_version,
    redoc_url=None if config.runtime_env_vars.no_docs else "/redoc",
    docs_url=None if config.runtime_env_vars.no_docs else "/docs",
)

process_model_args(args)
process_api_args(args, app)

configure_torch_optimizations()
