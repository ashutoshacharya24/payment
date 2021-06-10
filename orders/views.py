from django.shortcuts import render, redirect
import razorpay
from django.contrib import messages
from razorpay.errors import SignatureVerificationError
from django.views.decorators.csrf import csrf_exempt
client = razorpay.Client(auth=('rzp_test_uTDyXH9RZfKgds', 'XNLBYL7GUQbHSdMaI6M5070B'))

# Create your views here.

# Home
def home(request):
 return render(request, 'razorpay/home.html')

# transaction  
def transaction(request, amount):
    amount = amount * 100
    order_currency = 'INR'
    order_receipt = 'order_receipt'

    response = client.order.create(dict(amount=amount, currency=order_currency, receipt=order_receipt))

    if response is None:
        messages.error(request, 'Something went wrong please try again later')
        return redirect('home')

    context = {
        'razorpay_order_id': response['id'],
        'key': 'rzp_test_uTDyXH9RZfKgds',
        'amount': amount
    }
    return render(request,'razorpay/transaction.html', context)


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST['razorpay_payment_id']
        razorpay_order_id = request.POST['razorpay_order_id']
        razorpay_signature = request.POST['razorpay_signature']

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            return render(request, 'razorpay/payment_success.html')
        except SignatureVerificationError:
            messages.error(request, 'Something went wrong!!')
            return redirect('home')