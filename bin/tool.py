import urllib.request


class handle:
  def get_html_doc(url):
    response = urllib.request.urlopen(url)
    html_doc = response.read().decode('utf-8')
    return html_doc
