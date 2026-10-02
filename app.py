from pathlib import Path
import html
import pickle

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import base64


st.set_page_config(
    page_title="Passenger Insights",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent
SERVICES = [
    "Inflight wifi service",
    "Departure/Arrival time convenient",
    "Ease of Online booking",
    "Gate location",
    "Food and drink",
    "Online boarding",
    "Seat comfort",
    "Inflight entertainment",
    "On-board service",
    "Leg room service",
    "Baggage handling",
    "Checkin service",
    "Inflight service",
    "Cleanliness",
]
METRICS = pd.DataFrame(
    {
        "Metric": ["Accuracy", "Precision", "Sensitivity", "Specificity", "ROC-AUC"],
        "Decision Tree": [0.9556, 0.9629, 0.9348, 0.9718, 0.9847],
        "Random Forest": [0.9631, 0.9711, 0.9440, 0.9780, 0.9941],
    }
)
MATRICES = {
    "Decision Tree": [[14119, 409], [741, 10624]],
    "Random Forest": [[14209, 319], [637, 10728]],
}
IMPORTANCE = {
    "Decision Tree": {
        "Online boarding": 0.3976,
        "Inflight wifi service": 0.1953,
        "Business travel": 0.1449,
        "Inflight entertainment": 0.0500,
        "Loyal customer": 0.0392,
        "Checkin service": 0.0259,
    },
    "Random Forest": {
        "Online boarding": 0.1699,
        "Inflight wifi service": 0.1461,
        "Business class": 0.0836,
        "Personal travel": 0.0665,
        "Business travel": 0.0545,
        "Inflight entertainment": 0.0510,
    },
}


@st.cache_resource
def load_model(path, modified):
    with open(path, "rb") as file:
        return pickle.load(file)


@st.cache_data
def load_passengers(paths):
    return pd.concat(
        [pd.read_csv(path) for path, modified in paths],
        ignore_index=True,
    )


with st.sidebar:
    st.title("✈ Passenger Insights")
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    theme_label = (
        "☀ Switch to light mode"
        if st.session_state.dark_mode
        else "☾ Switch to dark mode"
    )

    if st.button(theme_label, key="theme_button", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    dark = st.session_state.dark_mode
    font_size = st.slider("Text size", 18, 30, 22, format="%d px")
    selected_model = st.selectbox("Model", ["Random Forest", "Decision Tree"])
    st.divider()
    st.subheader("Passenger details")

    passenger = {
        "Gender": st.selectbox("Gender", ["Male", "Female"]),
        "Customer Type": st.selectbox(
            "Customer type",
            ["Loyal Customer", "disloyal Customer"],
            format_func=lambda value: (
                "Returning" if value == "Loyal Customer" else "First-time"
            ),
        ),
        "Type of Travel": st.selectbox(
            "Travel purpose", ["Business travel", "Personal Travel"]
        ),
        "Class": st.selectbox("Cabin class", ["Business", "Eco", "Eco Plus"]),
        "Age": st.number_input("Age", 7, 85, 35),
        "Flight Distance": st.number_input("Flight distance", 31, 4983, 1000),
        "Departure Delay in Minutes": st.number_input(
            "Departure delay (minutes)", 0, 2000, 0
        ),
        "Arrival Delay in Minutes": st.number_input(
            "Arrival delay (minutes)", 0, 2000, 0
        ),
    }

    st.subheader("Service ratings")
    st.caption("1 = lowest · 5 = highest · 0 = not applicable")

    for service in SERVICES:
        minimum = 1 if service == "Baggage handling" else 0
        passenger[service] = st.slider(service, minimum, 5, 3)


background = "#0b1220" if dark else "#f3f6fb"
surface = "#152238" if dark else "#ffffff"
text = "#edf3ff" if dark else "#16263f"
muted = "#b8c6dc" if dark else "#52647d"
border = "#32425c" if dark else "#dce5f1"
green = "#86efac" if dark else "#15803d"
red = "#fca5a5" if dark else "#b91c1c"
green_background = "#123426" if dark else "#ecfdf3"
red_background = "#3a202b" if dark else "#fff1f2"
input_background = "#2a3c56" if dark else "#eef3fa"

background_path = ROOT / "images" / "airline_background.png"
background_image = base64.b64encode(background_path.read_bytes()).decode()

background_overlay = (
    "rgba(11, 18, 32, 0.40)"
    if dark
    else "rgba(243, 246, 251, 0.15)"
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {background};
        color: {text};
    }}
    [data-testid="stHeader"] {{ background: {background}; }}
    [data-testid="stMainBlockContainer"] {{
        max-width: 1700px;
        padding-top: 2rem;
    }}
    [data-testid="stSidebar"] {{
        background: {surface};
        width: 410px !important;
        min-width: 390px;
        max-width: 450px;
        border-right: 1px solid {border};
    }}
    .stApp p, .stApp label, .stApp input,
    [data-baseweb="select"] span {{
        font-size: {font_size}px !important;
        line-height: 1.5 !important;
        color: {text};
    }}
    .stApp h1 {{ font-size: {font_size + 16}px !important; color: {text}; }}
    .stApp h2, .stApp h3 {{
        font-size: {font_size + 6}px !important;
        color: {text};
    }}
    [data-testid="stSidebar"] h1 {{ font-size: {font_size + 6}px !important; }}
    [data-testid="stCaptionContainer"] p {{
        font-size: {font_size - 2}px !important;
        color: {muted} !important;
    }}
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] * {{
        font-size: {font_size + 14}px !important;
        font-weight: 750;
        color: {text};
    }}
    [data-testid="stMetricLabel"] p {{ font-size: {font_size - 2}px !important; }}
    [data-testid="stSliderThumbValue"] {{ font-size: {font_size}px !important; }}
    [data-testid="stVerticalBlockBorderWrapper"] > div {{
        background: {surface};
        border-color: {border} !important;
        border-radius: 16px;
    }}
    [data-baseweb="select"] > div,
    [data-testid="stNumberInputContainer"] {{
        background: {background};
        color: {text};
    }}
    [data-baseweb="popover"] ul, [role="listbox"],
    [data-baseweb="popover"] li {{ background: {surface}; color: {text}; }}
    [data-testid="stTabs"] button p {{ font-size: {font_size}px !important; }}
    [data-testid="stButton"] button[kind="primary"] {{
        background: linear-gradient(180deg, #3974e8, #2457c5);
        border: 2px solid #1d4cae;
        border-radius: 12px;
        min-height: 64px;
        padding: 12px 26px;
        box-shadow: 0 4px 0 #173e8e;
        cursor: pointer;
    }}
    [data-testid="stButton"] button[kind="primary"] p {{
        color: white !important;
        font-weight: 750;
    }}
    [data-testid="stButton"] button[kind="primary"]:hover {{
        background: #1d4cae;
        transform: translateY(-1px);
    }}
    [data-testid="stButton"] button[kind="primary"]:active {{
        transform: translateY(3px);
        box-shadow: none;
    }}
    [data-testid="stButton"] button[kind="primary"]:focus-visible {{
        outline: 3px solid #93b4fc;
        outline-offset: 5px;
    }}
    .prediction {{
        padding: 24px;
        border-radius: 14px;
        margin-top: 16px;
        font-size: {font_size}px;
        border-left: 6px solid;
    }}
    .prediction strong {{
        display: block;
        font-size: {font_size + 16}px;
        line-height: 1.2;
        margin: 12px 0;
    }}
    .positive {{ background: {green_background}; color: {green}; }}
    .negative {{ background: {red_background}; color: {red}; }}
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div > div {{
        background-color: {surface} !important;
        color: {text} !important;
        min-height: 54px;
    }}
    [data-testid="stSelectbox"] [data-baseweb="select"] * {{
        color: {text} !important;
        font-size: {font_size}px !important;
    }}
    [data-testid="stSelectbox"] input {{
        background-color: transparent !important;
        -webkit-text-fill-color: {text} !important;
    }}
    [data-testid="stSelectbox"] svg,
    [data-testid="stNumberInput"] svg {{
        fill: {text} !important;
        color: {text} !important;
    }}
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [role="listbox"] {{
        background-color: {surface} !important;
        color: {text} !important;
    }}
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] li *,
    [role="option"],
    [role="option"] * {{
        font-size: {font_size}px !important;
        line-height: 1.5 !important;
        color: {text} !important;
    }}
    [data-baseweb="popover"] li,
    [role="option"] {{
        background-color: {surface} !important;
        padding-top: 12px !important;
        padding-bottom: 12px !important;
    }}
    [data-baseweb="popover"] li:hover,
    [role="option"]:hover,
    [role="option"][aria-selected="true"] {{
        background-color: {border} !important;
    }}
    [data-testid="stNumberInputContainer"],
    [data-testid="stNumberInputContainer"] input,
    [data-testid="stNumberInputContainer"] button {{
        background-color: {surface} !important;
        color: {text} !important;
        font-size: {font_size}px !important;
    }}
    div[data-baseweb="select"],
    div[data-baseweb="select"] div {{
        background-color: {surface} !important;
        color: {text} !important;
        font-size: {font_size}px !important;
    }}
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input {{
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
        font-size: {font_size}px !important;
        background-color: transparent !important;
    }}
    div[data-baseweb="select"] svg {{
        fill: {text} !important;
        color: {text} !important;
    }}
    [data-testid="stAppDeployButton"] button,
    [data-testid="stAppDeployButton"] button *,
    [data-testid="stToolbar"] button,
    [data-testid="stToolbar"] button * {{
        font-size: {font_size}px !important;
        color: {text} !important;
    }}
    [data-testid="stAppDeployButton"] button {{
        min-height: 46px;
        padding: 8px 18px;
        background: {surface} !important;
        border: 1px solid {border} !important;
        border-radius: 10px;
    }}
    .stApp div[data-baseweb="select"],
    .stApp div[data-baseweb="select"] div {{
        background: {input_background} !important;
        color: {text} !important;
        border-color: {border} !important;
    }}
    .stApp div[data-baseweb="select"] span,
    .stApp div[data-baseweb="select"] input {{
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stButton"] button {{
        background: {input_background} !important;
        color: {text} !important;
        border: 2px solid {border} !important;
        min-height: 54px;
        border-radius: 12px;
    }}
    [data-testid="stSidebar"] [data-testid="stButton"] button p {{
        color: {text} !important;
        font-size: {font_size}px !important;
        font-weight: 650;
    }}
    [data-testid="stMainMenu"] svg,
    [data-testid="stToolbar"] svg {{
        width: 26px !important;
        height: 26px !important;
        color: {text} !important;
        fill: {text} !important;
    }}
    [data-testid="stMainMenu"] button {{
        min-width: 46px;
        min-height: 46px;
    }}
    [data-testid="stMainMenuPopover"],
    [data-testid="stMainMenuPopover"] *,
    [data-testid="stMainMenuPopover"] button,
    [data-testid="stMainMenuPopover"] p {{
        font-size: {font_size}px !important;
        line-height: 1.5 !important;
        color: {text} !important;
    }}
    [data-testid="stMainMenuPopover"] {{
        min-width: 310px !important;
        background: {surface} !important;
        padding: 14px !important;
    }}
    [data-testid="stMainMenuPopover"] button {{
        min-height: 48px;
        background: {input_background} !important;
    }}
    @media (max-width: 700px) {{
        [data-testid="stSidebar"] {{
            width: 90vw !important;
            min-width: 0;
            max-width: 90vw;
        }}
    }}


        [role="combobox"],
    button[role="combobox"],
    [data-testid="stSelectbox"] [role="combobox"] {{
        background: {input_background} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        font-size: {font_size}px !important;
    }}

    [role="combobox"] *,
    button[role="combobox"] * {{
        color: {text} !important;
        -webkit-text-fill-color: {text} !important;
        font-size: {font_size}px !important;
    }}

        [data-testid="stSelectbox"] button,
    [data-testid="stSelectbox"] button *,
    [data-testid="stSelectbox"] [role="combobox"] ~ *,
    [data-testid="stSelectbox"] [role="combobox"] ~ * * {{
        background: {input_background} !important;
        background-color: {input_background} !important;
        color: {text} !important;
    }}

    [data-testid="stSelectbox"] svg {{
        color: {text} !important;
        fill: currentColor !important;
        background: transparent !important;
    }}

    .dataset-panel {{
    background: {surface};
    border: 1px solid {border};
    border-radius: 24px;
    padding: 28px;
    margin: 12px 0 26px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.06);
}}

.dataset-heading {{
    color: {text};
    font-size: {font_size + 8}px;
    font-weight: 750;
    margin-bottom: 22px;
}}

.dataset-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
}}

.dataset-card {{
    background: {input_background};
    border: 1px solid {border};
    border-top: 4px solid #3974e8;
    border-radius: 16px;
    padding: 24px 20px;
}}

.dataset-label {{
    color: {text};
    font-size: {font_size + 2}px;
    font-weight: 650;
    line-height: 1.35;
}}

.dataset-value {{
    color: {text};
    font-size: {font_size + 20}px;
    font-weight: 800;
    line-height: 1.2;
    margin: 14px 0 10px;
    font-variant-numeric: tabular-nums;
}}

.dataset-detail {{
    color: {muted};
    font-size: {font_size}px;
    line-height: 1.4;
}}

.dataset-note {{
    color: {muted};
    font-size: {font_size}px;
    line-height: 1.5;
    margin-top: 22px;
}}

[data-testid="stTabs"] [role="tablist"] {{
    background: {surface};
    border: 1px solid {border};
    border-radius: 18px;
    padding: 10px;
    gap: 10px;
    flex-wrap: wrap;
    height: auto;
    margin-bottom: 24px;
}}

[data-testid="stTabs"] [role="tab"] {{
    background: {input_background};
    color: {text} !important;
    border: 1px solid {border};
    border-radius: 12px;
    padding: 14px 24px;
    min-height: 62px;
    height: auto;
    flex: 1 1 auto;
}}

[data-testid="stTabs"] [role="tab"] p {{
    color: inherit !important;
    font-size: {font_size + 4}px !important;
    font-weight: 700 !important;
    white-space: nowrap;
}}

[data-testid="stTabs"] [role="tab"]:hover {{
    border-color: #3974e8;
    box-shadow: 0 3px 12px rgba(57, 116, 232, 0.15);
}}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    background: #285ed1 !important;
    border-color: #285ed1 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(40, 94, 209, 0.25);
}}

[data-testid="stTabs"] [data-baseweb="tab-highlight"],
[data-testid="stTabs"] [data-baseweb="tab-border"] {{
    display: none;
}}

@media (max-width: 1100px) {{
    .dataset-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
}}

@media (max-width: 600px) {{
    .dataset-grid {{
        grid-template-columns: 1fr;
    }}

    .dataset-panel {{
        padding: 18px;
    }}
}}

.airline-banner {{
    box-sizing: border-box;
    min-height: 260px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background-color: {background};
    background-image:
        linear-gradient({background_overlay}, {background_overlay}),
        url("data:image/png;base64,{background_image}");
    background-size: cover;
    background-position: center;
    border: 1px solid {border};
    border-radius: 22px;
    padding: 36px;
    margin-bottom: 24px;
}}

.airline-banner h1 {{
    margin: 0 0 18px;
    padding: 0;
    color: #102a43 !important;
    font-size: {font_size + 30}px !important;
    font-weight: 850 !important;
    line-height: 1.2;
    text-shadow: 0 1px 3px rgba(255, 255, 255, 0.8);
}}

.airline-banner p {{
    margin: 0;
    color: #183b56 !important;
    font-size: {font_size + 8}px !important;
    font-weight: 650 !important;
    line-height: 1.5;
    max-width: 900px;
    text-shadow: 0 1px 3px rgba(255, 255, 255, 0.8);
}}
    
    </style>
    """,
    unsafe_allow_html=True,
)


def show_chart(figure, height=420):
    figure.update_layout(
        height=height,
        paper_bgcolor=surface,
        plot_bgcolor=surface,
        font={"color": text, "size": font_size - 2},
        margin={"l": 20, "r": 30, "t": 30, "b": 30},
        legend={"orientation": "h", "y": 1.16},
        colorway=["#3974e8", "#24b7a4", "#f49b54"],
    )
    figure.update_xaxes(gridcolor=border, automargin=True)
    figure.update_yaxes(gridcolor=border, automargin=True)
    st.plotly_chart(
        figure,
        use_container_width=True,
        theme=None,
        config={"displayModeBar": False},
    )


st.markdown(
    '<div class="airline-banner">'
    '<h1>Airline passenger satisfaction</h1>'
    '<p>Predict passenger satisfaction and explore '
    'the results of two models.</p>'
    '</div>',
    unsafe_allow_html=True,
)

dataset_summary = [
    ("Total passengers", "129,880", "Original dataset"),
    ("Training passengers", "103,594", "After cleaning"),
    ("Test passengers", "25,893", "Used for evaluation"),
    ("Input features", "22", "Passenger and service details"),
]

cards = "".join(
    f"""
    <div class="dataset-card">
        <div class="dataset-label">{label}</div>
        <div class="dataset-value">{value}</div>
        <div class="dataset-detail">{detail}</div>
    </div>
    """
    for label, value, detail in dataset_summary
)

st.markdown(
    f"""
    <section class="dataset-panel">
        <div class="dataset-heading">Dataset overview</div>
        <div class="dataset-grid">{cards}</div>
        <div class="dataset-note">
            Cleaning removed 393 passengers with missing arrival delays
            and excluded two identifier columns.
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

model_filename = (
    "random_forest_model.pkl"
    if selected_model == "Random Forest"
    else "decision_tree_model.pkl"
)
model_path = ROOT / "models" / model_filename
model = None

if model_path.exists():
    try:
        model = load_model(str(model_path), model_path.stat().st_mtime_ns)
    except Exception as error:
        st.error(f"Could not load the model: {error}")

signature = (selected_model, tuple(passenger.items()))
if st.session_state.get("prediction_signature") != signature:
    st.session_state.pop("prediction", None)

workspace, analytics, comparison, about = st.tabs(
    ["Predict", "Passenger analytics", "Model results", "About the project"]
)

with workspace:
    with st.container(border=True):
        st.subheader("Check prediction")
        st.write("Set the passenger details on the left, then run the prediction.")
        clicked = st.button("▶ Predict satisfaction", type="primary", key="predict")

        if clicked:
            if model is None:
                st.warning(f"Model unavailable. Expected file: models/{model_filename}")
            else:
                try:
                    row = pd.DataFrame([passenger])
                    if hasattr(model, "feature_names_in_"):
                        row = row[list(model.feature_names_in_)]
                    predicted = model.predict(row)[0]
                    classes = list(model.classes_)
                    positive_index = (
                        classes.index(1) if 1 in classes else classes.index("satisfied")
                    )
                    probability = float(model.predict_proba(row)[0][positive_index])
                    st.session_state.prediction = {
                        "satisfied": predicted in (1, "satisfied"),
                        "probability": probability,
                    }
                    st.session_state.prediction_signature = signature
                except Exception as error:
                    st.error(f"Prediction failed: {error}")

        result = st.session_state.get("prediction")
        if result:
            label = "Satisfied" if result["satisfied"] else "Neutral or dissatisfied"
            style = "positive" if result["satisfied"] else "negative"
            probability = result["probability"]
            st.markdown(
                f'<div class="prediction {style}">'
                f'{html.escape(selected_model)} prediction'
                f'<strong>{label}</strong>'
                f'Estimated probability of satisfaction: {probability:.1%}'
                '</div>',
                unsafe_allow_html=True,
            )
            figure = go.Figure(
                go.Bar(
                    x=[probability, 1 - probability],
                    y=["Satisfied", "Neutral / dissatisfied"],
                    orientation="h",
                    marker_color=["#16a34a", "#dc2626"],
                    text=[f"{probability:.1%}", f"{1 - probability:.1%}"],
                    textposition="auto",
                )
            )
            figure.update_xaxes(range=[0, 1], tickformat=".0%")
            show_chart(figure, 250)
            st.caption("Changing an input clears this result. Probabilities are estimates.")
        else:
            st.info("Your prediction will appear here after you press the button.")

    with st.container(border=True):
        st.subheader("Which services did this passenger rate well?")
        st.write(
            "These bars show the ratings selected on the left. "
            "Longer bars mean a higher rating; they are not dataset averages."
        )
        ratings = pd.DataFrame(
            {"Service": SERVICES, "Rating": [passenger[name] for name in SERVICES]}
        ).sort_values("Rating")
        figure = px.bar(
            ratings,
            x="Rating",
            y="Service",
            orientation="h",
            text="Rating",
            color_discrete_sequence=["#3974e8"],
        )
        figure.update_xaxes(range=[0, 5.6], dtick=1, title="Your rating (0–5)")
        figure.update_yaxes(title=None)
        figure.update_traces(textposition="outside", cliponaxis=False)
        show_chart(figure, max(580, font_size * 28))

with analytics:
    paths = [ROOT / "data" / "train.csv", ROOT / "data" / "test.csv"]
    if not all(path.exists() for path in paths):
        paths = [
            ROOT / "prepared_data" / "train_prepared.csv",
            ROOT / "prepared_data" / "test_prepared.csv",
        ]

    if not all(path.exists() for path in paths):
        st.info("Add your two data CSV files to enable passenger analytics.")
    else:
        try:
            passengers = load_passengers(
                tuple((str(path), path.stat().st_mtime_ns) for path in paths)
            )
            st.caption("Source: " + ", ".join(str(p.relative_to(ROOT)) for p in paths))
            filtered = passengers.copy()
            filter_columns = st.columns(3)
            for column, field in zip(
                filter_columns, ["Customer Type", "Class", "Type of Travel"]
            ):
                choice = column.selectbox(
                    field,
                    ["All"] + sorted(passengers[field].dropna().unique().tolist()),
                    key="filter_" + field,
                )
                if choice != "All":
                    filtered = filtered[filtered[field] == choice]

            if filtered.empty:
                st.info("No passengers match these filters.")
            else:
                satisfied = filtered["satisfaction"].eq("satisfied")
                columns = st.columns(3)
                columns[0].metric("Passengers", f"{len(filtered):,}")
                columns[1].metric("Satisfied", f"{satisfied.sum():,}")
                columns[2].metric("Satisfaction rate", f"{satisfied.mean():.1%}")

                with st.container(border=True):
                    st.subheader("Satisfaction by cabin class")
                    grouped = (
                        filtered.assign(Satisfied=satisfied)
                        .groupby(["Class", "Customer Type"])["Satisfied"]
                        .mean()
                        .mul(100)
                        .reset_index()
                    )
                    figure = px.bar(
                        grouped,
                        x="Class",
                        y="Satisfied",
                        color="Customer Type",
                        barmode="group",
                    )
                    figure.update_yaxes(range=[0, 100], title="Satisfied passengers (%)")
                    show_chart(figure)

                with st.container(border=True):
                    st.subheader("Average service ratings in the dataset")
                    averages = filtered[SERVICES].mean().sort_values().reset_index()
                    averages.columns = ["Service", "Average rating"]
                    figure = px.bar(
                        averages,
                        x="Average rating",
                        y="Service",
                        orientation="h",
                        text_auto=".2f",
                        color_discrete_sequence=["#3974e8"],
                    )
                    figure.update_xaxes(range=[0, 5.6])
                    figure.update_yaxes(title=None)
                    show_chart(figure, max(580, font_size * 28))
                    st.caption("Averages include 0 ratings, coded as not applicable.")

                with st.container(border=True):
                    st.subheader("Satisfied vs. neutral or dissatisfied")
                    counts = filtered["satisfaction"].value_counts()
                    figure = go.Figure(
                        go.Bar(
                            x=counts.index,
                            y=counts.values,
                            text=counts.values,
                            textposition="auto",
                            marker_color=[
                                "#16a34a" if label == "satisfied" else "#dc2626"
                                for label in counts.index
                            ],
                        )
                    )
                    figure.update_yaxes(title="Passengers")
                    show_chart(figure)
        except Exception as error:
            st.error(f"Could not load passenger analytics: {error}")

with comparison:
    st.subheader("How well do the models perform?")
    st.write("Saved final test results from your notebooks, using 25,893 passengers.")
    columns = st.columns(3)
    for column, index in zip(columns, [0, 1, 2]):
        column.metric(
            METRICS.loc[index, "Metric"],
            f"{METRICS.loc[index, selected_model]:.2%}",
        )

    with st.container(border=True):
        st.subheader("Decision Tree vs. Random Forest")
        figure = px.bar(
            METRICS.melt(id_vars="Metric", var_name="Model", value_name="Score"),
            x="Metric",
            y="Score",
            color="Model",
            barmode="group",
            text_auto=".1%",
        )
        figure.update_yaxes(range=[0, 1.12], tickformat=".0%", title="Test score")
        show_chart(figure, 480)
        st.write("Random Forest accuracy: 96.31%. Decision Tree accuracy: 95.56%.")

    with st.container(border=True):
        st.subheader("Which inputs does the model rely on most?")
        st.write(
            "Larger bars mean a greater contribution to the model’s decisions "
            "overall. They do not explain a particular passenger’s prediction."
        )
        important = pd.DataFrame(
            IMPORTANCE[selected_model].items(), columns=["Input", "Importance"]
        ).sort_values("Importance")
        figure = px.bar(
            important,
            x="Importance",
            y="Input",
            orientation="h",
            text_auto=".1%",
            color_discrete_sequence=["#3974e8"],
        )
        figure.update_xaxes(tickformat=".0%")
        figure.update_yaxes(title=None)
        show_chart(figure, 440)
        st.caption("Top six features from the saved notebook results; importance is not causation.")

    with st.container(border=True):
        st.subheader("Correct predictions and mistakes")
        st.write("Rows show actual labels. Columns show predicted labels.")
        labels = ["Neutral / dissatisfied", "Satisfied"]
        matrix = MATRICES[selected_model]
        figure = go.Figure(
            go.Heatmap(
                z=matrix,
                x=labels,
                y=labels,
                text=matrix,
                texttemplate="%{text:,}",
                textfont={"size": font_size + 4},
                colorscale=[[0, background], [1, "#3974e8"]],
                showscale=False,
            )
        )
        figure.update_xaxes(title="Predicted label")
        figure.update_yaxes(title="Actual label", autorange="reversed")
        show_chart(figure, 480)
        st.caption("The diagonal cells are correct predictions; the other two cells are mistakes.")

with about:
    st.subheader("About the project")
    st.write(
        "This project explores whether passenger details, flight delays and "
        "service ratings can predict airline passenger satisfaction. "
        "The outcome is either satisfied or neutral/dissatisfied."
    )
    st.subheader("How the models were developed")
    st.write(
        "The data was cleaned by removing identifiers and rows with missing "
        "arrival delays. Categorical inputs were encoded inside each model pipeline. "
        "A Decision Tree and a Random Forest were tuned using stratified "
        "5-fold cross-validation on the training set. Both were then evaluated "
        "on the separate test set."
    )
    st.subheader("Understanding the results")
    st.write(
        "Accuracy measures the share of correct predictions. Precision measures "
        "how often passengers predicted as satisfied were actually satisfied. "
        "Sensitivity measures how many truly satisfied passengers were identified. "
        "Specificity measures how many neutral/dissatisfied passengers were identified. "
        "ROC-AUC measures how well a model separates the two groups."
    )
    st.caption("Target coding: 0 = neutral or dissatisfied; 1 = satisfied.")
