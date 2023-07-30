import unittest
import ConversationAgent as ca


# The test class
class TestImport(unittest.TestCase):

    def test_add(self):
        self.assertIsInstance(ca.__version__, str, f"version tag should be STRING type: ({type(ca.__version__)}), {ca.__version__}") 
