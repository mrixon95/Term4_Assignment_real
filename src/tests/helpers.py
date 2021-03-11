import unittest
from main import create_app, db
from flask import template_rendered, url_for
from contextlib import contextmanager


@contextmanager
def captured_templates(app):

    """This will capture the variables passed to the template and is used alongside the testing client"""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class Helpers(unittest.TestCase):

    """The test cases will be set up as well as torn down by the methods in this class along with often
    used methods like login/logout post and get requests"""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.context = cls.app.test_request_context()
        cls.app_context.push()
        cls.context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        result = runner.invoke(args=["db-custom", "seed"])
        if result.exit_code != 0:
            raise ValueError(result.stdout)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        cls.context.pop()

    @classmethod
    def login(cls, data):
        return cls.client.post(
            url_for("auth.login"), data=data, follow_redirects=True)

    @classmethod
    def logout(cls):
        cls.client.get(url_for("auth.logout"))

    @classmethod
    def post_request(cls, endpoint, data=None, content_type=None):
        return cls.client.post(
            endpoint, data=data, content_type=content_type,
            follow_redirects=True)

    @classmethod
    def get_request(cls, endpoint):
        return cls.client.get(endpoint, follow_redirects=True)

    @classmethod
    def encode(cls, data, encoding="utf-8"):
        return data.encode(encoding)