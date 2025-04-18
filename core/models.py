from django.db import models
from django.contrib.auth.models import User

class Compte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comptes')
    nom = models.CharField(max_length=100)
    solde = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nom} - {self.solde} XAF"

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('CREDIT', 'Crédit'),
        ('DEBIT', 'Débit'),
    ]
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='transactions')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_transaction = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.type} - {self.montant} XAF"
