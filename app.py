from flask import Flask, request, redirect, url_for, session, render_template_string
from datetime import datetime
import json, os

app = Flask(__name__)
app.secret_key = "inner-radiance-secret"

DATA_FILE = "data.json"

# ---------- STORAGE ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------- CORE LOGIC ----------
def calculate_radiance(m, v, c, g):
    return round(0.3*m + 0.3*v + 0.2*c + 0.2*g, 2)

def categorize_radiance(r):
    if r < 0.3: return "Low"
    if r < 0.6: return "Medium"
    if r < 0.85: return "High"
    return "Blooming Lotus"

def ai_guidance(m, v, c, g):
    tips = []
    if m < 0.4: tips.append("Increase mindfulness with 5 minutes of breathing.")
    if v < 0.4: tips.append("Your vitality is low. Rest and hydrate.")
    if c < 0.4: tips.append("Reach out to someone today.")
    if g < 0.4: tips.append("Learn one small thing today.")
    if not tips: tips.append("You are balanced. Maintain consistency.")
    return tips

# ---------- AUTH ----------
@app.route("/login", methods=["GET","POST"])
def login():
    data = load_data()
    if request.method == "POST":
        user = request.form["username"].strip()
        if user:
            data["users"].setdefault(user, {
                "plan": "free",
                "history": []
            })
            save_data(data)
            session["user"] = user
            return redirect("/")
    return render_template_string(LOGIN_HTML)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------- MAIN APP ----------
@app.route("/", methods=["GET","POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    data = load_data()
    user = session["user"]
    profile = data["users"][user]
    history = profile["history"]

    result = tips = None

    if request.method == "POST":
        # PRO limit
        today = datetime.now().strftime("%Y-%m-%d")
        today_entries = [h for h in history if h["date"].startswith(today)]
        if profile["plan"] == "free" and len(today_entries) >= 1:
            return "Daily limit reached. Upgrade to PRO."

        m = float(request.form["mindfulness"]) / 10
        v = float(request.form["vitality"]) / 10
        c = float(request.form["connection"]) / 10
        g = float(request.form["growth"]) / 10

        r = calculate_radiance(m,v,c,g)
        level = categorize_radiance(r)
        tips = ai_guidance(m,v,c,g)

        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "m": m, "v": v, "c": c, "g": g,
            "radiance": r,
            "level": level
        }
        history.append(record)
        save_data(data)
        result = (r, level)

    return render_template_string(
        DASHBOARD_HTML,
        user=user,
        plan=profile["plan"],
        history=history,
        result=result,
        tips=tips
    )

# ---------- SUBSCRIPTION (LOGIC READY) ----------
@app.route("/upgrade")
def upgrade():
    data = load_data()
    user = session["user"]
    data["users"][user]["plan"] = "pro"   # replace with Stripe/Razorpay later
    save_data(data)
    return redirect("/")

# ---------- WEEKLY DATA (FOR CHARTS) ----------
@app.route("/weekly")
def weekly():
    data = load_data()
    user = session["user"]
    history = data["users"][user]["history"][-7:]
    return {
        "mindfulness": [h["m"] for h in history],
        "vitality": [h["v"] for h in history],
        "connection": [h["c"] for h in history],
        "growth": [h["g"] for h in history],
        "radiance": [h["radiance"] for h in history]
    }

# ---------- HTML ----------
LOGIN_HTML = """
<h2>Login</h2>
<form method="post">
<input name="username" placeholder="Enter username"/>
<button>Login</button>
</form>
"""

DASHBOARD_HTML = """
<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<h2>Inner Radiance</h2>
<p>User: {{user}} | Plan: {{plan.upper()}}</p>
<a href="/logout">Logout</a> |
<a href="/upgrade">Upgrade to PRO</a>

<form method="post">
<p>Mindfulness <input type="range" min="0" max="10" name="mindfulness" value="5"></p>
<p>Vitality <input type="range" min="0" max="10" name="vitality" value="5"></p>
<p>Connection <input type="range" min="0" max="10" name="connection" value="5"></p>
<p>Growth <input type="range" min="0" max="10" name="growth" value="5"></p>
<button>Submit</button>
</form>

{% if result %}
<h3>Today</h3>
<p>Radiance {{result[0]}} — {{result[1]}}</p>
<ul>
{% for t in tips %}<li>{{t}}</li>{% endfor %}
</ul>
{% endif %}

<h3>History</h3>
{% for h in history[-5:] %}
<p>{{h.date}} | {{h.radiance}} | {{h.level}}</p>
{% endfor %}
"""

if __name__ == "__main__":
    app.run() 