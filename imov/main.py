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
  pro = ['122.152.196.126', '114.215.174.227', '119.185.30.75']
  head = {
    'user-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64 x64)AppleWebkit/537.36(KHTML,like Gecko) chrome/58.0.3029.110 Safari/537.36'
  }
  resopnse = requests.get(url, proxies={'http': random.choice(pro)}, headers=head)
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
  html_str = """<table><thead>
                  <tr>
                  <th align="center">排名</th>
                  <th align="center">影片名(中)</th>
                  <th align="center">影片名(英)</th>
                  <th align="center">导演</th>
                  <th align="center">年份</th>
                  </tr>
                </thead><tbody>"""
  for i in range(len(res)):
    html_str += '<tr>'
    for j in range(len(res[i])):
      html_str += '<td align="center">%s</td>' % res[i][j]
    html_str += '</tr>'
  html_str += '</tbody></table>'
  with open('imdb_top_250.html', 'wb+') as f:
    f.write(html_str)


def save():
  url = "https://www.imdb.com/chart/top"
  imdb_doc = get_html_doc(url)
  pat = r'<td class="titleColumn">\s*(.*)..*\s*.*\s*title=".*" >(.*)</a>.*\s*<span class="secondaryInfo">\((.*)\)</span>'
  res = find_all_by_pat(pat, imdb_doc)
  for i in range(len(res)):
    info = get_douban_info(res[i][1])
    chinese_name = info['chineseName']
    director_name = info['directorName']
    res[i] = list(res[i])
    res[i].insert(1, chinese_name)
    res[i].insert(3, director_name)
    print(res[i])
    sleep(random.random() * 1.2)
  wb = Workbook()
  sheet = wb.active
  save_html(res)
  for i in range(len(res)):
    for j in range(len(res[i])):
      sheet.cell(row=i + 1, column=j + 1).value = res[i][j]
  wb.save('imdb_top_250.xlsx')
