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

        try:
            page = requests.get(URL, timeout=timeouts)
            page.raise_for_status()
            if page.status_code == 200:
                # data processcing
                soup = BeautifulSoup(page.content, 'lxml')
                container = soup.find('div', class_ = 'search-container-center')

                if container != None:
                    listing = container.find_all('div', class_='search-listing')
                    for company in listing:
                        img_link = company.find('a', class_ = 'search-business-img yp-click')
                        detail_link = img_link.get('href')
                        product_head = company.find('div', class_ = 'product-head')
                        product_detail = company.find('dl', class_ = 'product-detail')

                        # company name
                        ul = product_head.find('ul')
                        #print(ul)
                        lis = ul.find_all('li')
                        name = lis[1].a.text
                        detail_link = lis[1].a.get('href')

                        # address
                        dds = product_detail.find_all('dd')
                        address = dds[0].text
                        phone = dds[1].text
                        main_services = dds[2].text
                        main_routes = dds[3].text
                        city = ''
                        contact_person = ''
                        contact_position = ''
                        website = ''
                        email = ''
                        print(name)

                        #crawl company detail

                        # delay random seconds
                        t = random.randint(60, 90)
                        # print('page detail...delay for %s seconds...' % t)
                        time.sleep(t)

                        try:
                            company_detail = requests.get(detail_link, timeout=timeouts)
                            company_detail.raise_for_status()
                            if company_detail.status_code == 200:
                                # data processcing
                                company_detail_soup = BeautifulSoup(company_detail.content, 'lxml')
                                block_top_info = company_detail_soup.find('div', class_ = 'block-top-information')
                                block_introduce = company_detail_soup.find('div', class_ = 'block-introduce')
                                #city
                                #print(detail_link)
                                #print(company_detail_soup)
                                if block_top_info is not None:
                                    city = block_top_info.find('p', class_ = 'content-1-line').span.text
                                    contact_person = block_top_info.find_all('p')[0].text.split(':')[1]
                                    contact_position = block_top_info.find_all('p')[1].text.split(':')[1]
                                else:
                                    print('Error: block_top_info empty!')
                                # website
                                if block_introduce is not None:
                                    website = block_introduce.find_all('li')[2].span.text
                                else:
                                    print('Error: block_introduce empty!')
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


                        data.append({
                            "name": name,
                            "address": address,
                            "city": city,
                            "phone": phone,
                            "email": email,
                            "website": website,
                            "main_services": main_services,
                            "main_routes": main_routes,
                            "contact_person": contact_person,
                            "contact_position": contact_position
                        })

                # links processcing
                pagination = soup.find('ul', class_ = 'pagination')
                pagination_links = pagination.find_all('a')
                for link in pagination_links:
                    href = link.get('href')
                    if href != '#' and href not in completed and href != URL:
                        q.put(href)
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
