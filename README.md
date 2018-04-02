# Whats-Driving-College-Costs-Higher

1. Collect individual links to college pages/names using the selenium scripts in the dataCollection/scripts folder.
A selenium script had to be used because of the layout of collegedata.com. They have no full listing of all their
colleges anywhere, and the only way to get them is by doing individual searches that capture them all. Unfortunately,
the max number of colleges in a search query is 500, so you have to do multiple searches.

2. Use the scrapy spider in the 'colleges' folder to get information from each individual college link from step 1.

3. EDA in the dataExploration folder.

4. Analysis in the dataAnalysis foldder.
