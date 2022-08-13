import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


MATCH_ALL = r'.*'


def like(string):
    """
    Return a compiled regular expression that matches the given
    string with any prefix and postfix, e.g. if string = "hello",
    the returned regex matches r".*hello.*"
    """
    string_ = string
    if not isinstance(string_, str):
        string_ = str(string_)
    regex = MATCH_ALL + re.escape(string_) + MATCH_ALL
    return re.compile(regex, flags=re.DOTALL)


def find_by_text(soup, text, tag, **kwargs):
    """
    Find the tag in soup that matches all provided kwargs, and contains the
    text.

    If no match is found, return None.
    If more than one match is found, return first match.
    """
    elements = soup.find_all(tag, **kwargs)
    matches = []
    for element in elements:
        if element.find(text=like(text)):
            matches.append(element)
    if len(matches) == 0:
        return None
    else:
        return matches[0]


def get_by_label(soup, label, first_tag):
    """
    Get value from the tag:
    <div>
        <div><p>Label</p></div>
        <div><p>Value</p></div>
    </div>
    """
    value = ''
    el = find_by_text(
        soup,
        label,
        first_tag
        )
    if el is not None:
        target_el = el.parent.find_next_sibling().p
        value = target_el.get_text()
    return value


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
                listing = soup.find_all('div', class_='boxlistings')
                for company in listing:
                    clink = company.find('h2', class_='company_name').a
                    detail_link = clink.get('href')
                    # print(detail_link)
                    # delay random seconds
                    t = 5  # random.randint(10, 15)
                    print('     page detail...delay for %s seconds...' % t)
                    time.sleep(t)

                    try:
                        company_detail = requests.get(
                            detail_link, timeout=timeouts)
                        company_detail.raise_for_status()
                        if company_detail.status_code == 200:
                            # data processcing
                            company_name = ''
                            company_address = ''
                            company_telephone = ''
                            company_email = ''
                            company_website = ''
                            business_style = ''
                            main_market = ''
                            contact_name = ''
                            contact_email = ''
                            contact_mobile = ''
                            contact_job_title = ''

                            soup = BeautifulSoup(
                                company_detail.content, 'lxml')
                            # print(company_detail_soup)
                            company_container = soup.find(
                                'h1').parent.parent
                            contact_container = find_by_text(
                                soup,
                                'Contact infomation',
                                'p').parent.parent

                            # name
                            company_name = soup.find('h1').text
                            print("     ", company_name)

                            # address
                            company_address = get_by_label(
                                company_container, 'Address:', 'p')

                            # company telephone
                            company_telephone = get_by_label(
                                company_container, 'Telephone:', 'p')

                            # company category
                            category = get_by_label(
                                company_container, 'Categories:', 'li')

                            # business_style
                            business_style = get_by_label(
                                company_container, 'Busines style:', 'li')

                            # main_market
                            main_market = get_by_label(
                                company_container, 'Main markets:', 'li')

                            # contact_name
                            contact_name = get_by_label(
                                contact_container, 'Contact name:', 'p')

                            # contact_job_title
                            contact_job_title = get_by_label(
                                contact_container, 'Job Title:', 'p')

                            # contact_mobile
                            contact_mobile = get_by_label(
                                contact_container, 'Mobiphone:', 'p')

                            # contact_email
                            contact_email = get_by_label(
                                contact_container, 'Email:', 'p')

                            # company_email
                            print("TEST")
                            c_email_container = company_container.findChild()
                            email_container = c_email_container \
                                .find_next_sibling() \
                                .find_next_sibling().find_next_sibling()
                            links = email_container.find_all('a')
                            for link in links:
                                if 'mailto' in link.get('href'):
                                    company_email = link.text
                                if 'http' in link.get('href'):
                                    company_website = link.get('href')

                            info = {
                                "company_name": company_name,
                                "company_address": company_address,
                                "company_telephone": company_telephone.replace('\xa0', ""),
                                "company_email": company_email,
                                "company_website": company_website,
                                "category": category.replace('\n', ','),
                                "business_style": business_style,
                                "main_market": main_market,
                                "contact_name": contact_name,
                                "contact_job_title": contact_job_title,
                                "contact_mobile": contact_mobile.replace(" ", ""),
                                "contact_email": contact_email.strip("\n").strip()
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
                pagination = soup.find('ul', class_='pagination')
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

    # finally return data
    return data
