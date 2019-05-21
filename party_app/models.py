from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

class PartyType(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Place(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    latitude = models.CharField(verbose_name=_(u"Latitude"), max_length=32)
    longitude = models.CharField(verbose_name=_(u"Longitude"), max_length=32)
    address = models.CharField(verbose_name=_(u"Address"), max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("latitude", "longitude")
    def __unicode__(self):
        return "%s - %s - %s" % (self.latitude, self.longitude, self.address)
    def __str__(self):
        return self.name
    
class Party(models.Model):
    party_type = models.ForeignKey(PartyType, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, related_name='party_place')
    name = models.CharField(max_length=30)
    description = models.TextField()
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    can_prepurchase = models.BooleanField(default=False)
    can_buy_ticket = models.BooleanField(default=False)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    is_hot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class PartyLike(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='party_like')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

class PartyComment(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='party_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class PartyImage(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='party_image')
    image = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)