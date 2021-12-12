from fsgenlib.generator import DataUnit, initialize

t = initialize()
t.generate()
t.dump('./result.csv')