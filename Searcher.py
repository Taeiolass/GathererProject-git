import urllib.request

# todo: there are more options in a search that can be added
# todo: there are more option detections (such the type or the rarity) that can be added
class Search:
    """Use this class for performing a research in the gatherer."""
    '''
    Possible uses:
    url = Search().color([['AND','R']]).url
    ids = shift_pages(url)
    '''

    prefix = 'http://gatherer.wizards.com/Pages/Search/Default.aspx?page=\&action=advanced'
    modifiers = {
        'AND': '+',
        'OR': '|',
        'NOT': '+!'
    }

    # todo: maybe text could become an attribute in order not to download the page every time it is needed
    @staticmethod
    def get_search_page():
        text = urllib.request.urlopen('http://gatherer.wizards.com/Pages/Advanced.aspx').read().decode('utf-8')
        return text

    def adapt(self):
        self.url = self.url.replace(' ', '%20')

    def __init__(self):
        self.url = Search.prefix

    def name(self, opts):
        self.url += '&name='
        self.add_opts(opts)
        self.adapt()
        return self

    def color(self, opts):
        self.url += '&color='
        self.add_opts(opts)
        self.adapt()
        return self

    def type(self, opts):
        self.url += '&type='
        self.add_opts(opts)
        self.adapt()
        return self

    def subtype(self, opts):
        self.url += '&subtype='
        self.add_opts(opts)
        self.adapt()
        return self

    def set(self, opts):
        self.url += '&set='
        self.add_opts(opts)
        self.adapt()
        return self

    def set(self, opts):
        self.url += '&set='
        self.add_opts(opts)
        self.adapt()
        return self

    def rarity(self, opts):
        self.url += '&rarity='
        self.add_opts(opts)
        self.adapt()
        return self

    def add_opts(self, opts):
        for opt in opts:
            mod = opt[0]
            val = opt[1]
            self.url += Search.modifiers[mod]
            self.url += '["%s"]' % val

    # return all the possible sets he can found
    @classmethod
    def get_all_sets(cls, text):
        f = 0
        sets = []
        while True:
            f = text.find('id="ctl00_ctl00_MainContent_Content_setAddText_itemsRepeater_ctl', f+1)
            if f == -1:
                break
            part = text[f:f+1000].split('>')[1].split('<')[0]
            sets.append(part)
        return sets

