import requests
from bs4 import BeautifulSoup
import download_image
import re

#send a request to wikipedia website with a list of all states
response = requests.get('https://commons.wikimedia.org/wiki/Category:SVG_locator_maps_of_the_European_Union_(location_map_scheme)?uselang=de')
text = response.text
soup = BeautifulSoup(text, "lxml")
#print(soup.prettify())

#select the div saying "Weitere" from the table
div = soup.find('div', attrs={"aria-labelledby": re.compile("^Weitere")})
#print(div)
#select the table that is a child of the div
table = div.find('table')
#print('table: ', table)
tbody = table.find('tbody')
table_rows = tbody.find_all('tr')
#print(table_rows)

#create a new file to which will be written
file = open('import.txt', 'w', encoding = 'utf-8')

#countries left out:
left_out = []

#exclude table_rows not containing countries, so that the continents stay
continent_rows = table_rows[1:7]
#continent_rows = [continent_rows[2]]
#print(continent_rows)
for continent in continent_rows:
    #navigate to extract continent name in English
    th = continent.find('th')
    #print('th', th)
    b = th.find('b')
    continent_name_anchor = b.find('a')
    continent_name_anchor_title = continent_name_anchor["title"]

    #pattern to find the names of the conteinents in English
    pattern = re.compile('SVG locator maps of ([a-zA-Z]+[\s]*[a-zA-Z]*) [(]location')
    matches = pattern.findall(continent_name_anchor_title)
    continent_name = matches[0]

    #navigate to extract all the countries in the table row
    countries_div = continent.find('div')
    anchors = countries_div.find_all('a', href=True)
    #print(len(anchors))

    #for loop over all the country anchors in each continent
    for anchor in anchors:
        #print('anchor:', anchor)
        href = anchor["href"]
        country = anchor.string
        if country.startswith('(') and country.endswith(')'):
            left_out.append({'continent': continent_name, 'country': country})
            #print('left_out: ', left_out)
            continue
        #print('country: ', country)
        url = "https://commons.wikimedia.org/" + href

        #download and save image from the website
        html_soup = download_image.parse_page(url)

        #extract the english country name from html_soup
        country_name_pattern = re.compile('SVG locator maps of (.+) [(]location')
        #country_name_pattern = re.compile('SVG locator maps of ([a-zA-Zô-]+[\s]*[a-zA-Z\']*) [(]location')
        description = html_soup.select('#firstHeading')[0].string
        print('description', description)
        country_name = country_name_pattern.search(description).group(1)
        print('country_name', country_name)
        anchor_tag = download_image.get_map_page_anchor(html_soup, country_name, continent_name)
        #print('url', url)

        if anchor_tag == None:
            parse_url = download_image.get_alternative_url(html_soup)
            #print('parse_url: ', parse_url)
            html_soup = download_image.parse_page(parse_url)
            anchor_tag = download_image.get_map_page_anchor(html_soup, country_name, continent_name)
            #print('url', url)

        if anchor_tag == None:
            left_out.append({'continent': continent_name, 'country': country})
            print('left_out: ', left_out)
            continue

        url = download_image.get_map_page_url(anchor_tag)
        print('url', url)
        html_soup = download_image.parse_page(url)

        div = html_soup.find('div', class_="mw-filepage-resolutioninfo")
        #print('div', div)
        anchor = div.find('a')

        image_url = anchor["href"]
        print(image_url)


        #image_url = download_image.get_image_url(image)
        download_image.download_and_save_image(image_url, f'map_{country}')

        #write a new line into the file
        file.write(f'<html><img src="map_{country}.png"></html>; {country}\n')


print('Done')

#close the file
file.close()

print('left_out', left_out)
