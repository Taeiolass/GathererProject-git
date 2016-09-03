import urllib.request


# given a text of a search of the gatherer, it returns
# all the card ids he can found. Usually there are 100 in a single page.
def get_ids(text):
    urls = []
    while True:
        f = text.find('<a href="../Card/Details.aspx?multiverseid=')
        if f == -1:
            break
        tmp = text[f + 43:f + 49].replace('"', '')
        try:
            id = int(tmp)
            urls.append(id)
        except ValueError:
            print('Cant read the id %s' % tmp)
        text = text[f+1:]
    return urls


# given a text with a search in the gatherer, it returns the
# numbers of pages of the output
def number_pages(text):
    f = text.find('&gt;&gt;</a></div>')
    part = text[f - 1000:f].split('>')[-2]
    f = part.find('page=')
    part = part[f + 5:f + 8].replace('&', '').replace(' ', '').replace('a', '')
    try:
        num = int(part)
    except ValueError:
        num = 0
        print('Error while recognising number pages: %s' % part)
    print('%d pages detected' % num)
    return num + 1


# return all the ids found in a search given the url
# of a page of it. Note that in the url there should be
# the character backslash as placeholder for the page number.
# It is usually after the string 'page='
def shift_pages(url):
    ids = []
    print('starting finding pages')
    text = urllib.request.urlopen(url.replace('\\', '0')).read().decode('UTF-8')
    num = number_pages(text)
    for i in range(num):
        url2 = url.replace('\\', str(i))
        text = urllib.request.urlopen(url2).read().decode('UTF-8')
        print('reading page %d' % i)
        ids = ids + get_ids(text)
    return ids

