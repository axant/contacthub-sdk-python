from contacthub.models import Property


class Event(object):
    """
    Event model
    """
    __slots__ = ('internal_properties','mute')

    def __init__(self, **internal_properties):
        """
        :param customer_json_properties: A dictionary containing the json_properties related to customers
        """
        if internal_properties is None:
            internal_properties = Property()
        self.internal_properties = internal_properties
        self.mute = {}

    @classmethod
    def from_dict(cls, internal_properties=None, **kwargs):
        o = cls(**internal_properties)
        o.internal_properties = internal_properties or {}
        return o

    def __getattr__(self, item):
        """
        Check if a key is in the dictionary and return it if it's a simple property. Otherwise, if the
        element contains an object or list, redirect this element at the corresponding class.
        :param item: the key of the base property dict
        :return: an element of the dictionary, or an object if the element associated at the key containse an object or a list
        """
        try:
            if isinstance(self.internal_properties[item], dict):
                return Property.from_dict(parent_attr=item, parent=self,
                                          internal_properties=self.internal_properties[item])
            else:
                return self.internal_properties[item]
        except KeyError as e:
            raise AttributeError("%s object has no attribute %s" % (type(self).__name__, e))

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            return super(Event, self).__setattr__(attr, val)
        else:
            if isinstance(val, Property):
                self.internal_properties[attr] = val.internal_properties
            else:
                self.internal_properties[attr] = val

    class TYPES:
        """
        Event subclass for `type field of Event.
        Choose one of the above  API validated types or add your own in case of new types.
        """
        ABANDONED_CART = "abandonedCart"
        ADDED_COMPARE = "addedCompare"
        ADDED_PRODUCT = "addedProduct"
        ADDED_WISH_LIST = "addedWishlist"
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
        REMOVED_WISHLIST = "removedWishlist"
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





