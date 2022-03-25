from rest_framework import serializers

from api.models import User, Contacts


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["name","password", "phno", "email"]
        extra_kwargs = {
            "name": {"required": True},
            "phno": {"required": True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            phno=validated_data["phno"],
            name=validated_data["name"],
            email=validated_data.get("email")
        )

        user.set_password(validated_data["password"])
        user.save()

        Contacts.objects.create(
            name = validated_data.get("name"),
            phno = validated_data.get("phno"),
            #email = validated_data.get("email"),
            #is_registered = True,
            whose_contact = user
        )

        return user

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ["name","phno", "is_spam", "id"]