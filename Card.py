import urllib.request


prefixInfo = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=%d'
prefixImg = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%d&type=card'


class Card:

    def generate(self, download_image):

        info = urllib.request.urlopen(prefixInfo % self.id).read().decode('UTF-8')

        # find Card name
        find = info.find('Card Name:')
        part = info[find:find + 1000].split('>')[2].split('<')[0].replace('\n', '').replace('\r', '')
        x = part[0]
        while x == ' ':
            part = part[1:]
            x = part[0]
        self.name = part

        # find type of the card (creature, land, sorcery...)
        find = info.find('Types:')
        part = info[find:find+1000].split('>')[2].split('<')[0].replace('\n', '').replace('\r', '')
        x = part[0]
        while x == ' ':
            part = part[1:]
            x = part[0]
        self.type = part

        # find text with the rules of the card
        text = ''
        find = 0
        while True:
            find = info.find('cardtextbox', find + 1)
            if find == -1:
                break
            part = info[find:find + 1000]
            f = part.find('>')
            part = part[f+1:].split('</div')[0]
            text += part
            text += '\n'
        self.text = work_on_text(text)

        # find mana cost of the card if it is not a land
        if 'Land' not in self.type:
            find = info.find('  Mana Cost')
            part = info[find:find + 1000].split('div')[2]
            while True:
                k = part.find('name=')
                if k == -1:
                    break
                r = part[k + 5:k + 7].replace('&', '')
                try:
                    a = int(r)
                    self.manaCost['N'] = a
                except ValueError:
                    self.manaCost[r] += 1
                part = part[k + 1:]

        # if it is a creature, find his power and toughness
        if 'Creature' in self.type:
            find = info.find('P/T:')
            part = info[find:find + 1000].split('>')[3].split('<')[0]\
                .replace('\n', '').replace('\r', '').replace(' ', '')
            try:
                v = part.split('/')
                p = int(v[0])
                t = int(v[1])
                self.PT['P'] = p
                self.PT['T'] = t
            except ValueError:
                print('Error while reading power and toughness NaN')

        # if necessary, download the image of the card
        if download_image:
            self.img = urllib.request.urlopen(prefixImg % self.id).read()

    def __init__(self, id_num, download_image=False, need_generate=True):
        self.id = id_num
        self.manaCost = generate_types()
        self.type = ''
        self.name = ''
        self.text = ''
        self.img = b'\x00'
        self.PT = {'P': -1, 'T': -1}

        # if the card data needs to be downloaded, do it
        if need_generate:
            self.generate(download_image)

    # useful to serialize with json
    def to_dict(self):
        res = {
            'id': self.id,
            'mana': self.manaCost,
            'type': self.type,
            'name': self.name,
            'text': self.text,
            'img': self.img.decode('utf-8'),
            'pt': self.PT
        }
        return res

    # useful to serialize with json
    @classmethod
    def from_dict(cls, d):
        c = Card(0, need_generate=False)
        c.id = d['id']
        c.manaCost = d['mana']
        c.type = d['type']
        c.name = d['name']
        c.text = d['text']
        c.img = d['img'].encode()
        c.PT = d['pt']
        return c

    # return the converted mana cost of a card.
    # if the cost contains X, the return will be -1
    def get_converted_mana_cost(self):
        tp = self.manaCost
        tot = 0
        for ty in tp:
            tot += tp[ty]
            if ty == 'X' and tp[ty] != 0:
                tot = -1
                break
        return tot

# use this to convert the text with rules deleting images of mana
# and raplacing it with literals such as {4}{U} and deleting formatted text
def work_on_text(text):
    f = -1
    while True:
        f = text.find('<',f+1)
        if f == -1:
            break
        mod = text[f+1:text.find('>')]

        blacklist = ['i', '/i']
        if mod in blacklist:
            sub = ''
        elif 'type=symbol' in mod:
            t = mod.find('name=')
            sub = mod[t+5:t+8].replace('&', '').replace('a', '')
            sub = '{' + sub + '}'
        else:
            raise ValueError('new card text type found. please implement it\n%s\n\nin %s' % (mod, text))
        mod = '<' + mod + '>'
        text = text.replace(mod, sub)
    return text


# generate a dictionary with every possible combination of payment of mana
# todo: this method coould be improved
def generate_types():
    base = ['U', 'R', 'G', 'W', 'B']
    ret = []
    for a in base:
        for b in base:
            if not a == b:
                ret.append(a + b)
    ret += base
    ret += ['N', 'C', 'X']
    for a in base:
        ret.append(a + 'P')
    dict = {}
    for a in ret:
        dict[a] = 0
    return dict
