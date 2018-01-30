from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
import os
import pickle

# 237 colleges in the west #
# 101 colleges in the Mountain area #
# 210 colleges in the plain area
# 163 south central west  #
# 298 great lakes #
# 131 south central east #
# 346 south atlantic
# 491 north east #
#
# different search regions to keep search results under 500:
# great lakes, south central west (461)
# west, mountain, south central east (469)
# north east (491)
# south atlantic (346)
# plain (210)

glsw = ['gl', 'scw']
wmonsce = ['west', 'mon', 'sce']
ne = ['ne']
sa = ['sa']
pl = ['pl']

chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

#list to hold all of college links/names
college_links = []
college_names = []

def getColleges(regionList):
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://www.collegedata.com/cs/search/college/college_search_tmpl.jhtml")
    driver.execute_script("window.scrollTo(0, 100)")
    for region in regionList:
        if region == "west":
            #clicking on the west region. This is the only region where we have to use
            #action chains. The selection of the mountain region overlaps with the west.
            #This forces the click to be on the top left corner of the mountain region
            #element, which allows us to select the west region.
            element = driver.find_element_by_xpath('//*[@id="mon"]')
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(element, 0, 0)
            action.click()
            action.perform()
        else:
            element = driver.find_element_by_xpath('//*[@id="%s"]' % (region))
            element.click()

    #The website has a bootstrapped bar which covers the click of the 'search'
    #button unless you scroll down first.
    driver.execute_script("window.scrollTo(0, 1500)")
    search = driver.find_element_by_xpath('//*[@id="seachbyprefer"]/ul/li[8]/input')
    search.click()

    hasNextPage = True
    #this for loop just scrapes the first page. The indexes from the first and subsequent
    #pages are different (subsequent includes a 'previous' button), so need to loop through
    #them differently
    for i in range(1,9):
        #capturing all the names/links for colleges
        college_elements = driver.find_elements_by_class_name('collegelink')
        #looping through the links on each page to append
        for j in range(len(college_elements)):
             college_names.append(college_elements[j].text)
             college_links.append(college_elements[j].get_attribute("href"))
        driver.execute_script("window.scrollTo(0, 1500)")
        time.sleep(0.2)
        nextpage = driver.find_element_by_xpath('//*[@id="resultsListFixed"]/tfoot/tr/td/div/p/a[%s]' % (i))
        nextpage.click()

    while hasNextPage:
        try:
            for i in range(2,10):
                college_elements = driver.find_elements_by_class_name('collegelink')
                for j in range(len(college_elements)):
                     college_names.append(college_elements[j].text)
                     college_links.append(college_elements[j].get_attribute("href"))
                driver.execute_script("window.scrollTo(0, 1500)")
                time.sleep(0.2)
                nextpage = driver.find_element_by_xpath('//*[@id="resultsListFixed"]/tfoot/tr/td/div/p/a[%s]' % (i))
                nextpage.click()
        except:
            hasNextPage = False

getColleges(glsw)
getColleges(wmonsce)
getColleges(ne)
getColleges(sa)
getColleges(pl)

with open('college_links.pkl', 'wb') as f:
    pickle.dump(college_links, f)

with open('college_names.pkl', 'wb') as f:
    pickle.dump(college_names, f)
