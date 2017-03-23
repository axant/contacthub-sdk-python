import json
import unittest
from datetime import datetime

import mock

from contacthub.models import BaseProperties
from contacthub.models.customer import Customer
from contacthub.models.education import Education
from contacthub.models.entity import Entity
from contacthub.models.event import Event
from contacthub.models.job import Job
from contacthub.models.like import Like
from contacthub.workspace import Workspace
from copy import deepcopy
from requests import HTTPError
from tests.utility import FakeHTTPResponse


class TestCustomer(unittest.TestCase):

    @classmethod
    @mock.patch('requests.get', return_value=FakeHTTPResponse())
    def setUp(cls, mock_get):
        w = Workspace(workspace_id="123", token="456")
        cls.node = w.get_node("123")
        cls.customers = cls.node.get_customers()
        cls.headers_expected = {'Authorization': 'Bearer 456', 'Content-Type': 'application/json'}
        cls.base_url_events = 'https://api.contactlab.it/hub/v1/workspaces/123/events'
        cls.base_url_customer = 'https://api.contactlab.it/hub/v1/workspaces/123/customers'

    @classmethod
    def tearDown(cls):
        pass

    def test_customer_base(self):
        for customer in self.customers:
            assert type(customer.base) is Entity, type(customer.base)

    def test_customer_tags(self):
        tags = self.customers[0].tags
        assert type(tags) is Entity, type(tags)
        assert type(tags.auto) is list, type(tags.auto)
        assert type(tags.manual) is list, type(tags.manual)
        assert tags.auto[0] == 'auto', tags.auto[0]
        assert tags.manual[0] == 'manual', tags.manual[0]


    def test_customer_tags_wrog_attr(self):
        try:
            self.customers[0].tags.attr
        except AttributeError as e:
            assert 'attr' in str(e), str(e)

    def test_customer_tags_empty(self):
        tags = self.customers[1].tags
        assert type(tags) is Entity, type(tags)
        assert type(tags.auto) is list, type(tags.auto)
        assert type(tags.manual) is list, type(tags.manual)
        assert len(tags.auto) == 0, len(tags.auto)
        assert len(tags.manual) == 0, len(tags.manual)

    def test_customer_contacts_other_contacts(self):
        other_contact = self.customers[0].base.contacts.otherContacts[0]
        assert type(other_contact) is Entity, type(other_contact)
        assert other_contact.name == 'name', other_contact.name
        assert other_contact.value == 'value', other_contact.value

    def test_customer_contacts_mobile_devices(self):
        mobile_device = self.customers[0].base.contacts.mobileDevices[0]
        assert type(mobile_device) is Entity, type(mobile_device)
        assert mobile_device.identifier == 'identifier', mobile_device.name
        assert mobile_device.name == 'name', mobile_device.value

    def test_customer_contacts(self):
        contacts = self.customers[0].base.contacts
        assert type(contacts) is Entity, type(contacts)
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
        assert type(contacts) is Entity, type(contacts)
        assert contacts.fax is None, contacts.fax
        assert contacts.mobilePhone is None, contacts.mobilePhone
        assert contacts.phone is None, contacts.phone
        assert type(contacts.otherContacts) is list, type(contacts.otherContacts)
        assert type(contacts.mobileDevices) is list, type(contacts.mobileDevices)

    def test_customer_credentials(self):
        credentials = self.customers[0].base.credential
        assert type(credentials) is Entity, type(credentials)
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

    def test_customer_unexsistant_attribute(self):
        educations = self.customers[0].base.educations
        assert type(educations) is list, type(educations)
        education = educations[0]
        try:
            attr = education.attr
        except AttributeError as e:
            assert 'attr' in str(e), str(e)

    def test_customer_education_empty(self):
        educations = self.customers[1].base.educations
        assert type(educations) is list, type(educations)
        assert len(educations) == 0, len(educations)

    def test_customer_subscriptions(self):
        subscriptions = self.customers[0].base.subscriptions
        assert type(subscriptions) is list, type(subscriptions)
        subscription = subscriptions[0]
        assert type(subscription) is Entity, type(subscription)
        assert subscription.id == "id",  subscription.id
        assert subscription.name == "name", subscription.name
        assert subscription.type == "type", subscription.type
        assert subscription.subscribed, subscription.subscribed
        #assert type(subscription.startDate) is datetime, type(subscription.startDate)
        #assert type(subscription.endDate) is datetime, type(subscription.endDate)
        assert subscription.subscriberId == "subscriberId", subscription.id
        #assert type(subscription.registeredAt) is datetime, type(subscription.registeredAt)
        #assert type(subscription.updatedAt) is datetime, type(subscription.updatedAt)
        assert type(subscription.preferences) is list, type(subscription.preferences)

    def test_customer_subscriptions_preferences(self):
        preferences = self.customers[0].base.subscriptions[0].preferences
        assert type(preferences) is list, type(preferences)
        preference = preferences[0]
        assert type(preference) is Entity, type(preference)
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

    def test_customer_like(self):
        likes = self.customers[0].base.likes
        assert type(likes) is list, type(likes)
        like = likes[0]
        assert type(like) is Like, type(like)

    def test_customer_jobs_empty(self):
        jobs = self.customers[1].base.jobs
        assert type(jobs) is list, type(jobs)
        assert len(jobs) == 0, len(jobs)

    def test_customer_address(self):
        address = self.customers[0].base.address
        assert type(address) is Entity, type(address)
        assert address.street == 'street', address.street
        assert address.city == 'city', address.city
        assert address.country == 'country', address.country
        assert address.province == 'province', address.province
        assert address.zip == 'zip', address.zip
        assert type(address.geo) is Entity,  type(address.geo)

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

    def test_customer_unexistent_attr(self):
        with self.assertRaises(AttributeError) as context:
            attr = self.customers[0].attr
        self.assertTrue('attr' in str(context.exception))

    def test_customer_sett_attr(self):
        self.customers[0].externalId = 3
        assert self.customers[0].externalId == 3, self.customers[0].externalId

    def test_customer_address_unexistent_attr(self):
        with self.assertRaises(AttributeError) as context:
            attr = self.customers[0].base.address.attr
        self.assertTrue('attr' in str(context.exception))

    def test_customer_contacts_unexistent_attr(self):
        with self.assertRaises(AttributeError) as context:
            attr = self.customers[0].base.contacts.attr
        self.assertTrue('attr' in str(context.exception))


    def test_customer_base_unexistent_attr(self):
        with self.assertRaises(AttributeError) as context:
            attr = self.customers[0].base.attr
        self.assertTrue('attr' in str(context.exception))

    def test_customer_subscription_unexistent_attr(self):
        with self.assertRaises(AttributeError) as context:
            attr = self.customers[0].base.subscriptions[0].attr
        self.assertTrue('attr' in str(context.exception))

    def test_customer_property_unexistent_attr(self):
        with self.assertRaises(AttributeError) as context:
            p = Entity({'attributo':1})
            attr = p.attr
        self.assertTrue('attr' in str(context.exception))

    def test_customer_job_unexistent_attr(self):
        with self.assertRaises(AttributeError) as context:
            attr = self.customers[0].base.jobs[0].attr
        self.assertTrue('attr' in str(context.exception))

    def test_customer_like_unexistent_attr(self):
        with self.assertRaises(AttributeError) as context:
            attr = self.customers[0].base.likes[0].attr
        self.assertTrue('attr' in str(context.exception))

    def test_customer_like_created_time(self):
        ct = self.customers[0].base.likes[0].createdTime
        assert isinstance(ct, datetime), type(datetime)

    @mock.patch('requests.get', return_value=FakeHTTPResponse(resp_path='tests/util/fake_event_response'))
    def test_all_events(self, mock_get_event):
        events = self.customers[0].events
        params_expected = {'customerId': self.customers[0].id}
        mock_get_event.assert_called_with(self.base_url_events, params=params_expected, headers=self.headers_expected)
        assert isinstance(events, list), type(events)
        assert events[0].type == Event.TYPES.ADDED_COMPARE, events[0].type

    def test_all_events_new_customer(self):
        try:
            Customer(node=self.node).events
        except Exception as e:
            assert 'events' in str(e), str(e)

    def test_customer_create_extra(self):
        c = Customer(node=self.node, extra='extra')
        assert c.properties['extra'] == 'extra', c.properties['extra']
        assert c.extra == 'extra', c.extra

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_delete(self, mock_delete):
        id = self.customers[0].id
        self.customers[0].delete()
        mock_delete.assert_called_with(self.base_url_customer + '/' + id, headers=self.headers_expected)

    def test_delete_created_new_customer(self):
        try:
            Customer(node=self.node).delete()
        except Exception as e:
            assert 'delete' in str(e), str(e)

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response', status_code=401))
    def test_delete_not_permitted(self, mock_delete):
        try:
            self.customers[0].delete()
        except HTTPError as e:
            assert 'message' in str(e), str(e)

    @mock.patch('requests.delete', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_delete_created(self, mock_delete):
        Customer(id='01', node=self.node).delete()
        mock_delete.assert_called_with(self.base_url_customer + '/01', headers=self.headers_expected)

    @mock.patch('contacthub.APIManager.api_customer.CustomerAPIManager.post')
    def test_post_customer_creation_first_method(self, mock_post):
        expected_body = {'base': {'contacts': {'email': 'email@email.email'}}, 'extra': 'extra', 'extended': {'prova':'prova'},
                         'tags': {'auto': ['auto'], 'manual': ['manual']}}
        mock_post.return_value = json.loads(FakeHTTPResponse(resp_path='tests/util/fake_post_response').text)
        c = Customer(node=self.node,
            base=Entity(
                contacts=Entity(email='email@email.email')
            )
        )

        c.extra = 'extra'
        c.extended.prova = 'prova'
        c.tags.auto = ['auto']
        c.tags.manual = ['manual']

        posted = c.post()
        mock_post.assert_called_with(body=expected_body, force_update=False)
        assert isinstance(posted, Customer), type(posted)
        assert posted.base.contacts.email == c.base.contacts.email, posted.base.contacts.email
        assert posted.extra == c.extra, posted.extra

    # @mock.patch('contacthub.APIManager.api_customer.CustomerAPIManager.post')
    # def test_post_customer_creation_second_method(self, mock_post):
    #     expected_body = {'base': {'contacts': {'email': 'email@email.email'}}, 'extra': 'extra'}
    #     mock_post.return_value = json.loads(FakeHTTPResponse(resp_path='tests/util/fake_post_response').text)
    #     c = Customer(base=Entity(), node=self.node)
    #     c.base.contacts = Entity(email='email@email.email')
    #     c.extra = 'extra'
    #     posted = c.post()
    #     mock_post.assert_called_with(body=expected_body, force_update=False)
    #     assert isinstance(posted, Customer), type(posted)
    #     assert posted.base.contacts.email == c.base.contacts.email, posted.base.contacts.email
    #     assert posted.extra == c.extra, posted.extra

    @mock.patch('contacthub.APIManager.api_customer.CustomerAPIManager.post')
    def test_post_customer_creation_second_method(self, mock_post):
        expected_body = {'base': {'contacts': {'email': 'email@email.email'}}, 'extra': 'extra', 'extended': {}, 'tags': {'auto': [], 'manual': []}}
        mock_post.return_value = json.loads(FakeHTTPResponse(resp_path='tests/util/fake_post_response').text)
        c = Customer(node=self.node,base=Entity())
        c.base.contacts = {'email': 'email@email.email'}
        c.extra = 'extra'
        posted = c.post()
        mock_post.assert_called_with(body=expected_body, force_update=False)
        assert isinstance(posted, Customer), type(posted)
        assert posted.base.contacts.email == c.base.contacts.email, posted.base.contacts.email
        assert posted.extra == c.extra, posted.extra


    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch(self, mock_patch):
        self.customers[0].base.firstName = 'fn'
        self.customers[0].patch()
        body = {'base':{'firstName':'fn'}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id, headers=self.headers_expected, json=body)

    @mock.patch('requests.put', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_put(self, mock_patch):
        self.customers[0].base.firstName = 'fn'
        self.customers[0].put()
        body = deepcopy(self.customers[0].properties)
        body.pop('updatedAt')
        body.pop('registeredAt')
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_entity(self, mock_patch):
        self.customers[0].extended = Entity(a=1, prova=Entity(b=1))
        self.customers[0].patch()
        body = {'extended': {'prova': {'b': 1, 'oggetto': None, 'list': None}, 'a': 1}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)


    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_entity_extended_and_base(self, mock_patch):
        self.customers[0].extended = Entity(a=1, prova=Entity(b=1))
        self.customers[0].base.firstName = 'fn'
        self.customers[0].patch()
        body = {'extended': {'prova': {'b': 1, 'oggetto': None, 'list': None}, 'a': 1}, 'base': {'firstName': 'fn'}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_extended_entity_and_base_entity(self, mock_patch):
        self.customers[0].extended = Entity(a=1, prova=Entity(b=1))
        self.customers[0].base = Entity(contacts=Entity(email='email'))
        self.customers[0].patch()
        body = {'extended': {'prova': {'b': 1, 'oggetto': None, 'list': None}, 'a': 1},
                'base': {
                    'pictureUrl': None, 'title': None, 'prefix': None, 'firstName': None, 'lastName': None,
                    'middleName': None, 'gender': None, 'dob': None, 'locale': None, 'timezone': None,
                    'contacts':
                        {'email': 'email', 'fax': None, 'mobilePhone': None, 'phone': None, 'otherContacts': None, 'mobileDevices': None},
                    'address': None, 'credential': None, 'educations': None, 'likes': None, 'socialProfile': None, 'jobs': None, 'subscriptions': None}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_entity_with_entity(self, mock_patch):
        self.customers[0].extended = Entity(a=1, prova=Entity(b=1))
        self.customers[0].base.contacts = Entity(email='email')
        self.customers[0].patch()
        body = {'extended': {'prova': {'b': 1, 'oggetto': None, 'list': None}, 'a': 1},'base':
            {'contacts':{'email': 'email', 'fax': None, 'mobilePhone': None, 'phone': None, 'otherContacts': None, 'mobileDevices': None}}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_entity_with_rename(self, mock_patch):
        self.customers[0].extended = Entity(a=1, prova=Entity(b=1))
        self.customers[0].base.contacts = Entity(email1='email')
        self.customers[0].patch()
        body = {'extended': {'prova': {'b': 1, 'oggetto': None, 'list': None}, 'a': 1}, 'base':
            {'contacts': {'email': None,'email1':'email', 'fax': None, 'mobilePhone': None, 'phone': None, 'otherContacts': None,
                          'mobileDevices': None}}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_entity_with_rename_dict(self, mock_patch):
        self.customers[0].extended = Entity(a=1, prova=Entity(b=1))
        self.customers[0].base.contacts = Entity(email1=Entity(a=1))
        self.customers[0].patch()
        body = {'extended': {'prova': {'b': 1, 'oggetto': None, 'list': None}, 'a': 1}, 'base':
            {'contacts': {'email': None, 'email1': {'a': 1}, 'fax': None, 'mobilePhone': None, 'phone': None,
                          'otherContacts': None,
                          'mobileDevices': None}}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_entity_list(self, mock_patch):
        self.customers[0].extended = Entity(a=1, prova=Entity(b=1))
        self.customers[0].base.contacts.otherContacts = [Entity(email1=Entity(a=1))]
        self.customers[0].patch()
        body = {'extended': {'prova': {'b': 1, 'oggetto': None, 'list': None}, 'a': 1}, 'base': {'contacts': {'otherContacts': [{'email1': {'a': 1}}]}}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_entity_new_list(self, mock_patch):
        self.customers[0].base.contacts = Entity(email='email')
        self.customers[0].base.contacts.otherContacts = [Entity(email1=Entity(a=1))]
        self.customers[0].patch()
        body = {'base': {'contacts': {'email':'email', 'fax':None, 'mobilePhone':None,'phone':None, 'mobileDevices':None,
                                      'otherContacts': [{'email1': {'a': 1}}]}}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_entity_new_list_with_entities(self, mock_patch):
        self.customers[0].base.contacts = Entity(email='email')
        self.customers[0].base.contacts.otherContacts = [Entity(email1=Entity(a=Entity(b=1)))]
        self.customers[0].patch()
        body = {'base': {
            'contacts': {'email': 'email', 'fax': None, 'mobilePhone': None, 'phone': None, 'mobileDevices': None,
                         'otherContacts': [{'email1': {'a': {'b':1}}}]}}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_all_extended(self, mock_patch):
        self.customers[0].extended = Entity()
        self.customers[0].patch()
        body = {'extended': {'prova': None}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_all_base(self, mock_patch):
        self.customers[0].base = Entity()
        self.customers[0].patch()
        body = {'base': {'pictureUrl': None, 'title': None, 'prefix': None, 'firstName': None, 'lastName': None,
                         'middleName': None, 'gender': None, 'dob': None, 'locale': None,
                         'timezone': None, 'contacts': None, 'address': None, 'credential': None, 'educations': None,
                         'likes': None, 'socialProfile': None, 'jobs': None, 'subscriptions': None}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)

    @mock.patch('requests.patch', return_value=FakeHTTPResponse(resp_path='tests/util/fake_post_response'))
    def test_patch_elem_in_list(self, mock_patch):
        self.customers[0].base.contacts.otherContacts[0].type='TYPE'
        self.customers[0].patch()
        body = {'base':{'contacts': {'otherContacts':[{'name': 'name', 'type': 'TYPE', 'value': 'value'}, {'name': 'Casa di piero', 'type': 'PHONE', 'value': '12343241'}]}}}
        mock_patch.assert_called_with(self.base_url_customer + '/' + self.customers[0].id,
                                      headers=self.headers_expected, json=body)


