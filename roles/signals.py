from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

@receiver(post_save, sender=Profile)
def add_user_to_views_group(sender, instance, created, **kwargs):
    if created:
        try:
            group1 = Group.objects.get(name='visita')
        except Group.DoesNotExist:
            group1 = Group.objects.create(name='Lucas')
            group2 = Group.objects.create(name='visita')
            group3 = Group.objects.create(name='sustitucion')
            group4 = Group.objects.create(name='acta')
            group5 = Group.objects.create(name='medicion')
            group6 = Group.objects.create(name='estado')
        instance.user.groups.add(group1)

