# party/serializers.py
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CurrentUserDefault, CharField
from django.contrib.auth import get_user_model

from .models import User

class UserSerializer(ModelSerializer):

    image = SerializerMethodField('get_image_full_src')

    def get_image_full_src(self,user):
        if user.image is None or user.image == '':
            return '/images/no_profile_img.png'
        return os.path.join(settings.AWS_S3_ROOT,user.image)

    class Meta:
        model = get_user_model()
        #fields = '['name','image','is_active']'
        fields = '__all__'
