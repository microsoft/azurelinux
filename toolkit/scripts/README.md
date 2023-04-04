# Scripts
This folder contains a variety of useful scripts and tools to use for developers of CBL-Mariner.

## Installing python dependencies
Some python scripts have pip dependencies. To install all of them run:
`pip install -r requirements.txt` while in this folder.

### Regenerate requirements file
Generating python dependencies file might be tricky. There is no perfect tool for it unfortunately. We will use `pipreqs` to extract top dependencies out of scripts into a transitive `requirements.in` file and then `pip-tools` to get dependencies of a dependencies into final `requirements.txt` file.

#### Issues with pipreqs to extract dependency
**Note:** it is not perfect, and it might take wrong dependency if they have same import names, for example we need `python-rpm-spec` and `pyrm`, but both packages provide `pyrpm` file to import so the tool will only think that we need `pyrpm` dependency.

The tool also does not go deeper into getting dependencies of a dependency. In order to get those, we can use `pip-tools`. To do so:

1. Install the tools if you have not `pip install pipreqs pip-tools`
2. Generate the `requirements.in` file first using `pipreqs` by running `pipreqs --savepath=requirements.in`
3. Verify that `requirements.in` has included all dependencies and the correct ones, like mentioned in [Issues with pipreqs to extract dependency section](#issues-with-pipreqs-to-extract-dependency)
3. Generate the `requirements.txt` file using `requirements.in` and `pip-tools` by running `pip-compile`
4. Delete `requirements.in` as it was a transitive file.
5. Commit changes to the `requirements.txt` file
