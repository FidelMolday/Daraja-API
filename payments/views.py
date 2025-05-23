from django.shortcuts import render
from django.http import JsonResponse
from .forms import PaymentForm
from .utils import get_access_token
import datetime, base64, os, requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

SERVICE_PRICES = {
    'cleaning': 100,
    'delivery': 150,
    'gardening': 200,
}

def payment_view(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            service = form.cleaned_data['service']
            amount = SERVICE_PRICES[service]

            access_token = get_access_token()
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            password = base64.b64encode((os.getenv("BUSINESS_SHORTCODE") + os.getenv("PASSKEY") + timestamp).encode()).decode()

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "BusinessShortCode": os.getenv("BUSINESS_SHORTCODE"),
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone,
                "PartyB": os.getenv("BUSINESS_SHORTCODE"),
                "PhoneNumber": phone,
                "CallBackURL": os.getenv("CALLBACK_URL"),
                "AccountReference": "ServicePayment",
                "TransactionDesc": f"Payment for {service}"
            }

            r = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", headers=headers, json=payload)
            return JsonResponse(r.json())
    else:
        form = PaymentForm()
    return render(request, "payments/payment_form.html", {"form": form})

@csrf_exempt
def callback_url(request):
    print(request.body)
    return HttpResponse("Callback received", status=200)
