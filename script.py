#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
from slugify import slugify
import requests, sys, os

#lidice - 4575
#otto - 5523

#To-do: adicionar teste para checar se senador não fez nenhum pronunciamento

global BASE_URL, PARSER
PARSER = 'html5lib'
BASE_URL = 'https://www25.senado.leg.br/web/atividade/pronunciamentos/-/p/parlamentar/'

def choose_deputy(DEP):
    '''
    Esta função seleciona o deputado de acordo com seu código e acessa sua página ed pronunciametos
    '''    
    print('choose_deputy')
    dep_page = requests.get(BASE_URL+DEP).text
    dep_soup = BS(dep_page, PARSER)
    dep_name = dep_soup.find('h1', class_='titulo-pagina').text.split('em')[0]
    range_years = dep_soup.select('.portlet-borderless-container .form.row li')
    
    min_y = range_years[-1].text
    max_y = range_years[0].text

    iterate_deputy_years(min_y, max_y)

def iterate_deputy_years(min_y, max_y):
    print('iterate_deputy_years')
    for year in range(int(min_y), int(max_y)+1):
        year_url = BASE_URL+DEP+'/'+str(year)
        year_page = requests.get(year_url)
        r_page = BS(year_page.text, PARSER).select('.pagination ul li')
        range_page = []
        for li in r_page:
            try:
                range_page.append(int(li.text))
            except:
                pass

        min_page = range_page[0]
        max_page = range_page[-1]
        for page in range(int(min_page), int(max_page)+1):             
            get_page(page, year_url)

def get_page(page, year_url):
    print('get_page')
    page_html =  requests.get(year_url+'/'+str(page)).text
    page_speach_trs = BS(page_html, PARSER).select('.portlet-body table a')
    for i in page_speach_trs:
        speach_page_raw = requests.get(i['href']).text
        speach_link = BS(speach_page_raw, PARSER).select('.portlet-borderless-container a')[-1]
        speach_page = requests.get(speach_link['href'])
        speach = BS(speach_page.text, PARSER)
        name = speach.select('.well dd:nth-of-type(1) span:nth-of-type(1)')[0].text
        date = speach.select('.well dd:nth-of-type(2)')[0].text
        integral_text = speach.select('.texto-integral')[0].text
        save_page(integral_text, date, name)

def save_page(integral_text, date, name):
    print('save_page')
    if not os.path.exists('speachs/'+slugify(name)):
        os.makedirs('speachs/'+slugify(name))
    print('Saving speach from {}'.format(date))
    f = open('speachs/'+slugify(name)+'/'+slugify(date)+'.txt', "w")
    f.write(integral_text.replace('             ', ''))
    f.close()

    

if __name__ == '__main__':
    global DEP 
    DEP = input('Qual o código do deputado?\n')
    choose_deputy(DEP)