import stripe
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .models import Payment

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def upgrade_view(request):
    """Display the upgrade to premium page."""
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'premium_price': settings.PREMIUM_PRICE / 100,  # Convert cents to pounds
    }
    return render(request, 'payments/upgrade.html', context)


@login_required
def create_checkout_session(request):
    """Create a Stripe checkout session for premium subscription."""
    if request.method == 'POST':
        try:
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': 'Finance Tracker Premium',
                            'description': 'Unlimited transactions and categories for 1 year',
                        },
                        'unit_amount': settings.PREMIUM_PRICE,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/payments/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri('/payments/cancel/'),
                customer_email=request.user.email,
                metadata={
                    'user_id': request.user.id,
                },
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def payment_success(request):
    """Handle successful payment."""
    session_id = request.GET.get('session_id')

    if session_id:
        try:
            # Retrieve the session from Stripe
            session = stripe.checkout.Session.retrieve(session_id)

            # Check if payment was successful
            if session.payment_status == 'paid':
                # Check if we already processed this payment
                if not Payment.objects.filter(stripe_payment_id=session.payment_intent).exists():
                    # Create payment record
                    Payment.objects.create(
                        user=request.user,
                        stripe_payment_id=session.payment_intent,
                        amount=session.amount_total / 100,
                        status='completed',
                        description='Premium Subscription - 1 Year'
                    )

                    # Upgrade user to premium
                    request.user.is_premium = True
                    request.user.premium_until = timezone.now() + timedelta(days=365)
                    request.user.stripe_customer_id = session.customer
                    request.user.save()

                messages.success(request, 'Payment successful! You now have Premium access for 1 year.')
            else:
                messages.warning(request, 'Payment is still being processed.')

        except Exception as e:
            messages.error(request, 'Error processing payment. Please contact support.')

    return render(request, 'payments/success.html')


@login_required
def payment_cancel(request):
    """Handle cancelled payment."""
    messages.info(request, 'Payment was cancelled. You can try again anytime.')
    return render(request, 'payments/cancel.html')


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhooks for payment events."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('metadata', {}).get('user_id')

        if user_id and session.payment_status == 'paid':
            from accounts.models import CustomUser
            try:
                user = CustomUser.objects.get(id=user_id)

                # Create payment record if not exists
                if not Payment.objects.filter(stripe_payment_id=session.payment_intent).exists():
                    Payment.objects.create(
                        user=user,
                        stripe_payment_id=session.payment_intent,
                        amount=session.amount_total / 100,
                        status='completed',
                        description='Premium Subscription - 1 Year'
                    )

                    # Upgrade user to premium
                    user.is_premium = True
                    user.premium_until = timezone.now() + timedelta(days=365)
                    user.stripe_customer_id = session.customer
                    user.save()

            except CustomUser.DoesNotExist:
                pass

    return HttpResponse(status=200)
