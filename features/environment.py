from behave.runner import Context
from starlette.testclient import TestClient

from src.routes import app


def before_all(context: Context):
    context.client = TestClient(app)
    context.response = None
