# test flask application

import json
import unittest
import os
os.environ['TESTING'] = 'true'

from app import app


class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        # checks home page loads with correct title
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Juan Escalada</title>" in html

    def test_timeline(self):
        # checks timeline page contains the key elements
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Timeline</title>" in html
        assert '<div id="menu" onclick="menuOnClick()">' in html
        assert '<form id="post-form">' in html
        assert '<div class="timeline mb-3">' in html

    def test_timelineapi_get(self):
        # checks GET endpoint returns empty timelie_post array in json format
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_response = response.get_json()
        assert "timeline_posts" in json_response
        assert len(json_response["timeline_posts"]) == 0

    def test_timelineapi_post(self):
        # checks POST endpoint correctly adds 1 timeline post
        # .
        # create a post and send data using POST
        post_data = {"name":"Judy", "email":"judy@hopps.com", "content":"carrots"}
        response = self.client.post("/api/timeline_post", data=post_data)
        assert response.status_code == 200
        json_response = response.get_json()
        # .
        # GET data and check that the correct post has been added
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_response = response.get_json()
        assert "timeline_posts" in json_response
        assert len(json_response["timeline_posts"]) == 1
        first_post = json_response["timeline_posts"][0]
        assert first_post['name'] == "Judy"
        assert first_post['email'] == "judy@hopps.com"
        assert first_post['content'] == "carrots"
        
    def test_timelineapi_post_malformed_requests(self):
        # checks POST requests with malformed input are handledp properly
        # .
        # requests missing fields
        # .
        # POST request missing name field
        response = self.client.post('/api/timeline_post', data={
            "email": "johndoe@email.com",
            "content": "Testing from test_app.py!"
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400
        assert "Request missing the field 'name'" in html

        # POST request missing email field
        response = self.client.post('/api/timeline_post', data={
            "name": "Johnny",
            "content": "Testing from test_app.py!"
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400
        assert "Request missing the field 'email'" in html

        # POST request missing content field
        response = self.client.post('/api/timeline_post', data={
            "name": "Johnny",
            "email": "johndoe@email.com",
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400
        assert "Request missing the field 'content'" in html


        # requests with empty contents
        # .
        # POST request empty name
        response = self.client.post('/api/timeline_post', data={
            "name": "",
            "email": "johndoe@email.com",
            "content": "Testing from test_app.py!"
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400
        assert "Invalid name" in html

        # POST request empty email
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe",
            "email": "",
            "content": "some content"
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400
        assert "Invalid email" in html

        # POST request empty content
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe",
            "email": "johndoe@email.com",
            "content": ""
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400
        assert "Invalid content" in html

        # enforce email format
        # POST request with malformed email
        response = self.client.post('/api/timeline_post', data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello world, I'm John!"
        })
        html = response.get_data(as_text=True)
        assert response.status_code == 400
        assert "Invalid email" in html