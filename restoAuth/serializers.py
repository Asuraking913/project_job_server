from resto.models import User
from rest_framework_simplejwt import serializers

from resto.serializers import UserSerializer

class CustomTokenSerializer(serializers.TokenObtainPairSerializer):

    def get_token(data, user):
        # print(user)
        # print(data)

        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser


        return token
    
    def validate(self, attrs: serializers.Dict[str, serializers.Any]) -> serializers.Dict[str, str]:
        # print(self.user)
        data = super().validate(attrs)
        data['is_staff'] = self.user.is_staff
        data['is_admin'] = self.user.is_superuser

        
        return data
        
