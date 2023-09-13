# migrer:

```shell
python manage.py makemigrations
python manage.py migrate
```

# Start sapp

```shell
python manage.py runserver
```

# Start Django shell

```shell
python manage.py shell.objects
```

# Annuler makemigrations

```shell
python manage.py showmigrations
python manage.py migrate <appname> <migration_name>rm listings/migrations/0006_band_like_new.py


python manage.py makemigrations --merge
```
