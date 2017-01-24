from sqlalchemy import create_engine
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
import datetime

# Tells our program which database engine we want to communicate with.
engine = create_engine('sqlite:///puppyshelter.db')

# Make connection between class definitions and tables in the database.
Base.metadata.bind = engine

# Establish link between our code executions and the engine we just created.
# CRUD operations in SQLAlchemy are performed within a session.
# Sessions allow us to write down all the commands we want to execute but
# won't send them to the database until we commit
DBSession = sessionmaker(bind=engine)

session = DBSession()


def query_one():
    """Query all of the puppies and return the results in
    ascending alphabetical order.
    """
    results = session.query(Puppy.name).order_by(Puppy.name).all()
    for x in results:
        print(x[0])


def query_two():
    """Query all of the puppies that are less than 6 months old organized
    by the youngest first
    """
    today = datetime.date.today()
    if passesLeapDay(today):
        sixMonthsAgo = today - datetime.timedelta(days = 183)
    else:
        sixMonthsAgo = today - datetime.timedelta(days = 182)
    result = session.query(Puppy.name, Puppy.dateOfBirth)\
        .filter(Puppy.dateOfBirth >= sixMonthsAgo)\
        .order_by(Puppy.dateOfBirth.desc())

    # print the result with puppy name and dob
    for item in result:
        print "{name}: {dob}".format(name=item[0], dob=item[1])


def query_three():
    """Query all puppies by ascending weight
    """
    results = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight).all()
    for x in results:
        print(x[0], x[1])


def query_four():
    """Query all puppies grouped by the shelter in which they are staying"""
    result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    for item in result:
        print item[0].id, item[0].name, item[1]


# Helper Methods
def passesLeapDay(today):
    """
    Returns true if most recent February 29th occured after or exactly 183 days ago (366 / 2)
    """
    thisYear = today.timetuple()[0]
    if isLeapYear(thisYear):
        sixMonthsAgo = today - datetime.timedelta(days = 183)
        leapDay = datetime.date(thisYear, 2, 29)
        return leapDay >= sixMonthsAgo
    else:
        return False


def isLeapYear(thisYear):
    """
    Returns true iff the current year is a leap year.
    Implemented according to logic at https://en.wikipedia.org/wiki/Leap_year#Algorithm
    """
    if thisYear % 4 != 0:
        return False
    elif thisYear % 100 != 0:
        return True
    elif thisYear % 400 != 0:
        return False
    else:
        return True


if __name__ == "__main__":
    query_one()
    query_two()
    query_three()
    query_four()
