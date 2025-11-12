import streamlit as st
import pandas as pd
import os
from github import Github
import io

# === CONFIGURATION DE LA PAGE ===
st.set_page_config(page_title="Suivi Joueuse RMBB", layout="centered")

# === LOGO RMBB ===
logo_url = "https://raw.githubusercontent.com/Marchais795/mon_projet_streamlit/main/image/Rouen%20Bihorel%20basket.png"

st.markdown(f"""
<div class="header-banner">
    <div class="top-text">🏀 Saison 2025-2026 — Championnat LF2</div>
    <div class="header-content">
        <img src="{logo_url}" width="80">
        <h1>Suivi de la Charge - RMBB</h1>
        <img src="{logo_url}" width="80">
    </div>
</div>
""", unsafe_allow_html=True)

# === STYLE GÉNÉRAL ===
st.markdown("""
<style>
body, .stApp { background-color: #e0e0e0; color: black; font-family: 'Segoe UI', sans-serif; }

.header-banner { width: 100%; background-color: #003366; color: white; padding: 15px 20px;
border-bottom: 4px solid #0055a5; border-radius: 0 0 15px 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }

.header-content { display: flex; justify-content: space-between; align-items: center; }
.header-content h1 { color: white; text-align: center; font-weight: 700; font-size: 1.8em; flex-grow: 1; }

.top-text { text-align: center; font-size: 1em; color: #cce0ff; margin-bottom: 5px; letter-spacing: 0.5px; }

.card { background-color: #ffffff; padding: 20px; border-radius: 15px;
box-shadow: 0 3px 12px rgba(0,0,0,0.08); margin-bottom: 25px; }

.info-card { background-color: #f5f5f5; border-left: 6px solid #0055a5;
padding: 20px; border-radius: 10px; margin-bottom: 25px; }

h4 { color: #003366; margin-bottom: 10px; border-left: 5px solid #0055a5; padding-left: 8px; }

.label-line { font-weight: bold; color: #003366; margin-bottom: 5px; }

.scale-button {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    margin: 3px;
    cursor: pointer;
    text-align: center;
}
.green { background-color: #4CAF50; }
.orange { background-color: #FFC107; }
.red { background-color: #F44336; }

.stButton>button {
    background-color: #003366;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
    width: 100%;
    transition: all 0.2s ease-in-out;
}
.stButton>button:hover { background-color: #0055a5; transform: scale(1.02); }

.success-msg { text-align: center; font-weight: bold; color: #003366; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# === CARTE D'INFO ===
st.markdown("""
<div class="info-card">
<h4>ℹ️ Pourquoi remplir ce suivi ?</h4>
<p>
Ce questionnaire permet de suivre ton état de forme et ta récupération au fil des jours.<br>
L’objectif est d’adapter la charge d’entraînement pour éviter la fatigue excessive et améliorer la performance.
</p>
<ul>
<li><b>État mental :</b> ton ressenti psychologique, motivation, concentration, stress, fatigue mentale.</li>
<li><b>État physique :</b> ton ressenti corporel, douleurs, énergie, sommeil.</li>
<li><b>Échelle de Borg :</b> perception de l’intensité de l’effort à l’entraînement.</li>
</ul>
<p style='font-size:0.9em; color:#444;'>
🟢 Bon / 🟠 Moyen / 🔴 Difficile
</p>
</div>
""", unsafe_allow_html=True)

# === NOM JOUEUSE ===
joueuse = st.text_input("👤 Nom et prénom de la joueuse")

# === FONCTION BOUTONS COULEURS ===
def choix_couleur(label, key):
    st.markdown(f"<div class='label-line'>{label}</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    result = None
    with col1:
        if st.button("🟢 Bon", key=f"{key}_vert"): result = "Vert"
    with col2:
        if st.button("🟠 Moyen", key=f"{key}_orange"): result = "Orange"
    with col3:
        if st.button("🔴 Difficile", key=f"{key}_rouge"): result = "Rouge"
    return result

# === BLOC MENTAL ===
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h4>🧠 État mental</h4>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    epanouissement = choix_couleur("Épanouissement personnel", "epanouissement")
    concentration = choix_couleur("Concentration", "concentration")
    stress = choix_couleur("Stress", "stress")

with col2:
    motivation = choix_couleur("Motivation", "motivation")
    fatigue_mentale = choix_couleur("Fatigue mentale", "fatigue_mentale")

st.markdown('</div>', unsafe_allow_html=True)

# === BLOC PHYSIQUE ===
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h4>💪 État physique</h4>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    douleurs = choix_couleur("Douleurs", "douleurs")
    energie = choix_couleur("Énergie", "energie")
with col2:
    sommeil = choix_couleur("Sommeil", "sommeil")

# === ÉCHELLE DE BORG ===
st.markdown('<div style="margin-top:20px;">', unsafe_allow_html=True)
st.markdown('<div class="label-line">Échelle de Borg (effort perçu à l’entraînement)</div>', unsafe_allow_html=True)
entrainement = st.slider("💥 De 0 (très facile) à 10 (effort maximal)", 0, 10, 5)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# === COMMENTAIRE ===
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h4>📝 Commentaire libre</h4>", unsafe_allow_html=True)
commentaire = st.text_area("Comment t’es-tu sentie aujourd’hui ?", "")
st.markdown('</div>', unsafe_allow_html=True)

# === ENVOI GITHUB ===
def push_to_github(df_new):
    token = os.getenv("GITHUB_TOKEN")
    repo_name = "Marchais795/mon_projet_streamlit"
    g = Github(token)
    repo = g.get_repo(repo_name)
    path = "suivi_joueuse.csv"

    try:
        contents = repo.get_contents(path)
        old_csv = io.StringIO(contents.decoded_content.decode())
        df_old = pd.read_csv(old_csv)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        repo.update_file(contents.path, "Mise à jour données", df_combined.to_csv(index=False), contents.sha)
    except:
        repo.create_file(path, "Ajout des données", df_new.to_csv(index=False))

# === SAUVEGARDE ===
if st.button("💾 Enregistrer mes données"):
    if not joueuse:
        st.error("⚠️ Merci d’entrer ton nom avant d’enregistrer.")
    else:
        df_new = pd.DataFrame({
            "Joueuse": [joueuse],
            "Épanouissement": [epanouissement],
            "Concentration": [concentration],
            "Stress": [stress],
            "Motivation": [motivation],
            "Fatigue_mentale": [fatigue_mentale],
            "Douleurs": [douleurs],
            "Énergie": [energie],
            "Sommeil": [sommeil],
            "Borg": [entrainement],
            "Commentaire": [commentaire]
        })
        push_to_github(df_new)
        st.success("✅ Données enregistrées avec succès sur GitHub !")
        st.markdown("<div class='success-msg'>Merci pour ta participation 💙</div>", unsafe_allow_html=True)
