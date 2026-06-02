# ISO Installer in Local VM

The Azure Linux ISO may work in some bare-metal scenarios, but is generally intended for installation to a Virtual Machine.

## Using ISO Installer in Hyper-V VM
From a Windows PC:

**Create Generation 2 Virtual Machine with Hyper-V**

1. From Hyper-V Manager, select _Action->New->Virtual Machine_.
1. Provide a name for your VM and press _Next >_.
1. Select _Generation 2_, then press _Next >_.
1. Uncheck _Use Dynamic Memory for this virtual machine_, then press _Next >_.
1. Select a virtual switch, then press _Next >_.
1. Select _Create a virtual hard disk_, choose a location for your VHDX and set your desired disk size.  Then press _Next >_.
1. Select _Install an operating system from a bootable image file_ and browse to your Azure Linux ISO.
1. Press _Finish_.

**Adjust VM Settings**

1. Right click your virtual machine from Hyper-V Manager.
1. Select _Settings..._
1. Select Security and uncheck _Enable Secure Boot_.
   - _Note: Secure Boot will be supported in a future release of Azure Linux._
1. Select _Apply_ to apply all changes.

**Boot ISO Installer**
1. Right click your VM and select _Connect..._.
1. Select _Start_.
1. Follow the installer prompts to install your image.
   - During installation menu, ensure all `[!]` are addressed in order to continue.
1. When installation completes, press Enter to reboot the machine.
1. When prompted, sign in to your new Azure Linux installation using the username and password provisioned through the installer.
