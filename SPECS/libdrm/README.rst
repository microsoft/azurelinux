libdrm - userspace library for drm
----------------------------------

This is libdrm, a userspace library for accessing the DRM, direct rendering
manager, on Linux, BSD and other operating systems that support the ioctl
interface.
The library provides wrapper functions for the ioctls to avoid exposing the
kernel interface directly, and for chipsets with drm memory manager, support
for tracking relocations and buffers.
New functionality in the kernel DRM drivers typically requires a new libdrm,
but a new libdrm will always work with an older kernel.

libdrm is a low-level library, typically used by graphics drivers such as
the Mesa drivers, the X drivers, libva and similar projects.


Compiling
---------

libdrm has two build systems, a legacy autotools build system, and a newer
meson build system. The meson build system is much faster, and offers a
slightly different interface, but otherwise provides an equivalent feature set.

To use it:

    meson builddir/

By default this will install into /usr/local, you can change your prefix
with --prefix=/usr (or `meson configure builddir/ -Dprefix=/usr` after 
the initial meson setup).

Then use ninja to build and install:

    ninja -C builddir/ install

If you are installing into a system location you will need to run install
separately, and as root.


Alternatively you can invoke autotools configure:

	./configure

By default, libdrm  will install into the /usr/local/  prefix.  If you
want  to  install   this  DRM  to  replace  your   system  copy,  pass
--prefix=/usr and  --exec-prefix=/ to configure.  If  you are building
libdrm  from a  git checkout,  you first  need to  run  the autogen.sh
script.  You can  pass any options to autogen.sh  that you would other
wise  pass to configure,  or you  can just  re-run configure  with the
options you need once autogen.sh finishes.

Next step is to build libdrm:

	make

and once make finishes successfully, install the package using

	make install

If you are installing into a system location, you will need to be root
to perform the install step.
