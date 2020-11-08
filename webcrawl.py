# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 06:51:30 2020

@author: pr
"""

# checking for module requirements
# if not found then installing them
import sys
import subprocess
import pkg_resources

required = {'beautifulsoup4', 'nltk','lxml'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)



#Basic Imports 

# Beautiful soup to parse the html and perform operation like search and traverse
from bs4 import BeautifulSoup as bs

# Natural Language Processing library to remove the stop words and to tokenize the text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Collections to store the counts of the words
from collections import Counter

# Regular expression to find and replace text 
# Requests to make a request to url and get the response
import requests,re

"""
Function to get the top frequent words and pairs 
Inputs :
    1. HTML Body text
    2. The number of frequent words and pairs required

returns : Frequent words , Frequent Pairs

"""
def get_top_frq_words(html_body,top_n=10):        
    try:
        # Assigning input variable to a local variable to perform operations
        body = html_body
        
        # removing the links in the body text 
        body = re.sub(r"http.*"," ",body)
        
        # tokenizing words - Converting them to list of words includes spaces and special characters
        tokens = word_tokenize(body)
        
        # cleaning of the text - Removing stop words , removing the special characters , lowering them
        cleaned_tokens = [re.sub(r"\W"," ", word).lower().strip() for word in tokens if word not in stopwords.words('english')]
        
        # cleaning spaces and blank tokens
        cleaned_tokens = [token for token in cleaned_tokens if token!='']
        
        # To get the pairs taking the cleaned tokens array from 2 element onwards (i.e shifted by 1 to left)
        # Concatinating an element to make the array to similiar size of cleaned tokens
        # Now the cleaned_token and paired_token with same index forms the pairs 
        paired_tokens = cleaned_tokens[1:]
        paired_tokens.append('')
               
        # Initilizing counters
        frequent_words = Counter()
        frequent_pairs = Counter()
        
        #Most frequent words and pair of words       
        #looping through the words in cleaned tokens and paired tokens and incrementing the counters
        for a,b in zip(cleaned_tokens,paired_tokens):
            frequent_words[a]+=1
            frequent_pairs[" ".join([a,b])]+=1
        
        return frequent_words.most_common(top_n),frequent_pairs.most_common(top_n)
    except Exception as e:
        print(e)
        return [],[] 
        

"""
Function to print the top frequent words and pairs 
Inputs :
    1. url link
    2. Frequent words list
    3. Frequent pairs list
    4. Level 

returns : Frequent words , Frequent Pairs

"""
def print_frq_words(url,frq_words,frq_pairs,level):
    print('Link - ',url)
    print('At Level - ',level)
    print('Frequent Words')
    
    # looping through frequent words
    for word in frq_words:
        print('\t',word[0],' => ',word[1])
    
    print('Frequent Pairs')
    
    # looping through frequent pairs
    for pair in frq_pairs:
        print('\t',pair[0],' => ',pair[1])


"""
Function to crawl and scrape urls to find the top frequent words and pairs 
Inputs :
    1. Url
    2. n Top freqeuncy words and pairs
    3. No of levels of nesting through the urls
    4. Out True to return output dictionary or else it will print output to the console
    
returns : List of Dictionaries - url , level , Frequent words , Frequent Pairs

"""
def web_crawl(url,top_n=10,level=0,out=False):
    
    # Picking the base domain name in order to keep the control inside the domain 
    # To avoid external links
    base_domain = [i for i in url.split('/') if i.find('www.')!=-1][0]    
    
    # Variable to store the output
    output_list = []
    
    # Recursive Function to get the frequest words and pairs and nesting into other refs 
    def web_crawl_core(url,depth=0):  
        
        try:
            # Level limitation of the urls
            if depth<=level:
                
                # Requesting the given url to get the response object and checking the response status
                resp = requests.get(url)    
    
                if resp.status_code!=200:
                    print('Error while loading the page - '+url)
                else:
                    # Getting the html text using beautiful soup
                    html = bs(resp.text,'lxml')
                    
                    # Getting only the body
                    body = html.body.text
                    
                    # Calling the function to get the frequent words in the body text 
                    frq_words,frq_pairs = get_top_frq_words(body,top_n)
                    
                    # checking the output is requirement 
                    if out:
                        # Creating a dictionary and appending it to the list
                        out_dic = {}
                        out_dic['url']=url
                        out_dic['level']=depth
                        out_dic['frequent_words']=frq_words
                        out_dic['frequent_pairs']=frq_pairs
                        output_list.append(out_dic.copy())                    
                    else:
                        # Printing the frequent words and pairs                    
                        print_frq_words(url,frq_words,frq_pairs,level)
                    
                    # Finding all the html "<a>" tags and getting the links using href attribute
                    refs = html.body.find_all('a')        
                    refs = [ref.attrs['href'] for ref in refs if ref.has_attr('href')]
                    
                    # Ignoring links to the static files and ignoring the external links
                    refs = [lnk for lnk in refs if len(re.findall(r'^http.*',lnk))>0 and lnk.find(base_domain)!=-1]
                    
                    # For each valid link calling the recusrive function to get to frequent words and pairs
                    for ref in refs:
                        web_crawl_core(ref,depth+1)
        except Exception as e:
            print(e)
    
    # Entry point for recursive function                
    web_crawl_core(url,0)
    
    # Returning the output 
    if out:
        return output_list
    else:
        return 'Process Completed'
    

        
if __name__=='__main__':
    inp_url = "https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_installation.htm"
    inp_url = "https://www.314e.com/"
    op=web_crawl(inp_url,10,0,True)
    print(op)