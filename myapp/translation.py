from modeltranslation.translator import translator, TranslationOptions
from .models import (
    Tent, Combo, MenuItem, Drink, BlogPost,
    GalleryImage, Review
)

class TentTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class ComboTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'details',)

class MenuItemTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class DrinkTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'content',)

class GalleryImageTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

class ReviewTranslationOptions(TranslationOptions):
    fields = ('content',)

translator.register(Tent, TentTranslationOptions)
translator.register(Combo, ComboTranslationOptions)
translator.register(MenuItem, MenuItemTranslationOptions)
translator.register(Drink, DrinkTranslationOptions)
translator.register(BlogPost, BlogPostTranslationOptions)
translator.register(GalleryImage, GalleryImageTranslationOptions)
translator.register(Review, ReviewTranslationOptions)
