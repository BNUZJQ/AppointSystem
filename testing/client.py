import hashlib
import json

from django.conf import settings
from django.test.client import Client as DjangoClient


def get_sig(post, secret_key=settings.API_SECRET_KEY):
    params = []
    for key, value in post.iteritems():
        if key == 'sig':
            continue
        params.append({'key': key, 'value': value})
    params = sorted(params, key=lambda x: x['key'])
    md5 = hashlib.md5()
    string = u'&'.join(u'%s=%s' % (param['key'], param['value'])
                       for param in params)
    md5.update(string.encode('utf-8'))
    md5.update(secret_key)
    return md5.hexdigest()


class Client(DjangoClient):
    def _do_req(self, url, data, method, *args, **kwargs):
        if method == 'GET':
            response = super(Client, self).get(url, data, *args, **kwargs)
        else:
            response = super(Client, self).post(url, data, *args, **kwargs)

        decode = kwargs.get('decode', True)
        if decode:
            return json.loads(response.content)
        else:
            return response

    def get(self, url, data={}, *args, **kwargs):
        return self._do_req(url, data, 'GET', *args, **kwargs)

    def post(self, url, data={}, *args, **kwargs):
        return self._do_req(url, data, 'POST', *args, **kwargs)

    def sig_get(self, url, data={}, *args, **kwargs):
        data.update(sig=get_sig(data))
        return self._do_req(url, data, 'GET', *args, **kwargs)

    def sig_post(self, url, data={}, *args, **kwargs):
        data.update(sig=get_sig(data))
        return self._do_req(url, data, 'POST', *args, **kwargs)
