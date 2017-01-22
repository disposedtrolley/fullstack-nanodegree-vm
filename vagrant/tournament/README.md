# Tournament Results

This is my attempt at the Tournament Results project of Udacity's Full Stack course. The project involves building a simple database to house the details of players and matches taking place in a tournament. Queries and Python functions were written to pair these players into matches based on the [Swiss pairing system](https://en.wikipedia.org/wiki/Swiss-system_tournament).

We've used the PostgreSQL database running in a Vagrant virtual machine for this project.

## Running locally

1. Clone this repo to your machine.
2. Ensure Vagrant is [installed](https://www.vagrantup.com/docs/installation/).
3. Open up a terminal and `cd` into the `/vagrant` directory of the cloned repo.
4. Execute `vagrant up` to download and install the virtual machine.
5. Execute `vagrant ssh` to log into the virtual machine.
6. Once in the virtual machine, `cd` into the `/vagrant/tournament` directory.
7. Execute `psql` to launch the PostgreSQL console.
8. Execute `\i tournament.sql` to run the SQL script which will set up the database.
9. Execute `\q` to quit the PostgreSQL console.
10. Execute `python tournament_test.py` to run the unit tests for each function.