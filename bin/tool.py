from urllib import request


class handle:
  @staticmethod
  def get_html_doc(url):
    response = request.urlopen(url)
    html_doc = response.read().decode('utf-8')
    return html_doc
