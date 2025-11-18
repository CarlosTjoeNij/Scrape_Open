import pandas as pd
from jobspy import scrape_jobs
from supabase import create_client, Client
import numpy as np

# --- CONFIG ---
SUPABASE_URL = "https://xzfvrjuxhacdytbvgkcg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6ZnZyanV4aGFjZHl0YnZna2NnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyNDE3ODksImV4cCI6MjA3NzgxNzc4OX0.SVw2abCoXakoRKgl5YyrD28fHKsnIvJmtfg5fY5ZeRc"
TABLE_NAME = "carlos_linkedin_indeed"

# --- HELPER ---
def clean_df(df):
    df = df[['title', 'company', 'location', 'emails', 'job_url', 'date_posted']]
    df = df.rename(columns={
        'title': 'titel',
        'company': 'opdrachtgever',
        'location': 'locatie',
        'emails': 'email',
        'job_url': 'link',
        'date_posted': 'datum_geplaatst'
    })
    return df[df['titel'].str.contains('data', case=False, na=False)]


# --- INDEED ---
jobs_indeed = scrape_jobs(
    site_name=["indeed"],
    search_term="data analytics, data science, data analyse, machine learning, data engineer, big data",
    location="Netherlands",
    results_wanted=2000,
    country_indeed="Netherlands"
)

df_indeed = clean_df(pd.DataFrame(jobs_indeed))


# --- LINKEDIN ---
jobs_linkedin = scrape_jobs(
    site_name=["linkedin"],
    search_term="data, data analytics, data science, data analyse, machine learning, data engineer, big data",
    location="Netherlands",
    results_wanted=2000,
    linkedin_fetch_description=True
)

df_linkedin = clean_df(pd.DataFrame(jobs_linkedin))


# --- COMBINE ---
alles = pd.concat([df_indeed, df_linkedin], ignore_index=True)
alles["id"] = range(1, len(alles) + 1)
alles = alles.replace([np.inf, -np.inf], None)
alles = alles.where(pd.notnull(alles), None)

# --- SAVE TO SUPABASE ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
records = alles.to_dict(orient="records")

response = supabase.table(TABLE_NAME).insert(records).execute()

print("✔️ Data succesvol naar Supabase gestuurd!")
