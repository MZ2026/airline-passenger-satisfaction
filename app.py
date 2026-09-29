import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Airline Passenger Satisfaction Predictor",
    page_icon="✈️",
    layout="wide"
)

# Dark-mode styled header
st.title("✈️ Airline Passenger Satisfaction Predictor")
st.caption("Adjust passenger features on the left sidebar to predict real-time satisfaction probability.")

# -----------------------------------------------------------------------------
# 2. Model Training & Caching
# -----------------------------------------------------------------------------
@st.cache_resource
def train_model():
    """Load prepared training data and train the Random Forest pipeline."""
    train = pd.read_csv("prepared_data/train_prepared.csv")
    
    X_train = train.drop(columns=["satisfaction"])
    y_train = train["satisfaction"].map({"neutral or dissatisfied": 0, "satisfied": 1})
    
    categorical_cols = ['Gender', 'Customer Type', 'Type of Travel', 'Class']
    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ],
        remainder="passthrough"
    )
    
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            min_samples_split=10,
            random_state=42,
            n_jobs=-1
        ))
    ])
    
    model.fit(X_train, y_train)
    return model

with st.spinner("Loading Random Forest model..."):
    model = train_model()

# -----------------------------------------------------------------------------
# 3. Sidebar - Input Controls Organized into Expanders
# -----------------------------------------------------------------------------
st.sidebar.header("📋 Passenger Profile")

with st.sidebar.expander("👤 Demographics & Flight", expanded=True):
    gender = st.selectbox("Gender", ["Male", "Female"])
    customer_type = st.selectbox("Customer Type", ["Loyal Customer", "disloyal Customer"])
    age = st.slider("Age", 7, 85, 35)
    type_of_travel = st.selectbox("Type of Travel", ["Business travel", "Personal Travel"])
    flight_class = st.selectbox("Class", ["Business", "Eco", "Eco Plus"])
    flight_distance = st.slider("Flight Distance (miles)", 30, 5000, 1000)

with st.sidebar.expander("🛫 Pre-flight & Booking Services"):
    online_boarding = st.slider("Online Boarding", 0, 5, 4)
    booking_ease = st.slider("Ease of Online Booking", 0, 5, 3)
    checkin_service = st.slider("Check-in Service", 0, 5, 4)
    gate_location = st.slider("Gate Location", 0, 5, 3)
    dep_arr_time = st.slider("Time Convenient", 0, 5, 3)

with st.sidebar.expander("🎧 Inflight Services"):
    wifi_service = st.slider("Inflight WiFi", 0, 5, 3)
    entertainment = st.slider("Inflight Entertainment", 0, 5, 4)
    seat_comfort = st.slider("Seat Comfort", 0, 5, 4)
    onboard_service = st.slider("On-board Service", 0, 5, 4)
    leg_room = st.slider("Leg Room Service", 0, 5, 3)
    cleanliness = st.slider("Cleanliness", 0, 5, 4)
    food_drink = st.slider("Food and Drink", 0, 5, 3)
    baggage_handling = st.slider("Baggage Handling", 1, 5, 4)
    inflight_service = st.slider("Inflight Service", 0, 5, 4)

with st.sidebar.expander("⏱️ Flight Delays"):
    dep_delay = st.number_input("Departure Delay (mins)", min_value=0, max_value=1600, value=0)
    arr_delay = st.number_input("Arrival Delay (mins)", min_value=0, max_value=1600, value=0)

# -----------------------------------------------------------------------------
# 4. Construct Input Data
# -----------------------------------------------------------------------------
input_data = pd.DataFrame([{
    'Gender': gender,
    'Customer Type': customer_type,
    'Age': age,
    'Type of Travel': type_of_travel,
    'Class': flight_class,
    'Flight Distance': flight_distance,
    'Inflight wifi service': wifi_service,
    'Departure/Arrival time convenient': dep_arr_time,
    'Ease of Online booking': booking_ease,
    'Gate location': gate_location,
    'Food and drink': food_drink,
    'Online boarding': online_boarding,
    'Seat comfort': seat_comfort,
    'Inflight entertainment': entertainment,
    'On-board service': onboard_service,
    'Leg room service': leg_room,
    'Baggage handling': baggage_handling,
    'Checkin service': checkin_service,
    'Inflight service': inflight_service,
    'Cleanliness': cleanliness,
    'Departure Delay in Minutes': dep_delay,
    'Arrival Delay in Minutes': arr_delay
}])

# -----------------------------------------------------------------------------
# 5. Prediction & Main UI
# -----------------------------------------------------------------------------
prediction = model.predict(input_data)[0]
probabilities = model.predict_proba(input_data)[0]

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🎯 Satisfaction Prediction")
    if prediction == 1:
        st.success(f"### 🎉 SATISFIED ({probabilities[1]*100:.1f}% Confidence)")
    else:
        st.error(f"### ⚠️ NEUTRAL / DISSATISFIED ({probabilities[0]*100:.1f}% Confidence)")
    
    st.write("**Probability Breakdown:**")
    st.progress(float(probabilities[1]))
    
    # Clean Metric Summary instead of messy raw text
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("Satisfied Probability", f"{probabilities[1]*100:.1f}%")
    m_col2.metric("Dissatisfied Probability", f"{probabilities[0]*100:.1f}%")

with col2:
    st.subheader("📊 Key Driver Breakdown")
    key_ratings = {
        "Online Boarding": online_boarding,
        "Inflight WiFi": wifi_service,
        "Inflight Entertainment": entertainment,
        "Seat Comfort": seat_comfort,
        "Leg Room": leg_room
    }
    
    # Dark Mode Matplotlib Chart
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6, 3.2))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    colors = ['#2ea043' if v >= 4 else ('#e3b341' if v == 3 else '#f85149') for v in key_ratings.values()]
    bars = ax.barh(list(key_ratings.keys()), list(key_ratings.values()), color=colors, height=0.55)
    
    ax.set_xlim(0, 5)
    ax.set_xlabel("Rating (0 to 5)", color='white', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#30363d')
    ax.spines['left'].set_color('#30363d')
    ax.tick_params(colors='white', labelsize=9)
    
    st.pyplot(fig)

st.divider()

# -----------------------------------------------------------------------------
# 6. Structured Profile Summary (Replacing messy wide table)
# -----------------------------------------------------------------------------
st.subheader("📝 Active Passenger Profile")

p_col1, p_col2, p_col3, p_col4 = st.columns(4)
p_col1.metric("Customer", f"{gender}, {age} yrs")
p_col2.metric("Travel Type", type_of_travel)
p_col3.metric("Flight Class", flight_class)
p_col4.metric("Flight Distance", f"{flight_distance} mi")