# Interactive Streamlit dashboard for the Airline Passenger Satisfaction project

from pathlib import Path
import pickle

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Airline Passenger Satisfaction",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM DARK DESIGN
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   MAIN PAGE
========================================================= */

.stApp {
    background:
        radial-gradient(circle at top right, #162b46 0%, transparent 30%),
        linear-gradient(135deg, #08111f 0%, #0b1422 55%, #0d1828 100%);
    color: #e8eef7;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}


/* =========================================================
   STREAMLIT DEFAULT ELEMENTS
========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #071426 0%,
            #0a1d33 55%,
            #0c223b 100%
        );

    border-right: 1px solid rgba(100, 160, 220, 0.15);
}

section[data-testid="stSidebar"] * {
    color: #e8eef7;
}


/* =========================================================
   HEADINGS
========================================================= */

h1,
h2,
h3 {
    color: #f4f8ff !important;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 750;
    color: #f4f8ff;
    margin-bottom: 0.2rem;
}

.section-description {
    color: #8fa4bc;
    font-size: 0.93rem;
    margin-bottom: 1rem;
}


/* =========================================================
   HERO HEADER
========================================================= */

.hero {
    padding: 26px 30px;
    border-radius: 18px;
    margin-bottom: 22px;

    background:
        linear-gradient(
            120deg,
            rgba(18, 65, 108, 0.95) 0%,
            rgba(20, 92, 150, 0.92) 55%,
            rgba(25, 117, 181, 0.88) 100%
        );

    border: 1px solid rgba(94, 177, 255, 0.20);

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.25);
}

.hero-title {
    color: #ffffff;
    font-size: 2.25rem;
    font-weight: 800;
    margin-bottom: 7px;
    letter-spacing: -0.025em;
}

.hero-text {
    color: #dcecff;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 950px;
}


/* =========================================================
   SELECT BOXES
========================================================= */

div[data-baseweb="select"] > div {
    background-color: #111d2d !important;
    border: 1px solid #263b52 !important;
    border-radius: 10px !important;
    color: #f3f7fc !important;
}

div[data-baseweb="select"] span {
    color: #f3f7fc !important;
}


/* =========================================================
   NUMBER INPUTS
========================================================= */

div[data-testid="stNumberInput"] input {
    background-color: #111d2d !important;
    color: #f3f7fc !important;

    border: 1px solid #263b52 !important;
    border-radius: 10px !important;
}


/* =========================================================
   INPUT LABELS
========================================================= */

label,
[data-testid="stWidgetLabel"] {
    color: #dbe7f5 !important;
}


/* =========================================================
   MODEL BADGE
========================================================= */

.model-badge {
    display: inline-block;

    background: rgba(25, 132, 255, 0.14);
    color: #69b5ff;

    border: 1px solid rgba(65, 157, 255, 0.22);

    padding: 7px 13px;
    border-radius: 999px;

    font-weight: 700;
    font-size: 0.85rem;

    margin-top: 5px;
    margin-bottom: 5px;
}


/* =========================================================
   DIVIDERS
========================================================= */

hr {
    border-color: rgba(132, 164, 199, 0.14) !important;
}


/* =========================================================
   SLIDERS
========================================================= */

div[data-testid="stSlider"] {
    padding-right: 10px;
}


/* =========================================================
   METRIC CARDS
========================================================= */

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #111e2e,
            #0e1927
        );

    border: 1px solid #21364c;

    border-radius: 14px;

    padding: 16px 18px;

    box-shadow:
        0 7px 18px rgba(0, 0, 0, 0.18);
}

div[data-testid="stMetricLabel"] {
    color: #91a6bd !important;
}

div[data-testid="stMetricValue"] {
    color: #56adff !important;
    font-weight: 750;
}


/* =========================================================
   PREDICTION RESULT
========================================================= */

.result-success {
    padding: 22px;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            rgba(24, 145, 84, 0.20),
            rgba(19, 105, 66, 0.14)
        );

    border: 1px solid rgba(64, 206, 126, 0.32);

    color: #75e6a5;

    font-size: 1.2rem;
    font-weight: 750;

    margin-top: 14px;
}


.result-warning {
    padding: 22px;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            rgba(225, 143, 38, 0.18),
            rgba(159, 88, 18, 0.13)
        );

    border: 1px solid rgba(245, 169, 67, 0.30);

    color: #ffc46b;

    font-size: 1.2rem;
    font-weight: 750;

    margin-top: 14px;
}


/* =========================================================
   BUTTON
========================================================= */

div.stButton > button {
    width: 100%;

    min-height: 50px;

    border: 1px solid rgba(91, 177, 255, 0.30);
    border-radius: 11px;

    background:
        linear-gradient(
            90deg,
            #0878e8,
            #1697ff
        );

    color: white;

    font-size: 1rem;
    font-weight: 750;

    box-shadow:
        0 7px 20px rgba(0, 115, 230, 0.20);
}

div.stButton > button:hover {
    border-color: #6bbcff;

    background:
        linear-gradient(
            90deg,
            #1188fa,
            #27a3ff
        );

    color: white;
}


/* =========================================================
   DATAFRAME
========================================================= */

div[data-testid="stDataFrame"] {
    border: 1px solid #21364c;
    border-radius: 12px;
    overflow: hidden;
}


/* =========================================================
   INFO BOX
========================================================= */

div[data-testid="stAlert"] {
    background-color: #101f31;
    color: #dce9f7;

    border: 1px solid #26415e;
    border-radius: 12px;
}


/* =========================================================
   PROGRESS BAR
========================================================= */

div[data-testid="stProgress"] > div > div {
    background-color: #1595ff;
}


/* =========================================================
   RADIO / NAVIGATION
========================================================= */

div[role="radiogroup"] label {
    color: #dce8f6 !important;
}


/* =========================================================
   CAPTIONS / NORMAL TEXT
========================================================= */

p,
.stMarkdown {
    color: #c9d5e4;
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 800px) {

    .hero {
        padding: 20px;
    }

    .hero-title {
        font-size: 1.65rem;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_PATHS = {
    "Decision Tree": Path("models/decision_tree_model.pkl"),
    "Random Forest": Path("models/random_forest_model.pkl")
}


# ============================================================
# LOAD MODELS
# ============================================================

@st.cache_resource
def load_model(path):
    with open(path, "rb") as file:
        return pickle.load(file)


# ============================================================
# MODEL PERFORMANCE
# ============================================================

MODEL_METRICS = {

    "Decision Tree": {
        "Accuracy": 95.56,
        "Precision": 96.29,
        "Sensitivity": 93.48,
        "Specificity": 97.18,
        "ROC-AUC": 98.47
    },

    "Random Forest": {
        "Accuracy": 96.31,
        "Precision": 97.11,
        "Sensitivity": 94.40,
        "Specificity": 97.80,
        "ROC-AUC": 99.41
    }
}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        ## ✈️ Airline Passenger
        ### Satisfaction Project
        """
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Predict",
            "Model Comparison",
            "About"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("Machine Learning Project")

    st.caption(
        "Decision Tree • Random Forest"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-title">✈️ Airline Passenger Satisfaction Predictor</div>
    <div class="hero-text">
        Explore passenger satisfaction predictions using trained machine learning models.
        Enter passenger, flight and service information, select a model,
        then click Predict Satisfaction.
    </div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# PREDICTION PAGE
# ============================================================

if page == "Predict":

    # --------------------------------------------------------
    # MODEL SELECTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">⚙️ Model Selection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Choose which trained model should make the prediction.'
        '</div>',
        unsafe_allow_html=True
    )

    selected_model = st.selectbox(
        "Prediction model",
        [
            "Random Forest",
            "Decision Tree"
        ],
        label_visibility="collapsed"
    )


    model_path = MODEL_PATHS[selected_model]


    if not model_path.exists():

        st.error(
            f"{selected_model} model file was not found.\n\n"
            f"Expected: {model_path}"
        )

        st.stop()


    model = load_model(model_path)


    st.markdown(
        f"""
        <div class="model-badge">
            Active model: {selected_model}
        </div>
        """,
        unsafe_allow_html=True
    )


    st.divider()


    # ========================================================
    # PASSENGER + FLIGHT INFORMATION
    # ========================================================

    left, right = st.columns(
        [1.35, 1],
        gap="large"
    )


    # --------------------------------------------------------
    # PASSENGER
    # --------------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-title">'
            '👤 Passenger Information'
            '</div>',
            unsafe_allow_html=True
        )

        p1, p2 = st.columns(2)


        with p1:

            gender = st.selectbox(
                "Gender",
                ["Male", "Female"]
            )

            age = st.number_input(
                "Age",
                min_value=7,
                max_value=85,
                value=35
            )

            customer_type = st.selectbox(
                "Customer Type",
                [
                    "Loyal Customer",
                    "disloyal Customer"
                ]
            )


        with p2:

            type_of_travel = st.selectbox(
                "Type of Travel",
                [
                    "Business travel",
                    "Personal Travel"
                ]
            )

            travel_class = st.selectbox(
                "Class",
                [
                    "Business",
                    "Eco",
                    "Eco Plus"
                ]
            )

            flight_distance = st.number_input(
                "Flight Distance",
                min_value=31,
                max_value=4983,
                value=1000
            )


    # --------------------------------------------------------
    # FLIGHT
    # --------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-title">'
            '🛫 Flight Information'
            '</div>',
            unsafe_allow_html=True
        )


        departure_delay = st.number_input(
            "Departure Delay in Minutes",
            min_value=0,
            max_value=2000,
            value=0
        )


        arrival_delay = st.number_input(
            "Arrival Delay in Minutes",
            min_value=0,
            max_value=2000,
            value=0
        )


    st.divider()


    # ========================================================
    # SERVICE RATINGS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '⭐ Service Ratings'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Rate each airline service from 0 to 5.'
        '</div>',
        unsafe_allow_html=True
    )


    c1, c2, c3 = st.columns(
        3,
        gap="large"
    )


    # --------------------------------------------------------
    # COLUMN 1
    # --------------------------------------------------------

    with c1:

        inflight_wifi = st.slider(
            "Inflight wifi service",
            0, 5, 3
        )

        departure_arrival_time = st.slider(
            "Departure/Arrival time convenient",
            0, 5, 3
        )

        ease_online_booking = st.slider(
            "Ease of Online booking",
            0, 5, 3
        )

        gate_location = st.slider(
            "Gate location",
            0, 5, 3
        )

        food_drink = st.slider(
            "Food and drink",
            0, 5, 3
        )


    # --------------------------------------------------------
    # COLUMN 2
    # --------------------------------------------------------

    with c2:

        online_boarding = st.slider(
            "Online boarding",
            0, 5, 3
        )

        seat_comfort = st.slider(
            "Seat comfort",
            0, 5, 3
        )

        inflight_entertainment = st.slider(
            "Inflight entertainment",
            0, 5, 3
        )

        onboard_service = st.slider(
            "On-board service",
            0, 5, 3
        )

        leg_room = st.slider(
            "Leg room service",
            0, 5, 3
        )


    # --------------------------------------------------------
    # COLUMN 3
    # --------------------------------------------------------

    with c3:

        baggage_handling = st.slider(
            "Baggage handling",
            1, 5, 3
        )

        checkin_service = st.slider(
            "Checkin service",
            0, 5, 3
        )

        inflight_service = st.slider(
            "Inflight service",
            0, 5, 3
        )

        cleanliness = st.slider(
            "Cleanliness",
            0, 5, 3
        )


    # ========================================================
    # CREATE MODEL INPUT
    # ========================================================

    input_data = pd.DataFrame({

        "Gender": [gender],

        "Customer Type": [
            customer_type
        ],

        "Age": [age],

        "Type of Travel": [
            type_of_travel
        ],

        "Class": [
            travel_class
        ],

        "Flight Distance": [
            flight_distance
        ],

        "Inflight wifi service": [
            inflight_wifi
        ],

        "Departure/Arrival time convenient": [
            departure_arrival_time
        ],

        "Ease of Online booking": [
            ease_online_booking
        ],

        "Gate location": [
            gate_location
        ],

        "Food and drink": [
            food_drink
        ],

        "Online boarding": [
            online_boarding
        ],

        "Seat comfort": [
            seat_comfort
        ],

        "Inflight entertainment": [
            inflight_entertainment
        ],

        "On-board service": [
            onboard_service
        ],

        "Leg room service": [
            leg_room
        ],

        "Baggage handling": [
            baggage_handling
        ],

        "Checkin service": [
            checkin_service
        ],

        "Inflight service": [
            inflight_service
        ],

        "Cleanliness": [
            cleanliness
        ],

        "Departure Delay in Minutes": [
            departure_delay
        ],

        "Arrival Delay in Minutes": [
            arrival_delay
        ]
    })


    st.divider()


    # ========================================================
    # PREDICTION + PERFORMANCE
    # ========================================================

    result_col, metric_col = st.columns(
        [1, 1.35],
        gap="large"
    )


    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    with result_col:

        st.markdown(
            '<div class="section-title">'
            '🔮 Prediction Result'
            '</div>',
            unsafe_allow_html=True
        )


        predict_button = st.button(
            "▶ Predict Satisfaction",
            type="primary",
            use_container_width=True
        )


        if predict_button:

            prediction = model.predict(
                input_data
            )[0]


            probabilities = model.predict_proba(
                input_data
            )[0]


            class_labels = list(
                model.classes_
            )


            if prediction == 1:

                st.markdown(
                    """
                    <div class="result-success">
                        ✓ Passenger predicted to be
                        SATISFIED
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="result-warning">
                        ⚠ Passenger predicted to be
                        NEUTRAL OR DISSATISFIED
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            if 1 in class_labels:

                satisfied_index = (
                    class_labels.index(1)
                )

                satisfied_probability = (
                    probabilities[
                        satisfied_index
                    ] * 100
                )


                st.metric(
                    "Probability of Satisfaction",
                    f"{satisfied_probability:.1f}%"
                )

                st.progress(
                    int(
                        satisfied_probability
                    )
                )


    # --------------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------------

    with metric_col:

        st.markdown(
            f'<div class="section-title">'
            f'📊 {selected_model} Test Performance'
            f'</div>',
            unsafe_allow_html=True
        )


        metrics = MODEL_METRICS[
            selected_model
        ]


        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Accuracy",
            f"{metrics['Accuracy']:.2f}%"
        )

        m2.metric(
            "Precision",
            f"{metrics['Precision']:.2f}%"
        )

        m3.metric(
            "Sensitivity",
            f"{metrics['Sensitivity']:.2f}%"
        )


        m4, m5 = st.columns(2)

        m4.metric(
            "Specificity",
            f"{metrics['Specificity']:.2f}%"
        )

        m5.metric(
            "ROC-AUC",
            f"{metrics['ROC-AUC']:.2f}%"
        )


# ============================================================
# MODEL COMPARISON PAGE
# ============================================================

elif page == "Model Comparison":

    st.markdown(
        '<div class="section-title">'
        '📊 Final Model Comparison'
        '</div>',
        unsafe_allow_html=True
    )


    st.write(
        """
        Both models were evaluated on the same
        separate test dataset.
        """
    )


    comparison = pd.DataFrame({

        "Metric": [
            "Accuracy",
            "Precision",
            "Sensitivity",
            "Specificity",
            "ROC-AUC"
        ],

        "Decision Tree": [
            "95.56%",
            "96.29%",
            "93.48%",
            "97.18%",
            "98.47%"
        ],

        "Random Forest": [
            "96.31%",
            "97.11%",
            "94.40%",
            "97.80%",
            "99.41%"
        ]
    })


    st.dataframe(
        comparison,
        hide_index=True,
        use_container_width=True
    )


    st.markdown("### Accuracy")

    accuracy_chart = pd.DataFrame(
        {
            "Accuracy": [
                95.56,
                96.31
            ]
        },
        index=[
            "Decision Tree",
            "Random Forest"
        ]
    )


    st.bar_chart(
        accuracy_chart
    )


    st.info(
        """
        The Random Forest produced higher values
        than the Decision Tree on all five reported
        final test metrics.
        """
    )


# ============================================================
# ABOUT PAGE
# ============================================================

elif page == "About":

    st.markdown(
        '<div class="section-title">'
        'ℹ️ About the Project'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        ### Research Question

        Can we predict whether an airline passenger
        is satisfied or neutral/dissatisfied based on
        passenger information, flight information,
        and service ratings?

        ### Dataset

        Airline Passenger Satisfaction

        ### Models

        - Decision Tree
        - Random Forest

        ### Evaluation

        The models were developed using the training
        data with 5-fold cross-validation.

        Hyperparameters were tuned using the training
        data before final evaluation on the separate
        test dataset.

        ### Target

        **0** — Neutral or dissatisfied

        **1** — Satisfied
        """
    )