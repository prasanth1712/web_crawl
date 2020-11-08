# web_crawl
# Project - Web Crawl and Scrapping 


# Overall architecture. 
  The program consists of main core function to execute the functionality "web_crawl"
   # Modular functions are used for the re-usability
  
  This is recursive program which scrapes a particular web page and crawls to its related links 
  This crawl is controlled by level parameter 
  
  The scraped text is cleaned and processed   
    It uses regular expressions to clean the text
    Natural Language Processing is done to tokenize and remove the stop words in English Language
  
  The scraped text is used to find out the frequent word and pairs.
  The top n words / pairs is controlled by top_n parameter 
  
  The default output will be printed to console .
  If you wish the output to be given to another program it should be set to True so that a list will be returned
  
  # Line by Lines explaination is in the form of comments in the code 
  
# Integratation with an automated CI/CD pipeline.
  This module can be run on any platform having python on it.
  It installs the dependencies required for it.
  The modular functions help in re-usability of the code.
