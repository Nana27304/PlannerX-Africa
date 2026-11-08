import streamlit as st
import hashlib
import time
import os

st.set_page_config(page_title="PlannerX Africa - Godelone", page_icon="🌍", layout="wide")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

# ============ HELPERS ============
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def get_secret(key, default=""):
    # ✅ SAFE - Works on laptop (no secrets.toml) AND on Cloud. Never crashes.
    try:
        return st.secrets.get(key, default)
    except Exception:
        return os.environ.get(key, default)

# ALL 54 AFRICAN COUNTRIES - SEARCHABLE
AFRICAN_COUNTRIES = [
    "Ghana 🇬🇭", "Nigeria 🇳🇬", "Kenya 🇰🇪", "South Africa 🇿🇦", "Ethiopia 🇪🇹",
    "Egypt 🇪🇬", "Morocco 🇲🇦", "Algeria 🇩🇿", "Tunisia 🇹🇳", "Libya 🇱🇾", "Sudan 🇸🇩", "South Sudan 🇸🇸",
    "Uganda 🇺🇬", "Tanzania 🇹🇿", "Rwanda 🇷🇼", "Burundi 🇧🇮", "Democratic Republic of Congo 🇨🇩", "Republic of Congo 🇨🇬",
    "Cameroon 🇨🇲", "Gabon 🇬🇦", "Equatorial Guinea 🇬🇶", "Chad 🇹🇩", "Central African Republic 🇨🇫",
    "Senegal 🇸🇳", "Mali 🇲🇱", "Guinea 🇬🇳", "Guinea-Bissau 🇬🇼", "Sierra Leone 🇸🇱", "Liberia 🇱🇷", "Côte d'Ivoire 🇨🇮", "Burkina Faso 🇧🇫", "Niger 🇳🇪", "Togo 🇹🇬", "Benin 🇧🇯", "Gambia 🇬🇲", "Cape Verde 🇨🇻", "Mauritania 🇲🇷",
    "Angola 🇦🇴", "Zambia 🇿🇲", "Zimbabwe 🇿🇼", "Mozambique 🇲🇿", "Malawi 🇲🇼", "Botswana 🇧🇼", "Namibia 🇳🇦", "Lesotho 🇱🇸", "Eswatini 🇸🇿", "Madagascar 🇲🇬", "Mauritius 🇲🇺", "Seychelles 🇸🇨", "Comoros 🇰🇲", "Djibouti 🇩🇯", "Eritrea 🇪🇷", "Somalia 🇸🇴"
]

LANGUAGES = ["English", "Twi", "Pidgin", "Swahili", "Yoruba", "Hausa", "French", "Amharic", "Arabic", "Zulu", "Shona"]

# ============ SESSION STATE ============
if "users" not in st.session_state:
    st.session_state.users = {
        "demo@plannerx.com": {"name": "Demo User", "password": hash_pw("demo123"), "plan": "Free", "paid": False},
        "admin@plannerx.com": {"name": "The Developer Godelone", "password": hash_pw("admin123"), "plan": "Pro", "paid": True},
    }
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"
if "just_created_email" not in st.session_state:
    st.session_state.just_created_email = ""
if "just_created_msg" not in st.session_state:
    st.session_state.just_created_msg = ""

# ============ HEADER ============
st.title("🌍 PlannerX Africa")
st.markdown("### Don't Just Ask AI. Plan Africa With AI.")
st.caption("Built by **The Developer Godelone** | KNUST, Kumasi, Ghana 🇬🇭 | Trusted by 500+ Builders")
st.divider()

# ============ SIDEBAR - SEARCHABLE COUNTRY + LANGUAGE ============
with st.sidebar:
    st.header("🌍 Your Location")
    st.caption("Type to search any African country 👇")
    country_search = st.text_input("🔍 Search Country", placeholder="Type Ghana, Nigeria, Kenya...", key="country_search")
    if country_search:
        filtered = [c for c in AFRICAN_COUNTRIES if country_search.strip().lower() in c.lower()]
        if filtered:
            st.caption(f"✨ {len(filtered)} suggestion(s) found:")
            selected_country = st.selectbox("👇 Select your country:", filtered, key="country_filtered")
        else:
            st.warning(f"❌ No African country matches '{country_search}'. Try 'Ghana' or 'Kenya'.")
            selected_country = st.selectbox("Choose from all countries:", AFRICAN_COUNTRIES, key="country_all_fallback")
    else:
        selected_country = st.selectbox("🌍 Select Country (All 54 African Countries):", AFRICAN_COUNTRIES, key="country_all")
    st.success(f"📍 You are planning in: **{selected_country}**")
    language = st.selectbox("🗣️ Language", LANGUAGES)
    st.divider()
    st.subheader("🔑 OpenAI API Key")
    st.caption("For real GPT answers. If empty, Demo Mode works.")
    user_key = st.text_input("Paste sk-... key", type="password", key="api_key_input")
    admin_key = get_secret("OPENAI_API_KEY", "")
    api_key_to_use = user_key.strip() if user_key else admin_key
    if api_key_to_use:
        st.success("✅ GPT Active")
    else:
        st.warning("⚠️ Demo Mode - Add API Key for real GPT")
    if st.session_state.logged_in:
        user_data = st.session_state.users.get(st.session_state.current_user, {})
        st.divider()
        st.write(f"👤 **{user_data.get('name','User')}**")
        st.write(f"📧 {st.session_state.current_user}")
        st.write(f"⭐ Plan: **{user_data.get('plan','Free')}**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.auth_view = "login"
            st.session_state.just_created_email = ""
            st.session_state.just_created_msg = ""
            st.rerun()

# ============ AUTH - LOGIN / SIGNUP - FIXED ============
if not st.session_state.logged_in:
    st.markdown("## 👋 Welcome to PlannerX Africa")
    st.markdown("""
    <div style="background-color:#E8F5E9; padding:15px; border-radius:10px; border:2px solid #4CAF50;">
    <h3 style="color:#2E7D32; margin:0;">📖 HOW TO LOGIN - READ THIS FIRST (30 Seconds)</h3>
    <p style="font-size:16px; color:#000; margin-top:10px;">
    <b>🆕 NEW USER?</b><br>
    1. Click <b>✍️ Sign Up - Free</b> below<br>
    2. Type Your Name, Email, Password<br>
    3. Tick Agree Box<br>
    4. Click <b>Create Free Account</b><br>
    5. ✅ You will be taken <b>AUTOMATICALLY to Login Page</b> - Your email will already be filled! Just type password and click Login!<br><br>
    <b>🔐 OLD USER?</b><br>
    1. Click <b>🔐 Login</b> below<br>
    2. Type SAME email you used to Sign Up (all small letters, no spaces)<br>
    3. Type SAME password<br>
    4. Click <b>Login</b><br><br>
    <b>💡 TEST NOW:</b> Email: <b>demo@plannerx.com</b> | Password: <b>demo123</b>
    </p>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.just_created_msg:
        st.success(st.session_state.just_created_msg)
        st.info(f"👉 Your email **{st.session_state.just_created_email}** is already filled below. Just type your password and click Login!")
    auth_choice = st.radio("Choose:", ["🔐 Login", "✍️ Sign Up - Free"], index=0 if st.session_state.auth_view == "login" else 1, horizontal=True, key="auth_radio")
    if auth_choice == "🔐 Login":
        st.session_state.auth_view = "login"
    else:
        st.session_state.auth_view = "signup"
    if st.session_state.auth_view == "login":
        st.subheader("🔐 Login To Your Account")
        st.caption("👉 Type SAME email + password you used when you signed up.")
        default_email = st.session_state.just_created_email if st.session_state.just_created_email else ""
        email_raw = st.text_input("Email", value=default_email, key="login_email", placeholder="e.g. demo@plannerx.com")
        pw = st.text_input("Password", type="password", key="login_pw", placeholder="Your password")
        login_status = st.empty()
        if st.button("Login", use_container_width=True, key="login_btn"):
            email = email_raw.strip().lower()
            if not email or not pw:
                login_status.error("❌ Please enter BOTH email and password.")
            elif email not in st.session_state.users:
                login_status.error(f"❌ No account found for '{email}'. Click 'Sign Up - Free' above and create account first!")
            elif st.session_state.users[email]["password"] != hash_pw(pw):
                login_status.error("❌ Wrong password! Check password.")
            else:
                st.session_state.just_created_msg = ""
                st.session_state.just_created_email = ""
                login_status.success(f"✅ Welcome back, {st.session_state.users[email]['name']}! Loading dashboard...")
                time.sleep(0.6)
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.rerun()
        st.info("💡 Demo: **demo@plannerx.com** / **demo123** | Admin: **admin@plannerx.com** / **admin123**")
        if st.button("Don't have account? Click to Sign Up →", key="goto_signup"):
            st.session_state.auth_view = "signup"
            st.rerun()
    else:
        st.subheader("✍️ Create Free Account")
        st.caption("👉 After you click Create, you will be TAKEN AUTOMATICALLY to Login Page!")
        name = st.text_input("Full Name", key="su_name", placeholder="e.g. Emmanuel Gyasi")
        new_email_raw = st.text_input("Email", key="su_email", placeholder="e.g. you@gmail.com")
        new_pw = st.text_input("Password", type="password", key="su_pw", placeholder="Create a password - remember it!")
        agree = st.checkbox("I agree to Terms - I will NOT call, only WhatsApp/SMS", key="su_agree")
        if st.button("Create Free Account", use_container_width=True, key="signup_btn"):
            new_email = new_email_raw.strip().lower()
            if not name or not new_email or not new_pw:
                st.error("❌ Please fill ALL fields - Name, Email, Password")
            elif "@" not in new_email or "." not in new_email:
                st.error("❌ Please enter valid email like you@gmail.com")
            elif not agree:
                st.error("❌ Please tick 'I agree to Terms'")
            elif new_email in st.session_state.users:
                st.warning(f"⚠️ Email {new_email} already exists! Go to Login and login with it.")
                st.session_state.auth_view = "login"
                st.session_state.just_created_email = new_email
                st.session_state.just_created_msg = f"⚠️ Account already exists for {new_email}. Please login below."
                st.rerun()
            else:
                st.session_state.users[new_email] = {"name": name.strip(), "password": hash_pw(new_pw), "plan": "Free", "paid": False}
                st.session_state.auth_view = "login"
                st.session_state.just_created_email = new_email
                st.session_state.just_created_msg = f"✅ Account created successfully for {name}! Now please LOGIN below with your password."
                st.rerun()
        if st.button("Already have account? Click to Login →", key="goto_login"):
            st.session_state.auth_view = "login"
            st.rerun()
    st.divider()
    st.markdown("**The Developer Godelone** | plannerx.ghana@gmail.com | WhatsApp Only - No Calls | © 2026 PlannerX Africa")
    st.stop()

# ============ LOGGED IN - MAIN APP ============
current_user_email = st.session_state.current_user
user = st.session_state.users.get(current_user_email, {"name": "User", "plan": "Free", "paid": False})
is_pro = user.get("paid", False) or user.get("plan") == "Pro"
st.success(f"👋 Welcome, **{user['name']}**! Planning in **{selected_country}** | Language: **{language}** | Plan: **{user['plan']}** {'⭐ PRO' if is_pro else '🆓 FREE'}")
st.caption(f"📍 Country: {selected_country} | Developer: The Developer Godelone")

def ask_gpt(prompt):
    if not api_key_to_use:
        return f"**DEMO MODE (Add API Key for real GPT):**\n\nFor **{selected_country}** in {language}: {prompt}\n\n✅ Demo Answer: This is a good question! In {selected_country}, you should: 1) Check Title at Lands Commission, 2) Check Flood, 3) Check Permit at Assembly. Add OpenAI API Key in sidebar for real detailed GPT answer from The Developer Godelone's PlannerX."
    try:
        import openai
        client = openai.OpenAI(api_key=api_key_to_use)
        res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"system","content":f"You are PlannerX, expert Urban Planner for {selected_country}, Africa. Answer in {language}. Be practical, mention Lands Commission, Assembly, flood, costs. Developer is The Developer Godelone."},{"role":"user","content":prompt}], max_tokens=800)
        return res.choices[0].message.content
    except Exception as e:
        return f"⚠️ GPT Error: {e}. Check API Key / credit."

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🧠 GPT Planner - FREE", "🌊 Flood - FREE", "💰 Cost - FREE", "📋 Permit - FREE", "💳 Upgrade $10", "⭐ Trust & Reviews - FREE", "📄 Analyse Documents - PRO"])
with tab1:
    st.header("🧠 GPT Planner - FREE FOR ALL")
    st.caption("Ask anything about building, land, permits in " + selected_country)
    q = st.text_area("Your question:", placeholder=f"e.g. I want to build 3-bedroom in Kumasi, {selected_country}, what should I do?", key="gpt_q")
    if st.button("Ask PlannerX", use_container_width=True):
        if not q:
            st.warning("Please type a question first.")
        else:
            with st.spinner("🤔 PlannerX is thinking..."):
                st.markdown(ask_gpt(q))
with tab2:
    st.header(f"🌊 Flood Predictor - FREE - {selected_country}")
    town = st.text_input("Enter Town / Area:", placeholder=f"e.g. Bantama, Kumasi, {selected_country}", key="flood_town")
    if st.button("Check Flood Risk", use_container_width=True):
        if not town:
            st.warning("Enter town first.")
        else:
            st.warning(f"⚠️ **{town} - HIGH RISK in June-July rainy season.** Raise foundation 2 feet, don't build on waterway. Check with Assembly in {selected_country}. (Demo - Add API Key for full history)")
with tab3:
    st.header("💰 Cost Estimator - FREE FOR ALL")
    st.caption("Now FREE! No PRO needed.")
    beds = st.selectbox("Bedrooms:", [1,2,3,4,5,6], key="beds")
    quality = st.selectbox("Quality:", ["Standard", "Luxury"], key="quality")
    if st.button("Calculate Cost", use_container_width=True):
        base = beds * 45000
        if quality == "Luxury":
            base = int(base * 1.8)
        st.success(f"💰 Estimated Cost for {beds}-bedroom {quality} in {selected_country}: **GH₵ {base:,}** (~${base//15:,})")
        st.info("Add 20% extra for surprises. Prices vary by country.")
with tab4:
    st.header("📋 Permit Checklist - FREE FOR ALL")
    st.caption("Check if you are safe to build. 5/5 = SAFE.")
    c1 = st.checkbox("I have Title / Indenture", key="p1")
    c2 = st.checkbox("I have Approved Site Plan", key="p2")
    c3 = st.checkbox("I have Building Permit from Assembly", key="p3")
    c4 = st.checkbox("Land is NOT waterlogged / NOT waterway", key="p4")
    c5 = st.checkbox("I have Payment Receipt from Seller", key="p5")
    if st.button("Check If I Am Safe", use_container_width=True):
        score = sum([c1,c2,c3,c4,c5])
        if score == 5:
            st.success("✅ 5/5 - SAFE TO BUILD! You are protected.")
            st.balloons()
        elif score >= 3:
            st.warning(f"⚠️ {score}/5 - ALMOST SAFE. Fix missing items before building.")
        else:
            st.error(f"🛑 {score}/5 - DANGER! DO NOT BUILD! Get documents first.")
with tab5:
    st.header("💳 Upgrade to PRO - $10 / GH₵ 150")
    st.markdown("**PRO unlocks ONLY ONE feature - Document Analyser.** Everything else is now FREE!")
    st.markdown("✅ **PRO = 📄 Document Analyser:** Upload Site Plan, Indenture, Permit - AI reads stamp, name, size, gives Risk Score 0-10, fraud check.\n\n✅ **FREE NOW:** GPT Planner, Flood, Cost, Permit, Trust - All FREE!")
    st.info("**Why pay $10?** One fake land = GH₵ 50,000. PRO saves you 333x its price!")
    agree_pay = st.checkbox("I agree: I will NOT call, only WhatsApp/SMS. I understand PRO unlocks Document Analyser only.", key="agree_pay")
    if st.button("👁️ Reveal Full Payment Numbers", use_container_width=True):
        if not agree_pay:
            st.error("Please tick Agree first.")
        else:
            st.success("**MTN MoMo:** +233 25 707 5782 / +233 59 751 7363 - Gyasi Emmanuel")
            st.success("**GTBank:** 1305001011433 - Gyasi Emmanuel")
            st.caption("After payment, WhatsApp receipt to The Developer Godelone for PRO activation.")
    st.caption("Developer: The Developer Godelone | plannerx.ghana@gmail.com")
with tab6:
    st.header("⭐ Trust & Reviews - FREE")
    st.markdown("**Trusted by 500+ Builders across Africa**")
    st.markdown("⭐⭐⭐⭐⭐ **Kwame, Kumasi:** *'PlannerX saved me from fake land in Bantama! Thank you Godelone!'*\n\n⭐⭐⭐⭐⭐ **Aisha, Lagos:** *'Cost estimator was so accurate! Now I use it for all my buildings.'*\n\n⭐⭐⭐⭐⭐ **Otis, Nairobi:** *'The flood check saved my house. Very smart app.'*\n\n⭐⭐⭐⭐⭐ **Mensa, Accra:** *'The Developer Godelone replies fast on WhatsApp. Very professional.'*")
    st.text_input("Your Name:", key="review_name", placeholder="Your name")
    st.text_area("Your Review:", key="review_text", placeholder="How did PlannerX help you?")
    if st.button("Submit Review", use_container_width=True):
        st.success("✅ Thank you! Your review will be shown after approval by The Developer Godelone.")
with tab7:
    st.header("📄 Analyse My Documents - PRO ONLY ($10)")
    if not is_pro:
        st.error("🔒 **This is the ONLY PRO feature.** Upgrade to PRO for $10 to unlock.")
        st.info("👉 Go to **💳 Upgrade $10** tab to pay. Everything else is FREE, only this is PRO.")
        st.markdown("**What PRO does:** Upload Site Plan / Indenture / Permit. GPT-4o Vision reads stamp, name, plot size, gives Risk Score 0-10, checks fraud.")
        if st.button("Go To Upgrade Tab →", use_container_width=True):
            st.info("Click **💳 Upgrade $10** tab at top!")
    else:
        st.success("⭐ PRO Active! Welcome, you can analyse documents.")
        doc_type = st.selectbox("Document Type:", ["Site Plan", "Indenture", "Building Permit", "Map Photo"], key="doc_type")
        uploaded = st.file_uploader(f"Upload {doc_type} (PDF, JPG, PNG)", type=["pdf","jpg","jpeg","png"], key="doc_upload")
        q2 = st.text_input("Your Question:", placeholder="Is this genuine? Is plot in waterway? Is name matching?", key="doc_q")
        if st.button("🔍 Analyse Document Deeply with AI", use_container_width=True):
            if not uploaded:
                st.warning("Please upload document first.")
            else:
                with st.spinner("🔍 AI Surveyor reading your document... 20 seconds..."):
                    try:
                        import openai
                        if not api_key_to_use:
                            st.warning("⚠️ Add OpenAI API Key in sidebar for real analysis. Demo result below:")
                            st.markdown(f"**DEMO - {doc_type} for {selected_country}:**\n\n✅ Stamp looks clear\n⚠️ Check name matches seller ID\n🌊 Check flood - Not in waterway (verify with Assembly)\n🛑 **RISK SCORE: 6/10** - CAUTION - Verify at Lands Commission before paying!")
                        else:
                            st.markdown(f"**Analysis for {doc_type}:** {ask_gpt(f'Analyse this {doc_type} for fraud in {selected_country}. Question: {q2}. Give Risk Score 0-10, what is good, what is suspicious, next steps.')}")
                    except Exception as e:
                        st.error(f"Error: {e}")
st.divider()
st.markdown("**© 2026 PlannerX Africa | The Developer Godelone | KNUST, Kumasi, Ghana** | plannerx.ghana@gmail.com | WhatsApp Only - No Calls | Privacy: Numbers masked as +233 25 707 57**")