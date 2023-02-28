import unittest
from scrapper.TheguardianScrapper.spiders.process_helper import process
from scrapy.selector import Selector


class TestProcessingMethods(unittest.TestCase):
    """Used to test processing functions on extrem cases 
       and on updates of the config or functions
    """
    def test_proc_url(self):
        """ Tests the function proc_url() by providing a url and asserting the outputs
        """
        url = "https://www.theguardian.com/environment/2023/feb/24/weather-tracker-record-breaking-heat-australia"
        
        url_processing_result = process('./testdata/filter_config.json').proc_url(url)
        
        self.assertTrue(url_processing_result["url"] == url)
        self.assertTrue(url_processing_result["label"] == "environment")
        self.assertTrue(url_processing_result["headline"] == "weather tracker record breaking heat australia")
        self.assertTrue(url_processing_result["published_at"] == "2023-02-24T00:00:00")

    def test_proc_content(self):
        """ Tests the function proc_content() by providing a response from html page and asserting the outputs
        """
        html_content = open('./testdata/output.html',encoding="utf8").read()
        response = Selector(text=html_content)
        content_processing_result = process('./testdata/filter_config.json').proc_content(response)
        
        self.assertIsInstance(content_processing_result["author"], list)
        self.assertIsInstance(content_processing_result["content"], str)
        
if __name__ == '__main__':
    unittest.main()