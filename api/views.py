from sys import api_version
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from . models import User, Contacts
from . serializers import UserSerializer, ContactSerializer


# SHOWS ALL USERS AND CONTACTS
class usershow(APIView):

    def get(self, request):
        all_users = User.objects.all()
        all_contacts = Contacts.objects.all()
        serializer0 = UserSerializer(all_users, many = True)
        serializer1 = ContactSerializer(all_contacts, many = True)
        ret = {
            "Users" : serializer0.data,
            "Contacts" : serializer1.data
        }
        return Response(ret, status = status.HTTP_200_OK)

# ADDS USER - ACCEPTS NAME, PHNO, PASSWORD AND EMAIL (OPTIONAL)
class adduser(APIView):
    
    def post(self, request):

        # FETCHES REQUIRED DATA
        serializer = UserSerializer(data = request.data)

        # CHECKS IF DATA IS VALID AND SAVES THE USER
        if serializer.is_valid():
            serializer.save()

        else:
            return Response("Error", status = status.HTTP_400_BAD_REQUEST)

        return Response("User created", status = status.HTTP_201_CREATED)

# LOGS USER IN - ACCEPTS PHNO AND PASSWORD
class loginuser(APIView):

    def post(self, request):
        phno = request.data.get("phno")
        password = request.data.get("password")

        # FETCHES USER
        try:
            user = User.objects.get(phno = phno)

            # CHECKS PASSWORD
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user = user)

                # RETURNS AUTHORIZATION TOKEN
                return Response({"token" : token.key})

            # IF PASSWORD CHECK FAILS
            else:
                return Response("Bad password", status = status.HTTP_403_FORBIDDEN)

        # USER DOESNT EXIST
        except Exception as e:
            return Response("User not found", status = status.HTTP_404_NOT_FOUND)

# MARKS SPAM - ACCEPTS PHONE NUMBER
class markspam(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phno = request.data.get("phno")
    
        # FETCHING CONTACTS WITH PHNO
        contacts = Contacts.objects.filter(phno = phno) 

        # IF PHNO DOESNT EXIST
        if not contacts:
            return Response("No person with the provided credentials", status = status.HTTP_404_NOT_FOUND)

        # MARKING ALL CONTACTS WITH THE PHNO AS SPAM
        for contact in contacts:
            contact.is_spam = True
            contact.save()

        return Response("Number marked as spam", status = status.HTTP_200_OK)

# SEARCHES A USER BY NAME - ACCEPTS NAME
class namesearch(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")

        # FETCHING CONTACTS WHOSE NAME STARTS WITH SEARCH QUERY
        name_starts = Contacts.objects.filter(name__startswith = name)

        # FETCHING CONTACTS WHOSE NAMES CONTAIN BUT DONT START WITH SEARCH QUERY
        contains_name = Contacts.objects.filter(name__icontains = name).exclude(name__startswith = name)

        # IF NAME DOESNT EXIST
        if not name_starts and not contains_name:
            return Response("No person with the provided credentials", status = status.HTTP_404_NOT_FOUND)

        serializer0 = ContactSerializer(name_starts, many = True)
        serializer1 = ContactSerializer(contains_name, many = True)
    
        return Response(serializer0.data + serializer1.data, status = status.HTTP_200_OK)
            
# SEARCHES A USER BY PHNO - ACCEPTS PHNO
class phonesearch(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phno = request.data.get("phno")

        # CHECKING IF PHNO IS OF A REGISTERED USER
        try:
            user = User.objects.get(phno = phno)
            
            user = Contacts.objects.get(phno = phno, whose_contact = user)
            serializer = ContactSerializer(user)

        # CHECKING IF PHNO IS OF A CONTACT
        except:
            users = Contacts.objects.filter(phno = phno)

            # IF PHNO DOESNT EXIST
            if not users:
                return Response("User not found", status = status.HTTP_404_NOT_FOUND)

            serializer = ContactSerializer(users, many = True)
            
        return Response(serializer.data, status = status.HTTP_200_OK)

# ACCEPTS ID WHEN SEARCH RESULT IS CLICKED
class getcontactdetails(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # FETCHES CONTACT ID
        clicked_user_id = request.data.get("id")
        
        # CHECKS WHETHER PRVIDED ID IS VALID
        try:

            # FETCHES CONTACT'S DETAILS
            clicked_user = Contacts.objects.get(id = clicked_user_id)

            # GENERIC(WITHOUT EMAIL) DETAILS IF CONTACT ISNT A REGISTERED USER
            ret = {
                "name" : clicked_user.name,
                "phno" : clicked_user.phno,
                "is_spam" : clicked_user.is_spam,
            }

            try:
                searched_user = User.objects.get(phno = clicked_user.phno)

                contacts_list = Contacts.objects.filter(whose_contact = searched_user, phno = request.user.phno)

                if len(contacts_list) > 0:         
                    ret["email"] = searched_user.email

            except:
                print('Searched user is not registered')
                
            return Response(ret, status = status.HTTP_200_OK)
        
        except:
            return Response("No person found with the provided phone number", status = status.HTTP_404_NOT_FOUND)
            
# SEARCHES CONTACTS OF A USER
class contactsearch(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # FETCHES USERS CONTACTS EXCLUDING USER'S OWN ENTRY
        contact = Contacts.objects.filter(whose_contact__name = request.user) & Contacts.objects.exclude(phno = request.user.phno)

        serializer = ContactSerializer(contact, many = True)

        return Response(serializer.data)

def index(request):

    ret = "API LIST:\n\n" + "Get all User and Contact details - GET /global\n\n" + "Add User - POST /adduser - ACCEPTS NAME, PHNO, PASSWORD AND EMAIL (OPTIONAL)\n\n" +"Log in - POST /loginuser - ACCEPTS PHNO AND PASSWORD\n\n" + "Mark Spam - POST /markspam - ACCEPTS PHNO\n\n" + "Search by Name - POST /namesearch - ACCEPTS NAME\n\n" + "Search by Phone - POST /phonesearch - ACCEPTS PHNO\n\n" + "Advanced Search - POST /advancesearch - ACCEPTS ID\n\n" + "Search Contacts - GET /contactsearch"

    return HttpResponse(ret)