import os

from supabase import create_client, Client


url = "https://tvxaginourcwtvnrctfk.supabase.co"

key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2eGFnaW5vdXJjd3R2bnJjdGZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI4MzIyNDIsImV4cCI6MjA4ODQwODI0Mn0.YGaABksFazhb7M30XTbK4XyOoMd1b_i9ZMtebS-7i6M"

print ("Supabase URL: " + url)

supabase: Client = create_client(url, key)

response = supabase.auth.sign_up(
    {
        "email": "email@example.com",
        "password": "password",
    }
)