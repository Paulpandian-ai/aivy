"""
AIvy — Learn AI, Become a Doctor
A 40-day kids' learning app (medicine + AI). One child, no login.
Run locally:  streamlit run streamlit_app.py
"""

import streamlit as st
import json, os, re

STATE_FILE = "aivy_state.json"
TOTAL = 40

# ----------------------------------------------------------------------
# CURRICULUM
# ----------------------------------------------------------------------
L = {
    "claude": ("Open Claude (with a grown-up)", "https://claude.ai"),
    "teach":  ("Teachable Machine", "https://teachablemachine.withgoogle.com"),
    "qdraw":  ("Quick, Draw!", "https://quickdraw.withgoogle.com"),
    "scratch":("Scratch", "https://scratch.mit.edu"),
    "mlkids": ("ML for Kids", "https://machinelearningforkids.co.uk"),
    "codeAI": ("Code.org: How AI Works", "https://code.org/en-US/resources/videos"),
    "codeGen":("Code.org: How Generative AI Works", "https://code.org/en-US/resources/videos"),
    "kidGen": ("Kids encyclopedia: Generative AI", "https://kids.kiddle.co/Generative_artificial_intelligence"),
    "kidAI":  ("Kids encyclopedia: AI", "https://kids.kiddle.co/Artificial_intelligence"),
}
CHANNELS = [
    ("Code.org · How AI Works", "https://code.org/en-US/resources/videos"),
    ("Crash Course Kids", "https://www.youtube.com/@crashcoursekids"),
    ("SciShow Kids", "https://www.youtube.com/@scishowkids"),
    ("TED-Ed", "https://www.youtube.com/@TEDEd"),
]

MODULES = [
    {"key":"meet","kicker":"Mission 1 · Days 1–6","title":"Meet AI","emoji":"🧠","color":"#15B79E","days":[
        {"n":1,"t":"What even is intelligence?","time":"20 min","video":"G6de8L7cVvM",
         "steps":["Watch the video, then tell a grown-up one thing that surprised you.",
                  "Talk: what makes humans smart? Can a computer be smart too?",
                  "Start your AI Notebook. Write what you think \"AI\" means today — you'll read it again on Day 40!"],
         "links":["kidAI"],"c":"Doctors solve mysteries with their thinking. Soon you'll see AI help them solve health mysteries."},
        {"n":2,"t":"Teach a computer to see","time":"25 min",
         "steps":["Play Quick, Draw! and let the computer guess your doodles.",
                  "Notice: it learned by looking at millions of drawings.",
                  "Try to draw something it CAN'T guess. Why is that tricky for it?"],
         "links":["qdraw"],"c":"AI learns from examples. Later you'll see it learn from medical pictures the same way."},
        {"n":3,"t":"Your first chat with Claude","time":"25 min",
         "steps":["With a grown-up, open Claude.",
                  "Ask 3 questions: a silly one, a science one, and \"How does the heart work?\"",
                  "Write the answer you liked best in your Notebook."],
         "links":["claude"],"c":"GenAI writes brand-new answers just for you instead of copy-pasting them."},
        {"n":4,"t":"Train your own AI","time":"30 min",
         "steps":["Open Teachable Machine and pick \"Image Project.\"",
                  "Teach it to tell a healthy apple from a bruised one using the webcam.",
                  "Test it! Show a new apple and see if it guesses right."],
         "links":["teach"],"c":"This is exactly how AI learns to spot healthy vs. unhealthy cells in a lab one day."},
        {"n":5,"t":"AI can get things wrong","time":"20 min",
         "steps":["Ask Claude something tricky, or try to trick Quick, Draw!.",
                  "Find one mistake the AI makes.",
                  "Write the mistake in your Notebook."],
         "links":["claude","qdraw"],"c":"Never trust AI blindly — especially about health. Always check with a real person."},
        {"n":6,"t":"Rest & imagine","time":"20 min",
         "steps":["Easy day! Draw a comic or write a story: \"The day a robot helped at my doctor's office.\"",
                  "Then go play — soccer counts!"],
         "links":[],"c":"Great doctors are great storytellers too — they explain things so people understand."},
    ]},
    {"key":"genai","kicker":"Mission 2 · Days 7–13","title":"How GenAI Thinks","emoji":"💬","color":"#FF7A66","days":[
        {"n":7,"t":"The next-word game","time":"20 min",
         "steps":["Watch a short video on how generative AI works.",
                  "Play the next-word game: take turns guessing the next word in a sentence.",
                  "That's a tiny version of how language AI works!"],
         "links":["codeGen","kidGen"],"c":"GenAI predicts what word comes next, over and over, super fast."},
        {"n":8,"t":"Good questions = good answers","time":"25 min",
         "steps":["With Claude, ask the same thing two ways: once fuzzy, once super clear.",
                  "Spot the difference in the answers.",
                  "Write your 3 best tips for asking clear questions."],
         "links":["claude"],"c":"Clear instructions help AI and people — a great skill for a future team leader."},
        {"n":9,"t":"Claude, my study buddy","time":"30 min",
         "steps":["Ask Claude to explain how the heart pumps blood, simply.",
                  "Check one fact on a kids' science site.",
                  "Do they agree? Write what you found."],
         "links":["claude","kidAI"],"c":"A future doctor always checks sources — never trusts just one."},
        {"n":10,"t":"Quiz me!","time":"25 min",
         "steps":["Ask Claude to make a 5-question quiz about the human body.",
                  "Answer them, then ask Claude to grade you.",
                  "Re-study the ones you missed."],
         "links":["claude"],"c":"Knowing the body inside and out is a doctor's superpower."},
        {"n":11,"t":"Co-write a story","time":"30 min",
         "steps":["With Claude, co-write a story about a girl doctor and her helpful AI.",
                  "YOU lead the plot — Claude just helps.",
                  "Read your favorite part out loud."],
         "links":["claude"],"c":"You're the author and director — AI just holds the pen with you."},
        {"n":12,"t":"Real or AI?","time":"25 min",
         "steps":["Look at AI-made pictures with a grown-up.",
                  "Hunt for clues: weird hands, blurry letters, odd shadows.",
                  "Decide together: real or made-up?"],
         "links":["kidGen"],"c":"AI can make fake images, so be a smart detective and check before you believe."},
        {"n":13,"t":"Rest & reflect","time":"15 min",
         "steps":["List 3 cool things AI can do and 3 things it should NOT do.",
                  "Then take a break outside."],
         "links":[],"c":"Knowing a tool's limits is just as important as knowing its powers."},
    ]},
    {"key":"agent","kicker":"Mission 3 · Days 14–20","title":"What's an AI Agent?","emoji":"⚡","color":"#E0A21A","days":[
        {"n":14,"t":"Tool vs. Agent","time":"25 min",
         "steps":["A calculator waits for you. An agent makes a plan and takes steps on its own.",
                  "Find one example of each at home.",
                  "Draw the difference in your Notebook."],
         "links":["codeAI"],"c":"An agent works toward a goal — like a helper that doesn't need every step spelled out."},
        {"n":15,"t":"The Agent Loop","time":"25 min",
         "steps":["Learn the loop: Goal → Plan → Act → Check.",
                  "Use it to make a healthy snack from start to finish.",
                  "Draw the loop as a circle with 4 steps."],
         "links":[],"c":"Doctors use a loop too: check the patient, plan, treat, then check again."},
        {"n":16,"t":"Agents use tools","time":"25 min",
         "steps":["With a grown-up, watch Claude use search to find today's fun fact.",
                  "Notice it CHOSE a tool to reach a goal.",
                  "Ask it to summarize what it found in one sentence."],
         "links":["claude"],"c":"A smart agent picks the right tool for the job — like a doctor choosing the right test."},
        {"n":17,"t":"Build a sorter","time":"35 min",
         "steps":["Open ML for Kids and start a text project.",
                  "Train it to sort happy vs. sad words, then use it in Scratch.",
                  "Remember: it's a fun game, not real advice!"],
         "links":["mlkids","scratch"],"c":"You just taught a computer to notice patterns — the first step toward smart helpers."},
        {"n":18,"t":"Give it a mission","time":"30 min",
         "steps":["Ask Claude to plan a 3-day science-fair schedule with steps.",
                  "Watch it break one big goal into small ones.",
                  "Pick the step you'd start with."],
         "links":["claude"],"c":"Breaking a big goal into small steps is how agents (and great students) get things done."},
        {"n":19,"t":"Human in charge","time":"20 min",
         "steps":["Talk about why agents need rules and a human boss.",
                  "Make a short list of rules your helper must follow.",
                  "Star the most important rule."],
         "links":[],"c":"AI can suggest, but the doctor decides — always. This is called \"human in the loop.\""},
        {"n":20,"t":"Rest & poster","time":"25 min",
         "steps":["Creative day! Make a colorful poster of the Agent Loop for your wall.",
                  "Show it to someone and explain each step."],
         "links":[],"c":"Teaching an idea by drawing it means you really understand it."},
    ]},
    {"key":"med","kicker":"Mission 4 · Days 21–26","title":"AI in Medicine","emoji":"➕","color":"#0B8A78","days":[
        {"n":21,"t":"AI that sees scans","time":"30 min",
         "steps":["Doctors use AI to spot patterns in X-rays.",
                  "In Teachable Machine, train it to sort two simple picture types.",
                  "That's the same idea a scan-reading AI uses!"],
         "links":["teach"],"c":"Spotting patterns others miss is a doctor superpower — and AI can be a sidekick for it."},
        {"n":22,"t":"Symptom checkers","time":"25 min",
         "steps":["With a grown-up, imagine a symptom-checker app.",
                  "List 2 ways it helps and 2 ways it could be wrong.",
                  "Why is it NOT a real doctor?"],
         "links":["claude"],"c":"AI can give ideas, but only a real doctor can examine you and truly decide."},
        {"n":23,"t":"AI runs the hospital","time":"25 min",
         "steps":["Ask Claude for 3 ways AI helps hospitals run smoothly.",
                  "Think: scheduling, shorter waits, helping nurses.",
                  "Which idea is your favorite?"],
         "links":["claude"],"c":"A lot of doctor work is teamwork and timing — AI helps the whole hospital flow."},
        {"n":24,"t":"Reading X-rays","time":"30 min",
         "steps":["Learn how radiology AI flags spots for doctors to look at.",
                  "Talk about why a human ALWAYS double-checks.",
                  "Write why double-checking keeps patients safe."],
         "links":["kidAI"],"c":"AI points; the doctor confirms. Double-checking keeps patients safe."},
        {"n":25,"t":"Doctor + AI teammate","time":"25 min",
         "steps":["With a grown-up, ask Claude: \"How could a future doctor use an AI assistant during a check-up?\"",
                  "Discuss the answer together.",
                  "Journal your favorite idea."],
         "links":["claude"],"c":"Picture your future office: you, your patient, and a quiet AI helper taking notes."},
        {"n":26,"t":"Ask a real human","time":"30 min",
         "steps":["Write 5 questions for a real doctor, nurse, or pharmacist.",
                  "Ask one of them if you can!",
                  "Write down their best answer."],
         "links":[],"c":"Real mentors beat any app. The best learning comes from real people."},
    ]},
    {"key":"pharma","kicker":"Mission 5 · Days 27–32","title":"Medicines & Devices","emoji":"💊","color":"#E85A45","days":[
        {"n":27,"t":"How medicines are made","time":"25 min",
         "steps":["Ask Claude: what is pharma, and why does making medicine take years?",
                  "Then ask how AI speeds up the search.",
                  "Explain it back in your own words."],
         "links":["claude"],"c":"AI can test millions of ideas quickly, helping scientists find new medicines faster."},
        {"n":28,"t":"Folding proteins","time":"30 min",
         "steps":["Tiny shapes called proteins decide how medicine works.",
                  "AI (like AlphaFold) predicts their shapes.",
                  "Fold a paper \"protein\" to feel how shape matters."],
         "links":["claude"],"c":"Predicting protein shapes helps design new medicines — a huge real-world AI win."},
        {"n":29,"t":"Testing medicine safely","time":"25 min",
         "steps":["Learn what a clinical trial is — how medicine is tested to be safe.",
                  "Talk about how AI spots patterns in the results.",
                  "Why does safety always come first?"],
         "links":["claude"],"c":"Safety always comes first. AI helps, but careful humans run the tests."},
        {"n":30,"t":"Smart health devices","time":"25 min",
         "steps":["Explore smartwatches, smart insulin pumps, and hearing aids.",
                  "Find one device at home with a \"smart\" feature.",
                  "What does it measure?"],
         "links":["claude"],"c":"Tiny computers on your wrist can spot health changes early — AI helping you live well."},
        {"n":31,"t":"Design a kids' health watch","time":"35 min",
         "steps":["On paper, design a smart watch for kids.",
                  "With Claude, decide: What does it track? What does its AI agent do?",
                  "Draw it and give it a name!"],
         "links":["claude"],"c":"You just acted like a medical-device inventor — goal, plan, and helper in one."},
        {"n":32,"t":"Robot helpers in surgery","time":"25 min",
         "steps":["Explore surgery robots and AI stethoscopes.",
                  "They're helpers, not replacements.",
                  "List 2 things humans still do best."],
         "links":["claude"],"c":"Steady robot hands plus a caring human brain make the best team."},
    ]},
    {"key":"capstone","kicker":"Mission 6 · Days 33–40","title":"Ethics & Big Finish","emoji":"🛡️","color":"#2E5A8F","days":[
        {"n":33,"t":"Pick your favorite","time":"15 min",
         "steps":["Hospitals, medicines, or devices — which excites you most?",
                  "Write why.",
                  "Then rest — you're almost there!"],
         "links":[],"c":"Noticing what excites you is how you find your future path."},
        {"n":34,"t":"The 3 big rules","time":"25 min",
         "steps":["Privacy: your health data is yours.",
                  "Fairness: AI must work for everyone.",
                  "Humans decide: a person is always in charge."],
         "links":["claude"],"c":"Good medical AI is private, fair, and always has a human in charge."},
        {"n":35,"t":"When AI is wrong","time":"25 min",
         "steps":["In medicine, mistakes matter most.",
                  "List the rules a good medical AI agent must follow.",
                  "Star the rule that protects people most."],
         "links":[],"c":"The most caring engineers plan for mistakes BEFORE they happen."},
        {"n":36,"t":"Capstone: pick your mission","time":"30 min",
         "steps":["Design \"Dr. [Your Name]'s AI Helper.\"",
                  "Choose hospital, pharma, or device.",
                  "Write its Goal and its Agent Loop (Goal → Plan → Act → Check)."],
         "links":["claude"],"c":"This is your big project — your very own idea, start to finish."},
        {"n":37,"t":"Build the helper","time":"35 min",
         "steps":["With Claude, write your helper's rules and the tools it uses.",
                  "Write a sample chat between a doctor and your helper.",
                  "Make sure a human is always in charge!"],
         "links":["claude"],"c":"You're designing a real agent: a goal, tools, rules, and a human in charge."},
        {"n":38,"t":"Make it shine","time":"35 min",
         "steps":["Turn your idea into a poster or a few slides.",
                  "Add a drawing of how it works.",
                  "Practice pointing to each part."],
         "links":["claude"],"c":"Doctors and inventors share ideas clearly so others can help and cheer."},
        {"n":39,"t":"Practice your pitch","time":"25 min",
         "steps":["Present your project to your family.",
                  "Ask for one piece of feedback.",
                  "Make one improvement."],
         "links":[],"c":"Practicing out loud builds the confidence every leader needs."},
        {"n":40,"t":"Show time & celebrate!","time":"30 min",
         "steps":["Present your finished project!",
                  "Re-read your Day 1 Notebook page — look how much you learned.",
                  "Plan your next adventure."],
         "links":["claude"],"c":"You did it! You think like a doctor AND build like an AI explorer. What's next is up to you."},
    ]},
]

DAY_BY_N = {}
MODULE_OF = {}
for mi, m in enumerate(MODULES):
    for d in m["days"]:
        DAY_BY_N[d["n"]] = d
        MODULE_OF[d["n"]] = mi

# ----------------------------------------------------------------------
# STATE (progress saved to a small file; no login)
# ----------------------------------------------------------------------
def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"progress": [], "name": "", "videos": {}}

def save_state():
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({
                "progress": sorted(st.session_state.progress),
                "name": st.session_state.name,
                "videos": st.session_state.videos,
            }, f)
    except Exception:
        pass  # read-only filesystem: keep working in-session only

def parse_youtube_id(s):
    if not s:
        return None
    s = s.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})", s)
    if m:
        return m.group(1)
    m = re.search(r"[A-Za-z0-9_-]{11}", s)
    return m.group(0) if m else None

def get_video_id(day):
    """override (str id, '' = hidden) beats built-in default."""
    ov = st.session_state.videos.get(str(day))
    if ov is not None:
        return ov or None
    return DAY_BY_N[day].get("video")

# init session state once
if "loaded" not in st.session_state:
    s = load_state()
    st.session_state.progress = set(s.get("progress", []))
    st.session_state.name = s.get("name", "")
    st.session_state.videos = s.get("videos", {})
    st.session_state.view = "home"
    st.session_state.sel_module = 0
    st.session_state.sel_day = 1
    st.session_state.loaded = True

def go(view, **kw):
    st.session_state.view = view
    for k, v in kw.items():
        st.session_state[k] = v
    st.rerun()

# ----------------------------------------------------------------------
# PAGE + STYLE
# ----------------------------------------------------------------------
st.set_page_config(page_title="AIvy · Learn AI, Become a Doctor", page_icon="🩺", layout="centered")

st.markdown("""
<style>
  .stApp { background:#F2F7F4; }
  h1,h2,h3 { font-family:Georgia,'Times New Roman',serif; letter-spacing:-.01em; }
  .aivy-hero{background:linear-gradient(120deg,rgba(21,183,158,.14),rgba(255,122,102,.12));
    border:1px solid #DCE8E3;border-radius:20px;padding:22px 24px;margin-bottom:8px;}
  .aivy-kicker{font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#0B8A78;}
  .aivy-card{background:#fff;border:1px solid #DCE8E3;border-radius:16px;padding:16px 18px;margin-bottom:8px;}
  .aivy-connect{background:#FFF1EE;border:1px solid #FBD9D1;border-left:4px solid #FF7A66;
    border-radius:0 12px 12px 0;padding:12px 16px;margin:10px 0;}
  .aivy-connect b{color:#E85A45;}
  .aivy-guard{background:#FFF6EC;border:1px solid #F6E2C4;border-radius:14px;padding:12px 16px;color:#7a5a1e;font-size:.9rem;}
  .aivy-step{background:#fff;border:1px solid #DCE8E3;border-radius:12px;padding:10px 14px;margin-bottom:8px;}
  .aivy-badge{display:inline-block;font-size:.72rem;font-weight:800;color:#0B8A78;background:rgba(21,183,158,.12);
    border-radius:99px;padding:2px 10px;margin-left:6px;}
  .stButton>button{border-radius:10px;font-weight:700;}
</style>
""", unsafe_allow_html=True)

def link_row(link_keys):
    if not link_keys:
        return
    cols = st.columns(len(link_keys))
    for c, key in zip(cols, link_keys):
        label, url = L[key]
        with c:
            st.link_button(label, url, use_container_width=True)

# top ribbon: title + tiny progress
done = st.session_state.progress
count = len(done)
tc, pc = st.columns([3, 1])
with tc:
    st.markdown("### 🩺 AIvy")
with pc:
    st.markdown(f"<div style='text-align:right;font-weight:800;color:#4E6B74'>{count}/{TOTAL} days</div>",
                unsafe_allow_html=True)
st.progress(count / TOTAL)

# ----------------------------------------------------------------------
# HOME
# ----------------------------------------------------------------------
def render_home():
    name = st.session_state.name
    greet = f"Hi, {name}! " if name else ""
    st.markdown(f"""
    <div class="aivy-hero">
      <div class="aivy-kicker">Future Doctor · AI Explorer</div>
      <h1 style="margin:.2em 0 .1em">{greet}Learn how <span style="color:#E85A45">AI</span> helps doctors,
      medicines &amp; health gadgets.</h1>
      <p style="color:#4E6B74;margin:0">Pick a mission, watch a short video, try a hands-on activity,
      and check off your day. Forty small steps.</p>
    </div>
    """, unsafe_allow_html=True)

    # continue button
    nxt = next((i for i in range(1, TOTAL + 1) if i not in done), TOTAL)
    label = "Review Day 40" if count == TOTAL else f"▶ Start Day {nxt}"
    if st.button(label, type="primary", use_container_width=True):
        go("day", sel_day=nxt, sel_module=MODULE_OF[nxt])

    st.markdown('<div class="aivy-guard"><b>For grown-ups:</b> explore alongside your child. '
                'AI tools like Claude are made for adults, so sit together. Preview videos first, and consider '
                'YouTube Kids. Nothing here is medical advice. Progress saves automatically.</div>',
                unsafe_allow_html=True)

    st.markdown("#### The journey")
    for mi, m in enumerate(MODULES):
        c = sum(1 for d in m["days"] if d["n"] in done)
        with st.container(border=True):
            top, btn = st.columns([3, 1])
            with top:
                st.markdown(f"**{m['emoji']} {m['title']}**  \n"
                            f"<span style='color:#4E6B74;font-size:.85rem'>{m['kicker']} · {c}/{len(m['days'])} done</span>",
                            unsafe_allow_html=True)
                st.progress(c / len(m["days"]))
            with btn:
                if st.button("Open", key=f"mod_{mi}", use_container_width=True):
                    go("module", sel_module=mi)

    with st.expander("🎬 Video corner (trusted channels for kids)"):
        for label, url in CHANNELS:
            st.link_button(label, url, use_container_width=True)

    render_grownup_tools()

# ----------------------------------------------------------------------
# MODULE
# ----------------------------------------------------------------------
def render_module():
    m = MODULES[st.session_state.sel_module]
    if st.button("← Back to missions"):
        go("home")
    st.markdown(f"<div class='aivy-kicker'>{m['kicker']}</div>", unsafe_allow_html=True)
    st.markdown(f"## {m['emoji']} {m['title']}")
    for d in m["days"]:
        is_done = d["n"] in done
        with st.container(border=True):
            a, b = st.columns([4, 1])
            with a:
                tick = "✅ " if is_done else ""
                st.markdown(f"{tick}**Day {d['n']} · {d['t']}**  \n"
                            f"<span style='color:#4E6B74;font-size:.85rem'>{d['time']}</span>",
                            unsafe_allow_html=True)
            with b:
                if st.button("Open", key=f"day_{d['n']}", use_container_width=True):
                    go("day", sel_day=d["n"], sel_module=st.session_state.sel_module)

# ----------------------------------------------------------------------
# DAY
# ----------------------------------------------------------------------
def render_day():
    n = st.session_state.sel_day
    d = DAY_BY_N[n]
    m = MODULES[MODULE_OF[n]]
    if st.button("← Back"):
        go("module", sel_module=MODULE_OF[n])

    st.markdown(f"<div class='aivy-kicker'>{m['title']} · Day {n}</div>", unsafe_allow_html=True)
    st.markdown(f"## {d['t']}")
    st.markdown(f"<span class='aivy-badge'>⏱ {d['time']}</span>", unsafe_allow_html=True)

    vid = get_video_id(n)
    if vid:
        st.markdown("**🎬 Watch**")
        st.video(f"https://www.youtube.com/watch?v={vid}")
        st.caption("Grown-ups: a quick preview is a good idea before pressing play.")

    if d["links"]:
        st.markdown("**🧰 Explore & build**")
        link_row(d["links"])

    st.markdown("**✅ Your activity**")
    for i, s in enumerate(d["steps"], 1):
        st.markdown(f"<div class='aivy-step'><b>{i}.</b> {s}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='aivy-connect'>❤️ <b>Doctor connection:</b> {d['c']}</div>",
                unsafe_allow_html=True)

    is_done = n in done
    c1, c2 = st.columns(2)
    with c1:
        if not is_done:
            if st.button("✅ Mark complete", type="primary", use_container_width=True):
                done.add(n); save_state()
                if n < TOTAL:
                    go("day", sel_day=n + 1, sel_module=MODULE_OF[n + 1])
                else:
                    go("day", sel_day=n)
        else:
            if st.button("↩ Mark not done", use_container_width=True):
                done.discard(n); save_state(); st.rerun()
    with c2:
        if n < TOTAL and st.button("Next day →", use_container_width=True):
            go("day", sel_day=n + 1, sel_module=MODULE_OF[n + 1])

    if is_done:
        st.success("Nice work — this day is complete! 🌟")
    if n == TOTAL and count == TOTAL:
        st.balloons()
        st.success("Congratulations, Future Doctor & AI Explorer! You finished all 40 days. 🎉")

# ----------------------------------------------------------------------
# GROWN-UP TOOLS (no login)
# ----------------------------------------------------------------------
def render_grownup_tools():
    with st.expander("🔧 For grown-ups: tools"):
        st.caption("Everything saves on this device / app. No account needed.")

        st.markdown("**Learner's name**")
        nm = st.text_input("Shows a friendly greeting (optional)", value=st.session_state.name,
                           key="name_field", label_visibility="collapsed", placeholder="e.g. Emma")
        if st.button("Save name"):
            st.session_state.name = nm.strip(); save_state(); st.rerun()

        st.divider()
        st.markdown("**Backup & restore progress**")
        st.caption("Download a small file to keep a copy (you can even store it in GitHub). "
                   "Restore it later or on another device.")
        backup = json.dumps({"app": "AIvy", "version": 1,
                             "progress": sorted(done), "name": st.session_state.name,
                             "videos": st.session_state.videos}, indent=2)
        st.download_button("⬇ Download backup", backup, file_name="aivy-backup.json",
                           mime="application/json", use_container_width=True)
        up = st.file_uploader("Restore from a backup file", type="json", key="restore_up")
        if up is not None and st.button("Apply uploaded file"):
            try:
                data = json.load(up)
                st.session_state.progress = set(x for x in data.get("progress", []) if 1 <= x <= 40)
                if isinstance(data.get("videos"), dict):
                    st.session_state.videos = data["videos"]
                if isinstance(data.get("name"), str):
                    st.session_state.name = data["name"]
                save_state(); st.success("Restored ✓"); st.rerun()
            except Exception:
                st.error("That file didn't look right.")

        st.divider()
        st.markdown("**Choose the video for a day**")
        day_sel = st.number_input("Day", min_value=1, max_value=40, value=1, step=1)
        cur_id = get_video_id(int(day_sel)) or ""
        url_in = st.text_input("Paste a YouTube link or video ID", value=cur_id, key="vid_field")
        pid = parse_youtube_id(url_in)
        if url_in.strip():
            if pid:
                st.image(f"https://i.ytimg.com/vi/{pid}/mqdefault.jpg", width=220)
                st.caption(f"Looks good! ID: {pid}")
            else:
                st.warning("Couldn't find a video ID. Paste a full YouTube link or the 11-character ID.")
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("Save video", use_container_width=True, disabled=not pid):
                st.session_state.videos[str(int(day_sel))] = pid; save_state(); st.rerun()
        with b2:
            if st.button("Use default", use_container_width=True):
                st.session_state.videos.pop(str(int(day_sel)), None); save_state(); st.rerun()
        with b3:
            if st.button("Hide video", use_container_width=True):
                st.session_state.videos[str(int(day_sel))] = ""; save_state(); st.rerun()

        st.divider()
        if st.button("🗑 Reset all progress"):
            st.session_state.progress = set(); save_state(); st.rerun()

# ----------------------------------------------------------------------
# ROUTER
# ----------------------------------------------------------------------
view = st.session_state.view
if view == "module":
    render_module()
elif view == "day":
    render_day()
else:
    render_home()
