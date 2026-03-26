# comps

The files here are taken from https://pagure.io/fedora-comps and
reduced/modified for AzureLinux. Use "make" to generate the
comps-*.xml file(s) from the comps-*.xml.in file(s). The resulting
comps-*.xml file must be included in the corresponding repo created
using "createrepo -g comps-DISTRO.xml", for example for AzureLinux 4:
"createrepo -g comps-azl4.xml".
