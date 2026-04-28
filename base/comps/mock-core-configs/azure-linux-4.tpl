config_opts['chroot_setup_cmd'] = 'install bash bzip2 coreutils cpio diffutils dnf5 azurelinux-release-common findutils gawk glibc-minimal-langpack grep gzip info patch azurelinux-rpm-config rpm-build sed shadow-utils tar unzip util-linux which xz'
# TODO: Replace the explicit chroot_setup_cmd package list above with a
# distro-provided build group or metapackage (e.g. @buildsys-build) once one is
# defined for Azure Linux 4.0.

config_opts['dist'] = 'azl4'
config_opts['macros']['%dist'] = '.azl4'
config_opts['macros']['%vendor'] = 'Microsoft Corporation'
config_opts['macros']['%distribution'] = 'Azure Linux'
config_opts['releasever'] = '4.0'
config_opts['package_manager'] = 'dnf5'
config_opts['extra_chroot_dirs'] = [ '/run/lock', ]

# Bootstrap from the published Azure Linux 4.0 base/core container image.
config_opts['use_bootstrap'] = True
config_opts['use_bootstrap_image'] = True
config_opts['bootstrap_image'] = 'azlpubstagingacroxz2o4gw.azurecr.io/azurelinux/base/core:4.0'
# The image ships dnf5 but not dnf5-plugins, so mark it as not "ready" and
# let mock install the rest of the bootstrap packages itself.
config_opts['bootstrap_image_ready'] = False

config_opts['dnf.conf'] = """
[main]
keepcache=1
debuglevel=2
reposdir=/dev/null
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
syslog_ident=mock
syslog_device=
metadata_expire=0
mdpolicy=group:primary
best=1
install_weak_deps=0
protected_packages=
user_agent={{ user_agent }}

# Azure Linux 4.0 alpha2-prod blob storage repos.
# Note: alpha2 staging metadata is unsigned, so gpgcheck=0.

[azurelinux-base]
name=Azure Linux Base $releasever $basearch
baseurl=https://stcontroltowerdevjwisitg.blob.core.windows.net/alpha2-prod/base/$basearch
gpgcheck=0
enabled=1

[azurelinux-build-deps]
name=Azure Linux Additional Build Dependencies $releasever $basearch
baseurl=https://stcontroltowerdevjwisitg.blob.core.windows.net/alpha2-prod/sdk/$basearch
gpgcheck=0
enabled=1

"""
