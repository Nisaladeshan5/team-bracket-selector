import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

# -------------------- Firebase Setup --------------------

# Upload your service account JSON in Streamlit sidebar
st.sidebar.title("Firebase Setup")
firebase_file = st.sidebar.file_uploader("Upload Firebase Service Account JSON", type="json")

if firebase_file and "firebase_initialized" not in st.session_state:
    cred = credentials.Certificate(json.load(firebase_file))
    firebase_admin.initialize_app(cred)
    st.session_state["firebase_initialized"] = True
    db = firestore.client()
elif "firebase_initialized" in st.session_state:
    db = firestore.client()
else:
    st.warning("Please upload your Firebase credentials in the sidebar to begin.")
    st.stop()

# -------------------- Configuration --------------------

# Map colors to brackets
color_bracket_map = {
    "Red": "A",
    "Blue": "A",
    "Green": "A",
    "Orange": "B",
    "Purple": "B",
    "Yellow": "B"
}

colors = list(color_bracket_map.keys())

# Firestore collection name
COLLECTION = "team_brackets"

# -------------------- UI --------------------

st.title("🏆 Team Bracket Selector")
st.write("Select a color. Behind each color is a hidden bracket assignment (A or B).")

# Load taken colors from Firestore
taken_docs = db.collection(COLLECTION).stream()
taken_colors = {doc.id: doc.to_dict() for doc in taken_docs}

# Display buttons for colors
cols = st.columns(3)
for i, color in enumerate(colors):
    with cols[i % 3]:
        if color in taken_colors:
            st.button(f"{color} ❌ (Taken)", disabled=True, key=color)
        else:
            if st.button(color, key=color):
                # Assign bracket and store selection
                bracket = color_bracket_map[color]
                db.collection(COLLECTION).document(color).set({
                    "bracket": bracket
                })
                st.success(f"You selected {color} and you are in **Bracket {bracket}**")
                st.experimental_rerun()  # Refresh to disable color for others

# -------------------- Reset Button (admin use only) --------------------

with st.sidebar.expander("🔐 Admin: Reset Selections"):
    if st.button("Reset All Selections"):
        for color in colors:
            db.collection(COLLECTION).document(color).delete()
        st.success("All selections have been reset.")
        st.experimental_rerun()
