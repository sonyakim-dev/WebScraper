from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Selenium: prevent bot blocking and enable automating brower
options = Options()
options.add_argument("--no-sandbox") # only for replit
options.add_argument("--disable-dev-shm-usage") # only for replit

def extract_indeed_jobs(keyword):
  pages = get_page_count(keyword)
  
  for page in range(pages):
    base_url = "https://www.indeed.com/jobs"
    search_term = keyword.replace(' ', '+')
    
    browser = webdriver.Chrome(options=options)
    browser.get(f"{base_url}?q={search_term}&start={page*10}")
    
    soup = BeautifulSoup(browser.page_source, "html.parser")
    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = job_list.find_all("li", recursive=False)
    result = []
    
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone: continue
      
      anchor = job.select_one("h2 a")
      title = anchor.find('span').string
      link = anchor['href']
      company = job.find('span', class_="companyName")
      location = job.find('div', class_="companyLocation")
      job_data = {
        "link": f"https://www.indeed.com{link}",
        "company": company.string,
        "location": location.string,
        "position": title,
      }
      result.append(job_data)
    
  return result


def get_page_count(keyword):
  base_url = "https://www.indeed.com/jobs?q="
  search_term = keyword.replace(' ', '+')
  
  browser = webdriver.Chrome(options=options)
  browser.get(f"{base_url}{search_term}")
  
  soup = BeautifulSoup(browser.page_source, "html.parser")
  pagination = soup.find("nav", attrs={"aria-label": "pagination"})
  pages = len(pagination.find_all("div", recursive=False)) if pagination else 1
  
  return pages if pages < 5 else 5