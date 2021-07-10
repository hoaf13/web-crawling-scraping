import phonlp
from torch._C import get_num_interop_threads
from transformers.models.auto.tokenization_auto import NO_CONFIG_TOKENIZER
import logging
import re 
import json
import phonlp
from newspaper import Article
from newsplease import NewsPlease
from bs4 import BeautifulSoup
import requests

class NlpModel:
    def __init__(self, ckpt) -> None:
        self.model = phonlp.load(save_dir=ckpt)
    
    def get_per(self, text): 
        outs = self.model.annotate(text=text)
        words = outs[0]
        bio_tag = outs[2]
        print(bio_tag)
        ans = []
        name = ''
        for index,word in enumerate(words):
            if 'PER' in bio_tag[index] or index == len(words)-1:
                name = word[index] + ' '
            else:
                if name is not '':
                    ans.append(name.strip())
        return ans

    def get_org(self, text):
        pass 

    def get_loc(self, text):
        pass

    def __str__(self) -> str:
        return "PhoNLP VinAI Model"
# model = NlpModel('./pretrained_phonlp/')

class Crawler:
    def __init__(self, url) -> None:
        self.info = Article(url,language='vi') 
        self.info.download()
        self.info.parse()       
        # ['config', 'extractor', 'source_url', 'url', 'title', 'top_img', 'top_image', 'meta_img', 'imgs', 'images', 'movies', 'text', 'keywords', 'meta_keywords', 'tags', 'authors', 'publish_date', 'summary', 'html', 'article_html', 'is_parsed', 'download_state', 'download_exception_msg', 'meta_description', 'meta_lang', 'meta_favicon', 'meta_data', 'canonical_link', 'top_node', 'clean_top_node', 'doc', 'clean_doc', 'additional_data', 'link_hash', '__module__', '__doc__', '__init__', 'build', 'download', 'parse', 'fetch_images', 'has_top_image', 'is_valid_url', 'is_valid_body', 'is_media_news', 'nlp', 'get_parse_candidate', 'build_resource_path', 'get_resource_path', 'release_resources', 'set_reddit_top_img', 'set_title', 'set_text', 'set_html', 'set_article_html', 'set_meta_img', 'set_top_img', 'set_top_img_no_check', 'set_imgs', 'set_keywords', 'set_authors', 'set_summary', 'set_meta_language', 'set_meta_keywords', 'set_meta_favicon', 'set_meta_description', 'set_meta_data', 'set_canonical_link', 'set_tags', 'set_movies', 'throw_if_not_downloaded_verbose', 'throw_if_not_parsed_verbose', '__dict__', '__weakref__', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']

    def get_id(self):
        url = self.get_url()
        _id = re.findall('[0-9]+', url)[-1]
        return _id

    def get_title(self):
        title = self.info.title
        return title
    
    def get_source(self):
        source = self.info.source_url
        source = source.replace('https://','')
        source = source.replace('http://','') 
        return source
    
    def get_url(self):
        return self.info.url

    def get_date_publish(self):
        date = self.info.publish_date
        try:
            date_match = date.strftime("%d/%m/%Y")
            return date_match
        except:
            return date

    def get_summary(self):
        summary = self.info.meta_description
        summary = re.sub("[\(\[].*?[\)\]]", "", summary)
        return summary

    def get_content(self):
        content = self.info.text
        if not content:
            url = self.info.url 
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features='lxml')
            print("soup", soup.prettify())
            p_texts = [p.get_text() for p in p_tags]
            ans = '\n'.join(p_texts)
            return ans
        return content

    def get_paragraphs(self):
        ans = []
        try:
            paragraphs = self.get_content().split('\n')
            splited_paragraphs = list(dict.fromkeys(paragraphs))
            splited_paragraphs.remove('')
            for para in splited_paragraphs:
                para = re.sub("[\(\[].*?[\)\]]", "", para)
                ans.append(para)
            if '(' in ans[0] or '-' in ans[0]:
                ans.pop(0)
            if len(ans[-1].split(' ')) < 5:
                ans.pop(-1)
            if len(ans[-1].split(' ')) < 5:
                ans.pop(-1)
            return ans
        except Exception:
            return ans

    def get_author(self):
        try:
            authors = self.info.authors
            if not authors:
                authors = []
                last_sentence = self.get_paragraphs()[-1]
                if len(last_sentence.split(' ')) < 6:
                    authors.append(last_sentence)
            if not authors:
                content = self.info.text.split('\n')[-1]
                return content
            return authors[-1]
        except:
            return []

    def get_keywords(self):
        keywords = self.info.keywords
        if not keywords:
            keywords = self.info.meta_keywords
        return keywords
    
    def get_tags(self):
        return list(self.info.tags)

    def get_result(self):
        title = self.get_title()
        source = self.get_source()
        date_publish = self.get_date_publish()
        url = self.get_url()
        summary = self.get_summary()
        content = self.get_content()
        paragraphs = self.get_paragraphs()
        author = self.get_author()   
        keywords = self.get_keywords()
        tags = self.get_tags()
        
        ans = dict()
        ans['_id'] = self.get_id()
        ans['title'] = title
        ans['source'] = source
        ans['date'] = date_publish
        ans['url'] = url
        ans['summary'] =  summary
        ans['content'] = content
        ans['paragraphs'] = paragraphs
        ans['authors'] = author
        ans['keywords'] = keywords
        ans['tags'] = tags
        return ans

    @staticmethod
    def write2json(filename, result_dict):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, ensure_ascii=False, indent=4) 
        print(f"write {filename} successfully!")


