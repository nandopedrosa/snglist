"""
tests.py: Application unit tests

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import unittest
from app.util import getsoup


class ScrapingTests(unittest.TestCase):
    def test_cifraclub(self):
        soup = getsoup('https://www.cifraclub.com.br/jethro-tull/locomotive-breath/imprimir.html#columns=false')
        html = ''

        sections = soup.find_all('pre')
        for s in sections:
            html += str(s)

        self.assertIsNot(html, '')


if __name__ == '__main__':
    unittest.main()
