import openai
import requests
import pyttsx3
import re
from urllib.parse import quote

# Configuración de la API de OpenAI
openai.api_key = "TU API"
# Respuestas predefinidas para preguntas generales
general_responses = {
    "quién te creó": "Fui creado por un estudiante apasionado por la inteligencia artificial.",
    "quien te creo": "Fui creado por un estudiante apasionado por la inteligencia artificial.",
    "quien eres": "Soy un asistente virtual, preparado para ayudarte con tareas como resolución de cálculos, temperaturas climatologicas, preguntas generales, etc..",
    "para qué sirves": "Sirvo como un asistente virtual para ayudarte con consultas del clima, cálculos y responder preguntas generales.",
    "para que sirves": "Sirvo como un asistente virtual para ayudarte con consultas del clima, cálculos y responder preguntas generales.",
    "cómo estás": "Estoy aquí para ayudarte. ¿Qué necesitas?",
    "como estas": "Estoy aquí para ayudarte. ¿Qué necesitas?",
    "qué puedes hacer": "Puedo responder preguntas generales, calcular operaciones matemáticas y consultar el clima.",
    "que puedes hacer": "Puedo responder preguntas generales, calcular operaciones matemáticas y consultar el clima.",
    "cuando fuiste creado": "Fui creado el 16 de noviembre del año 2024.",
    "¿cuando fuiste creado?": "Fui creado el 16 de noviembre del año 2024.",
    "¿que puedes hacer?": "Puedo responder preguntas generales, calcular operaciones matemáticas y consultar el clima.",
    "que puedes hacer": "Puedo responder preguntas generales, calcular operaciones matemáticas y consultar el clima.",
}

def handle_general_question(user_input):
    """
    Responde preguntas generales predefinidas.
    """
    for question, response in general_responses.items():
        if question in user_input:
            return response
    return None

def get_weather_weatherstack(city):
    """
    Consulta el clima utilizando Weatherstack y devuelve una descripción clara del clima.
    """
    api_key = "TU API"  # Clave de API de Weatherstack
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={quote(city)}"  # URL de solicitud
    print(f"Realizando solicitud a: {url}")  # Muestra la URL de la solicitud
    response = requests.get(url)  # Realiza la solicitud HTTP

    if response.status_code == 200:  # Si la solicitud fue exitosa
        try:
            data = response.json()  # Convierte la respuesta JSON a un diccionario
            location = data.get("location", {})
            current = data.get("current", {})

            if location and current:  # Verifica si los datos esperados están presentes
                # Extrae la información requerida
                location_name = location.get("name", "Ubicación desconocida")
                region = location.get("region", "Región desconocida")
                country = location.get("country", "País desconocido")
                description = current.get("weather_descriptions", ["Descripción no disponible"])[0]
                temperature = current.get("temperature", "N/A")

                # Construye y devuelve la respuesta
                return (
                    f"El clima en {location_name}, {region}, {country} es {description.lower()} "
                    f"con una temperatura de {temperature}°C."
                )
            else:
                return "No se encontraron datos suficientes para esta ciudad."
        except Exception as e:
            return f"Error al procesar la respuesta de la API: {e}"
    else:
        return f"Error en la solicitud: {response.status_code}"


def extract_city(user_input):
    """
    Extrae el nombre de la ciudad del texto ingresado por el usuario.
    """
    try:
        # Detectar patrones como "clima en [ciudad]" o "qué clima hay en [ciudad]"
        match = re.search(r"clima(?: en| hay en| de)? ([a-záéíóúñ ]+)", user_input, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None
    except Exception as e:
        return None

def extract_and_evaluate_expression(user_input):
    """
    Extrae y evalúa expresiones matemáticas dentro del texto ingresado por el usuario.
    """
    try:
        # Buscar una operación matemática en el texto
        match = re.search(r"(\d+[\+\-\*/]\d+)", user_input)  # Detectar "34+6", "15*3", etc.
        if match:
            expression = match.group(1)  # Extraer la expresión matemática
            result = eval(expression)  # Evaluar la expresión
            return f"El resultado de {expression} es {result}."
        else:
            return "No encontré una expresión matemática válida en tu consulta."
    except Exception as e:
        return "Lo siento, no pude evaluar la expresión matemática."

def speak_response(response):
    """
    Convierte texto a voz para la salida del asistente.
    """
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()

def ask_gpt(user_input):
    """
    Consulta a GPT-4 usando la API de OpenAI.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Usar GPT-4 o text-davinci-003
            prompt=f"Asistente virtual, responde a esta pregunta: {user_input}",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return "Lo siento, ocurrió un problema al intentar responder tu pregunta."

def main():
    """
    Lógica principal del asistente virtual.
    """
    print("Asistente Virtual: Hola, soy tu asistente virtual. ¿Cómo puedo ayudarte?")
    while True:
        user_input = input("Tú: ").lower()

        # Condición para salir del programa
        if user_input in ['salir', 'adiós', 'exit']:
            print("Asistente Virtual: ¡Hasta luego!")
            break

        # Procesar consulta del clima
        if "clima" in user_input:
            city = extract_city(user_input)
            if city:
                response = get_weather_weatherstack(city)
            else:
                response = "Por favor, indícame la ciudad para consultar el clima."

        # Responder preguntas generales
        elif general_response := handle_general_question(user_input):
            response = general_response

        # Procesar cálculos matemáticos
        elif re.search(r"\d+[\+\-\*/]\d+", user_input):  # Detectar si hay una expresión matemática
            response = extract_and_evaluate_expression(user_input)

        # Manejar otras solicitudes con GPT
        else:
            response = ask_gpt(user_input)

        # Mostrar y pronunciar la respuesta
        print(f"Asistente Virtual: {response}")
        speak_response(response)

if __name__ == "__main__":
    main()
