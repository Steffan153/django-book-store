from django.urls.base import reverse
from django.db.models.base import Model
from django.db.models.fields import *
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

ZipCodeValidator = RegexValidator(r'^[0-9]{5}$', 'Valid zip code.')

class Country(Model):
    class Meta:
        verbose_name_plural = "countries"

    name = CharField(max_length=80)
    code = CharField(max_length=2)

    def __str__(self):
        return f"{self.code}: {self.name}"

class Address(Model):
    class Meta:
        verbose_name_plural = "addresses"
    street = CharField(max_length=80)
    city = CharField(max_length=50)
    zip_code = CharField(max_length=5, validators=[ZipCodeValidator])

    def __str__(self):
        return f"{self.street}, {self.city} {self.zip_code} "

class Author(Model):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    address = OneToOneField(Address, on_delete=CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(Model):
    title = CharField(max_length=50)
    rating = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = ForeignKey(Author, on_delete=CASCADE, null=True, related_name="books")
    is_bestselling = BooleanField(default=False)
    slug = SlugField(default="", blank=True, null=False, db_index=True)
    published_countries = ManyToManyField(Country, related_name="books")

    def get_absolute_url(self):
        return reverse("book-detail", args=[self.slug])

    def __str__(self):
        return f"{self.title} ({self.rating})"