from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Category
from .forms import CategoryForm


@login_required
def category_list(request):
    """Display list of user's categories."""
    categories = Category.objects.filter(user=request.user)

    # Get transaction count for each category
    category_data = []
    for category in categories:
        transaction_count = category.transactions.count()
        category_data.append({
            'category': category,
            'transaction_count': transaction_count
        })

    context = {
        'category_data': category_data,
        'form': CategoryForm(),
    }
    return render(request, 'categories/category_list.html', context)


@login_required
def add_category(request):
    """Add a new category."""
    if request.method == 'POST':
        # Check free tier limits
        if not request.user.has_active_premium():
            category_count = Category.objects.filter(user=request.user).count()
            if category_count >= settings.FREE_CATEGORY_LIMIT:
                messages.warning(
                    request,
                    f'Free users can only create {settings.FREE_CATEGORY_LIMIT} categories. '
                    'Upgrade to Premium for unlimited categories!'
                )
                return redirect('payments:upgrade')

        form = CategoryForm(request.POST)
        if form.is_valid():
            # Check if category name already exists for this user
            name = form.cleaned_data['name']
            if Category.objects.filter(user=request.user, name=name).exists():
                messages.warning(request, f'Category "{name}" already exists.')
                return redirect('categories:list')

            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
        else:
            messages.error(request, 'Error adding category. Please try again.')

    return redirect('categories:list')


@login_required
def edit_category(request, pk):
    """Edit an existing category."""
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            # Check if new name conflicts with existing category
            name = form.cleaned_data['name']
            if Category.objects.filter(user=request.user, name=name).exclude(pk=pk).exists():
                messages.warning(request, f'Category "{name}" already exists.')
                return redirect('categories:list')

            form.save()
            messages.success(request, 'Category updated successfully!')
        else:
            messages.error(request, 'Error updating category. Please try again.')

    return redirect('categories:list')


@login_required
def delete_category(request, pk):
    """Delete a category."""
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == 'POST':
        # Check if category has transactions
        transaction_count = category.transactions.count()
        if transaction_count > 0:
            messages.error(
                request,
                f'Cannot delete category "{category.name}" - it has {transaction_count} '
                'transaction(s) linked to it. Please delete or reassign all transactions first.'
            )
            return redirect('categories:list')

        category.delete()
        messages.success(request, 'Category deleted successfully!')

    return redirect('categories:list')
