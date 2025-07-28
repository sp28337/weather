import factory
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.models import City

faker = FakerFactory.create()


@register(_name="city")
class CityFactory(factory.Factory):

    class Meta:
        model = City

    id = factory.LazyFunction(lambda: faker.random_int())
    name = factory.LazyFunction(lambda: faker.name())
    requested = factory.LazyFunction(lambda: faker.random_int())
