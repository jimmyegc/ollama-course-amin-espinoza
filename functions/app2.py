import requests
from ollama import chat

def get_crypto_price(symbol: str) -> str:
    api_host = "https://api.api-ninjas.com/v1"
    api_key = "Mjajg2qrEXtyQGw0s0spkh5C8RsHMvYxUTDvhif3"

    url = f"{api_host}/cryptoprice?symbol={symbol}"
    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data and "price" in data:
            price = float(data['price'])
            return f"El precio actual de {symbol} es ${price:,.2f} USD"
        else:
            return f"No se pudo obtener el precio de {symbol}"

    except Exception as e:
        return f"Error al obtener el precio: {str(e)}"

messages = [
  {
    "role": "system", 
    "content": "Eres un asistente que SIEMPRE debe usar los resultados de las herramientas disponibles, en este caso la herramienta get_crypto_price y darles prioridad sobre la información que tu cuentas. Cuando una herramienta te proporcione información, DEBES usar esa información en tu respuesta. NUNCA digas que no tienes acceso a información en tiempo real sí una herramienta te ha proporcionado datos."  
  },
  {
    "role": "user", 
    "content": "¿Cuál es el precio actual de Bitcoin en dólares?"
  } 
]

response = chat(model="llama3.2", messages=messages, tools=[get_crypto_price])

messages.append(response.message)

if response.message.tool_calls:
  call = response.message.tool_calls[0]
  result = get_crypto_price(**call.function.arguments)

  messages.append({
    "role": "tool",
    "tool_name": call.function.name,
    "content": result
  })
    
  final_response = chat(model="llama3.2", messages=messages, tools=[get_crypto_price])
  print("\nRespuesta final del modelo:")
  print(final_response.message.content)    
else:
  print(response.message.content)