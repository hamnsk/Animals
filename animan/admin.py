from django.contrib import admin
from .models import Pet, PetPhoto, Shelter, ShelterPhoto, City, SocialNetwork
from django.contrib.contenttypes.admin import GenericTabularInline


class SocialNetworkInLine(GenericTabularInline):
    model = SocialNetwork


class PetPhotoInline(admin.TabularInline):
    model = PetPhoto


class ShelterPhotoInLine(admin.TabularInline):
    model = ShelterPhoto


class PetInline(GenericTabularInline):
    model = Pet
    inlines = [PetPhotoInline, ]


class ShelterAdmin(admin.ModelAdmin):
    inlines = [SocialNetworkInLine, ShelterPhotoInLine, PetInline, ]


class CityAdmin(admin.ModelAdmin):
    pass


class PetAdmin(admin.ModelAdmin):
    inlines = [PetPhotoInline, ]


admin.site.register(Pet, PetAdmin)
admin.site.register(Shelter, ShelterAdmin)
admin.site.register(City, CityAdmin)
