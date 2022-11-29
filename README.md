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

Docker, Docker Compose

# Installation

1. Clone the repo:
`git clone https://github.com/AlexandrZhydyk/PartsOnlineStore.git`

2. Enter your API in config.js
# code block
const API_KEY = 'ENTER YOUR API';
3. Run the command:
  docker compose up --build
