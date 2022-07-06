# template https://github.com/carletes/mock-ssh-server#sample-usage

from tests.base_test import PUB_FILE

from pytest import yield_fixture

import pwd
import os
import mockssh

@pytest.fixture()
def server():
    users = {
        pwd.getpwuid(os.geteuid()).pw_name: PUB_FILE,
    }
    with mockssh.Server(users) as s:
        yield s
