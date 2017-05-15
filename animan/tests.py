from django.test import TestCase
from .models import Pet

# Create your tests here.


def create_pet(name='Белка', age=10, weight=7, height=50, comment='Первый космонавт'):
    return Pet.objects.create(name=name, age=age, weight=weight, height=height, comment=comment)


class PetCreationTest(TestCase):

    def test_create_pet(self):
        dog = create_pet()
        self.assertTrue(isinstance(dog, Pet))
        self.assertEqual(dog.name, 'Белка')
