from django.contrib import admin
from .models import Pet, PetPhoto, Shelter, ShelterPhoto, City, SocialNetwork, ShelterAddress, ShelterPhone
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


class ShelterAddressInLine(admin.TabularInline):
    model = ShelterAddress


class ShelterPhoneInLine(admin.TabularInline):
    model = ShelterPhone


class ShelterAdmin(admin.ModelAdmin):
    inlines = [ShelterAddressInLine, ShelterPhoneInLine, SocialNetworkInLine, ShelterPhotoInLine, PetInline, ]


class CityAdmin(admin.ModelAdmin):
    pass


class PetAdmin(admin.ModelAdmin):
    inlines = [PetPhotoInline,]


admin.site.register(Pet, PetAdmin)
admin.site.register(Shelter, ShelterAdmin)
admin.site.register(City, CityAdmin)
