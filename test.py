from urllib.parse import urlparse

URL = 'https://www.yellowpages.vnn.vn/cls/489265/ac-quy-xe-nang.html?page=2'

d = urlparse(URL);
print(d.scheme)
