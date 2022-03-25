from django.core.management.base import BaseCommand, CommandError
from api.models import User, Contacts
from random import randint

from api.serializers import UserSerializer, ContactSerializer

# USERS DETAILS
users_list1 = [
    {
        "name": 'Aparna Murthy',
        'email': 'a@mail.com',
        'phno': '9999999901',
        'password':'qwe'
    },
    {
        "name": 'Aryan Ganguly',
        'email': 'b@mail.com',
        'phno': '9999999902',
        'password':'qwe'
    },

    {
        "name": 'Chanda Sandhu',
        'email': None,
        'phno': '9999999903',
        'password':'qwe'
    }
]

# CONTACTS DETAILS
contacts_list = [
    {
        "name": 'Isha Sane',
        'phno': '9999999904',
        'whose_contact': '9999999901'
    },
    {
        "name": 'Anup Tiwari',
        'phno': '9999999904',
        'whose_contact': '9999999901'
    },
    {
        "name": 'Anaya Anup',
        'phno': '9999999905',
        'whose_contact': '9999999902'
    },
    {
        "name": 'Sarvesh Karan',
        'phno': '9999999906',
        'whose_contact': '9999999902'
    },
    {
        "name": 'Aryan Sane',
        'phno': '9999999907',
        'whose_contact': '9999999903'
    },
    {
        "name": 'Sarvesh Tiwar',
        'phno': '9999999907',
        'whose_contact': '9999999903'
    }
]

# ADDING CONTACTS FOR TESTING ADVANCE SEARCH EX -
# SEARCHING ID OF ARYAN WITH APARNA'S TOKEN WILL GIVE EMAIL AS ARYAN HAS APARNA IN HER CONTACT
# SEARCHING ID OF CHANDA WITH APARNA'S TOKEN WILL NOT GIVE EMAIL AS CHANDA DOESNT HAVE APARNA IN HER CONTACT
advanced_contact_list = [
    {
        "name": 'Aparna M',
        'phno': '9999999901',
        'whose_contact': '9999999902'
    },
    {
        "name": 'Aryan G',
        'phno': '9999999902',
        'whose_contact': '9999999901'
    },
    {
        "name": 'Chanda Sandhu',
        'phno': '9999999903',
        'whose_contact': '9999999901'
    }
]


class Command(BaseCommand):
    help = "Populates the database with 3 Users and 9 Contacts (Total = 12)"

    def populate_users(self):
        for user in users_list1:
            print(user)
            serialized_user = UserSerializer(data = user)

            if serialized_user.is_valid():
                user = serialized_user.save()

    def populate_contacts(self, contacts):
        for contact in contacts:

            contact_of = User.objects.get(phno = contact['whose_contact'])

            Contacts.objects.create(
                name = contact['name'],
                phno = contact['phno'],
                whose_contact = contact_of,
            )
    
    def handle(self, *args, **options):

        self.populate_users()

        self.populate_contacts(contacts_list)

        self.populate_contacts(advanced_contact_list)

        print("Data added")