from flask import Flask, request, render_template
from nlp_processor import calculate_similarity, extract_skills  # Import extract_skills too
from database import init_db, save_match, get_all_matches

app = Flask(__name__)

# Initialize database
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    match_result = None
    history = get_all_matches()
    matched_skills = []  # Default empty list
    
    if request.method == "POST":
        job_desc = request.form["job_desc"]
        resume = request.form["resume"]
        
        # Calculate similarity
        score = calculate_similarity(job_desc, resume)
        match_result = f"Match Score: {score}%"
        
        # Extract and find matched skills
        job_skills = set(extract_skills(job_desc).split())
        resume_skills = set(extract_skills(resume).split())
        matched_skills = list(job_skills.intersection(resume_skills))  # Perform intersection in Python
        
        # Save to database
        save_match(job_desc, resume, score)
        history = get_all_matches()  # Refresh history
    
    return render_template("index.html", match_result=match_result, history=history, matched_skills=matched_skills)

if __name__ == "__main__":
    app.run(debug=True)
