import streamlit as st
import requests
import pytz
import pandas as pd
from datetime import time, datetime

'''
# TaxiFareModel - V1.0
'''
st.subheader('by alexandre-29')

st.caption('''
Cette appli permet de calculer le prix de ton taxi pour te balader à New York !!!
''')



pickup_date = st.date_input('''Date''')
pickup_time = st.slider('Heure du départ', value=(time(12, 00)))
pickup_longitude = st.number_input('''pickup longitude''')
pickup_latitude = st.number_input('''pickup latitude''')
dropoff_longitude = st.number_input('''dropoff longitude''')
dropoff_latitude = st.number_input('''dropoff latitude''')
passenger_count = st.selectbox('Nombre de passagers (max 6*)', [1,2,3,4,5,6])
st.caption("* Pour plus de 6 personnes voir l'application de location de bus bientôt disponible ici => ....")
pret = st.button('Calcul')


url = 'https://taxifare-alg-755145999508.europe-west1.run.app/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')


if pret :
    date_str = pickup_date.strftime('%Y-%m-%d %H:%M:%S')[0:10] + ' ' + pickup_time.strftime('%Y-%m-%d %H:%M:%S')[11:19]
    eastern = pytz.timezone("US/Eastern")
    pickup_datetime = pd.Timestamp(datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S'))
    localized_datetime = eastern.localize(pickup_datetime, is_dst=None)
    pickup_datetime_utc = localized_datetime.astimezone(pytz.utc)
    dico = {
            'pickup_datetime' : pickup_datetime_utc,
            'pickup_longitude' : pickup_longitude,
            'pickup_latitude' : pickup_latitude,
            'dropoff_longitude' : dropoff_longitude,
            'dropoff_latitude' : dropoff_latitude,
            'passenger_count' : passenger_count,
        }

    url = f'''{url}?pickup_datetime={dico['pickup_datetime']}&pickup_longitude={dico['pickup_longitude']}&pickup_latitude={dico['pickup_latitude']}&dropoff_longitude={dico['dropoff_longitude']}&dropoff_latitude={dico['dropoff_latitude']}&passenger_count={dico['passenger_count']}'''

    data = requests.get(url,auth=('user', 'pass'))

    json = data.json()

    result = f"{round(json['fare'],2)} $ pour ce trajet avec {passenger_count} personne(s)"
    st.subheader(result)
