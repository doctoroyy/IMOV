import random
import re
import requests
from openpyxl import Workbook
from time import sleep
from lxml import etree


def find_all_by_pat(pat, string):
  res = re.findall(pat, string)
  return res


def get_html_doc(url):
  proxies = ['122.152.196.126', '114.215.174.227', '119.185.30.75']
  head = {
    'user-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64 x64)AppleWebkit/537.36(KHTML,like Gecko) chrome/58.0.3029.110 Safari/537.36'
  }
  resopnse = requests.get(url, proxies={'http': random.choice(proxies)}, headers=head)
  resopnse.encoding = 'utf-8'
  html_doc = resopnse.text
  return html_doc


def search_fields_by_xpath(html):
  def func(__xpath):
    res = html.xpath(__xpath)
    try:
      return res[0].strip()
    except:
      return 'not found'

  return func


def get_chinese_name(html):
  chinese_name_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3/a/text()'
  return search_fields_by_xpath(html)(chinese_name_xpath)


def get_director_name(html):
  director_name_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/div/span[4]/text()'
  res = search_fields_by_xpath(html)(director_name_xpath)
  if res != 'not found':
    return res.split(' / ')[1]
  return res


def get_desc(html):
  desc_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/p/text()'
  return search_fields_by_xpath(html)(desc_xpath)


def get_douban_info(query_name):
  url = 'https://www.douban.com/search?cat=1002&q=%s' % query_name
  douban_doc = get_html_doc(url)
  html = etree.HTML(douban_doc)
  return {
    'chineseName': get_chinese_name(html),
    'directorName': get_director_name(html),
    'desc': get_desc(html)
  }


def save_html(res):
  html_str = """<table width="100%" cellpadding="2" style="border-collapse: collapse">
                  <thead>
                    <tr>
                      <th style="background-color: #f7f7f7; font-size: 18px; height: 80px" align="center">排名</th>
                      <th style="background-color: #f7f7f7;font-size: 18px" align="center">影片名(中)</th>
                      <th style="background-color: #f7f7f7;font-size: 18px" align="center">影片名(英)</th>
                      <th style="background-color: #f7f7f7;font-size: 18px" align="center">导演</th>
                      <th style="background-color: #f7f7f7;font-size: 18px" align="center">年份</th>
                    </tr>
                  </thead>
                <tbody>"""
  for i in range(len(res)):
    html_str += '<tr style="height: 60px">'
    for j in range(len(res[i])):
      html_str += '<td style="padding: 4px 8px;border-width: 1px; border-style:  solid; border-color:  #f4f4f4;" align="center">%s</td>' % res[i][j]
    html_str += '</tr>'
  html_str += '</tbody></table>'
  with open('imdb_top_250.html', 'wb+') as f:
    f.write(html_str.encode('utf-8'))


def fill_other_info(movie_tuples):
  for i in range(len(movie_tuples)):
    # ('1', 'tt0111161', 'The Shawshank Redemption', '1994')
    info = get_douban_info(movie_tuples[i][1])
    chinese_name = info['chineseName']
    director_name = info['directorName']
    movie_tuples[i] = list(movie_tuples[i])
    # 删除 IMDB 号，开始插入中文名
    movie_tuples[i].pop(1)
    movie_tuples[i].insert(1, chinese_name)
    movie_tuples[i].insert(3, director_name)
    print(movie_tuples[i])
    sleep(random.random() * 1.2)


def save_to_excel(movie_tuples):
  wb = Workbook()
  sheet = wb.active
  save_html(movie_tuples)
  movie_tuples = [('排名', '影片名（中）', '影片名（英）', '导演', '上映年份')] + movie_tuples
  for i in range(len(movie_tuples)):
    for j in range(len(movie_tuples[i])):
      sheet.cell(row=i + 1, column=j + 1).value = movie_tuples[i][j]
  wb.save('imdb_top_250.xlsx')


def save():
  url = "https://www.imdb.com/chart/top"
  imdb_doc = get_html_doc(url)
  pat = r'<td class="titleColumn">\s*(.*)..*\s*.*<a\s.*href="/title/(.*)/.*"\s*title=".*" >(.*)</a>.*\s*<span class="secondaryInfo">\((.*)\)</span>'
  movie_tuples = find_all_by_pat(pat, imdb_doc)
  fill_other_info(movie_tuples)
  save_to_excel(movie_tuples)
