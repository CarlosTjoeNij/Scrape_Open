import csv
from jobspy import scrape_jobs
import pandas as pd
import numpy as np
import fitz
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import streamlit as st
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from rapidfuzz import process, fuzz
import pyarrow.parquet as pq
from supabase import create_client, Client

# INDEED #
jobs_indeed = scrape_jobs(
    site_name=["indeed"], #, "zip_recruiter", "glassdoor", "google"],
    search_term = "data analytics, data science, data analyse, machine learning, data engineer, big data",
    location="Netherlands",
    results_wanted=2000,
    #hours_old=24,
    country_indeed='Netherlands',
    #linkedin_fetch_description=True
    # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
)
df_indeed = pd.DataFrame(jobs_indeed)
df_data = df_indeed[df_indeed['title'].str.contains('data', case=False, na=False)]
df_data = df_data[['title','company','location', 'emails', 'job_url', 'date_posted']]
df_data = df_data.rename(columns={
    'title': 'Titel',
    'company': 'Opdrachtgever',
    'location': 'Plaats',
    'emails': 'Email',
    'job_url': 'Link',
    'date_posted': 'Datum geplaatst'
})

# LINKED IN #
jobs_linked = scrape_jobs(
    site_name=["linkedin"], #, "zip_recruiter", "glassdoor", "google"],
    search_term = "data, data analytics, data science, data analyse, machine learning, data engineer, big data",
    location="Netherlands",
    results_wanted=2000,
    #hours_old=8766,
    country_indeed='Netherlands',
    #linkedin_fetch_description=True
    linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
)
df_linked = pd.DataFrame(jobs_linked)
data_vacas_linked = df_linked[df_linked['title'].str.contains('data', case=False, na=False)]

df_data_L = data_vacas_linked[['title','company','location', 'emails', 'job_url', 'date_posted']]
df_data_L = df_data_L.rename(columns={
    'title': 'Titel',
    'company': 'Opdrachtgever',
    'location': 'Plaats',
    'emails': 'Email',
    'job_url': 'Link',
    'date_posted': 'Datum geplaatst'
})

alles = pd.concat([df_data, df_data_L], ignore_index=True)
alles['id'] = range(1, len(alles) + 1)

# NAAR DB #
url = "https://xzfvrjuxhacdytbvgkcg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZnZyanV4aGFjZHl0YnZna2NnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyNDE3ODksImV4cCI6MjA3NzgxNzc4OX0.SVw2abCoXakoRKgl5YyrD28fHKsnIvJmtfg5fY5ZeRc"

supabase: Client = create_client(url, key)
table_name = "carlos"

records = scrapes.to_dict(orient="records")

response = supabase.table(table_name).insert(records).execute()
