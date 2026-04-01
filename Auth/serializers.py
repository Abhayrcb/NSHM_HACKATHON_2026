from rest_framework import serializers
from .models import User
import re
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['first_name','last_name','email','mobile','username','password1','password2','role']
        
    def validate(self,attr):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=(?:.*[0-9]){2,})(?=.*[#\$@])[a-zA-Z0-9#@\$]{8,}$'
        print(attr.get("password1"))
        if len(attr.get('password1'))<8:
            raise serializers.ValidationError("password length must be 8 characters")
        if attr.get("password1") != attr.get('password2'):
            raise serializers.ValidationError("Both password must be same")
        
        if not re.match(pattern,attr.get('password1')):
            raise serializers.ValidationError("Password is week")
        
        return attr
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email is already registered")
        return value
    
    def validate_mobile(self,value):
        pattern = '^[6-9]\d{9}'
        if not re.match(pattern,value):
            raise serializers.ValidationError("please enter a valid mobile number")
        return value
    
    
    
    def save(self):
        email= self.validated_data.get("email")
        username = self.validated_data.get("username")
        password = self.validated_data.get("password1")
        # self.validated_data.pop("password2")
        
        user = User.objects.create(
            email=email,
            username=username,
            first_name = self.validated_data.get("first_name"),
            last_name = self.validated_data.get("last_name"),
            mobile = self.validated_data.get("mobile"),
            role =  self.validated_data.get("role"),
        )
        user.set_password(password)
        
        user.save()
        return user