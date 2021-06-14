# restaurant_backend


### Set up in local development:
 - Install Macos dependencies
 ```bash
brew install postgresql 
```
 - Create virtualenv and install requirements
 ```bash
pip3 install virtualenv
python3 -m virtualenv .venv -p python3
source .venv/bin/activate
pip install -r requirements.txt
```
- Run postgres database in docker container
```bash
docker-compose up -d postgres
```


### To access swagger page
```bash
localhost:8080/v0/ui # local environment
```

### To upgrade database
```bash
export SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/postgres
export FLASK_APP=app:flask_app
flask db upgrade
flask db migrate -m 'message'
flask db upgrade
# REMEMBER TO CHECK IN THE MIGRATION FILES
```
###Run program 
```bash
export FLASK_APP=app:flask_app
python app.py
#ex: http://localhost:8080/v0/ui/
```