POSTGRES_USER="secureweb"
POSTGRES_PASSWORD="l9a3fvbgjf341gfa22acd09"
POSTGRES_URI="localhost:9998"

DATABASE_NAME="secureweb"
DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URI}/{DATABASE_NAME}"

class Config(object):
    APP_NAME = "Woo-Capstone"
