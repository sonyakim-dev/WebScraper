from extractors.wwr import extract_wwr_jobs
from extractors.indeed import extract_indeed_jobs

keyword = input("What do you wnat to search for? ")

indeed = extract_indeed_jobs(keyword)
wwr = extract_indeed_jobs(keyword)
jobs = indeed + wwr

for job in jobs:
  print(job)