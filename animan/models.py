from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from datetime import datetime


# Create your models here.


def pets_photo_path(instance, filename):
    """Установка пути выгрузки фотографий питомцев"""
    date_now = datetime.strftime(datetime.now(), "%Y/%m/%d")
    return 'pets/pet_id_{0}/photos/{1}/{2}'.format(instance.pet.id, date_now, filename)


def shelters_photo_path(instance, filename):
    """Установка пути выгрузки фотографий приютов"""
    date_now = datetime.strftime(datetime.now(), "%Y/%m/%d")
    return 'shelters/shelter_id_{0}/photos/{1}/{2}'.format(instance.shelter.id, date_now, filename)


def shelters_avatar_path(instance, filename):
    """Установка пути выгрузки фотографий приютов"""
    date_now = datetime.strftime(datetime.now(), "%Y/%m/%d")
    return 'shelters/shelter_id_{0}/photos/{1}/{2}'.format(instance.id, date_now, filename)


def pets_avatar_path(instance, filename):
    """Установка пути выгрузки фотографий приютов"""
    date_now = datetime.strftime(datetime.now(), "%Y/%m/%d")
    return 'pets/pet_id_{0}/photos/{1}/{2}'.format(instance.id, date_now, filename)


class AbstractDateTimeModel(models.Model):
    """Абстрактная модель AbstractDateTimeModel для отслеживания времения изменения объекта"""
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class City(models.Model):
    """Модель реализующая список городов"""
    name = models.CharField(verbose_name=_('Наименование'),
                            default='',
                            blank=True,
                            max_length=200,
                            help_text=_('Введите наименование города'))

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')
        db_table = 'city_table'

    def __str__(self):
        return str(self.name)


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


class PetKind(AbstractDateTimeModel):
    """Модель реализующая вид животного: собака, кошка, носорог..."""
    name = models.CharField(verbose_name=_('Наименование'),
                            default='Введите вид животного',
                            blank=False,
                            max_length=250,
                            help_text=_('Введите вид животного'))
    description = models.TextField(verbose_name=_('Описание вида'),
                                   blank=True,
                                   help_text=_('Описание вида животного'))

    class Meta:
        verbose_name = _('Вид животного')
        verbose_name_plural = _('Виды животных')
        db_table = 'pets_kind_table'

    def __str__(self):
        return str(self.name)


class PetBreed(AbstractDateTimeModel):
    """Модель реализующая породу животного: такса, овчарка, перс"""
    name = models.CharField(verbose_name=_('Наименование'),
                            default='Введите породу животного',
                            blank=False,
                            max_length=250,
                            help_text=_('Введите название породы животного'))
    description = models.TextField(verbose_name=_('Описание породы'),
                                   blank=True,
                                   help_text=_('Описание породы животного'))
    petkid_id = models.ForeignKey(PetKind, on_delete=models.CASCADE, verbose_name=_('Вид животного'))

    class Meta:
        verbose_name = _('Порода животного')
        verbose_name_plural = _('Породы животных')
        db_table = 'pets_breed_table'

    def __str__(self):
        return str(self.name)


class Pet(AbstractDateTimeModel):
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

    name = models.CharField(verbose_name=_('Кличка'),
                            default='',
                            blank=True,
                            max_length=64,
                            help_text=_('Укажите кличку питомца'))
    kind = models.ForeignKey(PetKind, on_delete=models.CASCADE, verbose_name=_('Вид животного'))
    breed = models.ForeignKey(PetBreed, on_delete=models.CASCADE, verbose_name=_('Порода животного'))
    age = models.DecimalField(verbose_name=_('Возраст'),
                              decimal_places=2,
                              max_digits=4, default=0,
                              help_text=_('Введите возраст питомца'))
    weight = models.DecimalField(verbose_name=_('Вес'), decimal_places=2, max_digits=4, default=0,
                                 help_text=_('Укажите вес питомца'))
    height = models.DecimalField(verbose_name=_('Рост'), decimal_places=2, max_digits=4, default=0,
                                 help_text=_('Укажите высоту в холке'))
    pet_status = models.PositiveSmallIntegerField(verbose_name=_('Статус'), choices=PET_STATUS, default=LOST)
    comment = models.TextField(verbose_name=_('Описание'), default='', blank=True, help_text=_('Расскажите о питомце'))
    avatar = models.ImageField(verbose_name=_('Аватар'), upload_to=pets_avatar_path, blank=True, null=True,
                               help_text=_('Фотография профиля, отображается первой на всех страницах'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _('Питомец')
        verbose_name_plural = _('Питомцы')
        db_table = 'pet_table'

    def __str__(self):
        return str(self.name)


class PetPhoto(AbstractDateTimeModel):
    """Модель реализующая фотографию животного"""
    image = models.ImageField(verbose_name=_('Фотография'), upload_to=pets_photo_path, blank=True, null=True)
    description = models.CharField(verbose_name=_('Описание'), default='', blank=True, max_length=250,
                                   help_text=_('Краткое описание'))
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name=_('Питомец'))

    class Meta:
        verbose_name = _('Фотография питомца')
        verbose_name_plural = _('Фотографии питомца')
        db_table = 'pet_image_table'

    def __str__(self):
        return 'Фотография {}'.format(str(self.pk))


class Shelter(AbstractDateTimeModel):
    """Модель реализующая объект приют"""
    PRIVATE = 1
    STATE = 2

    SHELTER_TYPES = (
        (PRIVATE, _(u'Частный')),
        (STATE, _(u'Муниципальный')),
    )
    shelter_type = models.PositiveSmallIntegerField(verbose_name=_('Вид приюта'), choices=SHELTER_TYPES,
                                                    default=STATE)
    name = models.CharField(verbose_name=_('Название'), default='', blank=True, max_length=200,
                            help_text=_('Укажите название приюта'))
    description = models.CharField(verbose_name=_('Описание'), default='', blank=True, max_length=250,
                                   help_text=_('Краткое описание'))
    site = models.URLField(verbose_name=_('Сайт'), help_text=_('Укажите адрес сайта в формате http(s)://sitename.zone'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Владелец'))
    moderators = models.ManyToManyField(User, verbose_name=_('Куратор'), related_name='shelter_moderators_list')
    volunteers = models.ManyToManyField(User, verbose_name=_('Волонтер'), related_name='shelter_volunteers_list')
    cities = models.ManyToManyField(City, verbose_name=_('Город'))
    pets = GenericRelation(Pet)
    social_networks = GenericRelation(SocialNetwork)
    avatar = models.ImageField(verbose_name=_('Аватар'), upload_to=shelters_avatar_path, blank=True, null=True,
                               help_text=_('Фотография профиля, отображается первой на всех страницах'))

    class Meta:
        verbose_name = _('Приют')
        verbose_name_plural = _('Приюты')
        db_table = 'shelter_table'

    def __str__(self):
        return str(self.name)


class ShelterPhoto(AbstractDateTimeModel):
    """Модель реализующая фотографию приюта"""
    image = models.ImageField(verbose_name=_('Фотография'), upload_to=shelters_photo_path, blank=True, null=True)
    description = models.CharField(verbose_name=_('Описание'), default='', blank=True, max_length=250,
                                   help_text=_('Краткое описание'))
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, verbose_name=_('Приют'))

    class Meta:
        verbose_name = _('Фотография приюта')
        verbose_name_plural = _('Фотографии приюта')
        db_table = 'shelter_image_table'

    def __str__(self):
        return 'Фотография {}'.format(str(self.pk))


class ShelterAddress(AbstractDateTimeModel):
    address = models.CharField(verbose_name=_('Адрес'), default='', blank=True, max_length=250,
                               help_text=_('Укажите адрес приюта'))
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, verbose_name=_('Приют'))

    class Meta:
        verbose_name = _('Адрес приюта')
        verbose_name_plural = _('Адреса приюта')
        db_table = 'shelter_address_table'

    def __str__(self):
        return 'Адрес {}'.format(str(self.pk))


class ShelterPhone(AbstractDateTimeModel):
    phone = models.CharField(verbose_name=_('Телефон'), max_length=11, null=True, blank=True,
                             help_text=_('Укажите телефон приюта'))
    description = models.CharField(verbose_name=_('Описание'), default='', blank=True, max_length=250,
                                   help_text=_('Краткое описание контакта'))
    person = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Укажите ответственного пользователя'),
                               blank=True)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, verbose_name=_('Приют'))

    class Meta:
        verbose_name = _('Телефон приюта')
        verbose_name_plural = _('Телефоны приюта')
        db_table = 'shelter_phone_table'

    def __str__(self):
        return 'Телефон {}'.format(str(self.pk))
