# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import json

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import SermepaResponse
from .mixins import SermepaMixin


class SermepaPaymentForm(SermepaMixin, forms.Form):
    Ds_SignatureVersion = forms.IntegerField(widget=forms.HiddenInput())
    Ds_MerchantParameters = forms.IntegerField(widget=forms.HiddenInput())
    Ds_Signature = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        merchant_parameters = kwargs.pop('merchant_parameters', None)
        super(SermepaPaymentForm, self).__init__(*args, **kwargs)
        if merchant_parameters:
            json_data = json.dumps(merchant_parameters)
            order = merchant_parameters['DS_MERCHANT_ORDER']
            b64_params = self.encode_base64(json_data)
            signature = self.get_firma_peticion(order, b64_params,
                                                settings.SERMEPA_SECRET_KEY)

            self.initial['Ds_SignatureVersion'] = settings.SERMEPA_SIGNATURE_VERSION
            self.initial['Ds_MerchantParameters'] = b64_params
            self.initial['Ds_Signature'] = signature

    def render(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            %s
            <input type="submit" name="submit" alt="Comprar ahora" value="Comprar ahora"/>
        </form>""" % (settings.SERMEPA_URL_PRO, self.as_p()))

    def sandbox(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            %s
            <input type="submit" name="submit" alt="Comprar ahora" value="Comprar ahora"/>
        </form>""" % (settings.SERMEPA_URL_TEST, self.as_p()))


class SermepaResponseForm(forms.ModelForm):
    Ds_Date = forms.DateField(required=False, input_formats=('%d/%m/%Y',))
    Ds_Hour = forms.TimeField(required=False, input_formats=('%H:%M',))

    class Meta:
        model = SermepaResponse
        exclude = ()
