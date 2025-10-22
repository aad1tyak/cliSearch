import argparse
#Define the Arguement Parser object instance 
parser = argparse.ArgumentParser('cliSearch', 'Let the user to make search query through terminal.')

#attach arguements for task 
parser.add_argument('query', nargs=1)

args = parser.parse_args()
print(args.query)
