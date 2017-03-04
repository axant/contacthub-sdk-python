from unittest import TestSuite

import mock
from datetime import datetime

from contacthub.models.address import Address, Geo
from contacthub.models.contacts import Contacts, OtherContact, MobileDevice
from contacthub.models.customer import Customer
from contacthub.models.customer_base_properties import CustomerBaseProperties
from contacthub.models.education import Education
from contacthub.models.job import Job
from contacthub.models.login_credentials import LoginCredentials
from contacthub.models.subscription import Subscription, Preference
from contacthub.models.tags import Tags
from contacthub.workspace import Workspace
from tests.utility import FakeHTTPResponse


class TestCustomer(TestSuite):

    @classmethod
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def setUp(cls, mock_get):
        w = Workspace(workspace_id=123, token=456)
        cls.node = w.get_node(123)
        cls.customers = cls.node.customers

    @classmethod
    def tearDown(cls):
        pass

    def test_customer(self):
        assert type(self.customers) is list, type(self.customers)
        assert self.customers[0].enabled, self.customers[0]

    def test_customer_base(self):
        for customer in self.customers:
            assert type(customer.base) is CustomerBaseProperties, type(customer.base)

    def test_customer_tags(self):
        tags = self.customers[0].tags
        assert type(tags) is Tags, type(tags)
        assert type(tags.auto) is list, type(tags.auto)
        assert type(tags.manual) is list, type(tags.manual)
        assert tags.auto[0] == 'auto', tags.auto[0]
        assert tags.manual[0] == 'manual', tags.manual[0]

    def test_customer_tags_empty(self):
        tags = self.customers[1].tags
        assert type(tags) is Tags, type(tags)
        assert type(tags.auto) is list, type(tags.auto)
        assert type(tags.manual) is list, type(tags.manual)
        assert len(tags.auto) == 0, len(tags.auto)
        assert len(tags.manual) == 0, len(tags.manual)

    def test_customer_contacts_other_contacts(self):
        other_contact = self.customers[0].base.contacts.otherContacts[0]
        assert type(other_contact) is OtherContact, type(other_contact)
        assert other_contact.name == 'name', other_contact.name
        assert other_contact.value == 'value', other_contact.value
        assert other_contact.type == OtherContact.TYPES.MOBILE, other_contact.type

    def test_customer_contacts_mobile_devices(self):
        mobile_device = self.customers[0].base.contacts.mobileDevices[0]
        assert type(mobile_device) is MobileDevice, type(mobile_device)
        assert mobile_device.identifier == 'identifier', mobile_device.name
        assert mobile_device.name == 'name', mobile_device.value
        assert mobile_device.type == MobileDevice.TYPES.IOS, mobile_device.type

    def test_customer_contacts(self):
        contacts = self.customers[0].base.contacts
        assert type(contacts) is Contacts, type(contacts)
        assert contacts.email == 'email@email.it', contacts.email
        assert contacts.fax == 'fax', contacts.fax
        assert contacts.mobilePhone == 'mobilePhone', contacts.mobilePhone
        assert contacts.phone == 'phone', contacts.phone
        assert type(contacts.otherContacts) is list, type(contacts.otherContacts)
        assert type(contacts.mobileDevices) is list, type(contacts.mobileDevices)

    def test_customer_contacts_other_contacts_empty(self):
        other_contacts = self.customers[1].base.contacts.otherContacts
        assert len(other_contacts) == 0, len(other_contacts)

    def test_customer_contacts_mobile_devices_empty(self):
        mobile_devices = self.customers[1].base.contacts.mobileDevices
        assert len(mobile_devices) == 0, len(mobile_devices)

    def test_customer_contacts_empty(self):
        contacts = self.customers[1].base.contacts
        assert type(contacts) is Contacts, type(contacts)
        assert contacts.fax is None, contacts.fax
        assert contacts.mobilePhone is None, contacts.mobilePhone
        assert contacts.phone is None, contacts.phone
        assert type(contacts.otherContacts) is list, type(contacts.otherContacts)
        assert type(contacts.mobileDevices) is list, type(contacts.mobileDevices)

    def test_customer_credentials(self):
        credentials = self.customers[0].base.credential
        assert type(credentials) is LoginCredentials, type(credentials)
        assert credentials.username == 'username', credentials.username
        assert credentials.password == 'password', credentials.password

    def test_customer_credentials_empty(self):
        credentials = self.customers[1].base.credential
        assert credentials is None, credentials

    def test_customer_education(self):
        educations = self.customers[0].base.educations
        assert type(educations) is list, type(educations)
        education = educations[0]
        assert type(education) is Education, type(education)
        assert education.schoolType == Education.SCHOOL_TYPES.COLLEGE,  education.schoolType
        assert education.schoolName == 'schoolName', education.schoolName
        assert education.schoolConcentration == 'schoolConcentration', education.schoolConcentration
        assert education.startYear == 1994, education.startYear
        assert education.endYear == 2000, education.endYear
        assert education.isCurrent, education.isCurrent

    def test_customer_education_empty(self):
        educations = self.customers[1].base.educations
        assert type(educations) is list, type(educations)
        assert len(educations) == 0, len(educations)

    def test_customer_subscriptions(self):
        subscriptions = self.customers[0].base.subscriptions
        assert type(subscriptions) is list, type(subscriptions)
        subscription = subscriptions[0]
        assert type(subscription) is Subscription, type(subscription)
        assert subscription.id == "id",  subscription.id
        assert subscription.name == "name", subscription.name
        assert subscription.type == "type", subscription.type
        assert subscription.kind == Subscription.KINDS.SERVICE, subscription.kind
        assert subscription.subscribed, subscription.subscribed
        assert type(subscription.startDate) is datetime, type(subscription.startDate)
        assert type(subscription.endDate) is datetime, type(subscription.endDate)
        assert subscription.subscriberId == "subscriberId", subscription.id
        assert type(subscription.registeredAt) is datetime, type(subscription.registeredAt)
        assert type(subscription.updatedAt) is datetime, type(subscription.updatedAt)
        assert type(subscription.preferences) is list, type(subscription.preferences)

    def test_customer_subscriptions_preferences(self):
        preferences = self.customers[0].base.subscriptions[0].preferences
        assert type(preferences) is list, type(preferences)
        preference = preferences[0]
        assert type(preference) is Preference, type(preference)
        assert preference.key == "key", preference.key
        assert preference.value == "value", preference.value

    def test_customer_subscriptions_empty(self):
        subscriptions = self.customers[1].base.subscriptions
        assert type(subscriptions) is list, type(subscriptions)
        assert len(subscriptions) == 0, len(subscriptions)

    def test_customer_jobs(self):
        jobs = self.customers[0].base.jobs
        assert type(jobs) is list, type(jobs)
        job = jobs[0]
        assert type(job) is Job, type(job)
        assert job.companyIndustry == 'companyIndustry', job.companyIndustry
        assert job.companyName == 'companyName', job.companyName
        assert job.jobTitle == 'jobTitle', job.jobTitle
        assert type(job.startDate) is datetime, type(job.startDate)
        assert type(job.endDate) is datetime, type(job.endDate)
        assert job.isCurrent, job.isCurrent

    def test_customer_jobs_empty(self):
        jobs = self.customers[1].base.jobs
        assert type(jobs) is list, type(jobs)
        assert len(jobs) == 0, len(jobs)

    def test_customer_address(self):
        address = self.customers[0].base.address
        assert type(address) is Address, type(address)
        assert address.street == 'street', address.street
        assert address.city == 'city', address.city
        assert address.country == 'country', address.country
        assert address.province == 'province', address.province
        assert address.zip == 'zip', address.zip
        assert type(address.geo) is Geo,  type(address.geo)

    def test_customer_address_geo(self):
        geo = self.customers[0].base.address.geo
        assert type(geo.lat) is int, type(geo.lat)
        assert type(geo.lon) is int, type(geo.lon)

    def test_customer_address_empty(self):
        address = self.customers[1].base.address
        assert address is None, address

    def test_customer_social_profile(self):
        social_profile = self.customers[0].base.socialProfile
        assert social_profile.facebook == 'facebook', social_profile.facebook
        assert social_profile.google == 'google', social_profile.google
        assert social_profile.instagram == 'instagram', social_profile.instagram
        assert social_profile.linkedin == 'linkedin', social_profile.linkedin
        assert social_profile.qzone == 'qzone', social_profile.qzone
        assert social_profile.twitter == 'twitter', social_profile.twitter

    def test_customer_social_profile_empty(self):
        social_profile = self.customers[1].base.socialProfile
        assert social_profile is None, social_profile

    # def test(self):
    #     ret = self.node.query(Customer).filter((Customer.base.contacts == 'marco.bosi@axant.it')).all()
    #     assert False, ret







