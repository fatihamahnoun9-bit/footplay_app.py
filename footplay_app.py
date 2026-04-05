import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import re

# Configuration de la page - Style mobile
st.set_page_config(
    page_title="FootPlay - Réservation de Terrains",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Palette de couleurs élégante
COLORS = {
    'primary': '#6C5CE7',
    'secondary': '#A29BFE',
    'accent': '#00CEC9',
    'success': '#00B894',
    'warning': '#FDCB6E',
    'danger': '#FF7675',
    'dark': '#2D3436',
    'light': '#F9F9F9',
    'white': '#FFFFFF',
    'gradient1': '#6C5CE7',
    'gradient2': '#A29BFE',
    'card_bg': '#FFFFFF',
    'text': '#2D3436',
    'text_light': '#636E72'
}

# CSS Style Mobile Élégant
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, #F5F7FA 0%, #E8ECF1 100%);
        font-family: 'Inter', sans-serif;
    }}
    
    .main-header {{
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['secondary']});
        border-radius: 30px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 35px rgba(108, 92, 231, 0.2);
        position: relative;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '⚽🏆🥅';
        position: absolute;
        right: -20px;
        bottom: -20px;
        font-size: 80px;
        opacity: 0.1;
    }}
    
    .title-main {{
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }}
    
    .subtitle {{
        font-size: 0.85rem;
        color: rgba(255,255,255,0.85);
    }}
    
    .card-modern {{
        background: {COLORS['white']};
        border-radius: 25px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 1px solid rgba(108, 92, 231, 0.1);
    }}
    
    .card-modern:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(108, 92, 231, 0.15);
    }}
    
    .terrain-card {{
        background: {COLORS['white']};
        border-radius: 20px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border-left: 4px solid {COLORS['primary']};
    }}
    
    .terrain-card:hover {{
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.12);
    }}
    
    .badge-elegant {{
        display: inline-block;
        background: linear-gradient(135deg, {COLORS['primary']}10, {COLORS['secondary']}10);
        border-radius: 50px;
        padding: 0.3rem 1rem;
        margin: 0.2rem;
        font-size: 0.75rem;
        color: {COLORS['primary']};
        font-weight: 500;
    }}
    
    .time-slot {{
        background: {COLORS['light']};
        border-radius: 15px;
        padding: 0.6rem;
        text-align: center;
        font-size: 0.8rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        margin: 0.2rem;
    }}
    
    .time-slot:hover {{
        background: {COLORS['primary']};
        color: white;
        transform: scale(1.02);
    }}
    
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
        border-radius: 15px !important;
        border: 1px solid #E0E0E0 !important;
        padding: 0.8rem !important;
        font-size: 0.9rem !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 2px {COLORS['primary']}20 !important;
    }}
    
    .avatar {{
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['secondary']});
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: bold;
        color: white;
    }}
    
    .toast-success {{
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        background: {COLORS['success']};
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        z-index: 1001;
        animation: slideUp 0.3s ease;
    }}
    
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateX(-50%) translateY(20px); }}
        to {{ opacity: 1; transform: translateX(-50%) translateY(0); }}
    }}
    
    .contact-section {{
        background: linear-gradient(135deg, {COLORS['primary']}05, {COLORS['secondary']}05);
        border-radius: 25px;
        padding: 1.5rem;
        margin: 1rem 0;
    }}
    
    .annonce-card {{
        background: {COLORS['white']};
        border-radius: 20px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #FFE0B2;
        border-left: 4px solid {COLORS['warning']};
    }}
    
    .footer {{
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        background: {COLORS['white']};
        border-radius: 20px;
        font-size: 0.8rem;
        color: {COLORS['text_light']};
    }}
    
    .avis-card {{
        background: {COLORS['light']};
        border-radius: 20px;
        padding: 1rem;
        margin: 0.5rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# Initialisation des sessions
if 'reservations' not in st.session_state:
    st.session_state.reservations = []
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 'home'
if 'toast' not in st.session_state:
    st.session_state.toast = None
if 'user' not in st.session_state:
    st.session_state.user = {'name': '', 'phone': '', 'is_logged': False}
if 'contact_messages' not in st.session_state:
    st.session_state.contact_messages = []
if 'annonces' not in st.session_state:
    st.session_state.annonces = [
        {"titre": "🏆 Tournoi Amical", "date": "15 Avril 2026", "lieu": "Meknès", "places": 8, "prix": 50},
        {"titre": "⚽ Match Amical", "date": "18 Avril 2026", "lieu": "Fès", "places": 6, "prix": 30},
        {"titre": "🎯 Séance d'entraînement", "date": "20 Avril 2026", "lieu": "Rabat", "places": 10, "prix": 20},
    ]
if 'avis' not in st.session_state:
    st.session_state.avis = [
        {"user": "Karim", "note": 5, "commentaire": "Super application, réservation facile !", "date": "01/04/2026"},
        {"user": "Sofia", "note": 5, "commentaire": "Les terrains sont de qualité", "date": "30/03/2026"},
        {"user": "Amine", "note": 4, "commentaire": "Bien mais peut mieux faire", "date": "28/03/2026"},
    ]

# Données des terrains - TOUTES LES VILLES DU MAROC
TERRAINS = [
    # Meknès
    {"id": 1, "nom": "Complexe Sportif Al Massira", "ville": "Meknès", "prix": 200, "type": "Pelouse synthétique", "note": 4.7, "image": "🏟️", "adresse": "Route d'El Hajeb, Meknès", "equipements": ["Éclairage LED", "Vestiaires", "Parking", "Cafétéria"], "horaires": ["9h", "10h", "11h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h"]},
    {"id": 2, "nom": "Stade d'Honneur", "ville": "Meknès", "prix": 250, "type": "Pelouse naturelle", "note": 4.9, "image": "🏆", "adresse": "Avenue des FAR, Meknès", "equipements": ["Éclairage LED Pro", "Vestiaires VIP", "Parking", "Buvette", "Terrain annexe"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]},
    {"id": 3, "nom": "Foot Center Meknès", "ville": "Meknès", "prix": 180, "type": "Pelouse synthétique", "note": 4.6, "image": "⚽", "adresse": "Bd My Ismail, Meknès", "equipements": ["Éclairage", "Vestiaires", "Parking", "Cafétéria"], "horaires": ["9h", "10h", "11h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]},
    
    # Casablanca
    {"id": 4, "nom": "Arena Casablanca", "ville": "Casablanca", "prix": 300, "type": "Pelouse synthétique Premium", "note": 4.9, "image": "⚡", "adresse": "Bd Mohammed VI, Casablanca", "equipements": ["Éclairage LED Pro", "Vestiaires VIP", "Parking", "Cafétéria", "Sauna", "Wifi"], "horaires": ["9h", "10h", "11h", "12h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"]},
    {"id": 5, "nom": "Stade Mohamed V", "ville": "Casablanca", "prix": 350, "type": "Pelouse naturelle", "note": 5.0, "image": "🏟️", "adresse": "Bd de l'Ocean Atlantique, Casablanca", "equipements": ["Éclairage LED Pro", "Vestiaires Luxe", "Parking VIP", "Cafétéria", "Tribunes", "Sonorisation"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]},
    
    # Rabat
    {"id": 6, "nom": "Football Center Rabat", "ville": "Rabat", "prix": 220, "type": "Pelouse synthétique", "note": 4.7, "image": "⚽", "adresse": "Avenue Annakhil, Rabat", "equipements": ["Éclairage LED", "Vestiaires", "Parking", "Buvette"], "horaires": ["9h", "10h", "11h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h"]},
    {"id": 7, "nom": "Prince Héritier Stadium", "ville": "Rabat", "prix": 280, "type": "Pelouse naturelle", "note": 4.8, "image": "🏆", "adresse": "Bd Moulay Youssef, Rabat", "equipements": ["Éclairage LED Pro", "Vestiaires VIP", "Parking", "Cafétéria", "Tribunes"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]},
    
    # Tanger
    {"id": 8, "nom": "Sporting Tanger", "ville": "Tanger", "prix": 200, "type": "Pelouse synthétique", "note": 4.6, "image": "🥅", "adresse": "Route de Tétouan, Tanger", "equipements": ["Éclairage LED", "Vestiaires", "Parking"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]},
    {"id": 9, "nom": "Ibn Batouta Arena", "ville": "Tanger", "prix": 260, "type": "Pelouse naturelle", "note": 4.8, "image": "🏟️", "adresse": "Bd du 9 Avril, Tanger", "equipements": ["Éclairage LED Pro", "Vestiaires VIP", "Parking", "Cafétéria", "Tribunes"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h"]},
    
    # Marrakech
    {"id": 10, "nom": "Pitch Marrakech", "ville": "Marrakech", "prix": 240, "type": "Pelouse synthétique Premium", "note": 4.9, "image": "💎", "adresse": "Bd Abdelkrim Khattabi, Marrakech", "equipements": ["Éclairage LED Pro", "Vestiaires Luxe", "Parking VIP", "Cafétéria", "Sauna", "Piscine"], "horaires": ["9h", "10h", "11h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"]},
    {"id": 11, "nom": "Marrakech Sports Center", "ville": "Marrakech", "prix": 200, "type": "Pelouse synthétique", "note": 4.6, "image": "⚽", "adresse": "Route de Safi, Marrakech", "equipements": ["Éclairage LED", "Vestiaires", "Parking", "Buvette"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]},
    
    # Fès
    {"id": 12, "nom": "Elite Center Fès", "ville": "Fès", "prix": 190, "type": "Pelouse synthétique", "note": 4.5, "image": "🎯", "adresse": "Route d'Imouzzer, Fès", "equipements": ["Éclairage LED", "Vestiaires", "Parking", "Cafétéria"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]},
    {"id": 13, "nom": "Fès Sport Complex", "ville": "Fès", "prix": 220, "type": "Pelouse naturelle", "note": 4.7, "image": "🏆", "adresse": "Bd Allal El Fassi, Fès", "equipements": ["Éclairage LED Pro", "Vestiaires VIP", "Parking", "Cafétéria", "Tribunes"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]},
    
    # Agadir
    {"id": 14, "nom": "Agadir Beach Foot", "ville": "Agadir", "prix": 210, "type": "Pelouse synthétique", "note": 4.6, "image": "🏖️", "adresse": "Bd du 20 Août, Agadir", "equipements": ["Éclairage LED", "Vestiaires", "Parking", "Cafétéria", "Vue sur mer"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]},
    
    # Tétouan
    {"id": 15, "nom": "Tétouan Foot Arena", "ville": "Tétouan", "prix": 180, "type": "Pelouse synthétique", "note": 4.4, "image": "⚽", "adresse": "Route de Martil, Tétouan", "equipements": ["Éclairage LED", "Vestiaires", "Parking"], "horaires": ["10h", "11h", "12h", "15h", "16h", "17h", "18h", "19h", "20h", "21h"]}
]

def show_toast(message):
    st.session_state.toast = message

def reservation_interface():
    st.markdown("### 🏟️ Réservation de terrain")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        villes = ["Toutes", "Meknès", "Casablanca", "Rabat", "Tanger", "Marrakech", "Fès", "Agadir", "Tétouan"]
        ville = st.selectbox("📍 Ville", villes)
    
    with col2:
        date = st.date_input("📅 Date", datetime.now())
    
    # Filtrage des terrains
    terrains_filtered = TERRAINS if ville == "Toutes" else [t for t in TERRAINS if t["ville"] == ville]
    
    st.markdown(f"**{len(terrains_filtered)} terrains disponibles à {ville if ville != 'Toutes' else 'tout le Maroc'}**")
    
    for terrain in terrains_filtered:
        with st.container():
            st.markdown(f"""
            <div class='terrain-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <div style='font-size: 2rem;'>{terrain['image']}</div>
                        <h3 style='margin: 0; color: {COLORS['primary']};'>{terrain['nom']}</h3>
                        <p style='margin: 0; font-size: 0.8rem; color: {COLORS['text_light']};'>📍 {terrain['adresse']}</p>
                        <p style='margin: 0; font-size: 0.7rem; color: {COLORS['accent']};'>🏙️ {terrain['ville']}</p>
                    </div>
                    <div style='text-align: right;'>
                        <div style='font-size: 1.5rem; font-weight: bold; color: {COLORS['primary']};'>{terrain['prix']} DH</div>
                        <div style='font-size: 0.8rem;'>⭐ {terrain['note']}/5</div>
                    </div>
                </div>
                <div style='margin-top: 0.5rem;'>
            """, unsafe_allow_html=True)
            
            # Équipements
            for equip in terrain['equipements']:
                st.markdown(f"<span class='badge-elegant'>✓ {equip}</span>", unsafe_allow_html=True)
            
            st.markdown(f"""
                </div>
                <div style='margin-top: 1rem;'>
                    <p style='font-size: 0.8rem; font-weight: 500;'>🕐 Horaires disponibles :</p>
                    <div style='display: flex; flex-wrap: wrap; gap: 0.3rem;'>
            """, unsafe_allow_html=True)
            
            for heure in terrain['horaires']:
                if st.button(heure, key=f"{terrain['id']}_{heure}", use_container_width=True):
                    show_toast(f"✅ Réservé {terrain['nom']} à {heure} - {terrain['prix']} DH")
                    st.session_state.reservations.append({
                        "terrain": terrain['nom'], 
                        "ville": terrain['ville'],
                        "heure": heure, 
                        "date": date.strftime("%d/%m/%Y"), 
                        "prix": terrain['prix']
                    })
                    st.rerun()
            
            st.markdown("</div></div></div>", unsafe_allow_html=True)

def contact_interface():
    st.markdown("### 📞 Contactez-nous")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='contact-section'>
            <h4 style='color: #6C5CE7;'>📱 Nos coordonnées</h4>
            <p>📍 <strong>Adresse :</strong> ENSAM Meknès, Maroc</p>
            <p>📧 <strong>Email :</strong> contact@footplay.ma</p>
            <p>📞 <strong>Téléphone :</strong> +212 5 35 52 00 00</p>
            <p>🕐 <strong>Horaires :</strong> 9h - 21h (7j/7)</p>
            <hr>
            <h4 style='color: #6C5CE7;'>🌐 Réseaux sociaux</h4>
            <p>📘 Facebook : @FootPlay.ma</p>
            <p>📸 Instagram : @footplay_ma</p>
            <p>🐦 Twitter : @FootPlay_ma</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='contact-section'>
            <h4 style='color: #6C5CE7;'>✉️ Envoyez-nous un message</h4>
        </div>
        """, unsafe_allow_html=True)
        
        nom = st.text_input("Votre nom", placeholder="ex: Yassine")
        email = st.text_input("Email", placeholder="ex: yassine@email.com")
        message = st.text_area("Message", placeholder="Décrivez votre demande...", height=100)
        
        if st.button("📨 Envoyer le message", use_container_width=True):
            if nom and message:
                st.session_state.contact_messages.append({"nom": nom, "email": email, "message": message, "date": datetime.now()})
                show_toast("✅ Message envoyé ! Nous vous répondrons rapidement.")
                st.rerun()
            else:
                st.warning("Veuillez remplir votre nom et message")

def annonces_interface():
    st.markdown("### 🎉 Annonces et Événements")
    
    with st.expander("➕ Proposer une annonce", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            titre = st.text_input("Titre de l'annonce", placeholder="ex: Tournoi du week-end")
            date = st.text_input("Date", placeholder="ex: 15 Avril 2026")
        with col2:
            lieu = st.selectbox("Lieu", ["Meknès", "Casablanca", "Rabat", "Tanger", "Marrakech", "Fès", "Agadir", "Tétouan"])
            prix = st.number_input("Prix par personne (DH)", min_value=0, value=50)
        places = st.number_input("Nombre de places", min_value=1, value=8, max_value=30)
        
        if st.button("📢 Publier l'annonce", use_container_width=True):
            if titre:
                st.session_state.annonces.insert(0, {"titre": titre, "date": date, "lieu": lieu, "places": places, "prix": prix})
                show_toast("✅ Annonce publiée !")
                st.rerun()
            else:
                st.warning("Veuillez entrer un titre")
    
    st.markdown("---")
    
    for i, annonce in enumerate(st.session_state.annonces):
        st.markdown(f"""
        <div class='annonce-card'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <h4 style='margin: 0; color: #FDCB6E;'>{annonce['titre']}</h4>
                    <p style='margin: 0.2rem 0; font-size: 0.8rem;'>📅 {annonce['date']} | 📍 {annonce['lieu']}</p>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 1.2rem; font-weight: bold; color: #00B894;'>{annonce['prix']} DH</div>
                    <div style='font-size: 0.7rem;'>👥 {annonce['places']} places</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"👍 Je participe - {annonce['titre']}", key=f"participe_{i}", use_container_width=True):
            show_toast(f"✅ Inscription confirmée pour {annonce['titre']} !")
            st.rerun()

def profil_interface():
    st.markdown("### 👤 Mon Profil")
    
    if not st.session_state.user['is_logged']:
        st.markdown("""
        <div class='card-modern' style='text-align: center; padding: 2rem;'>
            <div style='font-size: 3rem;'>👋</div>
            <h3>Bienvenue sur FootPlay</h3>
            <p>Connectez-vous pour gérer vos réservations</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nom", placeholder="Votre nom")
        with col2:
            phone = st.text_input("Téléphone", placeholder="06 XX XX XX XX")
        
        if st.button("🚀 Se connecter / S'inscrire", use_container_width=True):
            if name:
                st.session_state.user = {'name': name, 'phone': phone, 'is_logged': True}
                show_toast(f"✅ Bienvenue {name} !")
                st.rerun()
            else:
                st.warning("Veuillez entrer votre nom")
    else:
        st.markdown(f"""
        <div class='card-modern' style='display: flex; align-items: center; gap: 1rem;'>
            <div class='avatar'>{st.session_state.user['name'][0].upper()}</div>
            <div>
                <h3 style='margin: 0;'>{st.session_state.user['name']}</h3>
                <p style='margin: 0; color: {COLORS['text_light']};'>{st.session_state.user['phone'] or 'Téléphone non renseigné'}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Mes réservations")
        if st.session_state.reservations:
            for res in st.session_state.reservations:
                st.markdown(f"""
                <div class='terrain-card'>
                    <div style='display: flex; justify-content: space-between;'>
                        <div>
                            <strong>{res['terrain']}</strong><br>
                            📍 {res.get('ville', 'Maroc')}<br>
                            📅 {res['date']} à {res['heure']}
                        </div>
                        <div style='color: {COLORS['primary']}; font-weight: bold;'>{res['prix']} DH</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucune réservation pour le moment")
        
        if st.button("🔓 Se déconnecter", use_container_width=True):
            st.session_state.user = {'name': '', 'phone': '', 'is_logged': False}
            st.rerun()

def avis_interface():
    st.markdown("### ⭐ Avis et recommandations")
    
    with st.expander("✍️ Donnez votre avis", expanded=False):
        col1, col2 = st.columns([1, 2])
        with col1:
            note = st.select_slider("Note", options=[1, 2, 3, 4, 5], value=5)
        with col2:
            commentaire = st.text_area("Votre commentaire", placeholder="Partagez votre expérience...", height=80)
        
        if st.button("📝 Publier mon avis", use_container_width=True):
            if commentaire:
                st.session_state.avis.insert(0, {
                    "user": st.session_state.user['name'] if st.session_state.user['is_logged'] else "Anonyme",
                    "note": note,
                    "commentaire": commentaire,
                    "date": datetime.now().strftime("%d/%m/%Y")
                })
                show_toast("✅ Merci pour votre avis !")
                st.rerun()
            else:
                st.warning("Veuillez écrire un commentaire")
    
    st.markdown("---")
    
    for avis in st.session_state.avis:
        stars = "⭐" * avis['note'] + "☆" * (5 - avis['note'])
        st.markdown(f"""
        <div class='avis-card'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <strong>{avis['user']}</strong>
                    <span style='margin-left: 0.5rem; color: #FDCB6E;'>{stars}</span>
                </div>
                <div style='font-size: 0.7rem; color: {COLORS['text_light']};'>{avis['date']}</div>
            </div>
            <p style='margin-top: 0.5rem; font-size: 0.9rem;'>"{avis['commentaire']}"</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    if st.session_state.toast:
        st.markdown(f"<div class='toast-success'>{st.session_state.toast}</div>", unsafe_allow_html=True)
        st.session_state.toast = None
    
    st.markdown(f"""
    <div class='main-header'>
        <h1 class='title-main'>⚽ FootPlay</h1>
        <p class='subtitle'>Réservation de terrains de football | Simple, Rapide, Sécurisé</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu_cols = st.columns(5)
    menu_items = [
        {"name": "🏠 Accueil", "tab": "home"},
        {"name": "🎯 Réservation", "tab": "reservation"},
        {"name": "📞 Contact", "tab": "contact"},
        {"name": "🎉 Annonces", "tab": "annonces"},
        {"name": "👤 Profil", "tab": "profil"}
    ]
    
    for i, item in enumerate(menu_items):
        with menu_cols[i]:
            if st.button(item['name'], key=f"nav_{item['tab']}", use_container_width=True):
                st.session_state.current_tab = item['tab']
                st.rerun()
    
    st.markdown("---")
    
    if st.session_state.current_tab == "home":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🔥 Terrains populaires")
            for terrain in TERRAINS[:3]:
                st.markdown(f"""
                <div class='card-modern'>
                    <div style='display: flex; gap: 1rem; align-items: center;'>
                        <div style='font-size: 2rem;'>{terrain['image']}</div>
                        <div>
                            <h4 style='margin: 0;'>{terrain['nom']}</h4>
                            <p style='margin: 0; font-size: 0.8rem;'>⭐ {terrain['note']}/5 | {terrain['prix']} DH/h | 📍 {terrain['ville']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ⭐ Derniers avis")
            for avis in st.session_state.avis[:2]:
                stars = "⭐" * avis['note']
                st.markdown(f"""
                <div class='card-modern'>
                    <strong>{avis['user']}</strong> {stars}<br>
                    <span style='font-size: 0.8rem;'>"{avis['commentaire'][:50]}..."</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("### 📊 FootPlay en chiffres")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<div class='card-modern' style='text-align: center;'><div style='font-size: 2rem;'>🏟️</div><h2>15+</h2><p>Terrains</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='card-modern' style='text-align: center;'><div style='font-size: 2rem;'>🏙️</div><h2>8</h2><p>Villes</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='card-modern' style='text-align: center;'><div style='font-size: 2rem;'>⚽</div><h2>1000+</h2><p>Matchs</p></div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div class='card-modern' style='text-align: center;'><div style='font-size: 2rem;'>⭐</div><h2>4.7/5</h2><p>Note</p></div>", unsafe_allow_html=True)
    
    elif st.session_state.current_tab == "reservation":
        reservation_interface()
    
    elif st.session_state.current_tab == "contact":
        contact_interface()
        avis_interface()
    
    elif st.session_state.current_tab == "annonces":
        annonces_interface()
    
    elif st.session_state.current_tab == "profil":
        profil_interface()
    
    st.markdown(f"""
    <div class='footer'>
        <p>⚽ <strong>FootPlay</strong> - Réservez votre terrain de football en quelques clics</p>
        <p style='font-size: 0.7rem;'>ENSAM Meknès | Marketing 5.0 - 2025/2026</p>
        <p style='font-size: 0.7rem;'>« Organiser un match n'a jamais été aussi simple »</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()