from django import forms
from .models import Transaction
from categories.models import Category
from datetime import date


class TransactionForm(forms.ModelForm):
    """Form for creating and editing transactions."""
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Select Category'
    )
    description = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter description'
        })
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )
    transaction_type = forms.ChoiceField(
        choices=[('', 'Select Type')] + list(Transaction.TRANSACTION_TYPES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = Transaction
        fields = ['category', 'description', 'amount', 'transaction_type', 'date']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
