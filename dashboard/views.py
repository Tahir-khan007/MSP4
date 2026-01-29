from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from transactions.models import Transaction
from transactions.forms import TransactionForm
from categories.models import Category


def home(request):
    """Display the home/landing page."""
    return render(request, 'dashboard/index.html')


@login_required
def dashboard(request):
    """Display the user's financial dashboard."""
    # Get filter parameters
    filter_type = request.GET.get('filter', 'all')
    category_filter = request.GET.get('category', 'all')

    # Base query for user's transactions (use select_related to avoid N+1 queries)
    transactions = Transaction.objects.filter(user=request.user).select_related('category')

    # Apply transaction type filter
    if filter_type == 'income':
        transactions = transactions.filter(transaction_type='income')
    elif filter_type == 'expense':
        transactions = transactions.filter(transaction_type='expense')

    # Apply category filter
    if category_filter != 'all':
        try:
            transactions = transactions.filter(category_id=int(category_filter))
        except ValueError:
            pass

    # Order by date
    transactions = transactions.order_by('-date', '-created_at')

    # Calculate totals (always from all user transactions, not filtered)
    all_transactions = Transaction.objects.filter(user=request.user)
    total_income = all_transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expenses = all_transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_income - total_expenses

    # Get user's categories for forms and filters
    categories = Category.objects.filter(user=request.user).order_by('name')

    # Create form for adding transactions
    form = TransactionForm(user=request.user)
    
    # Calculate transaction count for free tier users (avoid .count() in template)
    transaction_count = Transaction.objects.filter(user=request.user).count()

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'filter_type': filter_type,
        'category_filter': category_filter,
        'categories': categories,
        'form': form,
        'transaction_count': transaction_count,
    }

    return render(request, 'dashboard/dashboard.html', context)


def handler404(request, exception):
    """Handle 404 errors."""
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    """Handle 500 errors."""
    return render(request, 'errors/500.html', status=500)
