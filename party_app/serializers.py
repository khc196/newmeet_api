    # party/serializers.py
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CurrentUserDefault, CharField

from .models import *

class PartyTypeListSerializer(ModelSerializer):
    class Meta:
        model = PartyType
        fields =("id", "code", "name", "created_at")
        
class PlaceListSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = ("id", "code", "name", "latitude", "longitude", "address", "created_at")
class PartyLikeSerializer(ModelSerializer):
    class Meta:
        model = PartyLike
        fields = '__all__'
class PartyImageSerializer(ModelSerializer):
    class Meta:
        model = PartyImage
        fields = '__all__'
class PartyListSerializer(ModelSerializer):
    place_name = CharField(source='place.name', read_only=True)
    type_name = CharField(source='party_type.name', read_only=True)
    likes = PartyLikeSerializer(many=True, read_only=True)
    is_liked = SerializerMethodField('check_is_liked')
    party_image = SerializerMethodField('get_first_image')
    def get_first_image(self, party):
        images_queryset = PartyImage.objects.all().filter(party=party)
        return PartyImageSerializer(images_queryset.first()).data
    def check_is_liked(self, party):
        if hasattr(party,'is_liked'):
            return party.is_liked
        else:
            pass
        return 0
    class Meta:
        model = Party
        fields = ("id", "party_type", "type_name", "place", "place_name", "is_liked", "likes", "name", "party_image", "description", "view_count", "like_count", "comment_count", "can_buy_ticket",  "can_prepurchase", "start_datetime", "end_datetime", "is_hot", "created_at")
class PartyCreateSerializer(ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class PartyUpdateSerializer(ModelSerializer):
    class Meta:
        model = Party
        fields = ('name','description','images')

class PartyCommentListSerializer(ModelSerializer):
    user_name = CharField(source='user.name', read_only=True)
    class Meta:
        model = PartyComment
        fields = ('id', 'comment', 'created_at', 'party', 'user', 'user_name')

    
class PartyDetailSerializer(ModelSerializer):
    place_name = CharField(source='place.name', read_only=True)
    place_lat = CharField(source='place.latitude', read_only=True)
    place_lon = CharField(source='place.longitude', read_only=True)
    type_name = CharField(source='party_type.name', read_only=True)
    is_liked = SerializerMethodField('check_is_liked')
    party_comments = PartyCommentListSerializer(many=True, read_only=True)
    party_images = SerializerMethodField('get_images')
    def get_images(self, party):
        images_queryset = PartyImage.objects.all().filter(party=party)
        return PartyImageSerializer(images_queryset, many=True).data
    def check_is_liked(self, party):
        if hasattr(party,'is_liked'):
            return party.is_liked
        else:
            return 0
    class Meta:
        model = Party
        fields = ('id', 'name', 'place_name', 'place_lat', 'place_lon', 'type_name', 'is_liked', 'party_images', 'description', 'view_count', 'comment_count', 'like_count', 'can_prepurchase', 'can_buy_ticket', 'start_datetime', 'end_datetime', 'is_hot', 'party_comments', 'created_at', 'party_type')

class PlaceDetailSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'



class PartyCommentCreateSerializer(ModelSerializer):
    user_name = CharField(source='user.name', read_only=True)
    class Meta:
        model = PartyComment
        fields = ('id', 'comment', 'created_at', 'party', 'user', 'user_name')

