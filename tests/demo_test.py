"""Demo version test."""

import unittest

from go_reaction_logic import __version__


class TestVersion(unittest.TestCase):

    """Test version."""

    def test_version_type(self):
        """Demo test."""
        self.assertIsInstance(__version__, str)
