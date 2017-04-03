from copy import deepcopy

from contacthub.api_manager.api_event import EventAPIManager
from contacthub.lib.utils import convert_properties_obj_in_prop
from contacthub.models import Properties



class Event(object):
    """
    Event model
    """
    __attributes__ = ('attributes','mute', 'node', 'event_api_manager')

    def __init__(self, node, **attributes):
        """
        :param customer_json_properties: A dictionary containing the json_properties related to customers
        """
        convert_properties_obj_in_prop(properties=attributes, properties_class=Properties)
        self.attributes = attributes
        self.node = node
        self.event_api_manager = EventAPIManager(node=self.node)

    @classmethod
    def from_dict(cls, node, attributes=None):
        o = cls(node=node)
        if attributes is None:
            o.attributes = {}
        else:
            o.attributes = attributes
        return o

    def to_dict(self):
        return deepcopy(self.attributes)

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple properties. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base properties dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        try:
            if isinstance(self.attributes[item], dict):
                return Properties.from_dict(attributes=self.attributes[item])
            else:
                return self.attributes[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__attributes__:
            return super(Event, self).__setattr__(attr, val)
        else:
            if isinstance(val, Properties):
                self.attributes[attr] = val.attributes
            else:
                if isinstance(val, list) and val and isinstance(val[0], Properties):
                        self.attributes[attr] = []
                        for elem in val:
                            self.attributes[attr] += [elem.attributes]
                else:
                    self.attributes[attr] = val

    def post(self):
        self.event_api_manager.post(body=self.attributes)


    class TYPES:
        """
        Event subclass for `type field of Event.
        Choose one of the above  API validated types or add your own in case of new types.
        """
        ABANDONED_CART = "abandonedCart"
        ADDED_COMPARE = "addedCompare"
        ADDED_PRODUCT = "addedProduct"
        ADDED_WISH_LIST = "addedWishList"
        CAMPAIGN_BLACKLISTED = "campaignBlacklisted"
        CAMPAIGN_BOUNCED = "campaignBounced"
        CAMPAIGN_LINK_CLICKED = "campaignLinkClicked"
        CAMPAIGN_MARKED_SPAM = "campaignMarkedSpam"
        CAMPAIGN_OPENED = "campaignOpened"
        CAMPAIGN_SENT = "campaignSent"
        CAMPAIGN_SUBSCRIBED = "campaignSubscribed"
        CAMPAIGN_UNSUBSCRIBED = "campaignUnsubscribed"
        CHANGED_SETTING = "changedSetting"
        CLICKED_LINK = "clickedLink"
        CLOSED_TICKET = "closedTicket"
        COMPLETED_ORDER = "completedOrder"
        EVENT_INVITED = "eventInvited"
        EVENT_PARTECIPATED = "eventParticipated"
        FORM_COMPILED = "formCompiled"
        GENERIC_ACTIVE_EVENT = "genericActiveEvent"
        GENERIC_PASSIVE_EVENT = "genericPassiveEvent"
        LOGGED_IN = "loggedIn"
        LOGGED_OUT = "loggedOut"
        OPENED_TICKET = "openedTicket"
        ORDER_SHIPPED = "orderShipped"
        REMOVED_COMPARE = "removedCompare"
        REMOVED_PRODUCT = "removedProduct"
        REMOVED_WISHLIST = "removedWishList"
        REPLIED_TICKET = "repliedTicket"
        REVIEWED_PRODUCT = "reviewedProduct"
        SEARCHED = "searched"
        SERVICE_SUBSCRIBED = "serviceSubscribed"
        SERVICE_UNSUBSCRIBED = "serviceUnsubscribed"
        VIEWED_PAGE = "viewedPage"
        VIEWED_PRODUCT = "viewedProduct"
        VIEWED_PRODUCT_CATEGORY = "viewedProductCategory"

    class CONTEXTS:
        """`
        Event subclass for `context` field of Event.
        Choose one of the above  API validated contexts or add your own in case of new types.
        """
        CONTACT_CENTER = "CONTACT_CENTER"
        WEB = "WEB"
        MOBILE = "MOBILE"
        ECOMMERCE = "ECOMMERCE"
        RETAIL = "RETAIL"
        IOT = "IOT"
        SOCIAL = "SOCIAL"
        DIGITAL_CAMPAIGN = "DIGITAL_CAMPAIGN"
        OTHER = "OTHER"





