from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import TransactionForm, AccountForm
from .models import Transaction, Compte

def index(request):
    return render(request, 'core/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form, 'hide_navbar': True})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form, 'hide_navbar': True})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        comptes = Compte.objects.all()
        transactions = Transaction.objects.all().order_by('-date_transaction')
    else:
        comptes = Compte.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(compte__user=request.user).order_by('-date_transaction')
    
    total_balance = sum(compte.solde for compte in comptes)
    total_comptes = comptes.count()
    total_transactions = transactions.count()
    
    context = {
        'comptes': comptes,
        'transactions': transactions,
        'total_balance': total_balance,
        'total_comptes': total_comptes,
        'total_transactions': total_transactions,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def ajouter_compte(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            compte = form.save(commit=False)
            compte.user = request.user  # Association du compte à l'utilisateur connecté
            compte.save()
            return redirect('dashboard')
    else:
        form = AccountForm()
    return render(request, 'core/ajouter_compte.html', {'form': form})

@login_required
def ajouter_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            # Si l'utilisateur n'est pas admin, vérifier que le compte appartient bien à l'utilisateur connecté
            if not request.user.is_superuser and transaction.compte.user != request.user:
                return redirect('dashboard')
            # Mettre à jour le solde du compte en fonction du type d'opération
            if transaction.type == 'CREDIT':
                transaction.compte.solde += transaction.montant
            elif transaction.type == 'DEBIT':
                transaction.compte.solde -= transaction.montant
            transaction.compte.save()
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
        # Limiter le choix des comptes aux comptes de l'utilisateur connecté (pour les non-admins)
        if not request.user.is_superuser:
            form.fields['compte'].queryset = Compte.objects.filter(user=request.user)
    return render(request, 'core/ajouter_transaction.html', {'form': form})

@login_required
def modifier_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    # Restriction pour que seuls les propriétaires ou admins puissent modifier
    if not request.user.is_superuser and transaction.compte.user != request.user:
        return redirect('dashboard')

    # Recalculer le solde (retirer l'ancien effet)
    ancien_montant = transaction.montant
    ancien_type = transaction.type
    compte = transaction.compte

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            nouvelle_transaction = form.save(commit=False)

            # Annuler l'ancien effet
            if ancien_type == 'CREDIT':
                compte.solde -= ancien_montant
            elif ancien_type == 'DEBIT':
                compte.solde += ancien_montant

            # Appliquer le nouveau
            if nouvelle_transaction.type == 'CREDIT':
                compte.solde += nouvelle_transaction.montant
            elif nouvelle_transaction.type == 'DEBIT':
                compte.solde -= nouvelle_transaction.montant

            compte.save()
            nouvelle_transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'core/modifier_transaction.html', {'form': form})


@login_required
def supprimer_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    # Vérification de permissions
    if not request.user.is_superuser and transaction.compte.user != request.user:
        return redirect('dashboard')

    compte = transaction.compte

    # Rétablir le solde avant suppression
    if transaction.type == 'CREDIT':
        compte.solde -= transaction.montant
    elif transaction.type == 'DEBIT':
        compte.solde += transaction.montant

    compte.save()
    transaction.delete()
    return redirect('dashboard')