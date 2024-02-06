# Some names are shorter than others

async def run():
	user_input = await js.interact('form', 'Write a name')
	prompt = f'Write this name in ASCII art: {user_input}'
	result = await js.query(prompt)
	js.draw('ascii', 'text', result)