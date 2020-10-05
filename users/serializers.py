from rest_framework import serializers
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def save(self):
        user = User(
            email=self.data['email'],
            username=self.data['username'],
            phone=self.data['phone']
        )
        password = self.data['password']
        user.set_password(password)
        user.save()
        return user
