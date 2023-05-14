#!/usr/bin/python3
"""
This module contain test cases for the states.py API views
"""
import unittest
from datetime import datetime
import uuid
import json
import requests
from models.state import State
from models import storage


class TestStates(unittest.TestCase):
    """Contain test cases for our APIs"""

    URL = 'http://0.0.0.0:5000/api/v1/states/'

    def setUp(self):
        """Delete all state objects in the database"""
        states = storage.all(State)
        [storage.delete(state) for state in states.values()]

    def tearDown(self):
        """Delete all states object"""
        states = storage.all(State)
        [storage.delete(state) for state in states.values()]

    def test_get_all_states(self):
        """
        Test if a get request to retrieve all state objects return
        a list of all state objects and response code of 200
        """
        state1 = State(name='Zanzibar')
        state2 = State(name='Tanganyika')
        state1.save()
        state2.save()
        r = requests.get(self.URL)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(isinstance(r.json(), list))
        self.assertEqual(len(r.json()), 2)
        output = r.json()
        ids = [item.get('id') for item in output]
        self.assertTrue(isinstance(output[0], dict))
        self.assertTrue(isinstance(output[1], dict))
        self.assertIn(state1.id, ids)
        self.assertIn(state2.id, ids)

    def test_get_single_state_with_valid_id(self):
        """
        Test if a get request to retrieve a state objects return
        a dictionary representation of it and response code of 200
        """
        state1 = State(name='Tanganyika')
        state1.save()
        r = requests.get('{}/{}'.format(self.URL, state1.id))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(isinstance(r.json(), dict))
        output = r.json()
        self.assertEqual(output.get('id'), state1.id)
        self.assertEqual(output.get('name'), state1.name)

    def test_get_single_state_with_fake_id(self):
        """
        Check whether an error is raised when the id does not exist
        """
        state1 = State(name='Zanzibar')
        state1.save()
        uid = str(uuid.uuid4())
        r = requests.get('{}/{}'.format(self.URL, uid))
        self.assertEqual(r.status_code, 404)
        out = r.json()
        self.assertTrue(isinstance(out, dict))
        self.assertEqual(len(out), 1)
        self.assertDictEqual(out, {"error": "Not found"})

    def test_delete_single_state(self):
        """
        Test deletion of a state from the user
        """
        state = State(name='Zanzibar')
        state.save()
        r = requests.delete('{}/{}'.format(self.URL, state.id))
        self.assertEqual(r.status_code, 200)
        output = r.json()
        self.assertTrue(isinstance(output, dict))
        self.assertEqual(len(output), 0)

    def test_delete_single_state_with_wrong_id(self):
        """Test if an error raise when we delete nonexistent state"""
        state1 = State(name='Zanzibar')
        state1.save()
        uid = str(uuid.uuid4())
        r = requests.delete('{}/{}'.format(self.URL, uid))
        self.assertEqual(r.status_code, 404)
        out = r.json()
        self.assertTrue(isinstance(out, dict))
        self.assertEqual(len(out), 1)
        self.assertDictEqual(out, {"error": "Not found"})

    def test_create_valid_state(self):
        """
        Test if a state is created given right input.
        Tests also that 201 is the response code and data is right
        """
        data = {
                'name': 'Zanzibar'
                }
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.URL, data=data, headers=headers)
        self.assertEqual(r.status_code, 201)
        out = r.json()
        self.assertIsInstance(out, dict)
        self.assertEqual(out.get('name'), 'Zanzibar')


    def test_create_state_with_invalid_json(self):
        """Test if Not a JSON error message is shown with 400 as
        status code"""
        data = "{'name': 'Zanzibar',}"
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.URL, data=data, headers=headers)
        self.assertEqual(r.status_code, 400)
        out = r.json()
        self.assertIsInstance(out, dict)
        self.assertDictEqual(out, {'error': 'Not a JSON'})

    def test_create_nameless_state(self):
        """Test if 400 error is raised"""
        data = {'nameless': 'valueless'}
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(data)
        r = requests.post(self.URL, data=data, headers=headers)
        self.assertEqual(r.status_code, 400)
        out = r.json()
        self.assertIsInstance(out, dict)
        self.assertDictEqual(out, {'error': 'Missing name'})

    def test_update_a_state(self):
        """
        Test if a PUT request returns status 200 and updates data
        """
        state = State(name='Tanganyika')
        state.save()
        data = {
                'name': 'Zanzibar'
                }
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(data)
        r = requests.put('{}/{}'.format(self.URL, state.id), data=data,
                         headers=headers)
        self.assertEqual(r.status_code, 200)
