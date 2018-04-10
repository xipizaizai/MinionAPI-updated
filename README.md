# MinionAPI-updated

This is a basic Flask API framework for the backend services for the minion character.
It should provide persistent storage, core services and REST CRUD access to data.
- The Flask-RESTPLUS framework is used on top of Flask to provide REST API and Swagger support.
- mongoengine is used as a Document Object Mapper.  This is a wrapper for the pymongo library.

### References:

- https://docs.mongodb.com/
- http://mongoengine.org/
- http://flask-restplus.readthedocs.io/en/stable/

### PyCharm Setup Notes:

- Add the following environment variable to the testing config:
    + FLASK_ENV=test
    + FLASK_CONFIG=config.TestingConfig

- Add contents roots and source roots to PYTHONPATH
    
- Set the src and src/minionapi as source folders under 
    + Preferences/Project/Project Structure
   
- Ensure that mongodb is running locally
- Ensure that all unit tests are successfully passing

### REST API

The URL for the REST API is:

- http://127.0.0.1:5000/api
