import streamlit as st
import google.generativeai as genai
from datetime import datetime
from google.api_core.exceptions import NotFound

# Configuration de l'API Gemini avec la clé fournie
genai.configure(api_key="AIzaSyBvbTSuRvT3OPk2sFy_xWlD3winaX0fato")

st.set_page_config(page_title="Chatbot Citoyen - Noisy Avenir", page_icon="🗳️")
st.title("🤖 Chatbot Citoyen – Équipe Noisy Avenir")

st.markdown("""
Bienvenue sur le chatbot de campagne municipale de **Noisy-le-Grand** 🇫🇷  
Ce chatbot est proposé par l'équipe **Noisy Avenir**, menée par la maire actuelle **Brigitte Marsigny**.  
Posez vos questions sur le programme électoral 2026, ou laissez une suggestion !

👤 *Ce projet est soutenu par Hicham SABIL, membre de l’équipe municipale.*
""")

# Nouveau programme enrichi
programme = """
🗳️ Programme Municipal 2026 – Équipe Noisy Avenir

1. 🛡️ Sécurité :
- Renforcement de la police municipale et caméras intelligentes
- Création d'une brigade de médiation urbaine

2. 📚 Éducation & Jeunesse :
- Rénovation des écoles primaires
- Pass Loisirs Jeunes, Conseil Municipal des Jeunes

3. 🌱 Environnement :
- Plantation de 1000 arbres, budget participatif vert
- Nouvelles pistes cyclables et bâtiments publics rénovés

4. 🚍 Mobilité :
- Amélioration du réseau de bus, ticket unique communal
- Zéro dépôts sauvages : vidéosurveillance + sanctions

5. 🧓 Seniors :
- Accompagnement à domicile personnalisé
- Pass Bien Vieillir + activités intergénérationnelles

6. 🏛️ Démocratie locale :
- Maisons citoyennes de quartier
- Budget participatif et bilan citoyen annuel

7. 🏘️ Urbanisme :
- Urbanisme maîtrisé, logements accessibles
- Pôle économique autour de Noisy-Champs (Grand Paris Express)

8. ❤️ Solidarité :
- Renforcement des aides sociales
- Fonds Citoyen pour soutenir les initiatives locales
"""

# Bloc de question citoyenne
question = st.text_input("💬 Posez votre question au chatbot")

# Affichage des modèles disponibles (debug facultatif)
with st.expander("📋 Voir les modèles disponibles (optionnel)"):
    try:
        models = genai.list_models()
        for m in models:
            st.markdown(f"**{m.name}** — `{m.supported_generation_methods}`")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des modèles : {e}")

# Réponse IA
if question:
    with st.spinner("Noisy Avenir réfléchit à votre question..."):
        try:
            model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

            prompt = f"""
Tu es un assistant virtuel de l’équipe municipale *Noisy Avenir*, conduite par la maire actuelle **Brigitte Marsigny**.
Tu réponds aux citoyens de **Noisy-le-Grand** sur le programme électoral municipal de 2026.

Adopte un ton clair, pédagogique, et bienveillant.
Tu peux utiliser des listes, puces, ou structurer ta réponse.

Voici le programme du mandat :
{programme}

Question du citoyen :
{question}

Réponds maintenant :
"""

            response = model.generate_content(prompt)
            st.success(response.text)

        except NotFound:
            st.error("❌ Erreur : le modèle 'gemini-1.5-pro' est introuvable. Vérifie le nom.")
        except Exception as e:
            st.error(f"Une erreur est survenue : {str(e)}")

# Suggestions citoyennes
st.markdown("---")
st.subheader("📨 Vous avez une suggestion pour le programme ?")
suggestion = st.text_area("Votre suggestion")

if st.button("Envoyer ma suggestion"):
    if suggestion.strip():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("suggestions.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {suggestion}\n")
        st.success("Merci pour votre suggestion, elle a été enregistrée ! ✅")
    else:
        st.warning("Merci de remplir le champ avant d’envoyer.")
