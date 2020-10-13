# anki_map_country_import
Repository for web scraping Wikipedia to extract country locator maps and country names and upload them to a deck in Anki.

## File Description
### download_image.py
download_image.py contains the functions which are being used to open a wikipedia country page, select the html <img> element on that page, that contains the flag of that country, download and save the image file to a local computer.

### main.py
main.py uses those functions in download_image.py to go through a list of countries on wikipedia which can be found [here](https://de.wikipedia.org/wiki/Liste_der_Staaten_der_Erde). For each country the country flag image is being downloaded. Then, main.py creates a for an Anki import usable textfile with the following structure:
`<html><img src="imagename.png"></html>`; countryname
  
Each line in the file represents one country. This format can be used for an import to akn.

## Step-by-Step instructions on how to get the deck with country flags into Anki
1. Fork this Repository
1. Open download_images.py and fill in the filepath on your computer where Anki saves its images (*see section Remarks)
1. Run main.py in your command line
1. In your current working directory this should have created a textfile with the name 'import.txt'
1. Open your Anki application on your computer
1. Create a new Anki deck for your cards
1. Go into the new deck by selecting it
1. Click on the tab file and choose import (alternatively ctrl+shift+I)
1. Choose import.txt as the file that you would like to import
1. Select the checkbox that says 'Allow HTML in Fields'
1. Click on 'Import' button

## Remarks
- Right now, this only works with with German country names, as the web scraping has been programmed to work with the link https://de.wikipedia.org/wiki/Liste_der_Staaten_der_Erde, which contains a list of all country names in German. Since the site with English country names has a different build-up, the scraping of this site does not work yet.
- (*) Regarding point 2 of the Step-by-Step-instructions: In the file download_images.py, there is the function download_and_save_image(). To correctly save the images on your local computer so that Anki can use them, you need to substitute the part of the file path in line 42 that comes before the expression that is marked by a ~: 
`file = open(f'C:\\~\\collection.media\\{img_name}.png', 'wb')`
Anki saves its images in the collection.media folder which you can find in the %APPDATA% folder. For more information on this, I refer you to the [Anki documentation](https://docs.ankiweb.net/#/files).

