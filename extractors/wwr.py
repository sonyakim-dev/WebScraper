from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
  results = []
  base_url = "https://weworkremotely.com/remote-jobs/search?term="
  response = get(f"{base_url}{keyword}")
  
  if response.status_code != 200:
    print("Can't request website")
  else:
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("section", class_="jobs")
    for job_section in jobs:
      job_posts = job_section.find_all("li")
      job_posts.pop()
      for post in job_posts:
        anchor = post.find_all('a')[1]
        # print(anchor)
        link = anchor["href"]
        company, kind, region = anchor.find_all("span", class_="company")
        title = anchor.find("span", class_="title")
        job_data = {
          'link': f"https://weworkremotely.com{link}",
          'company': company.string,
          'kind': kind.string,
          'region': region.string,
          'position': title.string
        }
        results.append(job_data)
        
  return results