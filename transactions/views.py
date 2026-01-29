from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Transaction
from .forms import TransactionForm
from categories.models import Category


@login_required
def add_transaction(request):
    """Add a new transaction."""
    if request.method == 'POST':
        # Check if user has any categories
        if not Category.objects.filter(user=request.user).exists():
            messages.warning(request, 'Please add at least one category before creating a transaction.')
            return redirect('categories:list')

        # Check free tier limits
        if not request.user.has_active_premium():
            transaction_count = Transaction.objects.filter(user=request.user).count()
            if transaction_count >= settings.FREE_TRANSACTION_LIMIT:
                messages.warning(
                    request,
                    f'Free users can only create {settings.FREE_TRANSACTION_LIMIT} transactions. '
                    'Upgrade to Premium for unlimited transactions!'
                )
                return redirect('payments:upgrade')

        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
        else:
            messages.error(request, 'Error adding transaction. Please check all fields.')

    return redirect('dashboard:home')


@login_required
def edit_transaction(request, pk):
    """Edit an existing transaction."""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
        else:
            messages.error(request, 'Error updating transaction. Please try again.')

    return redirect('dashboard:home')


@login_required
def delete_transaction(request, pk):
    """Delete a transaction."""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')

    return redirect('dashboard:home')
