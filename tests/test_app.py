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
        
