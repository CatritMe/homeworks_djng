from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version

wrong_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin(forms.ModelForm):
    '''Класс стилизации форм'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    '''Форма для редактирования товара'''

    class Meta:
        model = Product
        exclude = ('user',)

    def clean_title(self):
        '''Функция для отбраковки недопустимых слов в поле "Название"'''
        cleaned_data = self.cleaned_data.get('title')
        for word in wrong_words:
            if word in cleaned_data:
                raise forms.ValidationError('Недопустимые слова')

        return cleaned_data

    def clean_description(self):
        '''Функция для отбраковки недопустимых слов в поле "Описание"'''
        cleaned_data = self.cleaned_data.get('description')
        for word in wrong_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Недопустимые слова')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    '''Форма для редактирования версии товара'''
    class Meta:
        model = Version
        fields = '__all__'


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    '''Форма для редактирования товара с правами модератора'''
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published',)
