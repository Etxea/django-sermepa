#-*- coding: utf-8 -*-
import hashlib
import base64
import json
import pyDes
import hmac

import logging
log = logging.getLogger(__name__)


class SermepaMixin(object):

    @staticmethod
    def encode_base64(data):
        import ipdb; ipdb.set_trace()
        return base64.b64encode(data)

    @staticmethod
    def decode_base64(data):
        return base64.b64decode(data)

    @staticmethod
    def urlsafe_b64encode(data):
        return base64.urlsafe_b64encode(data)

    @staticmethod
    def urlsafe_b64decode(data):
        return base64.urlsafe_b64decode(data)

    @classmethod
    def decode_merchant_parameters(cls, merchant_parameters):
        return json.loads(cls.urlsafe_b64decode(str(merchant_parameters)))

    @staticmethod
    def encrypt_3des(message, key):
        des3 = pyDes.triple_des(key, mode=pyDes.CBC, IV='\0' * 8, pad='\0', padmode=pyDes.PAD_NORMAL)
        encrypted = des3.encrypt(str(message))
        return encrypted

    @staticmethod
    def hmac256(data, key):
        return hmac.new(key, data, hashlib.sha256).digest()

    def get_firma_peticion(self, merchant_order, merchant_parameters, clave_sha256):
        key = self.decode_base64(clave_sha256)
        key_3des = self.encrypt_3des(merchant_order, key)
        firma_hmac = self.hmac256(merchant_parameters, key_3des)
        firma = self.encode_base64(firma_hmac)
        return firma

    def get_firma_respuesta(self, ds_order, merchant_parameters, clave_sha256):
        key = self.decode_base64(clave_sha256)
        key_3des = self.encrypt_3des(ds_order, key)
        firma_hmac = self.hmac256(merchant_parameters, key_3des)
        firma = self.urlsafe_b64encode(firma_hmac)
        return firma

    def verifica_firma(self, ds_order, merchant_parameters, firma, clave_sha256):
        return firma == self.get_firma_respuesta(ds_order, merchant_parameters, clave_sha256)

    @staticmethod
    def operacion_valida(respuesta):
        valor = int(respuesta)
        log.debug('Valor : %s ' % valor)
        return (valor >= 0) and (valor <= 99)