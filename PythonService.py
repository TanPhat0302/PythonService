import logging
logging.basicConfig(level=logging.DEBUG)
from zeep import Client 
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class TimezoneService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def country_to_timezone(ctx, country):
        client = Client("http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL")
        countryCode = client.service.CountryISOCode(country)
        if countryCode == "FI" or countryCode == "SE" or countryCode == "EE" or countryCode == "PL":
            return "UTC+3"
        elif countryCode == "TH" or countryCode == "VN" or countryCode == "ID" or countryCode =="MY" or countryCode =="KH":
            return "UTC+7"
        elif countryCode == "JP" or countryCode == "KR":
            return "UTC+9"

         

application = Application([TimezoneService],
    tns='spyne.timezone',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
    