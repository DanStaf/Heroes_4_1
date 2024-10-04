from django import forms

from heroes.models import Hero, HeroStatus, Parent, ParentStatus


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class HeroForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Hero
        fields = '__all__'


class HeroStatusForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = HeroStatus
        fields = '__all__'


class ParentForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Parent
        fields = '__all__'


class ParentStatusForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = ParentStatus
        fields = '__all__'
