# Scripts
This folder contains variety of useful scripts and tools to use for developers of CBL-Mariner.

## Installing python dependecies
Some python scripts have pip dependencies. To install all of them run:
`pip install -r requirements.txt` while in this folder.

### Regenerate requirements file
To regenerate python requirements file it is recommended to install `pipreqs` pip tool that can quickly scan python scripts and generate file with dependencies. Once installed you can run `pipreqs --force ./` within the folder to generate or update the existing requirements file. 