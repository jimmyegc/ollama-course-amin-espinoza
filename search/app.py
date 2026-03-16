from typing import Union
from rich import print
from ollama import Client, WebFetchResponse, WebSearchResponse


def format_tool_results(
    results: Union[WebSearchResponse, WebFetchResponse],
    user_search: str,
):
    output = []

    if isinstance(results, WebSearchResponse):
        output.append(f'Search results for "{user_search}":')

        for result in results.results:
            output.append(f'[{result.title}]' if result.title else f'{result.content}')
            output.append(f'  URL: {result.url}')
            output.append(f'  Content: {result.content}')
            output.append('')

        return '\n'.join(output).rstrip()

    elif isinstance(results, WebFetchResponse):
        output.append(f'Fetch results for "{user_search}":')

        output.extend([
            f'Title: {results.title}',
            f'URL: {user_search}' if user_search else '',
            f'Content: {results.content}',
        ])

        if results.links:
            output.append(f'Links: {", ".join(results.links)}')

        output.append('')
        return '\n'.join(output).rstrip()


# API key
api_key = "f175a429c22f4737af7eac6943df63c4.kanSSls_Jdmfnff1VMJAByhP"

# Cliente
client = Client(headers={'Authorization': f'Bearer {api_key}'})


# Herramientas disponibles
available_tools = {
    'web_search': client.web_search,
    'web_fetch': client.web_fetch
}


query = "¿Qué es el nuevo motor de ollama?"
print('Query:', query)


messages = [{'role': 'user', 'content': query}]

while True:

    response = client.chat(
        model='llama3.2',
        messages=messages,
        tools=[client.web_search, client.web_fetch]
    )

    if response.message.content:
        print('Content:')
        print(response.message.content + '\n')

    messages.append(response.message)

    # Si el modelo quiere usar herramientas
    if response.message.tool_calls:

        for tool_call in response.message.tool_calls:

            function_to_call = available_tools.get(tool_call.function.name)

            if function_to_call:
                args = tool_call.function.arguments

                result: Union[WebSearchResponse, WebFetchResponse] = function_to_call(**args)

                print(
                    'Result from tool call name:',
                    tool_call.function.name,
                    'with arguments:'
                )
                print(args)
                print()

                user_search = args.get('query', '') or args.get('url', '')

                formatted_tool_results = format_tool_results(
                    result,
                    user_search=user_search
                )

                print(formatted_tool_results[:300])
                print()

                messages.append({
                    'role': 'tool',
                    'content': formatted_tool_results[:2000 * 4],
                    'tool_name': tool_call.function.name
                })

            else:
                print(f'Tool {tool_call.function.name} not found')

                messages.append({
                    'role': 'tool',
                    'content': f'Tool {tool_call.function.name} not found',
                    'tool_name': tool_call.function.name
                })

    else:
        break