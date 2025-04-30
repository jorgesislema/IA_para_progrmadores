# tests/test_extract.py
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from src.internet.extract import extract_text_from_url_newspaper, extract_content_from_links, is_valid_url
# Necesitamos importar ArticleException para simularla
from newspaper import ArticleException

# Mantener las pruebas de is_valid_url (sin cambios)
class TestURLValidation(unittest.TestCase):
    def test_valid_urls(self):
        self.assertTrue(is_valid_url("http://example.com"))
        self.assertTrue(is_valid_url("https://www.google.com/search?q=test"))
        # FTP ya no es válido según la implementación actual
        self.assertFalse(is_valid_url("ftp://ftp.debian.org"))

    def test_invalid_urls(self):
        self.assertFalse(is_valid_url("example.com")) # Falta esquema
        self.assertFalse(is_valid_url("http://")) # Falta netloc
        self.assertFalse(is_valid_url("just text"))
        self.assertFalse(is_valid_url(""))
        self.assertFalse(is_valid_url(None))
        self.assertFalse(is_valid_url(123))


class TestExtractNewspaper(unittest.TestCase):

    # Mockear la clase Article completa que se instancia dentro de la función
    @patch('src.internet.extract.Article')
    def test_extract_text_success(self, MockArticle):
        # Configurar el mock de la instancia de Article
        mock_article_instance = MagicMock()
        # Simular llamada a download y parse sin errores
        mock_article_instance.download.return_value = None
        mock_article_instance.parse.return_value = None
        # Simular que el parseo fue exitoso
        type(mock_article_instance).is_parsed = PropertyMock(return_value=True)
        # Simular el texto extraído
        mock_text = "Este es el texto principal del artículo. " * 10 # Asegurar > 100 chars
        type(mock_article_instance).text = PropertyMock(return_value=mock_text)
        # Hacer que el constructor de Article devuelva nuestra instancia mockeada
        MockArticle.return_value = mock_article_instance

        url = "http://example.com/test-article"
        extracted_text = extract_text_from_url_newspaper(url)

        # Verificaciones
        self.assertIsNotNone(extracted_text)
        self.assertEqual(extracted_text, mock_text.strip()) # newspaper suele devolver texto limpio
        # Verificar que los métodos del mock fueron llamados
        MockArticle.assert_called_once_with(url, language='es', fetch_images=False, request_timeout=15)
        mock_article_instance.download.assert_called_once()
        mock_article_instance.parse.assert_called_once()

    @patch('src.internet.extract.Article')
    def test_extract_text_too_short(self, MockArticle):
        mock_article_instance = MagicMock()
        mock_article_instance.download.return_value = None
        mock_article_instance.parse.return_value = None
        type(mock_article_instance).is_parsed = PropertyMock(return_value=True)
        # Texto demasiado corto
        type(mock_article_instance).text = PropertyMock(return_value="Texto corto.")
        # Título largo como fallback
        type(mock_article_instance).title = PropertyMock(return_value="Este es un Titulo Suficientemente Largo Para Ser Util")
        MockArticle.return_value = mock_article_instance

        extracted_text = extract_text_from_url_newspaper("http://example.com/short")
        self.assertIsNotNone(extracted_text)
        self.assertEqual(extracted_text, "Título: Este es un Titulo Suficientemente Largo Para Ser Util")

    @patch('src.internet.extract.Article')
    def test_extract_text_too_short_no_title_fallback(self, MockArticle):
        mock_article_instance = MagicMock()
        mock_article_instance.download.return_value = None
        mock_article_instance.parse.return_value = None
        type(mock_article_instance).is_parsed = PropertyMock(return_value=True)
        type(mock_article_instance).text = PropertyMock(return_value="Texto corto.")
        type(mock_article_instance).title = PropertyMock(return_value="Corto") # Título corto
        MockArticle.return_value = mock_article_instance

        extracted_text = extract_text_from_url_newspaper("http://example.com/short-no-title")
        self.assertIsNone(extracted_text) # Debe devolver None si texto y título son cortos

    @patch('src.internet.extract.Article')
    def test_extract_text_download_fails(self, MockArticle):
        mock_article_instance = MagicMock()
        # Simular error en download
        mock_article_instance.download.side_effect = ArticleException("Failed to download")
        MockArticle.return_value = mock_article_instance

        extracted_text = extract_text_from_url_newspaper("http://example.com/download-fail")
        self.assertIsNone(extracted_text)
        mock_article_instance.download.assert_called_once()
        mock_article_instance.parse.assert_not_called() # No debe llegar a parsear

    @patch('src.internet.extract.Article')
    def test_extract_text_parse_fails(self, MockArticle):
        mock_article_instance = MagicMock()
        mock_article_instance.download.return_value = None
        # Simular que parse no establece is_parsed
        mock_article_instance.parse.return_value = None
        type(mock_article_instance).is_parsed = PropertyMock(return_value=False)
        type(mock_article_instance).text = PropertyMock(return_value="") # Texto vacío
        MockArticle.return_value = mock_article_instance

        extracted_text = extract_text_from_url_newspaper("http://example.com/parse-fail")
        self.assertIsNone(extracted_text)
        mock_article_instance.download.assert_called_once()
        mock_article_instance.parse.assert_called_once()


    # Prueba para extract_content_from_links (usa la función mockeada de arriba)
    @patch('src.internet.extract.extract_text_from_url_newspaper')
    def test_extract_from_multiple_links_newspaper(self, mock_extract_single):
        links = ["http://example.com/page1", "http://example.com/page2", "http://invalid", "http://example.com/fail"]

        # Definir qué devuelve el mock para cada URL
        def side_effect_func(url, language='es', timeout=15):
            if url == "http://example.com/page1":
                return "Content from page 1. " * 10
            elif url == "http://example.com/page2":
                 return "Content from page 2 is also long enough. " * 10
            elif url == "http://example.com/fail":
                 return None # Simular fallo en esta URL
            else: # Para http://invalid y cualquier otra
                return None

        mock_extract_single.side_effect = side_effect_func

        results = extract_content_from_links(links)

        # Verificaciones
        self.assertEqual(len(results), 2) # Solo las exitosas
        self.assertIn("http://example.com/page1", results)
        self.assertTrue(results["http://example.com/page1"].startswith("Content from page 1"))
        self.assertIn("http://example.com/page2", results)
        self.assertTrue(results["http://example.com/page2"].startswith("Content from page 2"))
        # Asegurar que las fallidas no están
        self.assertNotIn("http://invalid", results)
        self.assertNotIn("http://example.com/fail", results)
        # Verificar número de llamadas al mock
        self.assertEqual(mock_extract_single.call_count, len(links))


if __name__ == '__main__':
    unittest.main()