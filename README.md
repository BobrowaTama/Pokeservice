Setup
=====

- `deployment_scripts/initialize_target_config_set.py`
- Then follow the instructions


Stack chosen
============

Application
-----------

* Flask web framework
  * Flask-RESTful for defining the resource-oriented views
  * Flask-SQLAlchemy-Session for SQLAlchemy integration
    - The minimalist approach
    - Flask-SQLAlchemy is more popular, but I feel it does too much behind
      the user's back and also unnecessarily ties access to the ORM models
      with the Flask application context.

* Requests - for querying external HTTP API-s

* SQLAlchemy ORM

* PostgreSQL


Testing
-------

* Pytest


Deployment
----------

* Docker containers
  * Debian as a base
    - Alpine seems to be popular, but can cause problems for Python applications
      because of it's libc implementation:
      - See: https://pythonspeed.com/articles/alpine-docker-python/

  * Multistage build
    - Building Python Wheels in separate container
      - Provides clean separation between build and runtime images
