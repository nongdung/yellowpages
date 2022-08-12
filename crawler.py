import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def crawl(URL, q, completed):
    data = []
    if URL not in completed:
        print('Harvesting %s' % URL)
        conn_timeout = 10
        read_timeout = 60
        timeouts = (conn_timeout, read_timeout)
        u = urlparse(URL)
        root_url = u.scheme + '://' + u.netloc

        try:
            page = requests.get(URL, timeout=timeouts)
            page.raise_for_status()
            if page.status_code == 200:
                # data processcing
                soup = BeautifulSoup(page.content, 'lxml')
                container = soup.find('div', id='main_listing')

                if container is not None:
                    listing = container.find_all('div', class_='listing_box')
                    # i = 0
                    for company in listing:
                        detail_link = company.find('h2').a.get('href')
                        # print(detail_link)
                        # crawl company detail
                        # delay random seconds
                        t = random.randint(15, 20)
                        print('     page detail...delay for %s seconds...' % t)
                        time.sleep(t)

                        try:
                            company_detail = requests.get(
                                detail_link, timeout=timeouts)
                            company_detail.raise_for_status()
                            if company_detail.status_code == 200:
                                # data processcing
                                name = ''
                                address = ''
                                mobile = ''
                                email = ''
                                website = ''

                                company_detail_soup = BeautifulSoup(
                                    company_detail.content, 'lxml')
                                main_content = company_detail_soup.find(
                                    'div', id='listings_left')
                                detail_diachi_box = company_detail_soup.find(
                                    'div', id='detail_diachi_box'
                                    )

                                info_p = detail_diachi_box.find_all('p')
                                # name
                                name = main_content.find('h1').text
                                print("     - ", name)

                                # address
                                if len(info_p) > 0:
                                    address = info_p[0].span.text

                                # mobile
                                    mobile_span = detail_diachi_box.find(
                                        'span',
                                        class_='span_mathoai')
                                    if mobile_span is not None:
                                        mobile = mobile_span.text

                                # email
                                # website
                                ilinks = detail_diachi_box.find_all('a')
                                for anchor in ilinks:
                                    if 'mailto' in anchor.get('href'):
                                        if len(email) > 0:
                                            email += " ,{}".format(anchor.text)
                                        else:
                                            email = anchor.text
                                    if 'http' in anchor.get('href'):
                                        if len(website) > 0:
                                            website += " ,{}".format(
                                                anchor.get('href'))
                                        else:
                                            website = anchor.get('href')

                                info = {
                                    "name": name,
                                    "address": address,
                                    "mobile": mobile,
                                    "email": email,
                                    "website": website,
                                }
                                print(info)
                                data.append(info)

                        except requests.exceptions.RequestException as err:
                            print("OOps: Something Else", err)
                            t = random.randint(60, 150)
                            time.sleep(t)
                        except requests.exceptions.HTTPError as errh:
                            print("Http Error:", errh)
                            t = random.randint(60, 150)
                            time.sleep(t)
                        except requests.exceptions.ConnectionError as errc:
                            print("Error Connecting:", errc)
                            t = random.randint(60, 150)
                            time.sleep(t)
                        except requests.exceptions.Timeout as errt:
                            print("Timeout Error:", errt)
                            t = random.randint(60, 150)
                            time.sleep(t)

                # links processcing
                pagination = soup.find('div', id='paging')
                if pagination is not None:
                    pagination_links = pagination.find_all('a')
                    last_page_a = pagination_links[-2]
                    N = int(last_page_a.text)
                    print('last_page_a: ', last_page_a)
                    if N > 1:
                        for i in range(2, N):
                            href = root_url + u.path + "?page={}".format(i)
                            print(href)
                            if 'javascript' not in href and href not in completed and href != URL:
                                q.put(href)
                    """
                    for link in pagination_links:
                        href = link.get('href')
                        if '/category/' in href:
                            next_link = root_url + href
                            if 'javascript' not in href and next_link not in completed and next_link != URL:
                                q.put(next_link)
                    """
            else:
                print("Error occur with code: %s" % soup.status_code, URL)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            t = random.randint(60, 150)
            time.sleep(t)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            t = random.randint(60, 150)
            time.sleep(t)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            t = random.randint(60, 150)
            time.sleep(t)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            t = random.randint(60, 150)
            time.sleep(t)
        completed.append(URL)

    # finally return data
    return data
