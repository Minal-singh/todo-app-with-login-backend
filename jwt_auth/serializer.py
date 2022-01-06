from rest_framework import serializers,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from testapp.models import CustomUser

#User serializzer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email']


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = CustomUser
        fields = ('email','username','password','password2')
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['email'],validated_data['username'],     
        password = validated_data['password'] )
        return user

#Change Password Serializer
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    password2 = serializers.CharField(write_only=True,required=True)
    old_password = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password','password','password2')
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})
        return attrs

    def validate_old_password(self,value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password":"Old Password is not correct"})
        return value

    def update(self,instance,validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()
        return instance


#Update Profile Serializer
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','email')

    def validate_email(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self,attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            return Response(status=status.HTTP_205_RESET_CONTENT)