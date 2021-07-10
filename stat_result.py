from typing_extensions import ParamSpecArgs


class Stater:
    def __init__(self) -> None:
        pass 

    @staticmethod
    def stat(results):
        stater = dict()
        stater['title'] = 0
        stater['source'] = 0 
        stater['date'] = 0
        stater['url'] = 0
        stater['summary'] = 0
        stater['content'] = 0
        stater['paragraphs'] = 0
        stater['authors'] = 0
        stater['keywords'] = 0

        for result in results:
            if result['title']:
                stater['title'] += 1
            if result['source']:
                stater['source'] += 1
            if result['date']:
                stater['date'] += 1
            if result['url']:
                stater['url'] += 1
            if result['summary']:
                stater['summary'] += 1
            if result['content']:
                stater['content'] += 1
            if result['authors']:
                stater['authors'] += 1
            if result['keywords']:
                stater['keywords'] += 1
    
        return stater    
