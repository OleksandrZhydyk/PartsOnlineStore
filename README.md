# PartsOnlineStore

App for searching and buying spare parts.

The application has an open and closed part of the functionality for registered users.
User registration can be done by sending a message to the email address specified by the user or via google account.

An unregistered user in the app can:
1) search for the necessary spare parts using the search field and the selected search criterion;
2) use preset search filters by sections;
3) search by category or models, adjust the quantity of goods before adding to the basket;
4) view the full information about the product, as well as the stores where the product is available, on which models of machines it is used;
5) view comments of other users about the product;
5) view the contents of the basket and make final changes to the quantity of goods or delete the position;

A registered user in the app can:
1) do all the steps above;
2) leave a comment under the product;
2) complete the order of goods by providing contact details and order data;
3) view the own history of orders, as well as their contents;

# Prerequisites

Docker, Docker Compose must be installed.
If not, please see:

[Docker](https://docs.docker.com/engine/install/) and
[Docker compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
for installation instructions.


# Installation

1. Clone the repo:
```sh
git clone https://github.com/AlexandrZhydyk/PartsOnlineStore.git
```

# Usage
1. Add app configuration to your .env file in the root of your project:
```sh
MODE=prod
DJANGO_SETTINGS_MODULE=config.settings.${MODE}

LOCAL_PORT=YOUR_LOCAL_PORT
WSGI_PORT=YOUR_WSGI_PORT

POSTGRES_DB=YOUR_DATABASE_NAME
POSTGRES_PASSWORD=YOUR_DATABASE_PASSWORD
POSTGRES_USER=YOUR_DATABASE_USER

POSTGRES_HOST=postgres
POSTGRES_PORT=5432

PGADMIN_DEFAULT_EMAIL=YOUR_PGADMIN_EMAIL
PGADMIN_DEFAULT_PASSWORD=YOUR_PGADMIN_PASSWORD

EMAIL_HOST_USER=YOUR_EMAIL_HOST
EMAIL_HOST_PASSWORD=YOUR_EMAIL_HOST_PASSWORD

GOOGLE_MAPS_API_KEY=YOUR_GOOGLE_API_KEY
```

2. Run the command for building and running the images:
```sh
docker compose up -d --build
```

3. Fill the database with preloaded data:
```sh
docker compose exec backend bash
python src/manage.py loaddata db.json
```
4. Finaly you will be able to access the web app via http://localhost on your host machine.
   
