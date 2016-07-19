"""
tests.py: Application unit tests

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import unittest
from app.models import Song


class ScrapingTests(unittest.TestCase):
    def test_cifraclub(self):
        html = Song.get_lyrics_or_chords('https://www.cifraclub.com.br/jethro-tull/locomotive-breath/')
        self.assertIsNot(html, '')

    def test_letras(self):
        html = Song.get_lyrics_or_chords('https://m.letras.mus.br/jethro-tull/19894/')
        self.assertIsNot(html, '')

    def test_echords(self):
        html = Song.get_lyrics_or_chords('http://www.e-chords.com/chords/the-beatles/day-tripper')
        self.assertIsNot(html, '')

    def test_lyricsfreak(self):
        html = Song.get_lyrics_or_chords('http://www.lyricsfreak.com/j/jethro+tull/locomotive+breath_20070951.html')
        self.assertIsNot(html, '')

if __name__ == '__main__':
    unittest.main()
