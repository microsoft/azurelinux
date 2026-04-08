#! /usr/bin/python3

# Small and dirty script to create the README-Trademarks.txt file. This file
# has to be created by scratch at every release. To do so, use:
# ./trademarks.py > README-Trademarks.txt

from urllib.request import urlopen
import json

response = urlopen('https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/metadata/icons.json')
if response.code != 200:
    print("Got HTTP ", response.code);
    exit(1)
document = json.loads(response.fp.read())

brands = []

for icon in document:
    if 'brands' in document[icon]['styles']:
        brands.append(icon)

brands.sort()

out = 'Brand icons may be subject to trademark and brand guidelines of their\n'
out+= 'respective owners. Always check before deploying other companies\' branding.\n'
out+= '\n'
out+= 'Brand Icons:'

for brand in brands:
    out+= '\n * fa-' + brand

print(out)
