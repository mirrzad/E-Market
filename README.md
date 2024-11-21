<!-- ABOUT THE PROJECT -->
## About The Project

E-commerce platform using Django REST Framework where users can interact with the online store through JSON APIs. This project covers API development for product browsing, cart management, checkout and order processing.


<!-- GETTING STARTED -->
## Getting Started

To get this repository, run the following command inside your git enabled terminal.
  ```sh
  git clone https://github.com/mirrzad/E-Market
  ```

<!-- Setup -->
## Setup

Create an enviroment in order to keep the repo dependencies seperated from your local machine.

 ```sh
  python -m venv venv
  ```
Make sure to install the dependencies of the project through the requirements.txt file.
 ```sh
  pip install -r requirements.txt
  ```
Once you have installed django and other packages, go to the cloned repo directory
and run the following command

 ```sh
  python manage.py makemigrations
  ```

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command

 ```sh
  python manage.py migrate
  ```

Now we just need to start the server and then we can start using application. 
Start the server by following command

 ```sh
  python manage.py runserver
  ```

Once the server is up and running, head over to http://127.0.0.1:8000 to launch the App.

 
