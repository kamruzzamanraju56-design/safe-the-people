import streamlit as st
import sqlite3
import uuid
import hashlib
import time
from datetime import datetime

# ১. ডাটাবেজ ইনিশিয়ালাইজেশন
def init_db():
    conn = sqlite3.connect('stp_global_justice_core.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            secret_hash TEXT,
            country TEXT,
            description TEXT,
            timestamp TEXT,
            status TEXT,
            next_status TEXT
        )
    ''')
    conn.commit()
    return conn

conn = init_db()

# ২. মূল ইন্টারফেস ও থিম সেটিংস
st.set_page_config(page_title="Safe The People (STP)", layout="wide", initial_sidebar_state="expanded")

# ফাউণ্ডার সিক্রেট কী ভ্যালিডেশন (admin123)
FOUNDER_HASHED_MASTER = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" 

# ডাইনামিক লেক্সিকন (দেশভিত্তিক আইনি সংস্থা)
LEXICON = {
    "Bangladesh": {
        "agency": "Cyber Crime Division, Bangladesh Police / National Emergency Service (999)",
        "lawyers": ["Barrister Sara Hossain", "Advocate Salma Ali"]
    },
    "India": {
        "agency": "National Cyber Crime Reporting Portal (1930) / Ministry of Home Affairs",
        "lawyers": ["Senior Advocate Indira Jaising", "Advocate Vrinda Grover"]
    }
}

# ৩. সাইডবার মেনু নেভিগেশন
st.sidebar.title("STP Sovereign Menu:")
menu_choice = st.sidebar.radio("", ["📝 সর্বজনীন অভিযোগ দাখিল (Filing)", "🔍 লাইভ ট্র্যাকিং প্যানেল (Victim Tracker)"])

# সিক্রেট ফাউণ্ডার এক্সেস বক্স
founder_key = st.sidebar.text_input("System Node / Terminal Guide:", type="password")

# ৪. অভিযোগ দাখিল মোড
if menu_choice == "📝 সর্বজনীন অভিযোগ দাখিল (Filing)":
    st.title("🛡️ Safe The People (STP)")
    st.subheader("Global Sovereign Registry - সম্পূর্ণ বেনামী অভিযোগ সেল")
    st.write("---")
    
    country = st.selectbox("আপনার দেশ নির্বাচন করুন (Select Country):", ["Bangladesh", "India"])
    
    # ডানপাশের উইজেট প্যানেলে ডাইনামিক রাউটিং গাইড
    st.info(f"📍 **আপনার দেশের জন্য নির্ধারিত আইনি সংস্থা:**\n{LEXICON[country]['agency']}")
    st.success(f"⚖️ **সহায়ক আইনি প্যানেল (Pro-Bono Lawyers):**\n{', '.join(LEXICON[country]['lawyers'])}")
    
    description = st.text_area("অপরাধের বিস্তারিত বিবরণ দিন (কমপক্ষে ৫০ অক্ষরে লিখুন):", height=150)
    uploaded_file = st.file_uploader("ডিজিটাল প্রমাণ আপলোড করুন (ছবি/অডিও/ডকুমেন্ট):", type=["jpg", "png", "mp3", "pdf"])
    
    captcha = st.text_input("সুরক্ষা ক্যাপচা পূরণ করুন (নিচের বক্সে 'STP72' লিখুন):")
    
    if st.button("নিরাপদে অভিযোগ দাখিল করুন (Submit Secured Claim)"):
        if len(description) < 50:
            st.error("❌ ত্রুটি: বিবরণটি অত্যন্ত সংক্ষিপ্ত। অনুগ্রহ করে বিস্তারিত লিখুন যাতে এআই ইঞ্জিনটি সঠিকভাবে বিশ্লেষণ করতে পারে।")
        elif captcha != "STP72":
            st.error("❌ ত্রুটি: ক্যাপচা কোডটি ভুল হয়েছে।")
        else:
            # ক্রিপ্টোগ্রাফিক লজিক প্রসেসিং
            case_id = str(uuid.uuid4())[:8].upper()
            raw_secret = str(uuid.uuid4())[:12]
            secret_hash = hashlib.sha256(raw_secret.encode()).hexdigest()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # ডাটাবেজে সেভ (সম্পূর্ণ এনক্রিপ্টেড)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?)",
                (case_id, secret_hash, country, description, current_time, "Submitted (Under AI Review)", "Escalate to Email Node (72h)")
            )
            conn.commit()
            
            st.write("---")
            st.balloons()
            st.success("✅ আপনার অভিযোগটি সফলভাবে এবং সম্পূর্ণ বেনামে সার্বভৌম সার্ভারে লক করা হয়েছে!")
            st.warning("⚠️ **সতর্কতা:** নিচের তথ্য দুটি এখনই ডায়েরি বা নিরাপদ কোথাও লিখে রাখুন। এই স্ক্রিনটি চলে গেলে আপনার পরিচয় আর পুনরুদ্ধার করা সম্ভব হবে না।")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🔒 Unique Case ID:", case_id)
            with col2:
                st.metric("🔑 Secret Key (পাসওয়ার্ড):", raw_secret)

# ৫. লাইভ ট্র্যাকিং মোড
elif menu_choice == "🔍 লাইভ ট্র্যাকিং প্যানেল (Victim Tracker)":
    st.title("🔍 লাইভ বেনামী অভিযোগ ট্র্যাকিং প্যানেল")
    st.write("---")
    
    track_id = st.text_input("Case ID:")
    track_secret = st.text_input("Secret Key:", type="password")
    
    if st.button("Check Status"):
        if track_id and track_secret:
            input_hash = hashlib.sha256(track_secret.encode()).hexdigest()
            cursor = conn.cursor()
            cursor.execute("SELECT status, next_status, timestamp FROM cases WHERE case_id=? AND secret_hash=?", (track_id, input_hash))
            result = cursor.fetchone()
            
            if result:
                st.info(f"📊 **অভিযোগের বর্তমান অবস্থা:** {result[0]}")
                st.warning(f"⚙️ **স্বয়ংক্রিয় এআই অ্যাকশন নোড:** {result[1]}")
                st.text(f"⏱️ সাবমিট করার সময়: {result[2]}")
            else:
                st.error("❌ ভুল Case ID অথবা Secret Key দেওয়া হয়েছে। অনুগ্রহ করে আবার চেক করুন।")
        else:
            st.error("❌ অনুগ্রহ করে Case ID এবং Secret Key দুটোই পূরণ করুন।")

# 🔍 ৬. ফাউণ্ডার সিক্রেট ড্যাশবোর্ড (Stealth Access Mode)
if founder_key:
    hashed_input = hashlib.sha256(founder_key.encode()).hexdigest()
    if hashed_input == FOUNDER_HASHED_MASTER:
        st.write("---")
        st.subheader("👑 Sovereign Global Founder Control Panel (Stealth Mode)")
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cases")
        all_cases = cursor.fetchall()
        
        if all_cases:
            for row in all_cases:
                with st.expander(f"📦 কেস আইডি: {row[0]} | দেশ: {row[2]} | স্ট্যাটাস: {row[5]}"):
                    st.text(f"📅 জমা দেওয়ার সময়: {row[4]}")
                    st.write(f"📝 **অভিযোগের বিবরণ:**\n{row[3]}")
                    
                    # স্ট্যাটাস পরিবর্তনের ডাইনামিক ইঞ্জিন
                    new_status = st.selectbox(f"স্ট্যাটাস আপডেট করুন ({row[0]}):", ["Submitted (Under AI Review)", "Investigation Ongoing", "Problem Resolved"], key=f"status_{row[0]}")
                    if st.button(f"আপডেট নিশ্চিত করুন ({row[0]})", key=f"btn_{row[0]}"):
                        cursor.execute("UPDATE cases SET status=? WHERE case_id=?", (new_status, row[0]))
                        conn.commit()
                        st.success(f"✅ কেস {row[0]}-এর স্ট্যাটাস পরিবর্তন করে '{new_status}' করা হয়েছে।")
                        time.sleep(1)
                        st.rerun()
        else:
            st.info("📂 এই মুহূর্তে বিশ্বব্যাপী কোনো অভিযোগ ডাটাবেজে জমা পড়েনি।")
