from supabase import create_client, Client
import os

# Best practice: keep credentials in environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client("https://zewstvvppkclrqevjzkd.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpld3N0dnZwcGtjbHJxZXZqemtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxMjM0MjAsImV4cCI6MjA3MzY5OTQyMH0.tJPvmWQQY-Gyi4WPJyRbJCRrxlKd-M2Eg0CkLrAB7p4")
