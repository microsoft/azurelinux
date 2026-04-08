
class Skipper:
    """Skip iso8601 and pretend tests

    RHEL buildroot doesn't have python-iso8601 and python-pretend. Skip
    all tests that use the excluded modules.
    """

    def parse_date(self, datestring):
        pytest.skip(f"iso8601 module is not available.")

    def stub(self, **kwargs):
        pytest.skip(f"pretend module is not available.")

    def raiser(self, exc):
        pytest.skip(f"pretend module is not available.")


import sys

sys.modules["iso8601"] = sys.modules["pretend"] = Skipper()

