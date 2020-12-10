import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_phone_by_uid(uid, PHPSESSION):
    url = 'https://quetsodienthoai.com/lib/scan123a@/api@123/convert6868.php'
    #url = url_template.format(uid)
    params = {'uid': uid}
    #cookies = dict(PHPSESSID=PHPSESSION)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    cookies = {'PHPSESSID': PHPSESSION}
    try:
        response = requests.get(url, cookies=cookies, headers=headers, params=params)
        #json_obj = response.json()
        #print(response.content)
        return response.json()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
        return {}

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
                container = soup.find('div', class_ = 'search-container-center')

                if container != None:
                    listing = container.find_all('div', class_='search-listing')
                    i = 0
                    for company in listing:
                        img_link = company.find('a', class_ = 'search-business-img yp-click')
                        detail_link = root_url + img_link.get('href')
                        # print(detail_link)
                        #crawl company detail
                        # delay random seconds
                        t = random.randint(15, 30)
                        print('     page detail...delay for %s seconds...' % t)
                        time.sleep(t)

                        try:
                            company_detail = requests.get(detail_link, timeout=timeouts)
                            company_detail.raise_for_status()
                            if company_detail.status_code == 200:
                                # data processcing
                                name = ''
                                address = ''
                                mobile = ''
                                email = ''
                                website = ''
                                social = ''
                                landlines = []

                                company_detail_soup = BeautifulSoup(company_detail.content, 'lxml')
                                #print(company_detail_soup)
                                container = company_detail_soup.find('div', class_ = 'container')
                                main_content = company_detail_soup.find('div', class_='main-content')
                                biz_items = company_detail_soup.find('div', class_='border-top').find_all('div', class_='biz-item')
                                # name
                                name = main_content.find('h1').text
                                print("     ",name)

                                #address
                                for item in biz_items:
                                    #print('##############')
                                    #print(item)
                                    label = item.find('div', class_='icon-la b')
                                    if label is not None:
                                        #address
                                        if label.text == 'Address':
                                            address = item.a.text
                                        #mobile
                                        if label.text == 'Mobile':
                                            mobile = item.a.get('href').split(':')[1]
                                        #email
                                        if label.text == 'Email':
                                            email = item.a.text
                                        #website
                                        if label.text == 'Website':
                                            website = item.a.get('href')
                                        #social
                                        if label.text == 'Social':
                                            social = item.a.get('href')
                                        #landlines
                                        if label.text == 'Landline':
                                            tel_links = item.find_all('a', class_='biz-link')
                                            for link in tel_links:
                                                # print(link.get('href'))
                                                href = link.get('href')
                                                if ":" in href:
                                                    landlines.append(href.split(':')[1])

                                data.append({
                                    "name": name,
                                    "address": address,
                                    "mobile": mobile,
                                    "landlines": " ".join(landlines),
                                    "email": email,
                                    "website": website,
                                    "social": social,
                                })

                        except requests.exceptions.RequestException as err:
                            print ("OOps: Something Else",err)
                            t = random.randint(60, 150)
                            time.sleep(t)
                        except requests.exceptions.HTTPError as errh:
                            print ("Http Error:",errh)
                            t = random.randint(60, 150)
                            time.sleep(t)
                        except requests.exceptions.ConnectionError as errc:
                            print ("Error Connecting:",errc)
                            t = random.randint(60, 150)
                            time.sleep(t)
                        except requests.exceptions.Timeout as errt:
                            print ("Timeout Error:",errt)
                            t = random.randint(60, 150)
                            time.sleep(t)

                # links processcing
                pagination = soup.find('ul', class_ = 'pagination')
                if pagination is not None:
                    pagination_links = pagination.find_all('a')
                    for link in pagination_links:
                        href = link.get('href')
                        if '/category/' in href:
                            next_link = root_url + href
                            if 'javascript' not in href and next_link not in completed and next_link != URL:
                                q.put(next_link)
            else:
                print("Error occur with code: %s" % soup.status_code, URL)

            completed.append(URL)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
            t = random.randint(60, 150)
            time.sleep(t)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
            t = random.randint(60, 150)
            time.sleep(t)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            t = random.randint(60, 150)
            time.sleep(t)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            t = random.randint(60, 150)
            time.sleep(t)

    # finally return data
    return data
