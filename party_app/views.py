from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings

from django.db.models import Count, Prefetch,Case,When,Q,F,IntegerField,BooleanField,Value,FilteredRelation
from django.db import transaction, IntegrityError
from django.http import Http404
from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject

from .serializers import *
from .models import PartyType, Place, Party, PartyLike
from authorization.models import User
from main_app.utils.file_helper import save_uploaded_file
from main_app.utils.pagination import MyPaginationMixin
import datetime

class PartyTypeListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = PartyType.objects.all()
        serializer = PartyTypeListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class PlaceListView(APIView, ):
    def get(self, request, *args, **kwargs):
        queryset = Place.objects.all()
        serializer = PlaceListSerializer(queryset, many=True,  context={'request': request})
        return Response(serializer.data)

class PartyListView(APIView, MyPaginationMixin):
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = PartyListSerializer
    def get(self, request, *args, **kwargs):
        print(request.user)
        try: 
            now=datetime.datetime.today()
            queryset = Party.objects.prefetch_related('place')
            if request.user.is_authenticated:
                queryset = queryset.filter(start_datetime__gte=now
                ).annotate(
                    party_like1 = FilteredRelation(
                        'party_like',
                        condition=Q(party_like__user_id=request.user.id)
                    ),
                    is_liked=Case(
                        When(Q(party_like1__isnull=True), then=False),
                        When(Q(party_like1__isnull=False), then=F('party_like1__like')),
                        output_field=BooleanField()
                    )   
                )
            else:
               queryset = queryset.filter(start_datetime__gte=now).annotate(
                    is_liked=Value(False, BooleanField()),
                )
            queryset = queryset.order_by('start_datetime')
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)
        except Party.DoesNotExist as e:
            raise Http404

class PartyDetailView(APIView):
    serializer_class = PartyDetailSerializer
    
    def get_object(self, request,pk):
        try:
            queryset = Party.objects.filter(id=pk).prefetch_related('place')
            if request.user.is_authenticated:
                queryset = queryset.filter(
                ).annotate(
                    party_like1 = FilteredRelation(
                        'party_like',
                        condition=Q(party_like__user_id=request.user.id)
                    ),
                    is_liked=Case(
                        When(Q(party_like1__isnull=True),then=False),
                        When(Q(party_like1__isnull=False),then=F('party_like1__like')),
                        output_field=BooleanField()
                    )
                )
            else:
                queryset = queryset.annotate(
                    is_liked=Value(False, BooleanField()),
                )
            return queryset.get(id=pk)
        except Party.DoesNotExist as e:
            raise Http404
    def get(self, request, *args, **kwargs):
        party_id = kwargs['id']
        party = self.get_object(request, party_id)
        party.view_count += 1
        party.save(update_fields=["view_count"])
        serializer = PartyDetailSerializer(party, many=False, context={'request': request})
        return Response(serializer.data)

class PlaceDetailView(APIView):
    def get_object(self, request, pk):
        try:
            queryset = Place.objects
            return queryset.get(id=pk)
        except Party.DoesNotExist as e:
            raise Http404
    def get(self, request, *args, **kwargs):
        place_id = kwargs['id']
        place = self.get_object(request, place_id)
        serializer = PlaceDetailSerializer(place, many=False, context={'request': request})
        return Response(serializer.data)

class PartyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_partytype_object(self, code):
        try:
            return PartyType.objects.get(code=code)
        except PartyType.DoesNotExist as e:
            raise Http404
    def post(self, request, *args, **kwargs):
        code = kwargs['category']
        partytype = self.get_partytype_object(code)
        request_image = request.data['file']
        serializer = PartyCreateSerializer(
            data = {
                'name': request.data['name'],
                'description': request.data['description'],
                'party_type':partytype.id,
                'image': request_image,
            }
        )
        if serializer.is_valid():
            party = serializer.save()
            return Response(data=party.id, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartyLikeView(APIView):
    def get_party_like_object(self,request,pk):
        try:
            return PartyLike.objects.select_related('party').only(
                'like','party__like_count'
            ).filter(user_id=request.user.id).get(party_id=pk)
        except PartyLike.DoesNotExist:
            return None

    def post(self,request,*args,**kwargs):
        party_id = kwargs['id']
        party_like = self.get_party_like_object(request, party_id)
        if party_like is None:
            party_like = PartyLike(like=True,party_id=party_id,user_id=request.user.id)
            party_like.party.like_count += 1
            try:
                with transaction.atomic():
                    party_like.save()
                    party_like.party.save(update_fields=['like_count'])
                return Response(data="success", status=status.HTTP_200_OK)
            except:
                return Response(data="error", status=status.HTTP_400_BAD_REQUEST)
        else :
            if party_like.like == True:
                party_like.like = False
                party_like.party.like_count -= 1
            else:
                party_like.like = True
                party_like.party.like_count += 1
            try:
                with transaction.atomic():
                    party_like.save(update_fields=['like'])
                    party_like.party.save(update_fields=['like_count'])
                return Response(data="success", status=status.HTTP_200_OK)
            except:
                return Response(data="error", status=status.HTTP_400_BAD_REQUEST)

class PartyCommentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        party_id = kwargs['id']
        if party_id is None:
            return Response(data=None,status=status.HTTP_400_BAD_REQUEST)
        serializer = PartyCommentListSerializer(data={
                                                'comment':request.data['content'],
                                                'party':party_id,
                                                'user':request.user.id,
                                                'user_name': request.user.name,
                                                })
        if serializer.is_valid():
            serializer.save()
            party = Party.objects.get(id=party_id)
            party.comment_count += 1
            party.save(update_fields=['comment_count'])
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
