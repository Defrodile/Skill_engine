Workforce Skill Analytics Engine

This app helps students see if their skills match real industry jobs. A user enters their email and gets a one-time password (OTP) to log in. Then, they upload their resume as a PDF. The app reads the document, pulls out their technical skills, and compares them to a database of job requirements. It gives the user a readiness score, shows them what skills they are missing, and generates a personalized learning plan. Everything runs on Streamlit and Python.

Core Files

    app.py: The main web app, login system, and resume reader.

    master_job_skills.csv: The database of job roles and the skills they require.

    .streamlit/secrets.toml: A hidden file where the email password is kept safe.

Quick start

    Install the required Python libraries:
    pip install pandas streamlit plotly PyPDF2

    Set up the email login:
    Create a folder named .streamlit and a file inside it called secrets.toml. Add your email credentials like this:
    EMAIL_SENDER = "your_email@gmail.com"
    EMAIL_PASSWORD = "your_16_character_app_password"

    Run the app:
    streamlit run app.py

    Open the local link, enter your email address, and use the OTP sent to your inbox to log in.

-Team Zenith G1T7
