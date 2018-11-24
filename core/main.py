import re
from openpyxl import Workbook
from bin.tool import handle


def find_all_by_pat(pat, string):
  res = re.findall(pat, string)
  return res


def get_douban_html(query_name):
  url = 'https://www.douban.com/search?cat=1002&q='

  douban_search_res = handle.get_html_doc(url + query_name)
  return douban_search_res


def get_chinise_name(pat, quer_name):
  html_doc = get_douban_html(quer_name)
  res_list = find_all_by_pat(pat, html_doc)
  return res_list


if __name__ == "__main__":
  url = "https://www.imdb.com/chart/top"
  imdb_doc = handle.get_html_doc(url)
  pat = r'<td class="titleColumn">\s*(.*)..*\s*.*\s*title=".*" >(.*)</a>.*\s*<span class="secondaryInfo">\((.*)\)</span>'
  res = find_all_by_pat(pat, imdb_doc)
  wb = Workbook()
  sheet = wb.active
  sheet.column_dimensions['B'].width = 60
  sheet.column_dimensions['C'].width = 25
  pat1 = '>(.*)\s*</a>\s*<span class="ic-mark ic-movie-mark">可播放</span>'
  pat2 = r'qcat.*\s*.*>(.*)</a>'
  for i in range(len(res)):
    chinise_name = get_chinise_name(pat2, res[i][1])

    if chinise_name == []:
      chinise_name = ['', '']
    res[i] = list(res[i])
    res[i].insert(2, chinise_name[1])
    # res[i].append(chinise_name[1])
    print(res[i])

  for i in range(len(res)):
    for j in range(len(res[i])):
      sheet.cell(row=i + 1, column=j + 1).value = res[i][j]
  wb.save('imdb.xlsx')
