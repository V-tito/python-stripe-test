from django.shortcuts import render
from django.template.response import TemplateResponse
from . import models
from django.http import HttpResponseNotFound,HttpResponseNotAllowed,HttpResponseRedirect,HttpResponseServerError,HttpResponseBadRequest
from . import forms
import stripe
from django.conf import settings

exchange_rates={ #заглушка
     'rub': {'usd':0.01},
     'usd':{'rub':100}
}

client = stripe.StripeClient(stripe.api_key)
def item(request, item_id):
    if request.method=='GET':
        try:
            item = models.Item.objects.get(id=item_id)
            form=forms.addToOrderForm({"item":item.id})
            return TemplateResponse(request, "item.html",{"item": item,"form":form})
        except models.Item.DoesNotExist:
            return HttpResponseNotFound("No such item found")
    else:
        return HttpResponseNotAllowed(['POST,PATCH,DELETE'])

def paymentAccepted (request):
    return TemplateResponse(request,'paymentSuccess.html')

def buy(request, item_id):
    if request.method=='GET':
        try:
            #client = stripe.StripeClient(stripe.api_key)
            item=models.Item.objects.get(id=item_id)
            amount=item.price
            if item.currency in ['usd','rub']: #ugly way to convert, but at least it's extensible
                 amount*=100
            intent = client.v1.payment_intents.create({"amount": int(amount), "currency": item.currency})
            return TemplateResponse(request,'checkout.html', {'client_secret':intent.client_secret, 'pub_key':settings.STRIPE_PUBLISHABLE_KEY})
        except ValueError:
            HttpResponseServerError()
    else:
            return HttpResponseNotAllowed(['POST,PATCH,DELETE'])
def buyOrdered(request,order_id):
    if request.method=='GET':
            try:
                order=models.Order.objects.get(id=order_id)
                total=0
                orderCurrency=order.items.first().currency
                for item in order.items.all():
                    if (item.currency==orderCurrency):
                          total+=item.price
                    else:
                         total+=item.price*exchange_rates[item.currency][orderCurrency]
                if orderCurrency in ['usd','rub']: #ugly way to convert, but at least it's extensible
                                 total*=100
                intent = client.v1.payment_intents.create({"amount": int(total), "currency": orderCurrency})
                return TemplateResponse(request,'checkout.html', {'client_secret':intent.client_secret, 'pub_key':settings.STRIPE_PUBLISHABLE_KEY})
            except ValueError:
                HttpResponseServerError()
    else:
                return HttpResponseNotAllowed(['POST,PATCH,DELETE'])

def order(request,order_id=None):
    
    if request.method=="GET":
        if order_id:
            order=models.Order.objects.get(id=order_id)
            return TemplateResponse(request,"order.html",{'order':order})
        else:
            orders=models.Order.objects.all()
            return TemplateResponse(request,"orders.html",{'orders':orders})

def addToOrder(request,item_id):
     if request.method == "POST":
             form = forms.addToOrderForm(request.POST)
             if form.is_valid():
                 print(form.cleaned_data)
                 order=models.Order.objects.get(id=form.cleaned_data['order'].id)
                 item=models.Item.objects.get(id=item_id)
                 order.items.add(item)
                 return HttpResponseRedirect(f"/orders/{order.id}")

