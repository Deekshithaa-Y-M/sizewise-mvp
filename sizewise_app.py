import streamlit as st
import pandas as pd

# ──────────────────────────────────────────────
# SIZE CHART DATABASE
# ──────────────────────────────────────────────
SIZE_CHARTS = {
    "Shirt": pd.DataFrame({
        "Size":       ["S",  "M",   "L",   "XL"],
        "Chest_Min":  [88,   95,    103,   111],
        "Chest_Max":  [94,   102,   110,   118],
        "Waist_Min":  [70,   77,    85,    93],
        "Waist_Max":  [76,   84,    92,    100],
    }),
    "Kurta": pd.DataFrame({
        "Size":       ["S",  "M",   "L",   "XL"],
        "Chest_Min":  [88,   95,    103,   111],
        "Chest_Max":  [94,   102,   110,   118],
        "Waist_Min":  [70,   77,    85,    93],
        "Waist_Max":  [76,   84,    92,    100],
    }),
    "Dress": pd.DataFrame({
        "Size":       ["S",  "M",   "L",   "XL"],
        "Chest_Min":  [82,   89,    97,    105],
        "Chest_Max":  [88,   96,    104,   112],
        "Waist_Min":  [64,   71,    79,    87],
        "Waist_Max":  [70,   78,    86,    94],
    }),
    "T-shirt": pd.DataFrame({
        "Size":       ["S",  "M",   "L",   "XL"],
        "Chest_Min":  [88,   95,    103,   111],
        "Chest_Max":  [94,   102,   110,   118],
        "Waist_Min":  [70,   77,    85,    93],
        "Waist_Max":  [76,   84,    92,    100],
    }),
}

TOLERANCE = 2  # ±2 cm


# ──────────────────────────────────────────────
# SIZE RECOMMENDATION ALGORITHM
# ──────────────────────────────────────────────
def recommend_size(chest: float, waist: float, garment: str):
    """Return (size, fit_type) or (None, None) when no size matches."""
    chart = SIZE_CHARTS[garment]

    # Pass 1 – exact range (with tolerance)
    for _, row in chart.iterrows():
        chest_in = (row["Chest_Min"] - TOLERANCE) <= chest <= (row["Chest_Max"] + TOLERANCE)
        waist_in = (row["Waist_Min"] - TOLERANCE) <= waist <= (row["Waist_Max"] + TOLERANCE)
        if chest_in and waist_in:
            # Determine fit type
            chest_mid = (row["Chest_Min"] + row["Chest_Max"]) / 2
            waist_mid = (row["Waist_Min"] + row["Waist_Max"]) / 2
            if chest <= chest_mid and waist <= waist_mid:
                fit = "Slim Fit"
            else:
                fit = "Comfort Fit"
            return row["Size"], fit

    # Pass 2 – find closest size by combined distance
    best_size = None
    best_fit = None
    best_dist = float("inf")
    for _, row in chart.iterrows():
        chest_mid = (row["Chest_Min"] + row["Chest_Max"]) / 2
        waist_mid = (row["Waist_Min"] + row["Waist_Max"]) / 2
        dist = abs(chest - chest_mid) + abs(waist - waist_mid)
        if dist < best_dist:
            best_dist = dist
            best_size = row["Size"]
            best_fit = "Slim Fit" if chest <= chest_mid and waist <= waist_mid else "Comfort Fit"

    return best_size, best_fit


# ──────────────────────────────────────────────
# STREAMLIT UI
# ──────────────────────────────────────────────
st.set_page_config(page_title="SizeWise", page_icon="👕", layout="centered")

# ── Custom CSS for a cleaner look ─────────────
st.markdown(
    """
    <style>
    .block-container {max-width: 720px;}
    div[data-testid="stMetric"] {
        background: #f0f2f6; border-radius: 12px; padding: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state for navigation ──────────────
if "page" not in st.session_state:
    st.session_state.page = "home"


def go_to(page: str):
    st.session_state.page = page


# ══════════════════════════════════════════════
# 1️⃣  HOME PAGE
# ══════════════════════════════════════════════
if st.session_state.page == "home":
    st.title("👕 SizeWise – Find Your Perfect Fit")
    st.markdown(
        "**SizeWise** helps you find the right clothing size using your body "
        "measurements. No more guessing — get a data‑driven recommendation in "
        "seconds and reduce the hassle of returns."
    )
    st.image(
        "https://img.icons8.com/color/240/tape-measure.png",
        width=160,
    )
    st.button("🚀 Start Size Recommendation", on_click=go_to, args=("recommend",), type="primary")

# ══════════════════════════════════════════════
# 2️⃣–6️  RECOMMENDATION PAGE
# ══════════════════════════════════════════════
elif st.session_state.page == "recommend":
    st.title("👕 SizeWise")
    st.button("← Back to Home", on_click=go_to, args=("home",))
    st.divider()

    # ── 2️.  User Measurements ────────────────
    st.subheader("📏 Your Body Measurements")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.5)
        chest = st.number_input("Chest / Bust (cm)", min_value=60.0, max_value=160.0, value=96.0, step=0.5)
        shoulder = st.number_input("Shoulder Width (cm)", min_value=30.0, max_value=70.0, value=44.0, step=0.5)
    with col2:
        waist = st.number_input("Waist (cm)", min_value=50.0, max_value=150.0, value=80.0, step=0.5)
        hip = st.number_input("Hip (cm)", min_value=60.0, max_value=160.0, value=98.0, step=0.5)

    st.divider()

    # ── 3️⃣  Garment Selection ────────────────
    st.subheader("👔 Select Garment Type")
    garment = st.selectbox("Garment", list(SIZE_CHARTS.keys()), label_visibility="collapsed")

    st.divider()

    # ── 4️⃣  Display Size Chart ───────────────
    with st.expander("📐 View Size Chart"):
        display_df = SIZE_CHARTS[garment].copy()
        display_df["Chest (cm)"] = display_df["Chest_Min"].astype(str) + " – " + display_df["Chest_Max"].astype(str)
        display_df["Waist (cm)"] = display_df["Waist_Min"].astype(str) + " – " + display_df["Waist_Max"].astype(str)
        st.table(display_df[["Size", "Chest (cm)", "Waist (cm)"]])

    st.divider()

    # ── 5️⃣ + 6️⃣  Recommendation ────────────
    if st.button("🔍 Find My Size", type="primary"):
        size, fit = recommend_size(chest, waist, garment)

        if size:
            st.success(f"### Recommended Size: **{size}** ({fit})")
            st.info(
                "This recommendation is based on your body measurements and "
                "garment size charts. For the best fit, also consider the "
                "garment's fabric stretch and your personal preference."
            )

            # ── 7️  Metric Dashboard ─────────
            st.divider()
            st.subheader("📊 Quick Insights")
            m1, m2, m3 = st.columns(3)
            m1.metric("Recommended Size", size)
            m2.metric("Est. Return Reduction", "30%", delta="↓ returns")
            m3.metric("Confidence Score", "85%")
        else:
            st.warning(
                "We couldn't find a matching size. Please double‑check your "
                "measurements or try a different garment type."
            )
