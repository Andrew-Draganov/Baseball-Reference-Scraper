import re
from bs4 import BeautifulSoup
import urllib2

# Some scraped strings will have arbitrary whitespaces throughout it
# So we take off whitespace and colons, then take string up to first newLine
def reformatString(s):
    nlf = '\n'
    while s[0] == nlf or s[0] == ' ' or s[0] == ':':
        s = s[1:]
    position = s.find(nlf)
    if position != -1:
        s = s[:position]
    s.strip()
    return s

# Similar string cleaning
def removeExtraCharacters(s):
    if s.endswith('*'):
        s = s[0:-1]
    if s.endswith('#'):
        s = s[0:-1]
    while (s.endswith(' ') or s.endswith(':')) and ':' in s:
        s = s[0:-1]
    return s

class BRScraper:
    
    def __init__(self, server_url="http://www.baseball-reference.com/"):
        self.server_url = server_url
   
    # Parse player names from a player's URL
    # Returns an array of the necessary strings
    def parse_names(self, resource):
        # Regex comment removal, since some tables/data are commented out in the HTML
        removeCommentMarkers = re.compile("<!--|-->")
        page = urllib2.urlopen(self.server_url + resource)

        soup = BeautifulSoup(removeCommentMarkers.sub("", page.read()), "lxml")
        info = soup.find_all("p")
        
        data = []
        
        # We care about paragraphs that have strong tags with the related data
        for paragraph in info:
            strongs = paragraph.find_all("strong")
            for strong in strongs:
                value = strong.next_sibling
                category = removeExtraCharacters(strong.text)
                
                # These are the categories for which we want to record data
                if category == 'Position' or category == 'Positions':
                    data.append(value)
                if category == 'Bats':
                    data.append(value)
                if category == 'Throws':
                    data.append(value)
                if category == '2017 Contract Status':
                    data.append(value)
                if category == 'Last Game':
                    lastGameInfo = paragraph.find('a')
                    lastGame = lastGameInfo.text
                    if '2017' not in lastGame:
                        data.append('Contract Info Unavailable')
                if category == 'Full Name':
                    data.append(value)
       
        for i in range(len(data)):
            data[i] = reformatString(data[i])
        
        return data

    # Same as parse_name but for team URLs
    def parse_team(self, resource):
        removeCommentMarkers = re.compile("<!--|-->")
        page = urllib2.urlopen(self.server_url + resource)

        soup = BeautifulSoup(removeCommentMarkers.sub("", page.read()), "lxml")
        info = soup.find_all("p")

        data = []
        for paragraph in info:
            strongs = paragraph.find_all("strong")
            for strong in strongs:
                value = strong.next_sibling
                category = removeExtraCharacters(strong.text)
                if category == 'Record':
                    # Put team record into database
                    data.append(value)
                    
                    # Put team conference and division into database
                    conferenceInfo = paragraph.find('a')
                    value = conferenceInfo.text
                    
                    if value[:2] == 'NL':
                        conference = 'National'
                    else:
                        conference = 'American'
                    division = value[3:]
                    
                    data.append(conference)
                    data.append(division)

                if category == 'Manager' or category == 'Managers':
                    managerInfo = paragraph.find('a')
                    value = managerInfo.text
                    data.append(value)
                
        for i in range(len(data)):
            data[i] = reformatString(data[i])
        
        return data

    # This code was referenced from github.com/andrewblim/br-scraper
    def parse_tables(self, resource, table_ids=None, verbose=False):
        """
        Given a resource on the baseball-reference server (should consist of 
        the url after the hostname and slash), returns a dictionary keyed on 
        table id containing arrays of data dictionaries keyed on the header 
        columns. table_ids is a string or array of strings that can optionally 
        be used to filter out which stats tables to return. 
        """

        def is_parseable_table(tag):
            if not tag.has_attr("class"): return False
            return tag.name == "table" and "stats_table" in tag["class"] and "sortable" in tag["class"]

        def is_parseable_row(tag):
            if not tag.name == "tr": return False
            if not tag.has_attr("class"): return True  # permissive
            return "league_average_table" not in tag["class"] and "stat_total" not in tag["class"]

        if isinstance(table_ids, str): table_ids = [table_ids]
        
        # Some of the tables in Baseball-Reference.com are commented out
        # So we need to remove the comment markers before we can access the tables
        removeCommentMarkers = re.compile("<!--|-->")
        page = urllib2.urlopen(self.server_url + resource)
        
        soup = BeautifulSoup(removeCommentMarkers.sub("", page.read()), "lxml")
        tables = soup.find_all("table")
        data = {}
        
        # Read through each table on the page
        for table in tables:
            
            if table_ids != None and table["id"] not in table_ids: continue
            if verbose: print "Processing table " + table["id"]
            data[table["id"]] = []
            
            # Headers will be keys in our dictionary
            headers = table.find("thead").find_all("th")
            header_names = []
            for header in headers:
                base_header_name = header.text.strip()
                if base_header_name in header_names:
                    i = 1
                    header_name = base_header_name + "_" + str(i)
                    # Watch out for repeat header_names, to avoid duplicate keys in our dict
                    while header_name in header_names:
                        i += 1
                        header_name = base_header_name + "_" + str(i)
                    if verbose: 
                        if base_header_name == "":
                            print "Empty header relabeled as %s" % header_name
                        else:
                            print "Header %s relabeled as %s" % (base_header_name, header_name)
                else:
                    header_name = base_header_name
                header_names.append(header_name)
            

            # Entries will be values in our dictionary
            rows = table.find("tbody").find_all(is_parseable_row)
            for row in rows:
                # Entries have either td or th tags, so we check for both
                entries = row.find_all("td")
                entries = row.find_all("th") + entries
                entry_data = []

                for entry in entries:
                    entry_data.append(removeExtraCharacters(entry.text.strip()))
                if len(entry_data) > 0:
                    data[table["id"]].append(dict(zip(header_names, entry_data)))
        
        return data
