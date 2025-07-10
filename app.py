import streamlit as st
import random

st.set_page_config(page_title="Team Bracket Picker", layout="centered")
st.title("🏆 Team Bracket Picker with Groups A & B")

# Fixed teams
fixed_teams = ["UOM", "USJ", "UOC", "UOP", "SUSL", "UWU"]

# Default group names as team entries
default_group_A = "Jaffna"
default_group_B = "Jaffna Legends"

# Initialize session state variables
if "randomize_count" not in st.session_state:
    st.session_state.randomize_count = 0

# Random assignment button
if st.session_state.randomize_count < 2:
    if st.button("🎲 Randomly Assign Numbers to Teams"):
        shuffled_teams = random.sample(fixed_teams, len(fixed_teams))
        st.session_state.team_order = {i + 1: shuffled_teams[i] for i in range(6)}
        st.session_state.color_to_group = {}
        st.session_state.revealed_colors = {}
        st.session_state.team_picks = {}
        st.session_state.current_number = 1
        st.session_state.randomize_count += 1

        # Color setup and random group assignment
        colors = ["🔴 Red", "🔵 Blue", "🟢 Green", "🟠 Orange", "🟣 Purple", "🟡 Yellow"]
        group_labels = ["A", "A", "A", "B", "B", "B"]
        shuffled_groups = random.sample(group_labels, len(group_labels))

        for i, color in enumerate(colors):
            st.session_state.color_to_group[color] = shuffled_groups[i]
            st.session_state.revealed_colors[color] = False
else:
    st.warning("⚠️ You have already randomized twice. Final team order is locked.")

# Main display
if "team_order" in st.session_state:
    st.markdown("### 📋 Team Number Assignments")
    card_cols = st.columns(3)
    for i in range(1, 7):
        team = st.session_state.team_order[i]
        with card_cols[(i - 1) % 3]:
            st.markdown(
                f"""
                <div style="border: 1px solid #ccc; border-radius: 8px; padding: 10px;
                            text-align: center; background-color: #fff;
                            box-shadow: 1px 1px 4px rgba(0,0,0,0.05); margin-bottom: 8px;">
                    <div style="font-size: 14px; color: #555;">Number</div>
                    <div style="font-size: 20px; font-weight: bold; color: #4CAF50;">{i}</div>
                    <div style="font-size: 14px; font-weight: bold; color: #333; margin-top: 4px;">{team}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Current team to pick color
    current_number = st.session_state.current_number
    if current_number <= 6:
        current_team = st.session_state.team_order[current_number]
        st.subheader(f"🎯 Team **{current_team}** (Number {current_number}), pick a color:")
    else:
        st.success("✅ All teams have picked colors!")

    # Color picking interface
    cols = st.columns(3)
    colors = list(st.session_state.color_to_group.keys())
    for i, color in enumerate(colors):
        col = cols[i % 3]
        with col:
            if st.session_state.revealed_colors[color]:
                picked_by = [k for k, v in st.session_state.team_picks.items() if v == color][0]
                st.success(f"{color} → {picked_by}")
            elif current_number <= 6:
                if st.button(color):
                    team = st.session_state.team_order[current_number]
                    st.session_state.team_picks[team] = color
                    st.session_state.revealed_colors[color] = True
                    st.session_state.current_number += 1
                    st.rerun()

    # Show grouped teams only if all have picked
    if st.session_state.current_number > 6:
        st.divider()
        st.markdown("### 👥 Group Teams")

        group_a_teams = [default_group_A]
        group_b_teams = [default_group_B]

        for team, color in st.session_state.team_picks.items():
            group = st.session_state.color_to_group[color]
            if group == "A":
                group_a_teams.append(team)
            else:
                group_b_teams.append(team)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🅰️ Group A")
            for t in group_a_teams:
                st.write(f"- {t}")
        with col2:
            st.markdown("#### 🅱️ Group B")
            for t in group_b_teams:
                st.write(f"- {t}")

    # Reset button
    st.divider()
    if st.button("🔄 Reset All"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
