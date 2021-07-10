import logging
import logging.config
from utils import NlpModel, Crawler
import os 
import datetime
from stat_result import Stater

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('logs/crawler.log')
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
logger.addHandler(c_handler)
logger.addHandler(f_handler)


def load_urls(path):
    with open(path, 'r') as f:
        ans = [line[:-1] for line in f]
        return ans          

count = 0
if __name__ == "__main__":
    urls = load_urls('inputs/test.in')
    # model = NlpModel(ckpt='./pretrained_phonlp')
    start_time = datetime.datetime.now()
    for index,url in enumerate(urls):
        try:
            crawler = Crawler(url=url)
            print(f"{index}/{len(urls)}. url: {url}")
            result = crawler.get_result()
            print(f"resutl: {result}")
            source = crawler.get_source()
            _id = crawler.get_id()
            prepath = 'outputs/' + source 
            if not os.path.exists(prepath):
                os.mkdir(prepath)
                print(f"Directory {prepath} was crseated")
            path = prepath + '/' + _id + '.json'
            Crawler.write2json(path,result_dict=result)
            count += 1
        except Exception as e:
            print(f"Can not crawl this {url} - error: {e}")

    end_time = datetime.datetime.now()
    enter_delta = datetime.timedelta(hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second).total_seconds()
    exit_delta = datetime.timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second).total_seconds()
    print(f"Count: {count}/{len(urls)} - Time to crawl 1news/sec: ", (exit_delta - enter_delta)/count)
