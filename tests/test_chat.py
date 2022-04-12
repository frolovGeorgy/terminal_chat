import socket
import threading

import pytest

from src.server import Server
from src.client import Client


@pytest.fixture
def setup():
    return Server(), Client()


def test_sas2(setup):
    assert True
