import streamlit as st
import requests

st.title("🤖 GitGrade – AI GitHub Repo Evaluator")

repo_url = st.text_input("Enter a GitHub repository URL")

def analyze_repo(url):
    try:
        user_repo = url.split("github.com/")[-1]
        api_url = f"https://api.github.com/repos/{user_repo}"

        data = requests.get(api_url).json()

        if "message" in data:
            return "Invalid URL or API limit reached.", "", ""

        # Basic metrics
        stars = data.get("stargazers_count", 0)
        forks = data.get("forks_count", 0)
        watchers = data.get("watchers_count", 0)
        has_readme = requests.get(f"{api_url}/contents/README.md").status_code == 200

        # Simple scoring
        score = 0
        if has_readme: score += 25
        if stars > 0: score += 15
        if forks > 0: score += 15
        if watchers > 0: score += 10
        score += min(stars, 10)  # small bonus
        score = min(100, score)

        # Summary
        summary = f"The repository has {stars} ⭐, {forks} forks, and {'a' if has_readme else 'no'} README file."

        # Roadmap
        roadmap = []
        if not has_readme:
            roadmap.append("📝 Add a detailed README.md with setup instructions.")
        if stars < 5:
            roadmap.append("🚀 Improve project visibility with better documentation and real-world examples.")
        if forks == 0:
            roadmap.append("🤝 Encourage collaboration by making contribution guidelines.")
        if not roadmap:
            roadmap.append("✅ Excellent! Consider adding CI/CD workflows for automation.")

        return score, summary, "\n".join(roadmap)

    except Exception as e:
        return "Error: " + str(e), "", ""

if st.button("Analyze"):
    with st.spinner("Analyzing repository..."):
        score, summary, roadmap = analyze_repo(repo_url)
        st.subheader(f"Score: {score}/100")
        st.write(summary)
        st.markdown("### 🧭 Personalized Roadmap:")
        st.text(roadmap)