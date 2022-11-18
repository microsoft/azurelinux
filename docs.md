---
layout: single
header:
  overlay_image: /assets/images/conor-sexton-hRemch0ZDwI-unsplash.jpg
toc: true
title: CBL-Mariner Documentation
---
# CBL-Mariner Linux

This is the official CBL-Mariner Linux build system. You can use this repository to
build a boot-able CBL-Mariner Linux image and use it as an AKS container host, where you can host your Kubernetes containers - Available in AKS (Azure Kubernetes Service).

CBL-Mariner Linux is a lightweight operating system, containing only the packages needed for a cloud environment. CBL-Mariner can be customized through custom
packages and tools, to fit the requirements of your application. CBL-Mariner undergoes Azure validation tests, is compatible with Azure agents, and is built and tested by the Azure Edge & Platform to power various use cases, ranging from Azure services to powering IoT infrastructure. CBL-Mariner is the internally recommended Linux distribution for use with Microsoft cloud services and related products.

## Who's using CBL-Mariner today?

CBL-Mariner is used internally by Microsoft and several
derivative versions are used by various teams within Microsoft.

These include:

- [Azure Kubernetes Services](https://kubernetes.io/) - Production grade
  container orchestration with CBL-Mariner as an option for container hosting.
- [AKS HCI](https://docs.microsoft.com/en-us/azure-stack/aks-hci/) - Azure
  Kubernetes Service on Azure Stack HCI - quick way to get started hosting
  Windows and Linux containers in your data center.

![CBL-Mariner Composition](images/MarinerComposition.png)

## Key Capabilities Of CBL-Mariner Linux

CBL-Mariner provides many of the traditional benefits of using Linux. In
addition to that, CBL-Mariner provides hardened security and efficient
lifecycle management.

- **CBL-Mariner core**
  - Minimal core system that supports a variety of profiles (Azure VM or on
bare-metal x64 or ARM64) and allows the customer to build on top of it
as needed.  
  - Lightweight footprint: 450MB uncompressed. 
- **Support & Updates**:
  - SLA for vulnerabilities.
  - Patches automatically available for the customer to update when most
    convenient for them.
  - `dnf` infrastructure used for upgrading packages.
- **Security hardened**
  - The kernel and other aspects of the OS are built with an emphasis on
    security and follow the secure-by-default principle, compliant with
    Microsoft security standards and industry certifications.
- **Federated Builds:**
  - Enables teams to innovate on top by allowing the generation and
    maintenance of packages on top of the CBL-Mariner builds.
  - With over 6000 packages already built, teams can customize their image easily. 
- **Robust Testing**
  - Through a robust testing matrix of package, image and kernel tests, we allow for earlier issue detections and mitigations prior to the image being published. 
- **Virtualization**
  - CBL-Mariner supports a container host image that includes the
    Kubernetes infrastructure.
- **Efficient lifecycle management**
  - CBL-Mariner supports both RPM package and image-based update mechanisms
	for releases - with an "evergreen" release alongside specific
	security-patched stable snaps.
  - New releases are made available annually and each release is supported for
	18 months.


## Getting Started With CBL-Mariner

Detailed instructions for building CBL-Mariner from sources are provided in the
[CBL-Mariner](https://github.com/microsoft/CBL-Mariner) GitHub repository.
This repository makes it possible for you to build a CBL-Mariner image, including all packages, from sources.

However, this is not the recommended approach. The
recommended approach is to use prebuilt images and packages provided by
Microsoft, which have already been built and validated. These prebuilt images are available in Azure Kubernetes Service.

## Building CBL-Mariner from Source
Should you still choose to build CBL-Mariner from source, the recommended approach
is to build a basic image and rely on the pre-compiled packages that are
already available in the package registry. Afterwards, you can replace some of
the default packages with your own versions if needed.

If you rely on prebuilt packages and are building a small image, you can
quickly get started and change configuration options that are independent of
the packages - such as preferred disk layout or the list of packages that get
included in the image by default.

To build your own product based on CBL-Mariner, you can use one of the existing
images. The recommended route for creating CBL-Mariner derivatives is to use
[CBL-MarinerDemo](https://github.com/microsoft/CBL-MarinerDemo) repository as a
template. However, if you need to change the base packages configuration, you
can also fork the main CBL-Mariner repository and make your own adjustments as
part of your fork.

When a new version of CBL-Mariner comes out, you can then simply do a git
rebase of your own changes on top of the new CBL-Mariner version. If your
changes are generic enough, you can also contribute your changes by submitting
a pull request - this will free you from the responsibility of having to
regularly rebase high number of custom commits in your own repository.

The [CBL-MarinerDemo](https://github.com/microsoft/CBL-MarinerDemo) repository
provides you with a basic template for getting started with your own
CBL-Mariner derivates for use with custom products. From there, you can
create a CBL-Mariner based product or you can generate quick experimental debug
builds to try out new ideas.

The CBL-MarinerDemo repository also demonstrates how you can augment
CBL-Mariner without forking the CBL-Mariner repository. This can be useful if
all you're doing is building upon the default configuration and adding your
own packages to it.

The CBL-MarinerDemo repository contains the SPEC file and sources for building
a simple "Hello World" application. This repository also includes a simple
"os-subrelease" package that allows you to add identifying information about
your derivative to an /etc/os-subrelease file.

### Using CBL-Mariner With AKS

CBL-Mariner can be also used as an AKS container host. This is accomplished through
a combination of az-cli and Kubernetes services.

First, install kubectl through az-cli:

    az aks install-cli

Deploying CBL-Mariner on AKS is described in detail in the following resources:

- [Microsoft Container Service: Managed Clusters](https://docs.microsoft.com/en-us/azure/templates/microsoft.containerservice/managedclusters?tabs=json)
- [Network Policies Setup](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

Below is an example of deploying AKS CBL-Mariner cluster with an ARM template:

1. First, create template file named `marineraksarm.yml`:

    {
      "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
      "contentVersion": "1.0.0.1",
      "parameters": {
        "clusterName": {
          "type": "string",
          "defaultValue": "marinerakscluster",
          "metadata": {
            "description": "The name of the Managed Cluster resource."
          }
        },
        "location": {
          "type": "string",
          "defaultValue": "[resourceGroup().location]",
          "metadata": {
            "description": "The location of the Managed Cluster resource."
          }
        },
        "dnsPrefix": {
          "type": "string",
          "metadata": {
            "description": "Optional DNS prefix to use with hosted Kubernetes API server FQDN."
          }
        },
        "osDiskSizeGB": {
          "type": "int",
          "defaultValue": 0,
          "minValue": 0,
          "maxValue": 1023,
          "metadata": {
            "description": "Disk size (in GB) to provision for each of the agent pool nodes. This value ranges from 0 to 1023. Specifying 0 will apply the default disk size for that agentVMSize."
          }
        },
        "agentCount": {
          "type": "int",
          "defaultValue": 3,
          "minValue": 1,
          "maxValue": 50,
          "metadata": {
            "description": "The number of nodes for the cluster."
          }
        },
        "agentVMSize": {
          "type": "string",
          "defaultValue": "Standard_DS2_v2",
          "metadata": {
            "description": "The size of the Virtual Machine."
          }
        },
        "linuxAdminUsername": {
          "type": "string",
          "metadata": {
            "description": "User name for the Linux Virtual Machines."
          }
        },
        "sshRSAPublicKey": {
          "type": "string",
          "metadata": {
            "description": "Configure all linux machines with the SSH RSA public key string. Your key should include three parts, for example 'ssh-rsa AAAAB...snip...UcyupgH azureuser@linuxvm'"
          }
        },
        "osType": {
          "type": "string",
          "defaultValue": "Linux",
          "allowedValues": [
            "Linux"
          ],
          "metadata": {
            "description": "The type of operating system."
          }
        },
        "osSKU": {
          "type": "string",
          "defaultValue": "CBLMariner",
          "allowedValues": [
            "CBLMariner",
            "Ubuntu",
          ],
          "metadata": {
            "description": "The Linux SKU to use."
          }
        }
      },
      "resources": [
        {
          "type": "Microsoft.ContainerService/managedClusters",
          "apiVersion": "2021-03-01",
          "name": "[parameters('clusterName')]",
          "location": "[parameters('location')]",
          "properties": {
            "dnsPrefix": "[parameters('dnsPrefix')]",
            "agentPoolProfiles": [
              {
                "name": "agentpool",
                "mode": "System",
                "osDiskSizeGB": "[parameters('osDiskSizeGB')]",
                "count": "[parameters('agentCount')]",
                "vmSize": "[parameters('agentVMSize')]",
                "osType": "[parameters('osType')]",
                "osSKU": "[parameters('osSKU')]",
                "storageProfile": "ManagedDisks"
              }
            ],
            "linuxProfile": {
              "adminUsername": "[parameters('linuxAdminUsername')]",
              "ssh": {
                "publicKeys": [
                  {
                    "keyData": "[parameters('sshRSAPublicKey')]"
                  }
                ]
              }
            }
          },
          "identity": {
              "type": "SystemAssigned"
          }
        }
      ],
      "outputs": {
        "controlPlaneFQDN": {
          "type": "string",
          "value": "[reference(parameters('clusterName')).fqdn]"
        }
      }
    }

2. Deploying a CBL-Mariner cluster with az-cli requires the latest release of the aks-preview extension:

    az extension remove --name aks-preview
    az extension add --name aks-preview

3. Once you have the latest aks-preview extension installed, you can create a CBL-Mariner cluster with the following commands:

    az group create --name cblmarinertestrg --location centraluseuap
    az deployment group create --resource-group cblmarinertestrg --template-file marineraksarm.yml --parameters clusterName=testcblmarinercluster dnsPrefix=cblmarineraks1 linuxAdminUsername=azureuser sshRSAPublicKey='<contents of your id_rsa.pub>'
    az aks get-credentials --resource-group cblmarinertestrg --name testcblmarinercluster
    kubectl get pods --all-namespaces

4. To deploy a CBL-Mariner container, use the following set of commands:

    az group create --name cblmarinertestrg --location centraluseuap
    az aks create --name testcblmarinercluster --resource-group cblmarinertestrg --os-sku CBL-Mariner --ssh-key-value <path to id_rsa.pub>
    az aks get-credentials --resource-group cblmarinertestrg --name testcblmarinercluster
    kubectl get pods --all-namespaces

![kubernetes pods](images/kubernetes-output.jpg)

5. You may need to restart the pods in the kube-system namespace:

    kubectl -n kube-system rollout restart deploy

## System Administration

In most cases, you would not need to do any on-system administration tasks and
you should use higher level tools instead. However, if you do have a situation
where you need to manually install packages or otherwise do low level
maintenance work, then you can do so by logging into the system over SSH or
through the serial console.

### Enabling Serial Console

The serial console is useful if you want to view boot logs or have a console to
the headless VM - or for GDB debugging on the VM. You can enable the serial
console by creating a named pipe to the Hyper-V VM.

See instructions on this page:

- [Enabling Hyper-V Serial Console](https://dev.azure.com/mariner-org/mariner/_wiki/wikis/mariner.wiki/37/Enable-Hyper-V-Serial-Console).  

### Managing Services With systemd

CBL-Mariner uses `systemd` for managing all running services. This means that you
can use `systemctl` for checking status, enabling, disabling, starting and
stopping services.

To view descriptions of all loaded and active services, run the `systemctl` command without any arguments:

    systemctl

To see all loaded, active and inactive services, supply the `--all` flag to `systemctl`:

    systemctl --all

To see all unit files and their current status run:

    systemctl list-unit-files

You can always use a combination of commands to show only certain kinds of services. For example, you can combine one of the above commands with grep:

    systemctl list-unit-files | grep network

For detailed usage instrucitons and full descriptions of all available options, check the official linux man pages for systemd utilities:

- [systemctl](https://www.man7.org/linux/man-pages/man1/systemctl.1.html)
- [systemd](https://man7.org/linux/man-pages/man1/systemd.1.html)

### Starting and stopping services

To start or stop a service you simply provide the `start` or `stop` command to `systemctl` followed by the name of the service you want to control:

    systemctl start lighttpd
    systemctl stop lighttpd

### Inspecting System Events

Use `journalctl` to inspect important system messages from systemd. It is
useful when something goes wrong and the system is either restarted or you
simply need to review what happened. To display messages in systemd log from
when the system was started last time, use the command:

    journalctl -b

If you want to specifically list messages generated by a particular service
then you can use the following command:

    journalctl -u [service-name]

`service-name` is in this case the same name you would pass to `systemctl
[start|stop]` group of commands and it represents the name by which systemd
knows a particular service.

To see what other options are available, run:

    man journalctl

### Installing a web server

To install the web server run:

    dnf install httpd

> You may need to manually create `/var/logs` directory:
> `sudo mkdir -p /var/logs`

You can start and stop the web server using the `systemctl` command.

    systemctl httpd start
    systemctl httpd stop

To check that the webserver is running do:

    sudo netstat -anl | grep :80

You also need to open port 80 on your vm. You can do this using the az-cli utility:

    az vm open-port --port 80 --name [vm-name] --resource-group [rg]

To show the public IP address of your vm, you can run this command:

    az vm show --name [vm-name] --resource-group [rg] --show-details --query [publicIps] --output tsv

### Configuring Firewall

Use the official Azure-CLI client to configure the firewall for your virtual machine.

## Updating CBL-Mariner

Minor versions of CBL-Mariner prebuilt images are released monthly. The frequency of prebuilt package updates depends on the severity of the CVE, and we maintain a defined SLA for each severity level. 

### Package Management Overview

The CBL-Mariner OS uses the "Tiny Dandified" (TDNF) package manager. TDNF is a C
based successor of the DNF package manager, which itself is the successor to
Fedora’s YUM package manager. TDNF is included in the base CBL-Mariner image by
default.
	
When installing a package on your system, TDNF connects to one or more RPM
repositories in the cloud. If a package is unavailable in one repository, a
subsequent repository is checked.

Repositories, and the order in which those repositories are scanned, are
specified in configuration files that reside in your CBL-Mariner image.

The TDNF configuration file /etc/tdnf/tdnf.conf contains configuration
information about how TDNF should handle caching and other local functions. It
also contains a pointer to the repo configuration directory. Owing to its YUM
heritage, the default is to point to /etc/yum.repos.d/ which contains the list
of repo configuration files.

### RPM Repositories

By default, all CBL-Mariner images are partially configured to connect with the
curated CBL-Mariner Repository. These repositories are mariner-official-base.repo
and mariner-official-update.repo. The Base Repository always maintains a static
list of RPMs built at the time of release.

The Update Repository always maintains a forward rolling list of Security
Patched RPMs updated over time.

This repository holds all RPMs that are built from the CBL-Mariner Repository. Please note that this list of
packages is a "super-set" of the packages installed on the Minimal
CBL-Mariner Image. The CBL-Mariner team manages more packages than the ones installed in
the default image.

### Regular Upgrades

To upgrade all your installed packages to the latest CBL-Mariner releases run:

    sudo dnf upgrade

>If you are running this command for the first time, dnf will ask you to confirm
>GPG keys. This is fine and you can just press 'y' to continue with the upgrade.

### Available Packages

Packages that are currently available can be found [here](https://packages.microsoft.com/cbl-mariner). You may add and build packages locally by adding them to your derivative
repository. 