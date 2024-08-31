import ezra_utils as utils_ai21
import ezra_utils_claude as utils_claude
import streamlit as st

# Add a selectbox for choosing between Claude and AI21
model_choice = st.radio(
    "Choose the AI model:",
    ("Free model", "Paid model"),
    index=0  # Default to Claude
)

# Convert the choice to a boolean for easier handling
use_claude = model_choice == "Claude"

if use_claude:
    utils_claude.main()
else:
    utils_ai21.main()
