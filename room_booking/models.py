from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Room(models.Model):
    ROOM_TYPES = [
        ('suite', _('Suite')),
        ('standard', _('Standard Room')),
        ('deluxe', _('Deluxe Room')),
    ]
    CURRENCY_TYPES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]
    name = models.CharField(_('Name'), max_length=100, blank=True, default='')
    type = models.CharField(_('Room Type'), max_length=100, choices=ROOM_TYPES)
    pricePerNight = models.IntegerField(_('Price per Night'), default=150)
    currency = models.CharField(_('Currency'), default="USD", max_length=10, choices=CURRENCY_TYPES)
    maxOccupancy = models.IntegerField(_('Maximum Occupancy'), default=1)
    description = models.TextField(_('Description'), max_length=1000)

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
class RoomImage(models.Model):
    image = models.ImageField(_('Image'), upload_to='room_images/')
    caption = models.CharField(_('Caption'), max_length=255, blank=True, null=True)
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE, verbose_name=_('Room'))
    
    class Meta:
        verbose_name = _('Room Image')
        verbose_name_plural = _('Room Images')

    def __str__(self):
        return f"{_('Image for')} {self.room.name} - {self.caption or _('No Caption')}"

class OccupiedDate(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='occupiedDates', verbose_name=_('Room'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='booked_dates', verbose_name=_('User'))
    date = models.DateField(_('Date'))

    class Meta:
        verbose_name = _('Occupied Date')
        verbose_name_plural = _('Occupied Dates')

    def __str__(self):
        return _('%(date)s - %(room)s booked by %(user)s') % {
            'date': self.date,
            'room': self.room.name,
            'user': self.user.username
        }



# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=100,default="")