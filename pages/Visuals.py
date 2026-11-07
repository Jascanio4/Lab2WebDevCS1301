import json
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.title("🏀 NBA Player Visualizations")
st.write("2024–25 regular-season averages for 50 NBA players.")

with open("data.json", "r") as file:
    data = json.load(file)

players = pd.DataFrame(data["players"])

st.header("1. Points per game")
ordered = players.sort_values("ppg")
fig1, ax1 = plt.subplots(figsize=(10, 13))
ax1.barh(ordered["name"], ordered["ppg"], color="#1769aa")
ax1.set_xlabel("Points per game")
ax1.set_ylabel("Player")
ax1.set_title("NBA points per game — 2024–25")
fig1.tight_layout()
st.pyplot(fig1)

st.header("2. Points vs. assists")

if "minimum_ppg" not in st.session_state:
    st.session_state.minimum_ppg = 0.0

minimum = st.slider("Minimum points per game", 0.0, 35.0, 0.0, 0.5, key="minimum_ppg")
filtered = players[players["ppg"] >= minimum]

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.scatter(filtered["ppg"], filtered["apg"], color="#d97706", s=100)
for _, player in filtered.iterrows():
    ax2.annotate(player["name"].split()[-1],
                 (player["ppg"], player["apg"]),
                 xytext=(5, 5), textcoords="offset points", fontsize=8)
fig2.tight_layout()
ax2.set_xlabel("Points per game")
ax2.set_ylabel("Assists per game")
ax2.set_title("Points vs. assists — filtered NBA players")
st.pyplot(fig2)

st.write(f"Showing {len(filtered)} out of {len(players)} players")

st.subheader("Extra credit: summary statistics")
if len(filtered) > 0:
    st.metric("Mean PPG", round(filtered["ppg"].mean(), 2))
    st.metric("Median PPG", round(filtered["ppg"].median(), 2))
else:
    st.write("No players meet the selected minimum.")

st.divider()
st.title("🏀 NBA Fan Survey Results")

survey = pd.read_csv("data.csv")

survey["Value"] = pd.to_numeric(survey["Value"], errors="coerce")
survey = survey.dropna(subset=["Category", "Value"])

if len(survey) == 0:
    st.warning("No survey responses have been submitted yet.")

else:
    st.header("3. Favorite NBA Teams")
    team_counts = survey["Category"].value_counts()

    fig3, ax3 = plt.subplots(figsize=(8, 6))
    ax3.pie(team_counts,labels=team_counts.index,autopct="%1.1f%%",startangle=90)
    ax3.set_title("Favorite NBA Teams Among Survey Respondents")
    st.pyplot(fig3)
    plt.close(fig3)

    st.write(f"Total survey responses: {len(survey)}")

    st.header("4. NBA Games Watched Per Week")

    if "minimum_games" not in st.session_state:
        st.session_state.minimum_games = 0

    minimum_games = st.slider("Minimum NBA games watched per week",0, 100, 0, 1,key="minimum_games")
    filtered_survey = survey[survey["Value"] >= minimum_games]

    if len(filtered_survey) > 0:
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.hist(filtered_survey["Value"],bins=10,color="#1769aa",edgecolor="black")
        ax4.set_title("NBA Games Watched Per Week")
        ax4.set_xlabel("Games Watched Per Week")
        ax4.set_ylabel("Number of Respondents")
        st.pyplot(fig4)
        plt.close(fig4)
        st.write(f"Showing {len(filtered_survey)} out of {len(survey)} survey responses")
        st.subheader("Survey Statistics")
        st.metric("Mean Games Watched",round(filtered_survey["Value"].mean(), 2))
        st.metric("Median Games Watched",round(filtered_survey["Value"].median(), 2))
    else:
        st.warning("No survey responses meet the selected minimum.")


