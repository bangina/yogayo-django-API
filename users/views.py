from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from .models import User
from users.serializers import RegistrationSerializer, UserSerializer
from rest_framework.parsers import FileUploadParser


@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered a new user.'
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)

# 유저 개인 정보 조회


class UserView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        id = self.request.user.id
        return User.objects.filter(id=id)


class UserUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = UserSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
