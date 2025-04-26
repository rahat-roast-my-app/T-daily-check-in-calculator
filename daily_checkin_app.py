
import streamlit as st
import pandas as pd

# Load the weight table
weights_df = pd.read_csv('data/Daily Check-in Weights v1.0.csv')

# Build the user-defined weight mapping
user_defined_weight_mapping = {}
for _, row in weights_df.iterrows():
    habit = row['Habit Name']
    score = int(row['User Input Score'])
    weight = float(row['Weight Applied'])
    user_defined_weight_mapping[(habit, score)] = weight

# Ordered habits
habits_in_order = weights_df['Habit Name'].unique().tolist()

def daily_check_in_calculator(current_testosterone, daily_scores):
    if len(daily_scores) != 20:
        raise ValueError("You must provide exactly 20 scores (one per habit).")
    weights_today = []
    for habit, score in zip(habits_in_order, daily_scores):
        weight = user_defined_weight_mapping.get((habit, score), 1.0)
        weights_today.append(weight)
    average_weight = sum(weights_today) / len(weights_today)
    updated_testosterone = current_testosterone * average_weight
    updated_testosterone = max(250, min(1100, round(updated_testosterone)))
    return updated_testosterone

st.title("🧠 Daily Testosterone Check-In Calculator")

st.markdown("""
Enter your current testosterone level and today's habit scores (1–10).  
We'll calculate your updated testosterone based on your real habits! 🚀
""")

base_testosterone = st.number_input("Enter your current/base testosterone (ng/dL):", min_value=250, max_value=1100, value=700)

st.subheader("Enter today's scores for each habit (1 to 10):")
daily_scores = []

for habit in habits_in_order:
    score = st.slider(habit, min_value=1, max_value=10, value=7)
    daily_scores.append(score)

if st.button("Calculate Updated Testosterone 🚀"):
    updated_testosterone = daily_check_in_calculator(base_testosterone, daily_scores)
    st.success(f"✅ Your updated testosterone level is: {updated_testosterone} ng/dL")
