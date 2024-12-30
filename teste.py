import streamlit as st
from streamlit_js_eval import get_geolocation
import requests

def get_address_from_coords(lat, lon):
    """Faz requisição à API do Nominatim e retorna o endereço como string."""
    if lat is None or lon is None:
        return "Erro: Coordenadas não fornecidas."

    try:
        url = 'https://nominatim.openstreetmap.org/reverse'
        params = {
            'format': 'jsonv2',
            'lat': lat,
            'lon': lon,
            'zoom': 18,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'GeolocationApp/1.0 riquelmem077@gmail.com'
        }
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            address = data.get('display_name', 'Endereço não encontrado.')
            return address
        else:
            return f"Erro ao obter o endereço: {response.status_code}"

    except Exception as e:
        return f"Erro ao processar a requisição: {str(e)}"


def main():
    st.title("Geolocation App - Versão Streamlit (automático)")

    # Retorno completo de geolocalização (coords + timestamp)
    local = get_geolocation("all")

    st.markdown("### Depuração: Retorno cru de get_geolocation('all')")
    st.write(local)

    if local:
        coords_data = local.get("coords", {})
        lat = coords_data.get("latitude")
        lon = coords_data.get("longitude")

        st.markdown("### Depuração: Extraindo Latitude/Longitude")
        st.write(f"Latitude extraída: {lat}")
        st.write(f"Longitude extraída: {lon}")

        # Se latitude e longitude forem válidas,
        # já obtemos o endereço sem precisar de um botão
        if lat is not None and lon is not None:
            endereco = get_address_from_coords(lat, lon)

            st.markdown("### Depuração: Retorno de get_address_from_coords")
            st.write(endereco)

            if not endereco.startswith("Erro"):
                st.success(f"Endereço obtido: {endereco}")
            else:
                st.error(endereco)
        else:
            st.warning("Latitude/Longitude ainda não disponíveis.")
    else:
        st.warning("Aguardando permissão ou captura de localização...")

if __name__ == "__main__":
    main()
