from django.db import models


class LatexField(models.Field):
    description = 'LaTeX input field'

    def db_type(self, connection):
        return 'string'


class TestNumField(models.SmallIntegerField):
    description = 'TestNum input field'

    def db_type(self, connection):
        return 'integer'
