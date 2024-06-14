from django import forms
from .models import CategoryModel, RecordModel


class CategoryNewForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['title', 'fk_id_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'fk_id_type': forms.Select(attrs={'class': 'form-select'}),
        }


class RecordForm(forms.ModelForm):
    class Meta:
        model = RecordModel
        fields = ['mount', 'note', 'fk_id_category']

        widgets = {
            'mount': forms.NumberInput(attrs={'class': 'form-mount'}),
            'note': forms.Textarea(attrs={'class': 'form-note'}),
            'fk_id_category': forms.Select(attrs={'class': 'form-category'})
        }


class HistorialRecordForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'class': 'form-date', 'type': 'datetime-local'})
    )
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'class': 'form-date', 'type': 'datetime-local'})
    )

    class Meta:
        model = RecordModel
        fields = ['note', 'fk_id_category']

        widgets = {
            'note': forms.TextInput(attrs={'class': 'form-note-optional'}),
            'fk_id_category': forms.Select(attrs={'class': 'form-category'}),
            # 'register_date': forms.DateInput(attrs={'class': 'form-date'}),
        }

    def __init__(self, *args, **kwargs):
        super(HistorialRecordForm, self).__init__(*args, **kwargs)
        self.fields['fk_id_category'].required = False


class HistorialCategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['fk_id_type']
        widgets = {
            'fk_id_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(HistorialCategoryForm, self).__init__(*args, **kwargs)
        self.fields['fk_id_type'].required = False
