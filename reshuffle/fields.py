from django.db import models


class LatexField(models.Field):
    description = 'LaTeX input field'
