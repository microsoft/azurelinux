# Fedora Comps #

comps files are XML files used by various Fedora tools to perform grouping of packages into functional groups.

## How comps is used ##

### Installation ###

comps is used by the installer during package selection. On the Software Selection screen, environment groups (as defined by the `environment` keyword in `comps.xml`) are listed down the left-hand side. All optional groups (defined by the `group` keyword) for that environment (listed in the environment's `optionlist`) are shown at the top of the right-hand pane. Other groups which have `uservisible` set are displayed lower in the right-hand pane.

At install time, the installer will usually install the `mandatory`, `default` and appropriate `conditional` packages from all groups listed in the selected environment group's `grouplist`, plus those from any optional groups the user selected on the right-hand side. See below for more details on these 'levels'.

### Running System ###

In dnf, groups and environment groups are used by the `dnf group install` and `dnf group remove` commands, and can be queried with the `dnf group list` command. There are many others besides these: see the [dnf documentation](https://dnf.readthedocs.io/en/latest/index.html) for more on this.

### Tree, Release, and Image Composition ###

The kickstart files in [fedora-kickstarts](https://pagure.io/fedora-kickstarts.git) use the group and environment group definitions from comps. Multiple tools use these kickstarts to compose different types of images, and the release trees. The manifests for rpm-ostree-based Fedora variants in [workstation-ostree-config](https://pagure.io/workstation-ostree-config) (the name is a misnomer these days) are synced against comps using the `comps-sync.py` script, and used to define the package sets included in those variants.

### Package levels ###

In any group, there are four levels of packages: `optional`, `default`, `mandatory`, and `conditional`.

 * `mandatory` - these packages must be installed for the group to be considered installed
 * `default` - these packages are installed by default, but can be removed while the group is still considered installed
 * `optional` - these packages are not installed by default, but can be pulled in by kickstart or dnf options
 * `conditional` - these packages are brought in if their `requires` package is installed

When using the interactive installer, you cannot include `optional` packages. However, if using a kickstart, you can add the `--optional` option for a group to specify that its optional packages should be included. Similarly, when installing a group with `dnf`, you can pass `--with-optional` to include the optional packages.

### Categories ###

Categories are barely used any more. They used to be something like environment groups for an older form of the Fedora installer. Some older graphical package management tools can still display these categories.

### Developing comps ###

For Fedora packagers:

    git clone ssh://git@pagure.io/fedora-comps.git

For others:

    git clone https://pagure.io/fedora-comps.git

When changing the packages, make sure the file is sorted. This helps to make it more maintainable. Use `make sort` command to fix the sorting. Also run `make validate` to check for XML syntax errors. You can submit pull requests using the common Github-style workflow - fork the repository from [the web UI](https://pagure.io/fedora-comps), push your changes to your fork, and submit a pull request for it. If you are not familiar with this workflow, see the [Pagure documentation](https://docs.pagure.org/pagure/usage/pull_requests.html).

## For more info ##

For more information, including rules on how and when to edit comps, see the [Fedora project wiki](https://fedoraproject.org/wiki/How_to_use_and_edit_comps.xml_for_package_groups).

Bugs against comps can be filed as Pagure [issues](https://pagure.io/fedora-comps/issues).
