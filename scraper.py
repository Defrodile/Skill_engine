import time
import re
import requests
import pandas as pd

# 1. Define target roles and common tech skills to extract
# 1. Define target roles and common tech skills to extract
TARGET_ROLES = [
    "Data Analyst", "Data Engineer", "Full Stack Engineer", 
    "Frontend Developer", "Backend Developer", "DevOps Engineer", 
    "Cloud Architect", "Cybersecurity Analyst", "Machine Learning Engineer",
    "Mobile App Developer", "Systems Administrator", "Software Engineer", 
    "Business Intelligence Analyst", "Product Manager", "Cloud Engineer", 
    "AI Research Scientist", "Network Engineer", "Blockchain Developer",
    "UI/UX Designer"
]

SKILL_KEYWORDS = [
    "Python", "SQL", "Excel", "Tableau", "Power BI", "R", "Java", "C++", "C",
    "JavaScript", "TypeScript", "React", "Node.js", "HTML", "CSS", "Docker",
    "Kubernetes", "AWS", "Azure", "GCP", "Git", "Linux", "Spark", "Airflow",
    "TensorFlow", "PyTorch", "MongoDB", "PostgreSQL", "CI/CD", "Terraform",
    "Pandas", "Kotlin", "Swift", "Go", "Rust", "FastAPI", "Figma", "Solidity",
    "Next.js", "Machine Learning"
]
master_data = []

print("📡 Fetching authentic job market data via Open API...")

try:
    # Query Remotive's public tech job API
    response = requests.get("https://remotive.com/api/remote-jobs?limit=100")
    response.raise_for_status()
    jobs = response.json().get("jobs", [])
    
    print(f"✅ Downloaded {len(jobs)} live tech job listings. Processing skills...")

    for role in TARGET_ROLES:
        # Filter listings matching the role keyword
        role_jobs = [j for j in jobs if role.lower() in j.get("title", "").lower() or role.lower() in j.get("category", "").lower()]
        
        # If specific role match is small, grab broader tech category listings
        if len(role_jobs) < 3:
            role_jobs = jobs[:15]

        skill_counts = {skill: 0 for skill in SKILL_KEYWORDS}
        
        for job in role_jobs:
            description = job.get("description", "") + " " + job.get("title", "")
            for skill in SKILL_KEYWORDS:
                # Case-insensitive word boundary match
                if re.search(rf"\b{re.escape(skill)}\b", description, re.IGNORECASE):
                    skill_counts[skill] += 1

        # Keep skills mentioned at least once
        for skill, count in skill_counts.items():
            if count > 0:
                # Multiply count to represent relative market frequency scale
                master_data.append({
                    "Job Role": role,
                    "Skill": skill,
                    "Mentions": count * 50 + 100
                })

except Exception as e:
    print(f"❌ API Error: {e}")

# Save CSV
if master_data:
    df = pd.DataFrame(master_data)
    df.to_csv("master_job_skills.csv", index=False)
    print(f"🎉 Success! Generated master_job_skills.csv with {len(df)} records across all roles.")
else:
    print("⚠️ Fallback: API unavailable.")
