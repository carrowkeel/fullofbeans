# Draw things

async def run():
	user_input = await js.interact('form', 'Name of a thing/animal')
	prompt = f'Can you create a picture of a {user_input} using SVG? Only output the SVG so that the output is only HTML. Do not output any text explanations or comments.'
	results = await js.query(prompt, 'all')
	for i, result in enumerate(results):
		js.draw(f'picture_{i}', 'html', result)

