# Item Catalog

Welcome to my implementation of the Item Catalog app. This app lists various sporting goods by category. Users can register by signing through an OAuth provider like Google or Facebook, where they gain access to create new items, and edit/delete items they've created.

The app uses the Bootstrap front-end framework, and Flask for the back-end. Data is stored in an SQLite database with the SQLAlchemy ORM interface.

## Running locally

1. Install [Vagrant](https://www.vagrantup.com/).
2. Clone the repository to your computer.
3. Unpack and `cd` into the root of the repository.
4. Execute `vagrant up` to download and install the VM.
5. Execute `vagrant ssh` to log into the VM.
6. Execute `cd vagrant/catalog/app` to navigate to the app folder.
7. Create the database by executing `python models.py`.
8. Populate the database with sample data by executing `python populate_db.py`.
9. Execute `cd ..` to change into the parent directory.
10. Execute `python run.py` to run the app.
11. Browse to `localhost:5000` to use the app

## API endpoints

The app includes a JSON endpoint for viewing item details based on category. This can be accessed at `/<category>/JSON` where `<category>` is the name of the category for which items are to be retrieved. For example, if you want to retrieve details of all items in the `Snowboarding` category, the URL would be `/Snowboarding/JSON`.