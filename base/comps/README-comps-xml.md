
The comps.xml file is generated using the upstream Fedora repo here:
https://pagure.io/fedora-comps.git

To create a new comps.xml for AzureLinux using that repo, first choose
which Fedora release to base it on (e.g. comps-f43.xml.in), and then
manually edit the file to remove all unwanted groups, environments,
categories, and langpacks. You can (optionally) then sort the file
content using:

(note: if you are using Ubuntu, or any system where /bin/sh is not
bash, add "SHELL=/bin/bash" as a make parameter to this and later
calls to make, e.g. "make SHELL=/bin/bash ...")

$ make sort

That will perform sorting of all the comps-*.xml.in contents (if any
is needed). Then build the resulting file with:

$ make comps-f43.xml

Replace "f43" in the filename with the actual Fedora release number of
the comps-*.xml.in file you have edited.

That file (e.g. "comps-f43.xml") may then be renamed to "comps.xml"
and checked in here.

The comps.xml file must be included into all generated rpm
repositories, for example using "createrepo":

$ createrepo -g comps.xml ...
