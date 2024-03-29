from rest_framework import serializers
from .models import User
from common.utils import otp, validators
from django.core.cache import cache


# Signup
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    gender = serializers.CharField(max_length=1)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email', 'password', 'msg_token']

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        gender = attrs.get('gender')
        email = attrs.get('email')
        password = attrs.get('password')
        msg_token = attrs.get('msg_token')

        # validations checks
        if validators.is_empty(first_name) or not validators.atleast_length(first_name, 3) or validators.contains_script(first_name):
            raise serializers.ValidationError({'first_name': 'First name must contains atleast 3 characters.'})

        if validators.is_empty(last_name) or not validators.atleast_length(last_name, 2) or validators.contains_script(last_name):
            raise serializers.ValidationError({'last_name': 'Last name must contains atleast 2 characters.'})

        if validators.is_empty(gender) or not validators.atleast_length(gender, 1):
            raise serializers.ValidationError({'gender': 'Gender Must be specified.'})

        if not validators.is_email(email):
            raise serializers.ValidationError({'email': 'Invalid Email'})

        if not validators.atleast_length(password, 8) or not validators.atmost_length(password, 32) or not validators.is_password(password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})
        
        if type(msg_token) is not str:
            raise serializers.ValidationError({'token': 'Invalid message token.'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'account': f'Account already exists with this email {email}. Try with another email.'})

        if cache.get(email):
            raise serializers.ValidationError({'email': 'Please, Try signup again after 10 minutes.'})
        
        return attrs


# Otp Verification
class VerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ['otp']

    def validate(self, attrs):
        entered_otp = attrs.get('otp')
        hashed_otp = self.context.get('hashed_otp')

        # validations checks
        if validators.is_empty(entered_otp) or not validators.is_equal_length(entered_otp, 6):
            raise serializers.ValidationError({'otp': 'OTP must be of 6 digit number.'})
        
        if not otp.compare(entered_otp, hashed_otp):
            raise serializers.ValidationError({'otp': 'Invalid OTP.'})

        return attrs


# Login
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password', 'msg_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        msg_token = attrs.get('msg_token')

        # validations checks
        if not validators.is_email(email):
            raise serializers.ValidationError({'email': 'Invalid Email'})

        if not validators.atleast_length(password, 8) or not validators.atmost_length(password, 32) or not validators.is_password(password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})

        if type(msg_token) is not str:
            raise serializers.ValidationError({'token': 'Invalid message token.'})

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'account': 'No account found.'})

        user = User.objects.get(email=email)
        if not user.is_signed:
            raise serializers.ValidationError({'account': 'Something went wrong!'})

        if not user.is_active:
            raise serializers.ValidationError({'account', 'Your account has been deactivated.'})
        
        return attrs


# Password Recovery
class PasswordRecoverySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        # validations checks
        if not validators.is_email(email):
            raise serializers.ValidationError({'email': 'Invalid Email'})

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'account': 'No account found.'})

        self.user = User.objects.get(email=email)
        if not self.user.is_signed:
            raise serializers.ValidationError({'account': 'Something went wrong!'})

        if not self.user.is_active:
            raise serializers.ValidationError({'account', 'Your account has been deactivated.'})

        return attrs


# Password Recovery New Password
class PasswordRecoveryNewPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def validate(self, attrs):
        password = attrs.get('password')

        # validations checks
        if not validators.atleast_length(password, 8) or not validators.atmost_length(password, 32) or not validators.is_password(password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})
        
        return attrs


# Email Change
class EmailChangeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        # validations checks
        if not validators.is_email(email):
            raise serializers.ValidationError({'email': 'Invalid Email'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'account': 'Email already in use'})

        return attrs


# Change Password
class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['password', 'new_password']

    def validate(self, attrs):
        password = attrs.get('password')
        new_password = attrs.get('new_password')

        # validations checks
        if not validators.atleast_length(password, 8) or not validators.atmost_length(password, 32) or not validators.is_password(password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})
        
        if not validators.atleast_length(new_password, 8) or not validators.atmost_length(new_password, 32) or not validators.is_password(new_password):
            raise serializers.ValidationError({'password': 'Password must be of 8 to 32 character, contains atleast one number and one character.'})
        
        if not self.context.get('user').check_password(password):
            raise serializers.ValidationError({'password': 'Current password is Invalid.'})
        
        return attrs


# Change Username
class ChangeUserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        # validations checks
        if validators.is_empty(first_name) or not validators.atleast_length(first_name, 3) or validators.contains_script(first_name):
            raise serializers.ValidationError({'first_name': 'First name must contains atleast 3 characters.'})

        if validators.is_empty(last_name) or not validators.atleast_length(last_name, 2) or validators.contains_script(last_name):
            raise serializers.ValidationError({'last_name': 'Last name must contains atleast 2 characters.'})
        
        return attrs


# User FCM Serializer
class UserFCMessagingTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['msg_token']

    def validate(self, attrs):
        msg_token = attrs.get('msg_token')

        if validators.is_empty(msg_token):
            raise serializers.ValidationError({'token': 'Invalid Messaging Token.'})

        return attrs


# User Update Profile Photo
class ProfilePhotoUpdateSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = User
        fields = ['photo']

    def validate(self, attrs):
        photo = attrs.get('photo')
        
        if photo is None:
            raise serializers.ValidationError({'user': 'Invalid Profile Pic.'})

        return attrs
