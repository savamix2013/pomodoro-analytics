import factory
from faker import Faker

from app.users.user_profile.models import UserProfile

faker = Faker()


EXISTS_GOOGLE_USER_ID = 20
EXISTS_GOOGLE_USER_EMAIL = "google@gmail.com"


class UserProfileFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.user_name())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.first_name())
    password = factory.LazyFunction(lambda: faker.password())