import pathlib

# first way
xd = pathlib.Path(__file__).parents[1] / pathlib.Path('Mods')
print(xd)
