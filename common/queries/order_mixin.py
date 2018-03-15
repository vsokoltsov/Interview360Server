import abc
import re

class QueryOrderMixin(abc.ABC):
    """ Mixin class for the order attribute """

    @property
    @abc.abstractmethod
    def order_fields(self):
        """ Value of order fields, which should be redefined in the query object """
        pass

    @property
    @abc.abstractmethod
    def params(self):
        """ Params value; Should be redefined in the child classes """
        pass

    @property
    def order(self):
        """ Return order value """

        order = self.params.get('order')
        return order if self.is_valid_order(order) else 'title'

    def is_valid_order(self, order):
        """ Return whether or not the order value is valid """

        order_template = re.compile('-')
        if order_template.match(str(order)):
            order = order[1:]
        return order in self.order_fields
