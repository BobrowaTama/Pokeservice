import os


DB_CONFIG = dict(
    sa_url='postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}'.format(
        POSTGRES_USER=os.environ['POSTGRES_USER'],
        POSTGRES_DB=os.environ['POSTGRES_DB'],
        POSTGRES_PASSWORD=os.environ['POSTGRES_PASSWORD'],
    )
)
