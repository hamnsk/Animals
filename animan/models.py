from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

# Create your models here.


class PetPhoto(models.Model):
    """Модель реализующая фотографию животного"""
    image = models.ImageField(verbose_name='Фотография', upload_to='pets/photos/%Y/%m/%d', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Автор'))

    class Meta:
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')
        db_table = 'pet_image_table'


class ShelterPhoto(models.Model):
    """Модель реализующая фотографию приюта"""
    image = models.ImageField(verbose_name='Фотография', upload_to='pets/photos/%Y/%m/%d', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')
        db_table = 'shelter_image_table'


class City(models.Model):
    """Модель реализующая список городов"""
    name = models.CharField(verbose_name=_('Наименование'), default='', blank=True, max_length=200)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
        db_table = 'city_table'


class SocialNetwork(models.Model):
    """Модель реализующая ссылку на социальную сеть"""
    VKONTAKTE = 1
    FACEBOOK = 2
    ODNOKLASSNIKI = 3
    INSTAGRAM = 4

    NETWORK_TYPES = (
        (VKONTAKTE, _(u'Вконтакте')),
        (FACEBOOK, _(u'Фейсбук')),
        (ODNOKLASSNIKI, _(u'Одноклассники')),
        (INSTAGRAM, _(u'Инстаграм')),
    )
    network_type = models.PositiveSmallIntegerField(verbose_name=_('Социальная сеть'), choices=NETWORK_TYPES,
                                                    default=VKONTAKTE)
    site = models.URLField(verbose_name=_('Ссылка'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _('Социальная сеть')
        verbose_name_plural = _('Социальные сети')
        db_table = 'social_network_table'


class Pet(models.Model):
    """Модель реализующая описание конкретного животного и все его характеристики"""
    LOST = 1
    FOUND = 2
    ATTACHED = 3
    SEARCHED = 4

    PET_STATUS = (
        (LOST, _(u'Потерянный')),
        (FOUND, _(u'Найденный')),
        (ATTACHED, _(u'Дома')),
        (SEARCHED, _(u'Ищет Дом')),
    )

    name = models.CharField(verbose_name=_('Кличка'), default='', blank=True, max_length=64)
    age = models.DecimalField(verbose_name='Возраст', decimal_places=2, max_digits=4, default=0)
    weight = models.DecimalField(verbose_name='Вес', decimal_places=2, max_digits=4, default=0)
    height = models.DecimalField(verbose_name='Рост', decimal_places=2, max_digits=4, default=0)
    pet_status = models.PositiveSmallIntegerField(verbose_name=_('Социальная сеть'), choices=PET_STATUS, default=LOST)
    comment = models.TextField(verbose_name=_('Описание'), default='', blank=True)
    photos = GenericRelation(PetPhoto)
    # owners = GenericRelation(PetOwner)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _('Питомец')
        verbose_name_plural = _('Питомцы')
        db_table = 'pet_table'

    # def __str__(self):
    #     pass
    #     # return '{} : {}'.format(str(self.user_id), str(self.app_id))


class Shelter(models.Model):
    """Модель реализующая объект приют"""
    name = models.CharField(verbose_name=_('Название'), default='', blank=True, max_length=200)
    description = models.CharField(verbose_name=_('Описание'), default='', blank=True, max_length=250)
    address = models.CharField(verbose_name=_('Адрес'), default='', blank=True, max_length=200)
    site = models.URLField(verbose_name=_('Сайт'))
    phone = models.CharField(verbose_name=_('Телефон'), max_length=11, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Владелец'))
    cities = GenericRelation(City)
    photos = GenericRelation(ShelterPhoto)
    pets = GenericRelation(Pet)
    social_networks = GenericRelation(SocialNetwork)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _('Приют')
        verbose_name_plural = _('Приюты')
        db_table = 'shelter_table'
