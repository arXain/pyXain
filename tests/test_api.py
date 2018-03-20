import unittest
import os
import json
import shutil
import io
from pyxain import api

class TestApi(unittest.TestCase):
    def setUp(self):
        # create a test api each test case can use
        api.testing = True

        self.test_api = api.app.test_client()

    def assertValid(self, response):
        self.assertEquals(response.status, "200 OK")


class TestPyxain(TestApi):

    @classmethod
    def teardown_class(self):
        """remove test_author_api directory"""
        arxain_path = os.path.join(os.path.expanduser("~"), 'arXain-data')
        test_dir = os.path.join(arxain_path, 'authors', 'test_author_api')
        shutil.rmtree(test_dir)

    def test_index(self):
        """api: `/`"""
        response = self.test_api.get('/')

        self.assertValid(response)

    def test_init_arxain(self):
        """api: `/init/arxain`"""
        response = self.test_api.get('/init/arxain')
        self.assertValid(response)

        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], True)

    def test_init_author(self):
        """api: `/init/author`"""
        response = self.test_api.get('/init/author', \
            query_string=dict(author_id='test_author_api'))
        self.assertValid(response)

        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], True)

    def test_submit_manuscript(self):
        """api: `/submit/manuscript`"""
        # Get the test pdf in the folder
        curr_dir = os.path.dirname(os.path.abspath(__file__))

        # Test valid submission
        payload = dict(author_id='test_author_api',\
                        paper_id='test_paper',\
                        paper_directory=os.path.join(curr_dir, 'test-paper'))

        response = self.test_api.get('/submit/manuscript', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        print(json_response)
        self.assertEquals(json_response['Success'], True)

        # Test submit with wrong author
        payload = dict(author_id='not_an_initiallized_author',\
                        paper_id='test_paper',\
                        paper_directory=os.path.join(curr_dir, 'test-paper'))
        response = self.test_api.get('/submit/manuscript', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], False)

        # Test submit an empty directory
        payload = dict(author_id='test_author_api',\
                        paper_id='test_paper',\
                        paper_directory=os.path.join(curr_dir, 'test-empty'))
        response = self.test_api.get('/submit/manuscript', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], False)

    def test_submit_revision(self):
        """api: `/submit/revision`"""
        # Get the test pdf in the folder
        curr_dir = os.path.dirname(os.path.abspath(__file__))

        # Test valid submission
        payload = dict(author_id='test_author_api',\
                        paper_id='test_paper',\
                        paper_directory=os.path.join(curr_dir, 'test-paper-rev'))

        response = self.test_api.get('/submit/revision', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        print(json_response)
        self.assertEquals(json_response['Success'], True)

        # Test submit with wrong author
        payload = dict(author_id='not_an_initiallized_author',\
                        paper_id='test_paper',\
                        paper_directory=os.path.join(curr_dir, 'test-paper-rev'))
        response = self.test_api.get('/submit/revision', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], False)

        # Test submit an empty directory
        payload = dict(author_id='test_author_api',\
                        paper_id='test_paper',\
                        paper_directory=os.path.join(curr_dir, 'test-empty'))
        response = self.test_api.get('/submit/revision', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], False)

        # Test submit with redundant paper
        payload = dict(author_id='not_an_initiallized_author',\
                        paper_id='test_paper',\
                        paper_directory=os.path.join(curr_dir, 'test-paper'))
        response = self.test_api.get('/submit/revision', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], False)

    def test_submit_comment(self):
        """api: `/submit/comment`"""
        # Get the test pdf in the folder
        curr_dir = os.path.dirname(os.path.abspath(__file__))

        # Test valid submission
        payload = dict(author_id='test_author_api',\
                        paper_id='test_paper',\
                        comment_directory=os.path.join(curr_dir, 'test-comment'))

        response = self.test_api.get('/submit/comment', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        print(json_response)
        self.assertEquals(json_response['Success'], True)

        # Test submit with wrong author
        payload = dict(author_id='not_an_initiallized_author',\
                        paper_id='test_paper',\
                        comment_directory=os.path.join(curr_dir, 'test-comment'))
        response = self.test_api.get('/submit/comment', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], False)

        # Test submit an empty directory
        payload = dict(author_id='test_author_api',\
                        paper_id='test_paper',\
                        comment_directory=os.path.join(curr_dir, 'test-empty'))
        response = self.test_api.get('/submit/comment', query_string=payload)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], False)

    def test_pin_manuscript(self):
        """api: `/pin/manuscript`"""
        response = self.test_api.get('/pin/manuscript')
        self.assertEquals(response.get_data(as_text=True), 'reserved for future use')

    def test_upload_file(self):
        """api: `/upload/file`"""

        # test pdf
        data = dict(paper=(io.BytesIO(b'testing123'), 'testPaper.pdf'))
        response = self.test_api.post(
            '/upload/file', data=data,
            content_type='multipart/form-data'
            )
        self.assertValid(response)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], True)

        # test txt
        data = dict(paper=(io.BytesIO(b'testing123'), 'testPaper.txt'))
        response = self.test_api.post(
            '/upload/file', data=data,
            content_type='multipart/form-data'
            )
        self.assertValid(response)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], True)

        #test json
        data = dict(paper=(io.BytesIO(b'testing123'), 'testPaper.json'))
        response = self.test_api.post(
            '/upload/file', data=data,
            content_type='multipart/form-data'
            )
        self.assertValid(response)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], True)

        # test html refusal
        data = dict(paper=(io.BytesIO(b'testing123'), 'testPaper.html'))
        response = self.test_api.post(
            '/upload/file', data=data,
            content_type='multipart/form-data'
            )
        self.assertValid(response)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEquals(json_response['Success'], False)
