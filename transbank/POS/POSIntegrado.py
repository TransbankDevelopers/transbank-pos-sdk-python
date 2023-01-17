from transbank.utils.serial_manager import Serial
from transbank.error.transbank_exception import TransbankException
from transbank.responses.load_keys_response import LoadKeysResponse
from transbank.responses.multicode_sale_response import MultiCodeSaleResponse
from transbank.responses.refund_response import RefundResponse
from transbank.responses.totals_response import TotalsResponse
from transbank.responses.sale_response import SaleResponse
from transbank.responses.last_sale_response import LastSaleResponse
from transbank.responses.multicode_last_sale_response import MultiCodeLastSaleResponse
from transbank.responses.sales_detail_response import SalesDetailResponse
from transbank.responses.multicode_sales_detail_response import MultiCodeSalesDetailResponse
from transbank.responses.close_response import CloseResponse


class POSIntegrado(Serial):

    def poll(self):
        try:
            self.can_write()
            command = self.create_command("0100")
            self.serial_port.write(command)
            return self.check_ack()
        except Exception as e:
            raise TransbankException("Unable to send Poll command on port") from e

    def load_keys(self):
        try:
            self.can_write()
            response = self.send_command("0800")
            load_keys_response = LoadKeysResponse(response)
            return load_keys_response.get_response()
        except Exception as e:
            raise TransbankException("Unable to send load Keys command on port") from e

    def set_normal_mode(self):
        try:
            self.can_write()
            command = self.create_command("0300")
            self.serial_port.write(command)
            return self.check_ack()
        except Exception as e:
            raise TransbankException("Unable to send Normal Mode command on port") from e

    def sale(self, amount: int, ticket: str, send_status=False, callback=None):
        if amount < 50:
            raise TransbankException("Amount must be greater than 50")
        if amount > 999999999:
            raise TransbankException("Amount must be less than 999999999")
        if len(ticket) > 6:
            raise TransbankException("Ticket must be up to 6 in length")
        if send_status and callback is None:
            raise TransbankException("A callback function is needed for intermediate messages")
        try:
            command = "0200|{}|{}|||{}|".format(str(amount), ticket, "1" if send_status else "0")
            response = self.send_command(command, intermediate_messages=send_status, callback=callback)
            sale_response = SaleResponse(response)
            return sale_response.get_response()
        except Exception as e:
            raise TransbankException("Unable to send Sale command") from e

    def multicode_sale(self, amount: int, ticket: str, commerce_code: int, send_status=False):
        if amount < 50:
            raise TransbankException("Amount must be greater than 50")
        if amount > 999999999:
            raise TransbankException("Amount must be less than 999999999")
        if len(ticket) > 6:
            raise TransbankException("Ticket must be up to 6 in length")
        try:
            command = "0270|{}|{}|||{}|{}|".format(str(amount), ticket, "1" if send_status else "0", str(commerce_code))
            response = self.send_command(command)
            multicode_sale_response = MultiCodeSaleResponse(response)
            return multicode_sale_response.get_response()
        except Exception as e:
            raise TransbankException("Unable to execute multicode sale on pos") from e

    def last_sale(self):
        try:
            response = self.send_command("0250|")
            last_sale_response = LastSaleResponse(response)
            return last_sale_response.get_response()
        except Exception as e:
            raise TransbankException("Unable to recover last sale from pos") from e

    def multicode_last_sale(self, send_voucher=False):
        try:
            command = "0280|{}".format("1" if send_voucher else "0")
            response = self.send_command(command)
            last_sale_response = MultiCodeLastSaleResponse(response) if send_voucher else MultiCodeSaleResponse(response)
            return last_sale_response.get_response()
        except Exception as e:
            raise TransbankException("Unable to recover multicode last sale from pos") from e

    def refund(self, operation_id: int):
        try:
            command = "1200|{}|".format(str(operation_id))
            response = self.send_command(command)
            refund_response = RefundResponse(response)
            return refund_response.get_response()
        except Exception as e:
            raise TransbankException("Unable to make refund on pos") from e

    def totals(self):
        try:
            response = self.send_command("0700||")
            totals_response = TotalsResponse(response)
            return totals_response.get_response()
        except Exception as e:
            raise TransbankException("Unable to get totals from pos") from e

    def details(self, print_on_pos=False):
        try:
            command = "0260|{}|".format("1" if print_on_pos else "0")
            details_response = []
            details = self.send_command(command, sales_detail=True, print_on_pos=print_on_pos)
            for response in details:
                sale = SalesDetailResponse(response)
                details_response.append(sale.get_response())
            return details_response
        except Exception as e:
            raise TransbankException("Unable to request sale detail on pos") from e

    def multicode_details(self, print_on_pos=False):
        try:
            command = "0290|{}|".format("1" if print_on_pos else "0")
            details_response = []
            details = self.send_command(command, sales_detail=True, print_on_pos=print_on_pos)
            for response in details:
                multicode_sale = MultiCodeSalesDetailResponse(response)
                details_response.append(multicode_sale.get_response())
            return details_response
        except Exception as e:
            raise TransbankException("Unable to request multicode sale detail on pos") from e

    def close(self):
        try:
            response = self.send_command("0500||")
            close_response = CloseResponse(response)
            return close_response.get_response()
        except Exception as e:
            raise TransbankException("Unable to execute close in pos") from e


