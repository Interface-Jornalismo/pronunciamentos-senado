#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
from slugify import slugify
import requests, sys, os, re

#To-do: adicionar teste para checar se senador não fez nenhum pronunciamento

global BASE_URL, PARSER
PARSER = 'html5lib'
BASE_URL = 'https://www25.senado.leg.br/web/atividade/pronunciamentos/-/p/parlamentar/'

def choose_deputy(DEP, ano, page):
    '''
    Seleciona o deputado de acordo com seu código e acessa sua página de pronunciametos.
    '''    
    dep_page = requests.get(BASE_URL+DEP).text
    dep_soup = BS(dep_page, PARSER)
    dep_name = dep_soup.find('h1', class_='titulo-pagina').text.split('em')[0]
    range_years = dep_soup.select('.portlet-borderless-container .form.row li')
    if ano is not None:
        min_y = ano
    else:
        min_y = range_years[-1].text

    max_y = range_years[0].text

    iterate_deputy_years(min_y, max_y, page)

def iterate_deputy_years(min_y, max_y, page):
    '''
    Navega as páginas com discursos por ano.
    '''    
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
        if page is not None:
            min_page = page
        else:
            min_page = range_page[0]
            
        max_page = range_page[-1]
        for page in range(int(min_page), int(max_page)+1):             
            get_page(page, year_url)

def get_page(page, year_url):
    '''
    Recupera data do discurso e link da página onde ele está disponível.
    '''    
    page_html =  requests.get(year_url+'/'+str(page)).text
    page_speach_trs = BS(page_html, PARSER).select('.portlet-body table a')
    for i in page_speach_trs:
        speach_page_raw = requests.get(i['href']).text
        speach_link = BS(speach_page_raw, PARSER).select('.portlet-borderless-container a')[-1]
        test_speach_exists = BS(speach_page_raw, PARSER).find_all(text='Texto integral não disponível')
        if len(test_speach_exists) == 0:
            speach_page = requests.get(speach_link['href'])
            speach = BS(speach_page.text, PARSER)
            name = speach.select('.portlet-body dd:nth-of-type(1) span:nth-of-type(1)')[0].text
            date = speach.select('.portlet-body dd:nth-of-type(2)')[0].text
            tipo = speach.select('.portlet-body dd:nth-of-type(4)')[0].text
            integral_text = speach.select('.texto-integral')[0].text
            print(date)
            save_page(integral_text, date, name, tipo)
        else:
            print('Texto integral não disponível')
            continue


def save_page(integral_text, date, name, tipo):
    '''
    Salva o discuso em formato txt para leitura de máquina.
    '''    
    if not os.path.exists('speachs/'+slugify(name)+'/'+slugify(date)+'-'+slugify(tipo)+'.txt'):
        if not os.path.exists('speachs/'+slugify(name)):
            os.makedirs('speachs/'+slugify(name))
        print('Saving speach from {}'.format(date))
        f = open('speachs/'+slugify(name)+'/'+slugify(date)+'-'+slugify(tipo)+'.txt', "w")
        f.write(integral_text.replace('             ', ''))
        f.close()
        

if __name__ == '__main__':
    global DEP 
    DEP = input('Qual o código do deputado?\n')
    ano = 2014
    page = 1
    choose_deputy(DEP, ano, page)