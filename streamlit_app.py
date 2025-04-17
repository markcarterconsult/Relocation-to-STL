
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
    st.markdown(f"📅 Selected Date: **{move_date.strftime('%B %d, %Y')}**")  # Friendly format shown below input

    current_city = st.text_input("Current City & State")
    work_address = st.text_input("Address of Work (for commute matching)")

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
    with st.spinner("Finding your STL spot..."):
        move_date_str = move_date.strftime("%B %d, %Y")
        prompt = f"""You are a helpful St. Louis relocation assistant. A person is moving from {current_city} to St. Louis and gave the following info:
- Reason for move: {reason}
- Budget: {budget}
- Commute preference: {commute}
- Address of work: {work_address}
- Home type: {', '.join(home_type)}
- Must-have features: {', '.join(features)}
- Move-in date: {move_date_str}

Based on this, give a personalized relocation recommendation including 2-3 STL neighborhoods that match, school advice if applicable, and a next-step tip. End with a friendly invitation to schedule a relocation call."""
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a relocation expert for people moving to St. Louis."},
                {"role": "user", "content": prompt}
            ]
        )

        advice = response.choices[0].message.content
        st.subheader("🎯 Your STL Relocation Insights")
        st.markdown(advice)

        st.markdown("---")
        st.markdown("✅ **Want help finding a home that matches your exact needs?**")
        st.markdown("[📅 Schedule My Relocation Call](https://calendly.com/YOUR-CALENDAR-LINK)")


