from rest_framework import generics, permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from testapp.models import CustomUser
from .serializer import RegisterSerializer,ChangePasswordSerializer,UpdateUserSerializer,LogoutSerializer,UserSerializer

#Register View
class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]


    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({
            "refresh": str(token),
            "access": str(token.access_token)
        })

#Change Password View
class ChangePasswordView(generics.UpdateAPIView):

    def get_object(self,queryset=None):
        return self.request.user

    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer

#Update Profile View
class UpdateProfileView(generics.UpdateAPIView):

    def get_object(self,queryset=None):
        return self.request.user

    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class UserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,]

    serializer_class = UserSerializer

    def get_object(self,queryset=None):
        return self.request.user