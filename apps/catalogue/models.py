from django.db import models
from django.utils.translation import ugettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from apps.books.models import Author, Serie, BookFormat, BookStore



storage_magazzino_virtuale = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'magazzino_virtuale'))

class Product(AbstractProduct):
    
    authors = models.ManyToManyField(
        Author, blank=True, related_name='books', verbose_name=_("authors"))
    
    bookstores = models.ManyToManyField(
        BookStore, blank=True, related_name='books', verbose_name=_("bookstores"))
    
    translation_authors = models.ManyToManyField(
        Author, blank=True, related_name='books_translated', verbose_name=_("translation authors"))
    
    serie = models.ForeignKey(
        Serie, null=True, blank=True, related_name='books', verbose_name=_("serie"))
    
    form = models.ForeignKey(
        BookFormat, null=True, blank=True, related_name='books', verbose_name=_("format"))
    
    background_color = models.CharField(max_length=7, blank=True, verbose_name=_("background color"))
    
    file = models.FileField(blank=True, storage=storage_magazzino_virtuale) 
    
    @property
    def is_virtual(self):
        if self.form:
            return self.form.virtual
        return False

    @property
    def is_shipping_required(self):
        spedizione_richiesta = self.get_product_class().requires_shipping
        if self.is_virtual:
            return False
        return spedizione_richiesta

    def primary_image(self):
        """
        Returns the primary image for a product. Usually used when one can
        only display one product image, e.g. in a list of products.
        """
        
        images = self.images.all()
        ordering = self.images.model.Meta.ordering
        if self.is_child:
            images = self.parent.images.all()
            ordering = self.parent.images.model.Meta.ordering
        
        
        if not ordering or ordering[0] != 'display_order':
            # Only apply order_by() if a custom model doesn't use default
            # ordering. Applying order_by() busts the prefetch cache of
            # the ProductManager
            images = images.order_by('display_order')
        try:
            return images[0]
        except IndexError:
            # We return a dict with fields that mirror the key properties of
            # the ProductImage class so this missing image can be used
            # interchangeably in templates.  Strategy pattern ftw!
            return {
                'original': self.get_missing_image(),
                'caption': '',
                'is_missing': True}


    def get_title(self):
        title = super(Product, self).get_title()
        
        if self.form:
            title += ' [{}]'.format(self.form.name)
        return title
        

from oscar.apps.catalogue.models import *  # noqa
