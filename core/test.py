import re

from bin.tool import handle


def find_all_by_pat(pat, string):
  res = re.findall(pat, string)
  return res


def get_douban_html(query_name):
  url = 'https://www.douban.com/search?q='
  douban_search_res = handle.get_html_doc(url + query_name + '&cat=1002')
  return douban_search_res


if __name__ == '__main__':
  html_doc = get_douban_html('The Matrix')
  print(html_doc)
  pat = r'qcat.*\s*.*>(.*)</a>'
  res = find_all_by_pat(pat, html_doc)
  print(res[1])