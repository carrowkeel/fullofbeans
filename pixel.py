async def run():
	user_input = await js.interact('form', 'Name of a thing/animal')
	prompt = f'Can you draw a 20x20 grayscale pixel drawing by printing a matrix of 20x20 with values between 0 and 1? Draw a {user_input}.'
	result = await js.query(prompt)
	print(result)
