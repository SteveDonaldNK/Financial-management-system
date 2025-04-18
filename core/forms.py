from django import forms
from .models import Transaction, Compte

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['compte', 'montant', 'type']
        widgets = {
            'compte': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ['nom', 'solde']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'solde': forms.NumberInput(attrs={'class': 'form-control'}),
        }

