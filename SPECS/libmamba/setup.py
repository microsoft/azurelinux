from setuptools import setup
from setuptools.dist import Distribution

# Tested with wheel v0.29.0
class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True


setup(
      # Include pre-compiled extension
      #package_data={"libmambapy": ["bindings.pyd"]},
      distclass=BinaryDistribution)
