from django.contrib import admin
from .models import Pet, PetPhoto, Shelter, ShelterPhoto, City, SocialNetwork, ShelterAddress, ShelterPhone
from django.contrib.contenttypes.admin import GenericTabularInline


class SocialNetworkInLine(GenericTabularInline):
    model = SocialNetwork
    can_delete = True
    extra = 1


class PetPhotoInline(admin.TabularInline):
    model = PetPhoto
    extra = 1


class ShelterPhotoInLine(admin.TabularInline):
    model = ShelterPhoto
    extra = 1


class PetInline(GenericTabularInline):
    model = Pet
    can_delete = True
    extra = 1


class ShelterAddressInLine(admin.TabularInline):
    model = ShelterAddress
    can_delete = True
    extra = 1


class ShelterPhoneInLine(admin.TabularInline):
    model = ShelterPhone
    can_delete = True
    extra = 1


class ShelterAdmin(admin.ModelAdmin):
    inlines = [ShelterAddressInLine, ShelterPhoneInLine, SocialNetworkInLine, ShelterPhotoInLine, PetInline, ]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'site', 'owner', )
        }),
        ('Настройки членов приюта', {
            'classes': ('collapse',),
            'fields': ('moderators', 'volunteers', )
        }),
        ('Города присутствия', {
            'classes': ('collapse',),
            'fields': ('cities', )
        }),
    )
    list_display = ('name', 'owner', 'site',)
    search_fields = ('name', 'owner', 'site', 'moderators', 'volunteers', 'cities')
    list_filter = ('name', 'owner', 'site', 'moderators', 'volunteers', 'cities')
    filter_horizontal = ('moderators', 'volunteers', 'cities')


class CityAdmin(admin.ModelAdmin):
    pass


class PetAdmin(admin.ModelAdmin):
    inlines = [PetPhotoInline, ]
    list_display = ('name', 'age', 'pet_status', )
    search_fields = ('name', 'age', 'pet_status', 'comment',)
    list_filter = ('name', 'age', 'pet_status', )


admin.site.register(Pet, PetAdmin)
admin.site.register(Shelter, ShelterAdmin)
admin.site.register(City, CityAdmin)
