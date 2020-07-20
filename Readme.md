

# Run

## Local

```
python manage.py db upgrade
python manage.py runserver
```

## With Docker
```
docker build -t intelias . 
docker run -p "5000:5000" intelias
```
