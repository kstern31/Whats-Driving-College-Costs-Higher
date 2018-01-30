import scrapy
import time
import os
import pickle
from collections import defaultdict

with open('/Users/kstern/ds/metis/Kevin/Projects/Luther/dataCollection/links/college_links.pkl', 'rb') as f:
    linkList = pickle.load(f)

with open('/Users/kstern/ds/metis/Kevin/Projects/Luther/dataCollection/links/college_names.pkl', 'rb') as f:
    nameList = pickle.load(f)


class WestMonSCECollegeSpider(scrapy.Spider):
    name = 'college'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'https://www.collegedata.com/cs/search/college/college_search_tmpl.jhtml'
    ]

    def parse(self, response):

        # Extract the links to the individual college pages
        college_links = linkList
        college_names = nameList

        for i in range(len(college_links)):
            yield scrapy.Request(
                url=college_links[i],
                callback=self.parse_overview,
                meta={'url': college_links[i], 'name': college_names[i], 'id': college_links[i].split("schoolId=",1)[1]},
            )

    def parse_overview(self, response):
        schoolDict = response.request.meta

        ##########
        # Overview
        # ########
        schoolDict['institutionType'] = (
            response.xpath('//*[@id="cont_overview"]/div[1]/table/tbody/tr[2]/td/text()').extract_first())

        yield scrapy.Request(
    		url = "https://www.collegedata.com/cs/data/college/college_pg02_tmpl.jhtml?schoolId=%s" % (schoolDict['id']),
    		callback = self.parse_admissions,
    		meta = schoolDict,
		)

    def parse_admissions(self, response):
        schoolDict = response.request.meta
        ##########
        # Admissions
        # ########
        schoolDict['admissionRate'] = (
            response.xpath('//*[@id="section8"]/table[1]/tbody/tr[1]/td/text()').extract_first())
        #do we want to check ^ later?
        schoolDict['SATMath'] = (
            response.xpath('//*[@id="section8"]/table[3]/tbody/tr[1]/td/text()').extract_first())

        schoolDict['SATReading'] = (
            response.xpath('//*[@id="section8"]/table[3]/tbody/tr[8]/td/text()').extract_first())

        schoolDict['SATWriting'] = (
            response.xpath('//*[@id="section8"]/table[3]/tbody/tr[15]/td/text()').extract_first())

        schoolDict['ACT'] = (
            response.xpath('//*[@id="section8"]/table[4]/tbody/tr[1]/td/text()').extract_first())

        schoolDict['avgGPA'] = (
            response.xpath('//*[@id="section8"]/table[2]/tbody/tr[1]/td/text()').extract_first())

        yield scrapy.Request(
    		url = "https://www.collegedata.com/cs/data/college/college_pg03_tmpl.jhtml?schoolId=%s" % (schoolDict['id']),
    		callback = self.parse_money,
    		meta = schoolDict,
		)

    def parse_money(self,response):
        schoolDict = response.request.meta
        ##########
        # Money
        # ########
        schoolDict['totalCost'] = (
            response.xpath('//*[@id="section9"]/table/tbody/tr[1]/td/text()').extract())

        schoolDict['tuitionCost'] = (
            response.xpath('//*[@id="section9"]/table/tbody/tr[2]/td/text()').extract())

        schoolDict['roomCost'] = (
            response.xpath('//*[@id="section9"]/table/tbody/tr[3]/td/text()').extract())

        schoolDict['bookCost'] = (
            response.xpath('//*[@id="section9"]/table/tbody/tr[4]/td/text()').extract())

        schoolDict['otherCost'] = (
            response.xpath('//*[@id="section9"]/table/tbody/tr[5]/td/text()').extract())

        schoolDict['gotFinancialNeed'] = (
            response.xpath('//*[@id="section11"]/table[2]/tbody/tr[3]/td/text()').extract_first())

        schoolDict['avgAward'] = (
            response.xpath('//*[@id="section11"]/table[2]/tbody/tr[6]/td/text()').extract_first())

        schoolDict['pctWithLoans'] = (
            response.xpath('//*[@id="section11"]/table[3]/tbody/tr[1]/td/text()').extract_first())

        schoolDict['avgIndebtness'] = (
            response.xpath('//*[@id="section11"]/table[3]/tbody/tr[2]/td/text()').extract_first())

        yield scrapy.Request(
    		url = "https://www.collegedata.com/cs/data/college/college_pg04_tmpl.jhtml?schoolId=%s" % (schoolDict['id']),
    		callback = self.parse_academics,
    		meta = schoolDict,
		)

    def parse_academics(self,response):
        schoolDict = response.request.meta
        ##########
        # Academics
        # ########
        schoolDict['classSize'] = (
            response.xpath('//*[@id="section15"]/table/tbody/tr[4]/td/text()').extract())

        schoolDict['numFaculty'] = (
            response.xpath('//*[@id="section15"]/table/tbody/tr[1]/td/text()').extract_first())

        yield scrapy.Request(
    		url = "https://www.collegedata.com/cs/data/college/college_pg05_tmpl.jhtml?schoolId=%s" % (schoolDict['id']),
    		callback = self.parse_campusLife,
    		meta = schoolDict,
		)

    def parse_campusLife(self,response):
        schoolDict = response.request.meta
        ##########
        # Campus Life
        # ########
        schoolDict['areaPop'] = (
            response.xpath('//*[@id="section20"]/table[1]/tbody/tr[1]/td/text()').extract_first())

        schoolDict['campusSize'] = (
            response.xpath('//*[@id="section20"]/table[1]/tbody/tr[4]/td/text()').extract_first())

        schoolDict['nearestAirport'] = (
            response.xpath('//*[@id="section20"]/table[3]/tbody/tr[2]/td/text()').extract_first())

        schoolDict['nearestBus'] = (
            response.xpath('//*[@id="section20"]/table[3]/tbody/tr[3]/td/text()').extract_first())

        schoolDict['nearestTrain'] = (
            response.xpath('//*[@id="section20"]/table[3]/tbody/tr[4]/td/text()').extract_first())

        schoolDict['sportsDivision'] = (
            response.xpath('//*[@id="section24"]/table[1]/tbody/tr[1]/td/text()').extract_first())

        schoolDict['mascot'] = (
            response.xpath('//*[@id="section24"]/table[1]/tbody/tr[2]/td/text()').extract_first())

        schoolDict['schoolColors'] = (
            response.xpath('//*[@id="section24"]/table[1]/tbody/tr[3]/td/text()').extract_first())

        schoolDict['sororities'] = (
            response.xpath('//*[@id="section25"]/table/tbody/tr[2]/td/text()').extract_first())

        schoolDict['fraternities'] = (
            response.xpath('//*[@id="section25"]/table/tbody/tr[3]/td/text()').extract_first())

        schoolDict['freshmanHousingGuaranteed'] = (
            response.xpath('//*[@id="section21"]/table/tbody/tr[5]/td/text()').extract_first())

        yield scrapy.Request(
    		url = "https://www.collegedata.com/cs/data/college/college_pg06_tmpl.jhtml?schoolId=%s" % (schoolDict['id']),
    		callback = self.parse_students,
    		meta = schoolDict,
		)

    def parse_students(self,response):
        schoolDict = response.request.meta
        ##########
        # Students
        # ########
        schoolDict['coed'] = (
            response.xpath('//*[@id="section26"]/table/tbody/tr[1]/td/text()').extract_first())

        schoolDict['numUndergrad'] = (
            response.xpath('//*[@id="section26"]/table/tbody/tr[2]/td/text()').extract_first())

        schoolDict['undergradWomen'] = (
            response.xpath('//*[@id="section26"]/table/tbody/tr[3]/td/text()').extract_first())

        schoolDict['undergradMen'] = (
            response.xpath('//*[@id="section26"]/table/tbody/tr[4]/td/text()').extract_first())

        schoolDict['numGrad'] = (
            response.xpath('//*[@id="section26"]/table/tbody/tr[9]/td/text()').extract_first())

        schoolDict['avgAge'] = (
            response.xpath('//*[@id="section26"]/table/tbody/tr[8]/td/text()').extract_first())

        schoolDict['pctInternationalStudents'] = (
            response.xpath('//*[@id="section26"]/table/tbody/tr[7]/td/text()').extract_first())

        schoolDict['pctStudentsGraduatingin4Yrs'] = (
            response.xpath('//*[@id="section27"]/table/tbody/tr[2]/td/text()').extract_first())

        schoolDict['pctEmployedin6Mo'] = (
            response.xpath('//*[@id="section28"]/table/tbody/tr[1]/td/text()').extract_first())

        schoolDict['pctAdvancedStudy'] = (
            response.xpath('//*[@id="section28"]/table/tbody/tr[3]/td/text()').extract_first())

        schoolDict['averageSalary'] = (
            response.xpath('//*[@id="section28"]/table/tbody/tr[2]/td/text()').extract_first())

        yield schoolDict
