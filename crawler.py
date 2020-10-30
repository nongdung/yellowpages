import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def crawl(URL, q, completed):
    data = []
    if URL not in completed:
        print('Harvesting %s' % URL)
        page = requests.get(URL)
        if page.status_code == 200:
            # data processcing
            soup = BeautifulSoup(page.content, 'lxml')
            results = soup.find(id = 'main_listing')

            if results != None:
                listing = results.find_all('div', class_='listing_box')
                for company in listing:
                    name = company.find('h2', class_ = 'company_name').find('a').string
                    add = company.find('p', class_='listing_diachi')
                    ct = add.em.extract()
                    address = add.string
                    city = ct.strong.string
                    tel = company.find('p', class_='listing_tel').string

                    email_el = company.find('p', class_='listing_email')
                    email = email_el is not None and email_el.string or ''

                    cat = company.find('div', class_ = 'listing_nganhnghe').find('strong').string

                    web = ''
                    web1 = company.find('div', class_='listing_website')
                    if web1 != None:
                        web2 = web1.find('a', rel = 'nofollow')
                        if web2 != None:
                            web = web2.get('href')
                    data.append({
                        "name": name,
                        "address": address,
                        "city": city,
                        "phone": tel,
                        "email": email,
                        "website": web,
                        "category": cat
                    })

            # links processcing
            u = urlparse(URL)
            url_without_query = u.scheme + '://' + u.netloc + u.path
            paging = soup.find(id = 'paging')
            paging_links = paging is not None and paging.findAll('a') or []
            #print(paging_links)
            i = 0
            for link in paging_links:
                if i < len(paging_links) - 1:
                    href = link.get('href')
                    url_need_process = ''
                    if href != None and href.find(URL) == 0:
                        #process full link
                        url_need_process = href
                    elif href != None and href.find('?page=') == 0:
                        # process internal link: href = ?page=1 | ?page=2
                        if href == '?page=1':
                            url_need_process = url_without_query
                        else:
                            url_need_process = url_without_query + href
                    else:
                        pass

                    if url_need_process != '' and url_need_process not in completed and url_need_process != URL:
                        # print('Found new URL to harvest %s' % url_need_process)
                        q.put(url_need_process)
                i = i + 1
        else:
            print("Error occur with code: %s" % soup.status_code, URL)

        completed.append(URL)

    # finally return data
    return data
