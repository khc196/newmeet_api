from django.contrib import admin
from django.conf import settings
from .models import PartyType, Place, PartyImage, Party

class PartyImageInline(admin.TabularInline):
    model = PartyImage
    extra = 3

class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'party_type_name', 'place_name', 'start_datetime')
    list_filter = ('party_type', 'place')
    search_fileds = ('name')
    fields = ('name', 'party_type', 'start_datetime', 'end_datetime', 'description', 'place')
    inlines = [ PartyImageInline, ]
    def party_type_name(self, obj):
        partytype = PartyType.objects.get(id=obj.party_type.id)
        return '{}({})'.format(partytype.name, partytype.id)
    def place_name(self, obj):
        place = Place.objects.get(id=obj.place.id)
        return '{}({})'.format(place.name, place.id)
    def images(self, obj):
        image_list = PartyImage.objects.all(party=obj)
        return image_list
    party_type_name.short_description = 'TYPE'
    place_name.short_description = 'PLACE'

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude',)
    search_fields = ('name',)

    fieldsets = (
        (None, {
            'fields': ( 'name', 'latitude', 'longitude',)
        }),
    )

    class Media:
        if hasattr(settings, 'KAKAO_MAPS_API_KEY') and settings.KAKAO_MAPS_API_KEY:
            css = {
                'all': ('admin/css/map.css',),
            }
            js = (
                'https://dapi.kakao.com/v2/maps/sdk.js?appkey={}'.format(settings.KAKAO_MAPS_API_KEY),
                'admin/js/map.js',
            )

admin.site.register(PartyType)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Party, PartyAdmin)

