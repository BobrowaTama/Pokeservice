from setuptools import setup, find_packages


requires = [
    'flask',
    'click',
    'flask-restful',
    'webargs',
    'SQLAlchemy',
    'SQLAlchemy-Utc',
    'psycopg2',
    'flask_sqlalchemy_session',
    'requests',
]


extras_require = {
    'tests': [
        'pytest',
        'pytest-flask',
    ],
    'deploy': [
        'cookiecutter',
    ]
}


setup(
    name='pokeservice',
    version='0.0',
    description='pokeservice',
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=extras_require,
    entry_points={
        'flask.commands': [
            'init_db=pokeservice.cli:init_db'
        ],
    },
)
