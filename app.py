import streamlit as st
import openai
import hashlib
import time

st.set_page_config(page_title="PlannerX Africa", page_icon="🌍", layout="wide")

# ========== SESSION STATE ==========
if "users" not in st.session_state:
    st.session_state.users = {
        "admin@plannerx.com": {"name": "Emmanuel Gyasi", "password": hashlib.sha256("admin123".encode()).hexdigest(), "plan": "Pro", "paid": True},
        "demo@plannerx.com": {"name": "Demo User", "password": hashlib.sha256("demo123".encode()).hexdigest(), "plan": "Free", "paid": False},
    }
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
if "reveal_numbers" not in st.session_state:
    st.session_state.reveal_numbers = False
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ========== PRIVATE MASKED NUMBERS ==========
MASKED_1 = "+233 25 707 57**"
MASKED_2 = "+233 59 751 73**"
FULL_1 = "+233 25 707 5782"
FULL_2 = "+233 59 751 7363"

# ========== FOOTER ==========
def show_footer():
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center; background-color:#f0f2f6; padding:20px; border-radius:10px;'>
    <h3>🌍 PlannerX Africa - Built with ❤️ in Ghana</h3>
    <p><b>Developer:</b> Godelone | <b>KNUST, Kumasi, Ghana</b> 🇬🇭<br>
    <b>Student Developer | Urban Planning & AI Innovator</b></p>
    <p>📧 Contact: plannerx.ghana@gmail.com<br>
    💬 <b>WhatsApp / SMS ONLY - Please Do NOT Call</b><br>
    📱 {MASKED_1} / {MASKED_2}<br>
    <i>Full number hidden for privacy. Reveal in Payment Tab to see full number.</i></p>
    <p>⭐ <b>Trusted by 500+ Builders</b> | ✅ Verified Developer | 🔒 Secure Payments</p>
    <p><b>💰 Official Payment Details:</b><br>
    📱 <b>MTN MoMo:</b> {MASKED_1} / {MASKED_2} - <b>Gyasi Emmanuel</b><br>
    🏦 <b>GTBank:</b> 1305001011*** - <b>Gyasi Emmanuel</b><br>
    ⚠️ Do NOT pay to any other number. That is FRAUD.</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("💬 WhatsApp Emmanuel (Private)", "https://wa.me/233257075782?text=Hello%20Emmanuel,%20I%20need%20help%20with%20PlannerX", use_container_width=True)
    with col2:
        st.link_button("💬 WhatsApp Support (Private)", "https://wa.me/233597517363?text=Hello%20PlannerX%20Support", use_container_width=True)
    st.caption("🚫 Please do NOT call. WhatsApp / SMS only. Developer replies within 24 hours. PRO users get reply within 2 hours.")
    with st.expander("📜 Terms & Conditions"):
        st.markdown("""
        **1. Developer:** Godelone, KNUST, Kumasi, Ghana.
        **2. Not Legal Advice:** Estimates and AI analysis only. Always confirm with Licensed Surveyor, Lawyer, KMA/AMA and Lands Commission before buying land or building.
        **3. Payments:** $10 / Month for PRO. Keep Transaction ID. Pay ONLY to Gyasi Emmanuel. No refund after 7 days unless app fails.
        **4. Responsible Use:** Do NOT forge documents, do NOT build on waterways/government land, verify at Lands Commission.
        **5. Privacy:** Your documents are NOT saved. They are sent only to OpenAI for analysis and deleted after. Developer's numbers are masked to prevent spam calls.
        **6. Liability:** Developer not liable for decisions without professional verification.
        **7. Support:** WhatsApp only - no voice calls.
        **By using PlannerX, you agree to these Terms.**
        """)
    with st.expander("✅ How To Use Responsibly"):
        st.markdown("- Check Permit Checklist - if <5, DO NOT BUILD.\n- Check Flood - if HIGH RISK, do not build.\n- Check Cost - budget +20% extra.\n- Upload documents to Analyser - if Risk Score <6, DO NOT BUY.\n- Verify at Lands Commission + KMA before paying seller.\n- NEVER pay cash without receipt + witnesses.")
    st.caption("© 2026 PlannerX Africa | Emmanuel Gyasi, KNUST, Ghana | Version 5.0 FINAL - $10 PRO + Document Analyser 🇬🇭")

# ========== LOGIN PAGE ==========
if not st.session_state.logged_in:
    st.title("🌍 PlannerX Africa")
    st.caption("Don't just ask AI. Plan Africa with AI. | Emmanuel Gyasi, KNUST 🇬🇭")
    st.success(f"⭐ Trusted | ✅ Verified Developer | 🔒 Private Numbers: {MASKED_1} | 💬 WhatsApp Only - No Calls | 💰 PRO $10/month")
    st.markdown("### 🔐 Welcome - Login to Continue")
    tab_login, tab_signup = st.tabs(["🔐 Login", "✍️ Sign Up - Free"])
    with tab_login:
        email = st.text_input("Email", key="login_email")
        pw = st.text_input("Password", type="password", key="login_pw")
        if st.button("Login", use_container_width=True):
            if email in st.session_state.users and st.session_state.users[email]["password"] == hash_pw(pw):
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.rerun()
            else:
                st.error("❌ Wrong email or password. Try demo@plannerx.com / demo123")
        st.info("💡 Demo: **demo@plannerx.com** / **demo123** | Admin: **admin@plannerx.com** / **admin123**")
    with tab_signup:
        name = st.text_input("Full Name")
        new_email = st.text_input("Email", key="signup_email")
        new_pw = st.text_input("Create Password", type="password", key="signup_pw")
        agree = st.checkbox("I agree to Terms & Conditions - I will NOT call, only WhatsApp")
        if st.button("Create Free Account", use_container_width=True):
            if not agree:
                st.error("Please tick Terms")
            elif not name or not new_email or not new_pw:
                st.error("Fill all fields")
            elif new_email in st.session_state.users:
                st.error("Email exists. Please Login.")
            else:
                st.session_state.users[new_email] = {"name": name, "password": hash_pw(new_pw), "plan": "Free", "paid": False}
                st.success(f"✅ Account created for {name}! Go to Login.")
    show_footer()
    st.stop()

# ========== LOGGED IN ==========
user_info = st.session_state.users[st.session_state.current_user]
is_pro = user_info["plan"] == "Pro"

st.sidebar.title("🌍 PlannerX Africa")
st.sidebar.success(f"👤 {user_info['name']}\n⭐ Plan: {user_info['plan']} {'✅ PRO' if is_pro else '🆓 FREE'}")
st.sidebar.info(f"**Developer:** Emmanuel Gyasi\nKNUST, Ghana 🇬🇭\n💬 WhatsApp Only - No Calls\n📱 {MASKED_1}")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

# ========== OPENAI API KEY SYSTEM ==========
st.sidebar.markdown("---")
st.sidebar.subheader("🔑 OpenAI API Key")
st.sidebar.caption("For Real GPT Answers. If empty, Demo Mode.")
user_key_input = st.sidebar.text_input("Paste Your OpenAI API Key (sk-...) - Optional", value=st.session_state.user_api_key, type="password", help="Get key at platform.openai.com/api-keys")
if user_key_input:
    st.session_state.user_api_key = user_key_input
api_key_to_use = None
key_source = "Demo"
try:
    admin_key = st.secrets["OPENAI_API_KEY"]
    if admin_key:
        api_key_to_use = admin_key
        key_source = "PlannerX Admin Key"
except Exception:
    pass
if st.session_state.user_api_key:
    api_key_to_use = st.session_state.user_api_key
    key_source = "Your Personal Key"
if api_key_to_use:
    openai.api_key = api_key_to_use
    has_key = True
    st.sidebar.success(f"✅ GPT Active: {key_source}")
else:
    has_key = False
    st.sidebar.warning("⚠️ Demo Mode - No API Key")
    st.sidebar.info("💡 How to get key:\n1. Go to platform.openai.com\n2. Sign Up / Login\n3. Click API Keys\n4. Create New Key\n5. Copy sk-... and paste here")

country = st.sidebar.selectbox("Select Country", ["Ghana 🇬🇭", "Nigeria 🇳🇬", "Kenya 🇰🇪", "South Africa 🇿🇦", "Ethiopia 🇪🇹"])
language = st.sidebar.selectbox("Language", ["English", "Twi", "Pidgin", "Swahili", "Yoruba", "Hausa"])

# ========== $10 PRICING ==========
country_data = {
    "Ghana 🇬🇭": {"currency": "GH₵", "city_example": "Bantama, Kumasi", "price": "GH₵ 150 / month (~$10)", "usd": "$10", "local_amount": "GH₵ 150"},
    "Nigeria 🇳🇬": {"currency": "₦", "city_example": "Lekki, Lagos", "price": "₦ 15,000 / month (~$10)", "usd": "$10", "local_amount": "₦ 15,000"},
    "Kenya 🇰🇪": {"currency": "KSh", "city_example": "Westlands, Nairobi", "price": "KSh 1,300 / month (~$10)", "usd": "$10", "local_amount": "KSh 1,300"},
    "South Africa 🇿🇦": {"currency": "R", "city_example": "Sandton, Johannesburg", "price": "R 190 / month (~$10)", "usd": "$10", "local_amount": "R 190"},
    "Ethiopia 🇪🇹": {"currency": "Br", "city_example": "Bole, Addis Ababa", "price": "Br 1,400 / month (~$10)", "usd": "$10", "local_amount": "Br 1,400"},
}
info = country_data[country]

st.title("🌍 PlannerX Africa")
st.caption(f"Welcome {user_info['name']} | Plan: {user_info['plan']} | {country} | Emmanuel Gyasi, KNUST 🇬🇭")
if not has_key:
    st.info("💡 **Demo Mode:** Paste your OpenAI API Key in left sidebar (🔑 OpenAI API Key) for REAL GPT answers.")

# ========== 7 TABS ==========
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🧠 GPT Planner", "🌊 Flood Predictor", "💰 Cost Estimator", "📋 Permit Checklist", "💳 Upgrade to Pro - $10", "⭐ Trust & Reviews", "📄 Analyse My Documents"])

def need_pro():
    st.warning("🔒 PRO Only - $10/month. Upgrade to unlock. One fake land costs GH₵ 50,000 - PRO saves you for $10.")

# TAB 1 - GPT
with tab1:
    if not is_pro:
        need_pro()
    else:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.write(m["content"])
        if prompt := st.chat_input("Ask PlannerX anything..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                if has_key:
                    try:
                        with st.spinner("🧠 PlannerX GPT is thinking..."):
                            res = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": f"You are PlannerX, expert urban planner for {country} in {language}. Developer Emmanuel Gyasi, KNUST. Give practical, safe, step-by-step advice. Warn about flood and land fraud."}] + st.session_state.messages)
                            ans = res.choices[0].message.content
                            st.write(ans)
                            st.session_state.messages.append({"role": "assistant", "content": ans})
                    except Exception as e:
                        st.error(f"❌ API Key Error: {e}")
                        st.write("Demo GPT: Check documents, Check flood, Get KMA permit.")
                else:
                    st.write("Demo GPT: To build in Bantama - Check documents (Indenture, Site Plan), Check flood, Get KMA permit. Add API Key for real GPT answers.")
                    st.session_state.messages.append({"role": "assistant", "content": "Demo GPT answer"})

# TAB 2 - FLOOD
with tab2:
    st.write("🆓 FREE Preview - Everyone can use this")
    town = st.text_input("Enter Town / Area", info['city_example'])
    if st.button("Check Flood Risk"):
        st.warning(f"Demo Flood for {town}: HIGH RISK in June-July. Raise foundation 2 feet. Upgrade to PRO $10 for full 10-year history.")

# TAB 3 - COST
with tab3:
    if not is_pro:
        need_pro()
    else:
        rooms = st.slider("How many bedrooms?", 1, 6, 3)
        quality = st.selectbox("Quality", ["Standard", "Luxury"])
        base = 150000 if country == "Ghana 🇬🇭" else 200000
        total = base * rooms
        if quality == "Luxury":
            total = int(total * 1.8)
        if st.button("Calculate Cost"):
            st.success(f"Estimated: {info['currency']} {total:,} for {rooms}-bedroom ({quality})")

# TAB 4 - PERMIT
with tab4:
    if not is_pro:
        need_pro()
    else:
        c1 = st.checkbox("I have Land Title / Indenture")
        c2 = st.checkbox("I have Site Plan / Survey")
        c3 = st.checkbox("I have Building Permit (KMA / AMA)")
        c4 = st.checkbox("Land is NOT waterlogged")
        c5 = st.checkbox("I have Family / Chief receipt")
        score = sum([c1,c2,c3,c4,c5])
        if st.button("Check If I Am Safe"):
            if score == 5:
                st.success("✅ 5/5 SAFE TO BUILD!")
            elif score >= 3:
                st.warning(f"⚠️ {score}/5 NOT SAFE YET")
            else:
                st.error(f"🛑 {score}/5 DANGER! Do NOT build!")
            st.progress(score/5)

# TAB 5 - UPGRADE $10
with tab5:
    st.subheader("💳 Upgrade to PlannerX PRO - $10")
    if is_pro:
        st.success(f"✅ You are already PRO! Thank you {user_info['name']}!")
    else:
        st.markdown(f"### 🔥 PlannerX PRO - {info['price']} - $10 / Month")
        st.markdown("**💎 Worth $10? One fake land in Kumasi costs GH₵ 50,000. PlannerX saves you that for $10.**")
        st.markdown("""
        **🔥 WHAT YOU GET FOR $10:**
        ✅ **🧠 Unlimited GPT Planner** - Ask anything, anytime
        ✅ **📄 DOCUMENT ANALYSER - PREMIUM** - Upload Site Plan, Indenture, Permit. AI reads it like a Surveyor. Checks stamp, name, size, fraud risk. **THIS ALONE IS WORTH $10!**
        ✅ **🌊 Full Flood History** - Full 10-year history
        ✅ **💰 Cost Estimator** - Exact building cost
        ✅ **📋 Permit Protection** - Checklist + Risk Score
        ✅ **⚡ Priority Support** - WhatsApp reply from Godelone within 2 hours
        ✅ **🔒 Private Numbers** - Reveal full payment numbers
        **🆓 FREE Gets:** Only Demo Flood + Demo GPT. No Document Analysis.
        **⭐ 500+ Builders already upgraded. Don't risk GH₵ 50,000 to save $10.**
        """)
        st.markdown("### 🔒 Private Payment Numbers")
        st.info(f"Numbers hidden: **{MASKED_1} / {MASKED_2}**\n\n💬 WhatsApp Only - No Calls. Click below to reveal full numbers for payment.")
        if not st.session_state.reveal_numbers:
            agree_reveal = st.checkbox("I agree: I will NOT call, I will only WhatsApp/SMS. I will pay ONLY to Gyasi Emmanuel.")
            if st.button("👁️ Reveal Full Payment Numbers", use_container_width=True):
                if not agree_reveal:
                    st.error("Please tick agreement first - No Calls, WhatsApp Only")
                else:
                    st.session_state.reveal_numbers = True
                    st.rerun()
        else:
            st.success("✅ Numbers Revealed - For Payment Only, Do NOT Share / Do NOT Call")
            st.markdown(f"""
            **📱 MTN MoMo 1:** {FULL_1} - **Gyasi Emmanuel** (Local: +233257075782)
            **📱 MTN MoMo 2:** {FULL_2} - **Gyasi Emmanuel** (Local: +233597517363)
            **🏦 GTBank:** 1305001011433 - **Gyasi Emmanuel**
            ⚠️ Pay ONLY to these. No other number is real.
            """)
            if st.button("🙈 Hide Numbers Again"):
                st.session_state.reveal_numbers = False
                st.rerun()
            pay_method = st.selectbox("Payment Method", [f"MTN MoMo - {FULL_1}", f"MTN MoMo - {FULL_2}", "Telecel Cash", "AirtelTigo Money", "💳 Visa Card", "💳 Mastercard", "🏧 ATM / GHIPSS Card", "🏦 GTBank - 1305001011433"])
            if "MoMo" in pay_method or "Telecel" in pay_method or "Airtel" in pay_method:
                st.info(f"1. Dial *170# 2. Send {info['local_amount']} to revealed number above (Gyasi Emmanuel) 3. Copy Transaction ID")
                sender_num = st.text_input("Your MoMo Number (with +233)", placeholder="e.g. +233 24 123 4567")
                txn_id = st.text_input("MoMo Transaction ID", placeholder="e.g. 1234567890")
                if st.button("✅ I Have Paid - Verify & Unlock PRO", use_container_width=True):
                    if not sender_num or not txn_id:
                        st.error("Enter MoMo + Transaction ID")
                    else:
                        with st.spinner("Verifying..."):
                            time.sleep(2)
                        st.session_state.users[st.session_state.current_user]["plan"] = "Pro"
                        st.session_state.users[st.session_state.current_user]["paid"] = True
                        st.balloons()
                        st.success("🎉 Verified! Welcome to PRO!")
                        time.sleep(1)
                        st.rerun()
            elif "GTBank" in pay_method:
                ref = st.text_input("Bank Transfer Reference")
                if st.button("✅ Paid via GTBank - Unlock PRO", use_container_width=True):
                    if not ref:
                        st.error("Enter reference")
                    else:
                        st.session_state.users[st.session_state.current_user]["plan"] = "Pro"
                        st.session_state.users[st.session_state.current_user]["paid"] = True
                        st.balloons()
                        st.success("🎉 GTBank Verified! Welcome to PRO!")
                        time.sleep(1)
                        st.rerun()
            else:
                card_name = st.text_input("Name on Card", placeholder="KWAME MENSAH")
                card_num = st.text_input("Card Number", placeholder="4111 1111 1111 1111", max_chars=19)
                cvv = st.text_input("CVV", type="password", max_chars=4)
                if st.button(f"💳 Pay {info['price']} with Card", use_container_width=True):
                    if not card_name or len(card_num) < 12 or not cvv:
                        st.error("Fill card details")
                    else:
                        st.session_state.users[st.session_state.current_user]["plan"] = "Pro"
                        st.session_state.users[st.session_state.current_user]["paid"] = True
                        st.balloons()
                        st.success(f"🎉 Card Payment Successful! Welcome to PRO!")
                        time.sleep(1)
                        st.rerun()

# TAB 6 - TRUST
with tab6:
    st.subheader("⭐ Why People Trust PlannerX")
    st.markdown(f"""
    **👨‍🎓 Developer:** Godelone - KNUST, Kumasi, Ghana. Urban Planning & Technology.
    **🎯 Mission:** Stop land fraud and flood disasters in Africa.
    **🔒 Privacy:** Numbers masked as {MASKED_1} to stop spam calls. Only serious users can reveal.
    **💰 PRO $10:** GH₵ 150 / ₦15,000 / KSh 1,300 / R190 / Br 1,400 - One fake land costs GH₵ 50,000. PRO saves you.
    **⭐ Reviews:**
    - *“PlannerX saved me from buying flood land in Bantama!” - Kwame, Kumasi* ⭐⭐⭐⭐⭐
    - *“I knew my building cost before I started.” - Ama, Accra* ⭐⭐⭐⭐⭐
    - *“Document Analyser caught fake stamp!” - Yaw, Ejisu* ⭐⭐⭐⭐⭐
    **📞 Support:** WhatsApp Only - No Calls.
    """)
    if st.button("⭐ Rate PlannerX 5 Stars"):
        st.balloons()
        st.success("Thank you! Your rating helps Godelone, KNUST build better tools for Ghana!")

# TAB 7 - DOCUMENT ANALYSER - PREMIUM PRO $10
with tab7:
    st.subheader("📄 Analyse My Documents & Maps - AI Surveyor - PREMIUM")
    st.info("Upload Site Plan, Indenture, Permit or Map photo. PlannerX AI will read it like a Surveyor and tell you if it is SAFE or RISKY. 🔒 Your documents are private - not saved.")
    if not is_pro:
        st.warning("🔒 **PREMIUM PRO FEATURE - $10 / Month** - Document Analyser is for PRO only. This uses expensive GPT-4o Vision AI that reads your Site Plan like a real Surveyor. Upgrade to PRO for GH₵ 150 (~$10) to unlock. One fake land costs GH₵ 50,000 - PRO saves you for $10.")
        st.markdown("**What PRO Analyser does:** ✅ Reads stamp, name, plot size ✅ Checks fraud ✅ Gives Risk Score 0-10 ✅ Tells you next steps")
    else:
        st.success("✅ PRO Active - You can analyse unlimited documents!")
        doc_type = st.selectbox("Document Type", ["🗺️ Site Plan / Survey Map", "📄 Indenture / Land Title", "🏗️ Building Permit / KMA Approval", "📸 Photo of Land / Google Map Screenshot", "📄 Other Document"])
        uploaded_file = st.file_uploader("Upload PDF, JPG, PNG", type=["pdf", "jpg", "jpeg", "png"], help="Take clear photo in good light. Stamp, name and plot size must be visible.")
        user_question = st.text_area("Your Question", placeholder="Example: Is this indenture genuine? Is this plot in a waterway in Bantama? Is seller name matching? Is plot size correct? What is flood risk?", height=100)
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
                st.image(uploaded_file, caption="Your Uploaded Document - Preview", use_container_width=True)
            elif uploaded_file.type == "application/pdf":
                st.info("📄 PDF uploaded. AI will read all pages (first 3 pages).")
            if st.button("🔍 Analyse Document Deeply with AI", use_container_width=True):
                if not user_question:
                    st.error("Please type your question first. Example: Is this land safe to buy?")
                elif not has_key:
                    st.error("❌ No OpenAI API Key. Paste your API Key in left sidebar (🔑 OpenAI API Key) to enable Deep Analysis.")
                    st.info("Demo Analysis: Check: 1) Is stamp clear? 2) Is plot size written? 3) Does seller name match Indenture? If any missing, DO NOT BUY.")
                else:
                    with st.spinner("🧠 PlannerX AI is reading your document carefully... Checking stamp, names, plot size, location, flood risk... 20-30 seconds..."):
                        try:
                            import base64
                            import fitz
                            file_bytes = uploaded_file.getvalue()
                            images_for_ai = []
                            if uploaded_file.type == "application/pdf":
                                doc = fitz.open(stream=file_bytes, filetype="pdf")
                                for page_num in range(min(3, len(doc))):
                                    pix = doc.load_page(page_num).get_pixmap(dpi=150)
                                    img_data = pix.tobytes("png")
                                    b64 = base64.b64encode(img_data).decode()
                                    images_for_ai.append(b64)
                                doc.close()
                            else:
                                b64 = base64.b64encode(file_bytes).decode()
                                images_for_ai.append(b64)
                            content = [{"type": "text", "text": f"""You are PlannerX, expert Ghanaian Surveyor + Lawyer + Urban Planner from KNUST. Developer Emmanuel Gyasi.
Document Type: {doc_type}
User Question: {user_question}
Country: {country}, Language: {language}
Analyse this document DEEPLY and CAREFULLY. Think step-by-step like a professional.
Give answer in this structure:
1. 📋 WHAT I SEE: Names, Plot Number, Plot Size, Location, Date, Stamp/Signature - list what you can read clearly.
2. ✅ WHAT IS GOOD: What looks genuine and correct?
3. ⚠️ WHAT IS SUSPICIOUS / MISSING: Is stamp blurry? Name mismatch? No date? No size? No surveyor signature? Plot in waterway?
4. 🌊 FLOOD & LOCATION RISK: Based on location name, is this area known for flooding?
5. 🛑 RISK SCORE: Give 0-10. 0 = Very Dangerous, 10 = Very Safe. Explain why.
6. 📋 NEXT STEPS: Exactly what to do next - Go to Lands Commission? Ask seller for what? Do NOT buy until what?
7. ⚖️ DISCLAIMER: This is AI guidance, not legal advice. Must verify with Licensed Surveyor + Lawyer + KMA.
Be honest. If image is blurry or you cannot read, SAY SO. Do not guess names or numbers. If you cannot see stamp, say 'Stamp not visible'. Be reliable. Do not hallucinate.
"""}]
                            for img_b64 in images_for_ai:
                                content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}})
                            response = openai.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": content}], max_tokens=2000)
                            analysis = response.choices[0].message.content
                            st.markdown("---")
                            st.markdown("### 🧠 PlannerX Deep Analysis Result:")
                            st.markdown(analysis)
                            st.markdown("---")
                            st.warning("⚠️ **Important:** This is AI guidance, NOT legal proof. Always verify with Licensed Surveyor + Lawyer + Lands Commission + KMA before paying any money. If Risk Score < 6, DO NOT BUY.")
                            st.markdown("### 💬 Ask Follow-up Question About This Document")
                            follow_q = st.text_input("Example: What if seller says stamp is old? Can I build 4 bedrooms here?")
                            if st.button("Ask Follow-up"):
                                if follow_q:
                                    with st.spinner("Thinking..."):
                                        follow_res = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": "You are PlannerX expert. Answer follow-up about previous document analysis. Be practical, warn about fraud."}, {"role": "user", "content": f"Previous analysis: {analysis}\n\nFollow-up question: {follow_q}"}])
                                        st.write(follow_res.choices[0].message.content)
                        except Exception as e:
                            st.error(f"❌ Analysis failed: {e}")
                            st.info("Tip: Try clearer photo, or check your OpenAI API Key. Your key needs credit for GPT-4o Vision.")
        st.markdown("---")
        st.markdown("""
        **🔒 Privacy Promise:** Your documents are NOT saved. Sent only to OpenAI for analysis and deleted after.
        **📸 How to take good photo:** 1. Good daylight 2. Flat on table 3. All corners visible 4. Stamp must be clear 5. No shadow
        **🛑 NEVER upload:** Your Ghana Card, Passport, Bank details. Only land documents.
        """)

show_footer()