from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

class ObtainTokenPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(ObtainTokenPairSerializer, cls).get_token(user)

        token["username"] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    conf_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("conf_password"):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs    
    def create(self, validate_data):
        # user = User.objects.create(
        #     username = validate_data["username"], 
        #     email = validate_data["email"], 
        #     password = validate_data["password"],
        #     first_name = validate_data["first_name"],
        #     last_name = validate_data["last_name"],
        # )

        # user.set_password(validate_data['password'])
        user = User.objects.create_user(validate_data["username"], validate_data["email"], validate_data["password"])
        user.first_name = validate_data.get("first_name", "")
        user.last_name = validate_data.get("last_name", "")
        user.save()

        return user
    
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    conf_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['password', 'conf_password', 'old_password'] 

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("conf_password"):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value
    
    def update(self, instance, validated_data):
        # instance.set_password(validated_data["password"])  
        instance.set_password(validated_data["password"])
        instance.save()
        print(instance)
        return instance