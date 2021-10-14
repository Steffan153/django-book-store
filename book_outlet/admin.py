from django.contrib.admin.decorators import register
from django.contrib.admin.options import ModelAdmin
from .models import Address, Author, Book, Country

@register(Book)
class BookAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_filter = ('rating', 'author', 'is_bestselling', 'published_countries')
    list_display = ('title', 'author', 'rating', 'is_bestselling', 'get_published_countries')

    def get_published_countries(self, obj):
        return ", ".join(country.code for country in obj.published_countries.all())

@register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('__str__', 'address')

@register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('__str__', 'author')

@register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ('__str__', 'get_published_books')
    def get_published_books(self, obj):
        return ", ".join(book.title for book in obj.books.all())
