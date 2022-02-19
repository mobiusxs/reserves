import pathlib

ROOT = pathlib.Path(__file__).parent.parent
DATABASE_PATH = ROOT / 'db.sqlite'
ENV_PATH = ROOT / '.env'
JWT_FILE_PATH = ROOT / 'jwt.json'
TEMPLATES_PATH = ROOT / 'templates'
