# Contact List REST API

A REST api to be consumed by a mobile app, which is somewhat similar to various popular apps
which tell you if a number is spam, or allow you to find a person’s name by searching for their phone
number.

## Points:

A user can register with at least name and phone number, along with a password, before
using. He can optionally add an email address.

Only one user can register on the app with a particular phone number.

A user needs to be logged in to do anything; there is no public access to anything.

Token Authorization is used to authorize users. After loggin in, the user is returned with a token key which the user has to provide while accessing the apis.

## API Functions:

### Search

A user can search for all his contacts.

A user can search for a person by name in the global database. Search results display the name,
phone number and spam likelihood for each result matching that name completely or partially.

A user can search for a person by phone number in the global database. If there is a registered
user with that phone number, only shows that result. Otherwise, shows all results matching that
phone number completely.

Clicking a search result (in front-end) displays all the details for that person along with the spam likelihood. But
the person’s email is only displayed if the person is a registered user and the user who is
searching is in the person’s contact list.

### Spam 

A user is able to mark a number as spam so that other users can identify spammers via
the global database. The number may or may not belong to any registered user or
contact - it could be a random number.

## Instructions to run:

Install dependencies from requirements.txt -> `pip install -r requirements.txt`

Make migrations -> `python manage.py makemigrations`

Migrate -> `python manage.py migrate`

To populate the database -> `python manage.py populate`
(this will populate the database with 3 users and 6 unregistered contacts)

Run Server -> `python manage.py runserver`
