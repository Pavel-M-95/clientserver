import sys

import pytest
import socket as s

from JIMProtocol import MessageBuilder
from client import Client


@pytest.fixture
def socket_old_style(request):
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    def socket_teardown():
        _socket.close()
    request.addfinalizer(socket_teardown)
    return _socket


@pytest.yield_fixture
def socket():
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()


@pytest.yield_fixture
def client():
    _client = Client()
    yield _client
    # После ничего не делаем после


@pytest.yield_fixture
def my_std():
    orig_std = sys.stdin
    sys.stdout = "User"
    yield sys.stdin
    sys.stdout = orig_std


@pytest.yield_fixture
def responce():
    msg = MessageBuilder.create_presence_message("User")
    yield msg


def test_server_connect(socket):
    socket.connect(('localhost', 7777))
    assert socket


def test_responce_generating(responce):
    assert responce == MessageBuilder({"response": 200, "alert": "default"})