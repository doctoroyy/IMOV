import requests

class handle:
  def get_html_doc(url):
    resopnse = requests.get(url)
    html_doc = resopnse.text
    return html_doc