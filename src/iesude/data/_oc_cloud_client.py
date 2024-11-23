from ._cloud_client import Client
from ._external_deps import ocClient as _Client


def create_sciebo_client_from_public_url(url: str) -> Client:
    return _Client.from_public_link(url)
