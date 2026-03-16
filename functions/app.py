from ollama import chat

def get_temperature(city: str) -> str:
    """Obtener la temperatura actual de una ciudad.

    Args:
        city: El nombre de la ciudad

    Regresa:
        La temperatura actual de la ciudad
    """
    temperatures = {
        "New York": "22°C",
        "London": "15°C",
        "Tokyo": "18°C"
    }

    return temperatures.get(city, "Unknown")


messages = [{"role": "user", "content": "¿Cuál es la temperatura en Tokyo?"}]

response = chat(model="llama3.2", messages=messages, tools=[get_temperature])

messages.append(response.message)

if response.message.tool_calls:
    call = response.message.tool_calls[0]
    result = get_temperature(**call.function.arguments)
    messages.append({
        "role": "tool",
        "tool_name": call.function.name,
        "content": str(result)
    })

final_response = chat(model="llama3.2", messages=messages, tools=[get_temperature])

print(final_response.message.content)