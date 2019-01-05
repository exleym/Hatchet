import requests
from bs4 import BeautifulSoup


WIKI_URL = "https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_stadiums"
CREATE_STADIUM_URL = "http://localhost:5000/api/v1/stadiums"
COLUMNS = ['image', 'name', 'city', 'state', 'team', 'conference', 'capacity', 'record',
           'built', 'expanded', 'surface']


class Image(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __repr__(self):
        return f"<Image(title='{self.title}')>"

class Stadium(object):
    def __init__(self, name, state, city, team, capacity, built,
                 expanded, surface, image, wiki_link):
        self.name = name
        self.city = city
        self.state = state
        self.team = team
        self.capacity = capacity
        self.built = built
        self.expanded = expanded
        self.surface = surface
        self.image = image
        self.wiki_link = wiki_link

    def dump(self):
        return {
            "name": self.name,
            "nickname": None,
            "built": self.built,
            "capacity": self.capacity,
            "surface": self.surface
        }

    def __repr__(self):
        return f"<Stadium(name={self.name}')>"

def parse_image(element):
    img = element.find('img')
    if not img:
        return {'image': None}
    return {'image': Image(title=img.get('alt'), url=img.get('src'))}


def parse_normal_link(element):
    link = element.find('a')
    if not link:
        if element.text:
            return (None, element.text)
        return (None, None)
    return (link.get('href'), link.text)


def parse_text(element, numeric=False):
    sortkeys = element.find_all("span", {"class": "sortkey"})
    references = element.find_all("sup", {"class": "reference"})
    smalls = element.find_all('small')
    for banned in [sortkeys, references, smalls]:
        if banned:
            for ref in banned:
                ref.extract()
    text = element.text.strip('\n')
    if numeric:
        if text:
            if text == 'N/A':
                return None
            text = text.split('-')[0].split(' ')[0].split('–')[0]
            return int(text.replace(',', ''))
        return None
    return text


def parse_element(element, index):
    if index == 0: return parse_image(element)
    elif index == 1:
        parsed = parse_normal_link(element)
        return {'wiki_link': parsed[0], 'name': parsed[1]}
    elif index == 2:
        return {'city': parse_normal_link(element)[1]}
    elif index == 3:
        return {'state': parse_normal_link(element)[1]}
    elif index == 4:
        return {'team': parse_normal_link(element)[1]}
    elif index == 6:
        return {'capacity': parse_text(element, numeric=True)}
    elif index == 8:
        return {'built': parse_text(element, numeric=True)}
    elif index == 9:
        return {'expanded': parse_text(element, numeric=True)}
    elif index == 10:
        return {'surface': parse_text(element, numeric=False)}
    return dict()

def main():
    html = requests.get(WIKI_URL).content
    soup = BeautifulSoup(html, features='html.parser')
    stadium_table = soup.find_all('table', {'class': 'wikitable sortable'})[0]
    table_body = stadium_table.find('tbody')
    rows = table_body.find_all('tr')
    data = []


    for row in rows[1:]:
        elements = row.find_all('td')
        counter = 0
        fields = dict()

        for e in elements:
            fields.update(parse_element(element=e, index=counter))
            counter += 1

        data.append(Stadium(**fields))

    for d in data:
        resp = requests.post(CREATE_STADIUM_URL, json=d.dump())
        if resp.status_code == 201:
            print(resp)
        else:
            print(resp.json())


if __name__ == '__main__':
    main()