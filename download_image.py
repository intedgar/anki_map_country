import requests
#import beautiful soup 4
import bs4
import re
import shutil

def parse_page(url):
    response = requests.get(url)
    #print(response)
    text = response.text
    soup = bs4.BeautifulSoup(text, "lxml")
    return soup


def get_map_page_anchor(soup, country, continent):

    anchor = soup.find(title=re.compile(f'^File:{country} in its region.svg$'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'{country} in its region.svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'{country} in its region [(]undisputed[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'{country} in {continent} [(]-rivers -mini map[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'{country} in {continent} [(]-mini map -rivers[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'{country} in {continent} [(]undisputed only[)] [(]-mini map -rivers[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'{country} in {continent} [(]undisputed[)] [(]-mini map -rivers[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'{country} in {continent} [(]only undisputed[)] [(]-mini map -rivers[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'{country} in its region [(]de-facto[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'{country} in {continent} [(]de-facto[)] [(]-mini map -rivers[)].svg'))
    #in case the country is not mentioned or spelled differently
    if anchor == None:
        anchor = soup.find(title=re.compile(f'in its region.svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'in its region [(]undisputed[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'in {continent} [(]-rivers -mini map[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'in {continent} [(]-mini map -rivers[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'in {continent} [(]undisputed only[)] [(]-mini map -rivers[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'in {continent} [(]undisputed[)] [(]-mini map -rivers[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'in {continent} [(]only undisputed[)] [(]-mini map -rivers[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'in its region [(]de-facto[)].svg'))
    if anchor == None:
        anchor = soup.find(title=re.compile(f'in {continent} [(]de-facto[)] [(]-mini map -rivers[)].svg'))

    return anchor


def get_map_image(soup, continent):
    image = soup.find(alt=re.compile(f'in its region.svg'))
    if image == None:
        image = soup.find(alt=re.compile(f'in its region [(]undisputed[)].svg'))
    if image == None:
        image = soup.find(alt=re.compile(f'in {continent} [(]-rivers -mini map[)].svg'))
    if image == None:
        image = soup.find(alt=re.compile(f'in {continent} [(]-mini map -rivers[)].svg'))
    if image == None:
        image = soup.find(alt=re.compile(f'in {continent} [(]undisputed only[)] [(]-mini map -rivers[)].svg'))
    if image == None:
        image = soup.find(alt=re.compile(f'in {continent} [(]undisputed[)] [(]-mini map -rivers[)].svg'))
    if image == None:
        image = soup.find(alt=re.compile(f'in {continent} [(]only undisputed[)] [(]-mini map -rivers[)].svg'))
    if image == None:
        image = soup.find(alt=re.compile(f'in its region [(]de-facto[)].svg'))
    if image == None:
        image = soup.find(alt=re.compile(f'in {continent} [(]de-facto[)] [(]-mini map -rivers[)].svg'))



    print('continent', continent)
    print('image', image)
    return image


def get_alternative_url(soup):
    anchor = soup.find('a', attrs={'href':re.compile('/wiki/Category:SVG_locator_maps_of')})
    print('anchor: ', anchor)
    url = 'https://commons.wikimedia.org' + anchor['href']
    print('url: ', url)
    return url

def get_map_page_url(anchor):
    map_page_url = 'https://commons.wikimedia.org' + anchor['href']
    return map_page_url


def download_and_save_image(image_url, img_name):
    response = requests.get(f"{image_url}", stream=True)

    file = open(f'C:\\Users\\Eddie\\AppData\\Roaming\\Anki2\\Benutzer 1\\collection.media\\{img_name}.png', 'wb') #fill in your own user path here

    file.write(response.content)

    file.close()



#test the functions
if __name__ == '__main__':

    html_soup = parse_page("https://commons.wikimedia.org/wiki/Category:SVG_locator_maps_of_Egypt_(location_map_scheme)?uselang=de")

    anchor = get_map_page_anchor(html_soup, 'Africa')
    print(anchor)

    url = get_map_page_url(anchor)

    html_soup = parse_page(url)
    #print(html_soup.prettify())

    anchor_tags = html_soup.find_all('a')
    print(anchor_tags)
    anchor = None
    for tag in anchor_tags:
        anchor_string = tag.string
        if anchor_string == "Original file":
            anchor = tag

    #print(anchor)
    image_url = anchor["href"]

    download_and_save_image(image_url, "map_Ägypten")
