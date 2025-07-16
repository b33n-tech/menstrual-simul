import streamlit as st

# Correspondance tags <-> phases et "intérêt" (simplifié)
PHASE_TAGS_MAP = {
    "Menstruation": {"repos": 0.9, "créatif_doux": 0.8, "logistique": 0.5, "social": 0.3, "physique": 0.2, "communication": 0.4},
    "Folliculaire": {"créatif": 0.9, "exploration": 0.8, "apprentissage": 0.7, "social": 0.6, "physique": 0.6, "logistique": 0.5},
    "Ovulation": {"social": 0.9, "communication": 0.9, "leadership": 0.8, "physique": 0.7, "créatif": 0.6, "logistique": 0.4},
    "Lutéale": {"exécutif": 0.8, "analytique": 0.7, "automatisme": 0.6, "repos": 0.5, "logistique": 0.6, "créatif_doux": 0.4}
}

PHASES_ORDER = ["Menstruation", "Folliculaire", "Ovulation", "Lutéale"]

def get_phase(day, cycle_length=28):
    if 1 <= day <= 5:
        return "Menstruation"
    elif 6 <= day <= 14:
        return "Folliculaire"
    elif 15 <= day <= 17:
        return "Ovulation"
    elif 18 <= day <= cycle_length:
        return "Lutéale"
    else:
        return "Inconnu"

st.title("🔮 Simulateur d’adoption d’activité selon le cycle")

cycle_length = st.slider("Durée moyenne du cycle (jours)", 21, 35, 28)
day = st.number_input("Jour actuel du cycle", 1, cycle_length, 1)

phase = get_phase(day, cycle_length)
st.write(f"Phase actuelle détectée : **{phase}**")

activity_name = st.text_input("Nom de l'activité proposée")

tags_list = [
    "social", "créatif", "créatif_doux", "exploration",
    "apprentissage", "leadership", "physique",
    "logistique", "communication", "exécutif",
    "analytique", "automatisme", "repos"
]

selected_tags = st.multiselect("Sélectionnez jusqu'à 3 tags correspondant à l'activité", tags_list, max_selections=3)

if activity_name and selected_tags:
    phase_scores = PHASE_TAGS_MAP.get(phase, {})
    if not phase_scores:
        st.warning("Phase inconnue, impossible de calculer les scores.")
    else:
        # Calcul du score d'alignement moyen avec la phase actuelle
        scores = [phase_scores.get(tag, 0.1) for tag in selected_tags]  # 0.1 si tag inconnu
        alignement = sum(scores) / len(scores) if scores else 0

        # Estimation du % de succès d’adoption : 
        # on simule que tags très bien alignés avec la phase et quelques règles basiques
        # Ici on fait simple : plus le score est élevé, meilleur le succès.
        succes_adoption = alignement * 100  # en pourcentage

        st.markdown(f"### Résultats pour l'activité **{activity_name}** :")
        st.write(f"- **% de succès potentiel d’adoption** : {succes_adoption:.1f}%")
        st.write(f"- **% d’alignement avec le rythme actuel ({phase})** : {alignement*100:.1f}%")

        if succes_adoption > 70:
            st.success("💡 Cette activité semble bien adaptée et a de bonnes chances d’être adoptée !")
        elif succes_adoption > 40:
            st.info("ℹ️ Cette activité a un potentiel moyen, à envisager avec prudence.")
        else:
            st.warning("⚠️ Cette activité risque de ne pas bien correspondre au moment actuel.")
else:
    st.info("Entrez le nom de l’activité et sélectionnez les tags pour obtenir une estimation.")
