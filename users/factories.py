import uuid

from django.contrib.auth import get_user_model

import factory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    password = 'Password1!'
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = User

    @factory.lazy_attribute
    def username(self):
        return str(uuid.uuid4())

    @factory.lazy_attribute
    def email(self):
        return f'{self.username}@example.com'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
