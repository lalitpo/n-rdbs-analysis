# n-rdbs-analysis 📈

This project is developed to analyse and compare the efficiency of 
Relational Database systems, like Redis and Non-Relational Database
systems like Presto for query processing of large size data.


# Pre-requisite 🗞
You may download the data for this project from the following link:
https://dblp.org/xml/dblp.xml.gz

And place it in resource folder of the project before running it.

# Setting up PrestoDB

PREREQUISITE :

- Download, setup Docker Desktop(https://www.docker.com/products/docker-desktop/) on your local Machine and keep it running(launch the app).

PrestoDB is not a DB, it's a SQL query engine to connect to multiple datasources(SQLServer, mySQL, PostgresSQL, Oracle, etc.).
Here we are setting up first PostgresSQL first on our system as a background datasource/DB and then connect our application to Presto, which in turn do the transactions and perform SQL queries on PostgreSQL.

1. Download PostgresSQL docker image.
```
docker pull postgres
```
2. Run the postgres docker container for the local setup with default configuration as below

```
docker run --name postgres_DIMs -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p 5432:5432 postgres
```

3. Download PGAdmin4 client(https://www.pgadmin.org) to use Postgres Database through a UI.

4. Download Homebrew, if you already dont have on your system.
5. Run below command to install presto on your system.
```
brew install presto
```
Presto gets installed here(on MAC systems): /usr/local/Cellar/prestodb/

6. Go to Path : /usr/local/Cellar/prestodb/0.277/bin and start Presto
```
presto-server start

```
You'll see the Presto Web UI launched on http://localhost:8080 

7. Presto has different catalogs, which are nothing but the kind of booklet or close to datasources, some of which are by default created in presto related to memory, jmx, etc.
Property file for them are usually located in path /usr/local/Cellar/prestodb/0.277/libexec/etc/catalog. For the custom(user-defined) datasource that you are creating for yourself,
you have to write your own property file here for the connection of presto to the database/datasource that you have on your system running, in this example, Postgres.

8. Create postgres.properties in path : /usr/local/Cellar/prestodb/0.277/libexec/etc/catalog.
Add below contents in the properties file 
```
connector.name=postgresql
connection-url=jdbc:postgresql://localhost:5432/postgres
connection-user=admin
connection-password=admin
```

9. Rename the jar at location /usr/local/Cellar/prestodb/0.277/libexec to 'presto' and run below command :
```
./presto --server localhost:8080 --catalog postgres --schema public
```
Here, 'postgres' is the catalog name you gave in properties file with tag connector.name
and 'public' is the default schema created in a default database in PostgresSQL.

10. You will see a prompt like below : presto:public> 
    This is to enter commands and play with Presto like below.
11. If you want to see what all catalogs are available and connected in your local Presto, type:
```
show catalogs;
```
# Running the project 🚀
To run the project, you may use the following command:
```
python3 -m venv ve
source ve/bin/activate
pip install -r requirements.txt
```

then navigate to the script you want to run and run it using the following command:
```
python3 <script_name>.py
```

to exit the virtual environment, run the following command:
```
deactivate
```
