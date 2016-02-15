import gazeru
import pprint

pp = pprint.PrettyPrinter(indent=4)

gazeru = gazeru.Gazeru()
pp.pprint(gazeru.pull())
