from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from oscar.core.utils import slugify

from ckeditor_uploader.fields import RichTextUploadingField
 
    
    
@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('description'), blank=True)
    
    slug = models.SlugField(_('slug'), max_length=128, unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = _('authors')

    def generate_slug(self):
        return slugify(self.name)
    
    def ensure_slug_uniqueness(self):
        unique_slug = self.slug
        siblings = Author.objects.exclude(id=self.id)
        next_num = 2
        while siblings.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1
        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        if self.slug and self.slug != '':
            self.ensure_slug_uniqueness()
            super(Author, self).save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            self.ensure_slug_uniqueness()
            super(Author, self).save(*args, **kwargs)

    #def num_books(self):
        #return self.books.count()

    #def num_translations(self):
        #return self.books_translated.count()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'pk': self.pk})



@python_2_unicode_compatible
class Serie(models.Model):
    name = models.CharField(_('name'), max_length=128, unique=True)
    description = models.TextField(_('Description'), blank=True)
    
    slug = models.SlugField(_('slug'), max_length=128, unique=True, blank=True)

    def generate_slug(self):
        return slugify(self.name)
    
    def ensure_slug_uniqueness(self):
        unique_slug = self.slug
        siblings = Serie.objects.exclude(id=self.id)
        next_num = 2
        while siblings.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1
        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        if self.slug and self.slug != '':
            self.ensure_slug_uniqueness()
            super(Serie, self).save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            self.ensure_slug_uniqueness()
            super(Serie, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = _('series')
        
    #def num_books(self):
        #return self.books.count()
    
    def __str__(self):
        return self.name





@python_2_unicode_compatible
class BookFormat(models.Model):
    name = models.CharField(_('Name'), max_length=128, unique=True)
    description = models.TextField(_('Description'), blank=True)
    virtual = models.BooleanField(_('Virtual'), default=False)
    
    slug = models.SlugField(_('slug'), max_length=128, unique=True, blank=True)
    
    def generate_slug(self):
        return slugify(self.name)
    
    def ensure_slug_uniqueness(self):
        unique_slug = self.slug
        siblings = BookFormat.objects.exclude(id=self.id)
        next_num = 2
        while siblings.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1
        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        if self.slug and self.slug != '':
            self.ensure_slug_uniqueness()
            super(BookFormat, self).save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            self.ensure_slug_uniqueness()
            super(BookFormat, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('book format')
        verbose_name_plural = _('book formats')
    
    def num_books(self):
        return self.books.count()
    
    def __str__(self):
        return self.name




@python_2_unicode_compatible
class BookStore(models.Model):
    name = models.CharField(_('Name'), max_length=128, unique=True)
    description = RichTextUploadingField()
    
    slug = models.SlugField(_('slug'), max_length=128, unique=True, blank=True)

    def generate_slug(self):
        return slugify(self.name)
    
    def ensure_slug_uniqueness(self):
        unique_slug = self.slug
        siblings = BookStore.objects.exclude(id=self.id)
        next_num = 2
        while siblings.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1
        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        if self.slug and self.slug != '':
            self.ensure_slug_uniqueness()
            super(BookStore, self).save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            self.ensure_slug_uniqueness()
            super(BookStore, self).save(*args, **kwargs)
    
    
    class Meta:
        verbose_name = _('book store')
        verbose_name_plural = _('book stores')
    
    def num_books(self):
        return self.books.count()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('bookstore_detail', kwargs={'pk': self.pk})


