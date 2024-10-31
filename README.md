# Narvi example app

## Starting

To start application run:

    docker compose up -d
    docker compose run --rm migrate

After that you can visit http://127.0.0.1:8000/

To access admin panel, create superuser first:

    docker compose run --rm api createsuperuser

Then you can access http://127.0.0.1:8000/admin

Exercise 1 is available in `words/utils/word_grouping.py` or at extra action in http://127.0.0.1:8000/folders/group_words/.