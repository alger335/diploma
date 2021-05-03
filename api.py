class ApiBasic:

    host = ''

    def _call_api(self, http_method, api_method, params, response_type):
        ...
        try:
            response = requests.request(http_method, f'{self.host}/{api_method}', params=params)
        except requests.exceptions.ConnectionError:
            ...
        except ...:
            ...

        if response_type == 'json':
            ...

class YandexClient(ApiBasic):
    host = 'http://yandex.ru'
    pass
