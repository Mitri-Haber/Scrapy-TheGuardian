import json
import datetime


class process:
    """This module helps process the pages returned.
       it loads xpath config from filter_config.json,
       so that we can adjust to changes
       has two functions:
            1- proc_url : which extracts date,headline, label from the url
            2- proc_content : extracts info from the response page
    """
    def __init__(self, config_dir='filter_config.json'):
        self.config = json.load(open(config_dir))
        self.content_text_selector = self\
            .config['parse_article']['content_text_selector']
        self.author_selector = self\
            .config['parse_article']['author_selector']

    def proc_content(self, response) -> dict:
        """This function takes response and process it contents,
            returns a dict containing author names, and content text.
        """
        CONTENT_TEXT_SELECTOR = self.content_text_selector
        AUTHOR_SELECTOR = self.author_selector

        proccessed_content = {}

        for filter in AUTHOR_SELECTOR:
            possible_author = response.xpath(filter).extract()
            if possible_author:
                break
        proccessed_content['author'] =\
              possible_author if possible_author else "not available"

        for filter in CONTENT_TEXT_SELECTOR:
            possible_content = ''.join(response.xpath(filter).extract())
            if possible_content:
                break
        proccessed_content['content'] =\
            " ".join(possible_content.strip('<.*?>')\
                     .split()) if possible_content else "not available"

        return proccessed_content

    def proc_url(self, url: str) -> dict:
        """This function takes the url, and returns
           a dict containing date,url,headline,label
        """
        proccessed_url = {}
        extracted_link_list = url.split("//")[1].split("/")
        proccessed_url['url'] = url
        proccessed_url['label'] = extracted_link_list[1]
        proccessed_url['headline'] = extracted_link_list[-1].replace("-", " ")
        datestr = extracted_link_list[-4] +\
              '-' + extracted_link_list[-3] + '-' + extracted_link_list[-2]
        proccessed_url['published_at'] = datetime.datetime.strptime(datestr, "%Y-%b-%d").isoformat()
        return proccessed_url
