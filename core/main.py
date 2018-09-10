import re
from openpyxl import Workbook
from bin.tool import handle

if __name__ == "__main__":
  url = "https://www.imdb.com/chart/top"
  imdb_doc = handle.get_html_doc(url)
  pat = r'<td class="titleColumn">\s*(.*)..*\s*.*\s*title=".*" >(.*)</a>.*\s*<span class="secondaryInfo">\((.*)\)</span>'
  html_doc = re.findall(pat, imdb_doc)
  wb = Workbook()
  sheet = wb.active
  sheet.column_dimensions['B'].width = 60
  for i in range(len(html_doc)):
    for j in range(len(html_doc[i])):
      sheet.cell(row=i + 1, column=j + 1).value = html_doc[i][j]
  wb.save('imdb.xlsx')