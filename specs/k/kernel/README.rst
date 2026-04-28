===================
The Kernel dist-git
===================

The kernel is maintained in a `source tree`_ rather than directly in dist-git.
The specfile is maintained as a `template`_ in the source tree along with a set
of build scripts to generate configurations, (S)RPMs, and to populate the
dist-git repository.

The `documentation`_ for the source tree covers how to contribute and maintain
the tree.

If you're looking for the downstream patch set it's available in the source
tree with "git log master..ark-patches" or
`online`_.

Each release in dist-git is tagged in the source repository so you can easily
check out the source tree for a build. The tags are in the format
name-version-release, but note release doesn't contain the dist tag since the
source can be built in different build roots (Fedora, CentOS, etc.)

.. _source tree: https://gitlab.com/cki-project/kernel-ark.git
.. _template: https://gitlab.com/cki-project/kernel-ark/-/blob/os-build/redhat/kernel.spec.template
.. _documentation: https://gitlab.com/cki-project/kernel-ark/-/wikis/home
.. _online: https://gitlab.com/cki-project/kernel-ark/-/commits/ark-patches
