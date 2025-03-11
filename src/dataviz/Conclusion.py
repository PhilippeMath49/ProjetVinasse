import streamlit as st

def main():
    # Configuration de la page
    st.set_page_config(page_title="Conclusion - Qualité du Vin", layout="centered")

    # Titre principal
    st.title("Conclusion sur la Qualité du Vin")

    # Présentation de la conclusion
    st.write("## Facteurs clés de la qualité du vin")
    st.write("- Le principal facteur de la qualité du vin est **l'alcool**.")
    st.write("- Pour obtenir un vin de qualité, **l'ensoleillement et le type de sol** sont nécessaires.")

    st.write("## Déduction")
    st.write("En combinant ces éléments, on peut en déduire que les régions viticoles émergentes de demain posséderont :")
    st.write("- **Un climat offrant un ensoleillement optimal** pour favoriser la maturation du raisin.")
    st.write("- **Des sols riches et adaptés** à la culture de la vigne.")
    st.write("- **Des conditions propices à un bon taux d'alcool dans le vin.**")

    st.write("## Perspectives")
    st.write("Ainsi, les futures puissances viticoles pourraient être des régions qui remplissent ces conditions. Certaines zones aujourd’hui en développement pourraient devenir des références en matière de production de vin de qualité.")

    # Interaction avec l'utilisateur
    st.write("### Selon vous, quelles régions pourraient émerger dans le futur ?")
    region = st.text_input("Entrez une région potentielle :")
    if region:
        st.write(f"🌍 {region} pourrait bien être une future terre d'excellence pour le vin !")