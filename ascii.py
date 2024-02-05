
async def run():
	user_input = await js.interact('name')
	prompt = f'Write this name in ASCII art: {user_input}'
	result = await js.query(prompt)
	js.draw('ascii', 'text', result)