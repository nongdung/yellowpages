import sys
import queue
import time
import crawler
import random
import csv

q = queue.Queue()
completed = []

if len(sys.argv) > 3 and sys.argv[1] != None:
    uid_file = './raw_uid/' + sys.argv[1]
    PHPSESSION = sys.argv[3]
    result_filename = sys.argv[2] is not None and sys.argv[2] or 'data.csv'
    full_result_file_name = './data/' + result_filename

    with open(full_result_file_name, mode='w+',newline='',encoding='utf-8') as csv_file:
        fieldnames = ['uid', 'phone']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # read uid file
        read_uid_file = open(uid_file, 'r')
        count = 0
        while True:
            count += 1
            # Get next line from file
            uid = read_uid_file.readline()
            if uid != '':
                result = crawler.get_phone_by_uid(uid, PHPSESSION)
                phone = ''
                if result['code'] == 200:
                    phone = result['phone']
                    #print(result['phone'])
                data = {'uid': uid.strip(), 'phone': phone}
                print(data)
                writer.writerow(data)
                #print(result)

            # if line is empty
            # end of file is reached
            if not uid:
                break
            #print("Line{}: {}".format(count, uid.strip()))

        read_uid_file.close()

    # insert URL to the queue
    '''
    filename = sys.argv[2] is not None and sys.argv[2] or 'data.csv'
    full_file_name = './data/' + filename
    q.put(URL)
    total = 0
    with open(full_file_name, mode='w+',newline='',encoding='utf-8') as csv_file:
        fieldnames = ['#', 'name', 'address', 'landlines', 'mobile', 'email', 'website', 'social']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while not q.empty():
            processcing_url = q.get()
            if processcing_url not in completed:
                data = crawler.crawl(processcing_url, q, completed)
                # total = total + len(data)
                for company in data:
                    total = total + 1
                    company['#'] = total
                    writer.writerow(company)

                print('...harvested %s item(s)' % len(data))
                if not q.empty():
                    t = random.randint(30, 65)
                    print('...delay for %s seconds...' % t)
                    time.sleep(t)

    print('Finished')
    print('Total items: %s' % total)
    '''
    exit()
else:
    print("Error! Command need arguments, eg: python main.py uid.txt result.csv PHPSESSION")
