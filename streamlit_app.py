
import streamlit as st
import openai
import datetime

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Moving to STL? Let’s Find Your Spot", layout="centered")

st.title("🚚 Moving to STL? Let’s Find Your Spot")
st.write("Tell us a little about your move, and we’ll match you with the best neighborhoods, home types, and resources — all based on *your* priorities.")

with st.form("relocation_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    move_date = st.date_input("Target Move-In Date", value=datetime.date.today())
    st.markdown(f"📅 Selected Date: **{move_date.strftime('%B %d, %Y')}**")

    current_city = st.text_input("Current City & State")
    work_address = st.text_input("Full Work Address (Street, City, State, ZIP)")

    reason = st.selectbox("What's the main reason for your move?", ["Job", "Family", "Lifestyle", "Retirement", "College", "Other"])
    budget = st.selectbox("What’s your home budget?", ["Under $200k", "$200k–$300k", "$300k–$400k", "$400k–$500k", "Over $500k"])
    commute = st.selectbox("Ideal Commute Time?", ["<15 min", "15–30 min", "30–45 min", "45+ min"])
    
    home_type = st.multiselect("What type of home are you looking for?", [
        "Single-Family Home",
        "Condo",
        "Townhome",
        "Multi-Family (Duplex/Triplex)",
        "New Construction",
        "Historic Home",
        "Fixer Upper",
        "Luxury Home",
        "Gated Community",
        "Loft/Urban Apartment"
    ])
    
    features = st.multiselect("Must-have features?", ["Garage", "Yard", "Near Good Schools", "Public Transport", "Walkable Area"])

    submitted = st.form_submit_button("Get My STL Match")

if submitted:
    with st.spinner("Creating your STL relocation plan..."):
        move_date_str = move_date.strftime("%B %d, %Y")
        prompt = f"""You are a relocation assistant working for a local St. Louis real estate team. 
The user below is considering a move and just filled out our relocation form.

Here are the details:
- Full Name: {name}
- Email: {email}
- Phone: {phone}
- Current City: {current_city}
- Move-in Date: {move_date_str}
- Work Address: {work_address}
- Reason for Moving: {reason}
- Budget: {budget}
- Commute Preference: {commute}
- Home Type: {', '.join(home_type)}
- Must-Have Features: {', '.join(features)}

Using this info, provide a short and helpful relocation insight for the client. 
Include 2–3 St. Louis neighborhoods that align with their preferences, and why. 
Then close with a friendly message letting them know our real estate team will be reaching out to help with the next steps — including home searches, tours, and local guidance.
"""
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a relocation expert on a real estate team helping clients move to St. Louis."},
                {"role": "user", "content": prompt}
            ]
        )

        advice = response.choices[0].message.content
        st.subheader("📍 Your STL Relocation Overview")
        st.markdown(advice)

        st.markdown("---")
        st.markdown("✅ **Thanks for sharing your goals — we’ll be reaching out shortly to help guide your STL home search.**")
        st.markdown("[📅 Prefer to chat sooner? Schedule a call here.](https://calendly.com/YOUR-CALENDAR-LINK)")



