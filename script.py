#!/usr/bin/env python
from bs4 import BeautifulSoup as BS
import requests


#lidice - 4575
#otto - 5523

BASE_URL = 'https://www25.senado.leg.br/web/atividade/pronunciamentos/-/p/parlamentar/'

def choose_deputy():
    #dep = input('Qual o código do deputado?\n')
    
    dep_page = requests.get(BASE_URL+'4575').text
    dep_soup = BS(dep_page, 'html5lib')
    dep_name = dep_soup.find('h1', class_='titulo-pagina').text.split('em')[0]
    range_years = dep_soup.select('.portlet-borderless-container .form.row li')

    print(dep_name)
    less = 0
    more = 0
    for year in range_years:

        print(year.text)
    

if __name__ == '__main__':
    choose_deputy()