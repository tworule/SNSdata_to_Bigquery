from mwviews.api import PageviewsClient
import json

def wiki_api(keyword, start, end, agent = 'user'):
    output_list = []
    
    p = PageviewsClient('what is it..?') #parameter로 스트링이 들어가야함. 아무거나 넣어도 가능..
    output_dict = dict(p.article_views('en.wikipedia.org', [keyword], start = start, end = end, agent = agent))
    
    for key,val in output_dict.items():
        tem_dict = {}
        tem_dict['date'] = key.strftime("%Y%m%d")
        tem_dict['view_count'] = val[keyword.replace(" ","_")]
        output_list.append(tem_dict)
    
    result = json.dumps(output_list)
    return result


# TEST
print('-------------------------------------------')
keyword = 'Subway (restaurant)'
print(keyword)
print(wiki_api(keyword = keyword, start = '20180401', end = '20180501'))
print('-------------------------------------------')
print('\n')

print('-------------------------------------------')
keyword = 'Subway'
print(keyword)
print(wiki_api(keyword = keyword, start = '20180401', end = '20180501'))
print('-------------------------------------------')
print('\n')

print('-------------------------------------------')
keyword = 'subway'
print(keyword)
print(wiki_api(keyword = keyword, start = '20180401', end = '20180501'))
print('-------------------------------------------')
print('\n')


#print(wiki_api(keyword = keyword, start = '20180401', end = '20180501', agent = 'all-agents'))


"""
agent = 'user' 'all-agents', 'spider', 'bot'
user agent : 문서를 보는 모든 사람(편집자, 익명 편집자, 독자)
spider agent : 검색 결과 개선을 목적으로 문서를 읽는 웹크롤러 등을 포함
bot agent : 기타 목적을 위해 문서를 가져올 수 있는 자동화된 모든 프로그램을 포함
--> code에서 defalut : user
"""
# https://tools.wmflabs.org/pageviews/?project=en.wikipedia.org&platform=all-access&agent=user&range=latest-20&pages=Cat|Dog
# 에서 api 결과값 일치하는지 비교 가능 (일치함)