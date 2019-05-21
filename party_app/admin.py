from django.contrib import admin
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
admin.site.register(PartyType)
admin.site.register(Place)
admin.site.register(Party, PartyAdmin)
