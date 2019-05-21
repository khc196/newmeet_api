from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

class MeetingType(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

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
    
class MeetingRequest(models.Model):
    meeting_type = models.ForeignKey(MeetingType, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    age_range = models.SmallIntegerField(null=True)
    is_matched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Matching(models.Model):
    male = models.ForeignKey(MeetingRequest, on_delete=models.CASCADE, related_name='male')
    female = models.ForeignKey(MeetingRequest, on_delete=models.CASCADE, related_name='female')
    created_at = models.DateTimeField(auto_now_add=True)


