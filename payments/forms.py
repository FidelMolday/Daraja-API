from django import forms

SERVICES = [
    ('cleaning', 'Cleaning - KES 100'),
    ('delivery', 'Delivery - KES 150'),
    ('gardening', 'Gardening - KES 200'),
]

class PaymentForm(forms.Form):
    phone_number = forms.CharField(label="Phone Number (2547XXXXXXX)")
    service = forms.ChoiceField(choices=SERVICES)
