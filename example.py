from transbank.POS.POSIntegrado import POSIntegrado
from transbank.error.transbank_exception import TransbankException


def intermediate_message_callback(response):
    print("Intermediate message: {}".format(str(response['response_message'])))


port = "/dev/cu.usbmodem0123456789ABCD1"
POS = POSIntegrado()
print(POS.list_ports())
print(POS.open_port(port))
try:
    print(POS.load_keys())
except TransbankException as e:
    print(e)
    print(e.__cause__)
#print(POS.sale(25000, "abcd12", True, callback=intermediate_message_callback))
#print(POS.multicode_sale(1200, "Tic123", 597029414301))
#print(POS.set_normal_mode())
#print(POS.last_sale())
#print(POS.multicode_last_sale(True))
#print(POS.refund(83))
#print(POS.totals())
#print(POS.details(True))
#print(POS.multicode_details(True))
#print(POS.close())
