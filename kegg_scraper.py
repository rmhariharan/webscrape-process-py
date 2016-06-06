'''This module contains functions for web scraping off KEGG pages'''

import pandas as pd
import urllib.request
import re
 
def kegg_gene_scraper(myfile,baseurl,output_file):

    '''This is a script for scraping gene symbols and gene Entrez ids from KEGG pathway web pages.
        Input is a csv file (myfile) with at least two columns. One column has the KEGG Ids for pathways ("KEGG ID")
        while the other ('Pathway Name') has corresponding pathway names. Base url is url without the pathway variable part.
        (e.g. http://www.genome.jp/dbget-bin/www_bget?pathway+mmu for mouse pathways). The code does webscraping
        and retrieves gene lists (Entrez Ids, and Gene symbols) for all pathways (here, 45 pathways)
        listed in the input file. It then writes the genes lists per pathway as separate .csv files to a
        specified local disk (output_file)'''

    # Read in the data

    mydata = pd.read_csv(myfile)
    assert myfile.endswith(".csv")
    url_base = baseurl
    x = 0
    row_index = 0
    Pathway = ""
    # Get kegg ids and pathway names form the csv file
    num_of_pathways = mydata.shape[0]

    for i in range (0,num_of_pathways):
        x = mydata['KEGG ID'][row_index]
        pathway = mydata['Pathway Name'][row_index]
        x = str(x)
        if len(x) == 2:
            x = "000"+x
        elif len(x) == 3:
            x = "00"+x
        row_index = row_index+1

        
    #Access the webpage using urllib, and scrape pages using python re module. Since in ome cases gene ids may not have
    #corresponding gene symbols, we will use only those (with the if statement) where we have both'''

        full_url = url_base+x
         
        web_page = urllib.request.urlopen(full_url)

        my_webpage_data = str(web_page.read())

        pattern_list = re.findall("mmu:(\d+)",my_webpage_data)
        pattern_list_2 = re.findall("<div>(\w+\s*\w*);\s",my_webpage_data)
        if len(pattern_list) == len(pattern_list_2):
            
            mydataframe = pd.DataFrame()
            mydataframe['Entrez Id'] = pattern_list
            mydataframe['Gene symbol'] = pattern_list_2
            pathway = pathway.replace("/","")
            mydataframe.to_csv(output_file+"/"+pathway +".csv",index = False)
            print("KEGG scraping in progress")
        full_url = ""
    return "KEGG Scraping complete"

def kegg_image_scraper(url_list,output_file):
    '''Given a list of kegg pathway urls (.txt file, "url_list"),scrapes the colored pathway image from the
    webpage, writes it to aspecified folder. This function was originally written to retrieve
    PathWave diagrams (metabolic analysis)'''
    
    # Read in url list file
    
    url_file = open(url_list,"r")
    assert url_list.endswith(".txt")

    # Web Scraping for images
    local_url_file = url_file.read()
    url = re.findall("http.+",local_url_file)
    x = 1
    for i in url:
        x = str(x)
        resp = urllib.request.urlopen(i)
        respdata = resp.read()
        respdata = str(respdata)
        image_url_part2 = re.findall("/tmp/mark_pathway.+png",respdata)
        image_url_part2 = image_url_part2[0]
        image_url_part1 = "http://www.kegg.jp"
        full_image_url = image_url_part1 + image_url_part2
        part_of_outfile_name = re.findall("DEFINITION\s+(\w+\s\w+)",respdata)
        if part_of_outfile_name:
            urllib.request.urlretrieve(full_image_url,output_file+"/"+part_of_outfile_name[0]+".png")    ##Specify target path

        else:
            urllib.request.urlretrieve(full_image_url,output_file+"/"+x+".png")
            x = int(x)
            x = x+1
    return "KEGG image scraping complete"

    








