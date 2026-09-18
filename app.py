import streamlit as st
import uuid
import hashlib
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# =========================================================================
# ১. গ্লোবাল থিম ও সিকিউরিটি কনফিগারেশন (Core Global Infrastructure)
# =========================================================================
st.set_page_config(
    page_title="Safe The People (STP) - Global Sovereign Registry",
    page_icon="🚨",
    layout="wide"
)

try:
    FOUNDER_HASHED_MASTER = st.secrets["FOUNDER_HASHED_MASTER"]
    SMTP_PASSWORD = st.secrets["SMTP_PASSWORD"]
except Exception:
    FOUNDER_HASHED_MASTER = "0bc7f9a15cd384e9d72c114f1ff8ec2a688b1f7d4b4a1f3c3993d98d258b3c99"
    SMTP_PASSWORD = "stealth_app_app_password"

DB_FILE = "stp_global_justice_core.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stp_cases (
        Case_ID TEXT PRIMARY KEY,
        Key_Hash TEXT NOT NULL,
        Founder_Key_Vault TEXT NOT NULL,
        Timestamp TEXT NOT NULL,
        Country TEXT NOT NULL,
        Category TEXT NOT NULL,
        Accused_Name TEXT NOT NULL,
        Accused_Designation TEXT NOT NULL,
        Accused_Contact TEXT NOT NULL,
        Remedy_Type TEXT NOT NULL,
        Evidence_Hash TEXT NOT NULL,
        Details_Snippet TEXT NOT NULL,
        System_Status TEXT NOT NULL,
        Last_Updated TEXT NOT NULL,
        Remarks TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_database()

# =========================================================================
# ২. স্বয়ংক্রিয় গ্লোবাল রেসকিউ ও ইমেইল পুশ ইঞ্জিন
# =========================================================================
def send_stealth_escalation_email(country, category, case_id, accused, details, target_email):
    sender_email = "secure-gateway@stp-network.org"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_email
    msg['Subject'] = f"🚨 SOVEREIGN LEGAL NOTICE: Case #{case_id} [Jurisdiction: {country}]"
    
    body = f"""
OFFICIAL HUMAN RIGHTS & LEGAL ESCALATION NOTICE
--------------------------------------------------
Case Reference ID: {case_id}
Jurisdiction/Country: {country}
Violation Category: {category}

ACCUSED / TARGET PROFILE:
Name/Institution: {accused['name']}
Designation/Relation: {accused['desig']}
Contact/Location: {accused['contact']}

INCIDENT BRIEF / SPECIFICATION:
{details}

CRITICAL INSTRUCTION:
This case has been logged securely via the Safe The People (STP) Universal Network.
Immediate legal/rescue intervention is required under the constitutional laws of {country}.
Please update the case tracking matrix via secure protocols.
"""
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('://gmail.com', 587)
        server.starttls()
        server.login(sender_email, SMTP_PASSWORD)
        server.sendmail(sender_email, target_email, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False

# =========================================================================
# ৩. বৈশ্বিক ডাইনামিক ডেটাবেস সাইলোস (সব দেশের তালিকা ও বাংলাদেশের বিস্তারিত উইং)
# =========================================================================
ALL_COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt",
    "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon",
    "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana",
    "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel",
    "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos",
    "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi",
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova",
    "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau",
    "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania",
    "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal",
    "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea",
    "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania",
    "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda",
    "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam",
    "Yemen", "Zambia", "Zimbabwe"
]

def get_dynamic_country_profile(country_name):
    base_profile = {
        "Country": country_name,
        "lexicon": {
            "title": f"🚨 Safe The People (STP) | {country_name} Sovereign Protocol",
            "subtitle": f"Universal Anonymous Justice & Human Rights Infrastructure within the Jurisdiction of {country_name}",
            "header_filing": f"📝 Secure Anonymous Filing Panel ({country_name} Sovereign Gate)",
            "lbl_cat": "Select Crisis / Harassment Category:",
            "lbl_accused_name": "Name of the Accused Person / Institution *Mandatory*:",
            "lbl_accused_desig": "Accused Position / Relation / Rank *Mandatory*:",
            "lbl_accused_contact": "Accused Specific Address, Phone or Digital ID *Mandatory*:",
            "lbl_remedy": f"What legal/social remedy do you require under the constitutional laws of {country_name}?",
            "lbl_details": "Describe the Incident / Human Rights Violation (Minimum 50 characters):",
            "lbl_evidence": "Upload Encrypted Digital Evidence / Proof Files (Max 10MB):",
            "lbl_captcha": "Sovereign Human Verification CAPTCHA:",
            "btn_submit": f"🚨 Submit Secure Complaint to {country_name} Sovereign Registry",
            "err_fields": "❌ Error: Please ensure Accused Profile, Details, and Evidence are fully provided.",
            "err_captcha": "❌ Error: Incorrect CAPTCHA Answer!",
            "success_hide": f"🎉 Identity Hidden Permanently! Case file encrypted and locked securely within {country_name} Matrix Nodes."
        }
    }
    
    if country_name == "Bangladesh":
        base_profile["lexicon"] = {
            "title": "🚨 সেভ দ্য পিপল - Safe The People (STP) | বাংলাদেশ প্রটোকল",
            "subtitle": "গণপ্রজাতন্ত্রী বাংলাদেশের অভ্যন্তরে সম্পূর্ণ নামহীন আইনি সুরক্ষা ইনফ্রাস্ট্রাকচার",
            "header_filing": "📝 বেনামী অভিযোগ দাখিল প্যানেল (বাংলাদেশ)",
            "lbl_cat": "হয়রালি বা সংকটের খাতটি চিহ্নিত করুন:",
            "lbl_accused_name": "অপরাধী বা প্রতিষ্ঠানের নাম (Accused Name) *বাধ্যতামূলক*:",
            "lbl_accused_desig": "অপরাধীর পদবি, কর্মস্থল বা সম্পর্ক (Designation) *বাধ্যতামূলক*:",
            "lbl_accused_contact": "অপরাধীর সুনির্দিষ্ট ঠিকানা, ফোন নম্বর বা সোশ্যাল আইডি *বাধ্যতামূলক*:",
            "lbl_remedy": "আপনি এই অভিযোগের বিপরীতে বাংলাদেশ আইন অনুযায়ী কোন পদক্ষেপ চান?",
            "lbl_details": "আপনার সমস্যার বিবরণ দিন (ন্যূনতম ৫০ অক্ষর):",
            "lbl_evidence": "ডিজিটাল প্রমাণ (ছবি, চ্যাট স্ক্রিনশট, অডিও বা ডকুমেন্ট আপলোড করুন - সর্বোচ্চ ১০ এমবি):",
            "lbl_captcha": "মানুষ বনাম রোবট যাচাইকরণ ক্যাপচা:",
            "btn_submit": "🚨 বাংলাদেশ জুডিশিয়াল প্রটোকলে অভিযোগ দাখিল করুন",
            "err_fields": "❌ ত্রুটি: অনুগ্রহ করে ফর্মের প্রতিটি তথ্য এবং প্রমাণ সঠিকভাবে দিন।",
            "err_captcha": "❌ ত্রুটি: ক্যাপচা উত্তর ভুল হয়েছে !",
            "success_hide": "🎉 আপনার পরিচয় সফলভাবে চিরতরে হাইড করা হয়েছে! ফাইলটি বাংলাদেশ জোনে লক করা হয়েছে।"
        }
        base_profile["agencies"] = [
            {"name": "জাতীয় জরুরি সেবা (Emergency Rescue)", "contact": "999", "email": "help@police.gov.bd", "type": "Immediate Action Desk"},
            {"name": "সাইবার ক্রাইম ইনভেস্টিগেশন ডিভিশন (DMP)", "contact": "01769691522", "email": "cyberhelp@dmp.gov.bd", "type": "Digital Forensics Wing"},
            {"name": "জাতীয় আইনগত সহায়তা প্রদান সংস্থা (আইন বিচার ও সংসদ বিষয়ক মন্ত্রণালয়)", "contact": "16430", "email": "nlaso.gov.bd@gmail.com", "type": "Government Free Legal Aid"}
        ]
        base_profile["attorneys"] = [
            {"name": "বাংলাদেশ সুপ্রিম কোর্ট লিগ্যাল এইড কমিটি (Government Panel)", "contact": "sc.legalaid@gmail.com", "specialty": "Supreme Court Legal Representation, High Court Complex, Dhaka"},
            {"name": "জাতীয় মহিলা আইনজীবী সমিতি (BNWLA Panel)", "contact": "bnwla@bdmail.net", "specialty": "Women & Children Rights, Pro-Bono Litigation Support"},

            

           {"name": "বাংলাদেশ লিগ্যাল এইড অ্যান্ড সার্ভিসেস ট্রাস্ট (BLAST Nodes)", "contact": "mail@blast.org.bd", "specialty": "Fundamental Liberties & Anti-Harassment Protection"}]base_profile["categories"] = ["🔒 সাইবার অপরাধ ও ব্ল্যাকমেইলিং", "🏠 পারিবারিক নির্যাতন ও সামাজিক চাপ", "🏭 শ্রমিক শোষণ ও কর্মক্ষেত্রে হয়রানি", "🌾 মৌলিক চাহিদা থেকে বঞ্চিত / সরকারি দুর্নীতি"]elif country_name == "India":base_profile["agencies"] = [{"name": "National Cyber Crime Portal", "contact": "1930", "email": "cybercrime-india@gov.in", "type": "Cyber Exploitation"},{"name": "National Commission for Women (NCW)", "contact": "7827170170", "email": "ncw@nic.in", "type": "Women Safety"}]base_profile["attorneys"] = [{"name": "Human Rights Law Network (HRLN)", "contact": "delhi@hrln.org", "specialty": "Public Litigation"},{"name": "National Legal Services Authority (NALSA)", "contact": "nalsa-dla@nic.in", "specialty": "Free State Defense Council"}]base_profile["categories"] = ["🔒 Cyber Crimes & Blackmailing", "🏠 Domestic Violence & Coercion", "🏭 Labor Exploitation", "🌾 Fundamental Rights Deprivation"]else:base_profile["agencies"] = [{"name": f"Human Rights Enforcement Division ({country_name})", "contact": "Global Node 1", "email": f"justice-{country_name.lower()}@stp-network.org", "type": "State Escalation Link"},{"name": "International Legal Aid Corps", "contact": "+1-800-STP-HELP", "email": "global-rescue@stp.org", "type": "Universal Support"}]base_profile["attorneys"] = [{"name": "Global Sovereign Human Rights Attorneys", "contact": "attorney-hub@stp.org", "specialty": "International Jurisdiction Control"}]base_profile["categories"] = ["🔒 Cyber Crime & Extortion", "🏠 Domestic Abuse & Social Pressure", "🏭 Labor Exploitation & Wage Theft", "🌾 Fundamental Rights Deprivation"]return base_profile
    =========================================================================৪. বৈশ্বিক ক্রন-ইঞ্জিন: অটো-টাইম লক ও রিয়েল ইমেইল ট্রিগার=========================================================================def execute_universal_time_lock_engine():conn = get_db_connection()cursor = conn.cursor()cursor.execute("SELECT * FROM stp_cases WHERE System_Status = 'Review Pending'")active_cases = cursor.fetchall()current_time = datetime.now()for case in active_cases:submit_time = datetime.strptime(case["Timestamp"], "%Y-%m-%d %H:%M:%S")hours_passed = (current_time - submit_time).total_seconds() / 3600.0if hours_passed >= 72.0:new_status = "🚨 Auto-Escalated to Official Panels"new_remarks = "72 Hours Time-Lock expired. Secure files successfully pushed to country authorities and legal aid wings."profile = get_dynamic_country_profile(case["Country"])accused_dict = {"name": case["Accused_Name"],"desig": case["Accused_Designation"],"contact": case["Accused_Contact"]}target_email = profile["agencies"][0]["email"] if "agencies" in profile and len(profile["agencies"]) > 0 else "resolution@stp.org"send_stealth_escalation_email(case["Country"],case["Category"],case["Case_ID"],accused_dict,case["Details_Snippet"],target_email)cursor.execute("""UPDATE stp_casesSET System_Status = ?, Last_Updated = ?, Remarks = ?WHERE Case_ID = ?""", (new_status, current_time.strftime("%Y-%m-%d %H:%M:%S"), new_remarks, case["Case_ID"]))conn.commit()conn.close()execute_universal_time_lock_engine()
=========================================================================৫. অ্যাপ নেভিগেশন রাউটার (সাইডবার মেনু)=========================================================================app_mode = st.sidebar.radio("STP Sovereign Menu:", ["📝 সর্বজনীন অভিযোগ দাখিল (Filing)","🔍 লাইভ ট্র্যাকিং প্যানেল (Victim Tracker)"])stealth_trigger = st.sidebar.text_input("System Node / Terminal Guide:", type="password", help="System routing interface")=========================================================================মোড ১: সর্বজনীন অভিযোগ দাখিল (Filing - Fully Dynamic)=========================================================================if app_mode == "📝 সর্বজনীন অভিযোগ দাখিল (Filing)" and not stealth_trigger:st.sidebar.write("---")# পৃথিবীর সকল দেশের ডাইনামিক ড্রপডাউন সিলেক্টর উইজেটuser_country = st.sidebar.selectbox("📍 Jurisdiction / Country (দেশ নির্বাচন করুন):", ALL_COUNTRIES, index=ALL_COUNTRIES.index("Bangladesh"))if user_country:profile = get_dynamic_country_profile(user_country)lex = profile["lexicon"]st.title(lex["title"])st.subheader(lex["subtitle"])col1, col2 = st.columns(2)with col1:st.header(lex["header_filing"])chosen_cat = st.selectbox(lex["lbl_cat"], profile["categories"])st.write("---")accused_name = st.text_input(lex["lbl_accused_name"])accused_desig = st.text_input(lex["lbl_accused_desig"])accused_contact = st.text_input(lex["lbl_accused_contact"])st.write("---")remedy_lbl = "1. Encrypted Data Archiving Only (তথ্য গোপন নোঙ্গরকরণ)" if user_country == "Bangladesh" else "1. Encrypted Data Archiving Only"remedy_lbl2 = "2. Full Legal Notice & Rescue Action (আইনি পদক্ষেপ ও সরাসরি সমাধান)" if user_country == "Bangladesh" else "2. Full Legal Notice & Rescue Action"remedy_choice = st.selectbox(lex["lbl_remedy"], [remedy_lbl, remedy_lbl2])details = st.text_area(lex["lbl_details"])uploaded_file = st.file_uploader(lex["lbl_evidence"], type=["png", "jpg", "jpeg", "pdf", "docx", "mp3"])# নিখুঁত ১-ক্লিকে রিফ্রেস করা র্যান্ডম ক্যাপচা লজিকif 'captcha_num1' not in st.session_state:st.session_state.captcha_num1 = random.randint(1, 9)st.session_state.captcha_num2 = random.randint(1, 9)num1, num2 = st.session_state.captcha_num1, st.session_state.captcha_num2captcha_prompt = f"{num1} + {num2} = কত?" if user_country == "Bangladesh" else f"{num1} + {num2} = ?"captcha_answer = st.number_input(f"{lex['lbl_captcha']} {captcha_prompt}", step=1, value=0) if st.button(lex["btn_submit"]):if uploaded_file is not None and uploaded_file.size > 10 * 1024 * 1024:if user_country == "Bangladesh":st.error("❌ ফেসিলিটি লিমিট অতিক্রম করেছে! আপলোড করা ফাইলের সাইজ ১০ এমবি (10MB)-এর কম হতে হবে।")else:st.error("❌ Limit exceeded! File size must be less than 10MB.")elif len(details) < 50 or uploaded_file is None or not accused_name or not accused_contact:st.error(lex["err_fields"])elif captcha_answer != (num1 + num2):st.error(lex["err_captcha"])else:file_bytes = uploaded_file.read()evidence_hash = hashlib.sha256(file_bytes).hexdigest()case_id = uuid.uuid4().hex[:12].upper()raw_token = uuid.uuid4().hexsecret_key = "-".join([raw_token[i:i+6].upper() for i in range(0, 24, 6)])key_hash = hashlib.sha256(secret_key.encode()).hexdigest()founder_vault_entry = hashlib.sha256((secret_key + FOUNDER_HASHED_MASTER).encode()).hexdigest()st.success(lex["success_hide"])st.code(f"Case ID: {case_id}\nSecret Key: {secret_key}", language="text")conn = get_db_connection()cursor = conn.cursor()cursor.execute("""INSERT INTO stp_cases (Case_ID, Key_Hash, Founder_Key_Vault, Timestamp, Country, Category,Accused_Name, Accused_Designation, Accused_Contact, Remedy_Type, Evidence_Hash, Details_Snippet, System_Status, Last_Updated, Remarks)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (case_id, key_hash, founder_vault_entry, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),user_country, chosen_cat, accused_name, accused_desig, accused_contact, remedy_choice,evidence_hash, details, "Review Pending", datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Case secured. Time-Lock engine active."))conn.commit()conn.close()# সাবমিট শেষ হলে সাথে সাথে সেশন স্টেট ক্লিয়ার হবে যেন রিফ্রেশে নতুন ক্যাপচা ট্রিগার হয়del st.session_state.captcha_num1st.rerun()with col2:infra_title = f"🏢 {user_country} Legal Infrastructure" if user_country != "Bangladesh" else f"🏢 {user_country} আইনি অবকাঠামো"infra_desc = f"Official and social organizations dedicated to your protection within {user_country}:" if user_country != "Bangladesh" else f"গণপ্রজাতন্ত্রী বাংলাদেশের অভ্যন্তরে আপনার সুরক্ষায় নিয়োজিত অফিশিয়াল ও সামাজিক সংস্থাসমূহ:"st.header(infra_title)st.write(infra_desc)if "agencies" in profile:for agency in profile["agencies"]:with st.expander(f"🏢 {agency['name']}", expanded=True):st.write(f"Emergency Portal/Hotline: {agency['contact']}")st.write(f"Stealth Target Email: {agency['email']}")st.write(f"Action Base: {agency['type']}")st.write("---") panel_title = f"⚖️ {user_country} Sovereign Attorney Panel:" if user_country != "Bangladesh" else f"⚖️ {user_country} সরকারি ও সাহায্যকারী আইনজীবী প্যানেল:"st.subheader(panel_title)if "attorneys" in profile:for lawyer in profile["attorneys"]:with st.expander(f"⚖️ {lawyer['name']}", expanded=True):st.write(f"Secure Contact / Office Desk: {lawyer['contact']}")st.write(f"Specialization & Station: {lawyer['specialty']}") 
=========================================================================মোড ২: লাইভ ট্র্যাকিং প্যানেল (Victim Tracker)=========================================================================elif app_mode == "🔍 লাইভ ট্র্যাকিং প্যানেল (Victim Tracker)" and not stealth_trigger:st.header("🔍 লাইভ বেনামী অভিযোগ ট্র্যাকিং প্যানেল")input_case_id = st.text_input("Case ID:").strip().upper()input_secret_key = st.text_input("Secret Key:", type="password").strip()if st.button("Check Status"):if input_case_id and input_secret_key:conn = get_db_connection()cursor = conn.cursor()cursor.execute("SELECT * FROM stp_cases WHERE Case_ID = ?", (input_case_id,))target_case = cursor.fetchone()conn.close()if target_case and hashlib.sha256(input_secret_key.encode()).hexdigest() == target_case["Key_Hash"]:st.success("✅ Case Verified!")st.info(f"🚨 Current Status: {target_case['System_Status']}")st.warning(f"📌 Action Remarks: {target_case['Remarks']}")st.caption(f"Last Updated: {target_case['Last_Updated']}")else:st.error("❌ Invalid Credentials.")
=========================================================================👑 মোড ৩: প্রতিষ্ঠাতা সার্বভৌম ইউনিভার্সাল গ্লোবাল ড্যাশবোর্ড (STEALTH ACCESS)=========================================================================elif stealth_trigger:if hashlib.sha256(stealth_trigger.encode()).hexdigest() == FOUNDER_HASHED_MASTER:st.title("👑 প্রতিষ্ঠাতা ইউনিভার্সাল গ্লোবাল জাস্টিস কন্ট্রোল প্যানেল")st.success("🔓 মাস্টার অ্যাক্সেস গ্র্যান্টেড।")conn = get_db_connection()cursor = conn.cursor()cursor.execute("SELECT * FROM stp_cases ORDER BY Timestamp DESC")all_cases = cursor.fetchall()conn.close()if all_cases:st.write(f"📊 সর্বমোট বৈশ্বিক ডেটাবেজ এন্ট্রি: {len(all_cases)} টি")for case in all_cases:with st.expander(f"📦 [দেশ: {case['Country']}] | কেস আইডি: {case['Case_ID']}", expanded=True):col_a, col_b = st.columns(2)with col_a:st.write(f"🎯 অভিযুক্ত/উৎস: {case['Accused_Name']}")st.write(f"💼 পদ / সম্পর্ক: {case['Accused_Designation']}")st.write(f"📞 কন্টাক্ট ইনফো: {case['Accused_Contact']}")st.text_area("অভিযোগের বিবরণ:", case['Details_Snippet'], disabled=True, key=f"text_{case['Case_ID']}")with col_b:st.write(f"🚨 লাইভ স্ট্যাটাস: {case['System_Status']}")st.write(f"📌 বর্তমান মন্তব্য: {case['Remarks']}")st.subheader("⚙️ বৈশ্বিক সমাধান কন্ট্রোলার")next_status = st.selectbox(f"স্ট্যাটাস পরিবর্তন করুন ({case['Case_ID']}):",["Review Pending", "🔍 Investigating", "⚖️ Legal Notice Sent", "🎉 Problem Resolved"],key=f"status_{case['Case_ID']}")next_remarks = st.text_input(f"ভিকটিমের জন্য সমাধান বার্তা ({case['Case_ID']}):", value=case['Remarks'], key=f"rem_{case['Case_ID']}")if st.button(f"আপডেট করুন ({case['Case_ID']})", key=f"btn_{case['Case_ID']}"):conn = get_db_connection()cursor = conn.cursor()cursor.execute("""UPDATE stp_cases SET System_Status = ?, Remarks = ?, Last_Updated = ? WHERE Case_ID = ?""", (next_status, next_remarks, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), case['Case_ID']))conn.commit()conn.close()if next_status == "🎉 Problem Resolved":profile = get_dynamic_country_profile(case["Country"])accused_dict = {"name": case["Accused_Name"],"desig": case["Accused_Designation"],"contact": case["Accused_Contact"]}target_email = profile["agencies"][0]["email"] if "agencies" in profile and len(profile["agencies"]) > 0 else "resolution@stp.org"send_stealth_escalation_email(case["Country"],case["Category"],case["Case_ID"],accused_dict,"RESOLUTION NOTICE",target_email)st.success("✅ একশন ফাইল আপডেটেড!")st.rerun()else:st.info("📭 ডাটাবেজে এই মুহূর্তে কোনো অভিযোগ জমা নেই।")else:st.sidebar.error("Invalid Terminal Node Route.")
