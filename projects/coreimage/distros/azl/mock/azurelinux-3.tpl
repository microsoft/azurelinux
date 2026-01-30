config_opts['chroot_setup_cmd'] = 'install'

# Additional packages required in the bootstrap root
config_opts['use_bootstrap_image'] = False
config_opts['bootstrap_chroot_additional_packages'] = ['ca-certificates']

# General packages required
config_opts['chroot_setup_cmd'] += ' build-essential'
config_opts['chroot_setup_cmd'] += ' core-packages-container'

# Additional core requirements
config_opts['chroot_setup_cmd'] += ' audit'
config_opts['chroot_setup_cmd'] += ' azurelinux-check-macros'
config_opts['chroot_setup_cmd'] += ' ca-certificates'
config_opts['chroot_setup_cmd'] += ' createrepo_c'
config_opts['chroot_setup_cmd'] += ' dwz'
config_opts['chroot_setup_cmd'] += ' flex'
config_opts['chroot_setup_cmd'] += ' glib'
config_opts['chroot_setup_cmd'] += ' glibc-iconv'
config_opts['chroot_setup_cmd'] += ' glibc-locales-all'
config_opts['chroot_setup_cmd'] += ' glibc-nscd'
config_opts['chroot_setup_cmd'] += ' glibc-tools'
config_opts['chroot_setup_cmd'] += ' libltdl'
config_opts['chroot_setup_cmd'] += ' libmetalink'
config_opts['chroot_setup_cmd'] += ' libpipeline'
config_opts['chroot_setup_cmd'] += ' msopenjdk-17'
config_opts['chroot_setup_cmd'] += ' ncurses-compat'
config_opts['chroot_setup_cmd'] += ' ncurses-term'
config_opts['chroot_setup_cmd'] += ' ocaml-srpm-macros'
config_opts['chroot_setup_cmd'] += ' openssl-perl'
config_opts['chroot_setup_cmd'] += ' openssl-static'
config_opts['chroot_setup_cmd'] += ' perl'
config_opts['chroot_setup_cmd'] += ' procps-ng'
config_opts['chroot_setup_cmd'] += ' pyproject-rpm-macros'
config_opts['chroot_setup_cmd'] += ' python3-rpm-generators'
config_opts['chroot_setup_cmd'] += ' python3-setuptools'
config_opts['chroot_setup_cmd'] += ' rpm-build'
config_opts['chroot_setup_cmd'] += ' sqlite'
config_opts['chroot_setup_cmd'] += ' util-linux'
config_opts['chroot_setup_cmd'] += ' texinfo'
config_opts['chroot_setup_cmd'] += ' which'

# -lang requirements
config_opts['chroot_setup_cmd'] += ' bash-lang'
config_opts['chroot_setup_cmd'] += ' chkconfig-lang'
config_opts['chroot_setup_cmd'] += ' coreutils-lang'
config_opts['chroot_setup_cmd'] += ' cpio-lang'
config_opts['chroot_setup_cmd'] += ' elfutils-libelf-lang'
config_opts['chroot_setup_cmd'] += ' findutils-lang'
config_opts['chroot_setup_cmd'] += ' gdbm-lang'
config_opts['chroot_setup_cmd'] += ' glibc-lang'
config_opts['chroot_setup_cmd'] += ' gnupg2-lang'
config_opts['chroot_setup_cmd'] += ' grep-lang'
config_opts['chroot_setup_cmd'] += ' newt-lang'
config_opts['chroot_setup_cmd'] += ' popt-lang'
config_opts['chroot_setup_cmd'] += ' procps-ng-lang'
config_opts['chroot_setup_cmd'] += ' rpm-lang'
config_opts['chroot_setup_cmd'] += ' sed-lang'
config_opts['chroot_setup_cmd'] += ' xz-lang'

# -devel requirements
config_opts['chroot_setup_cmd'] += ' bash-devel'
config_opts['chroot_setup_cmd'] += ' binutils-devel'
config_opts['chroot_setup_cmd'] += ' bzip2-devel'
config_opts['chroot_setup_cmd'] += ' curl-devel'
config_opts['chroot_setup_cmd'] += ' elfutils-devel'
config_opts['chroot_setup_cmd'] += ' elfutils-devel-static'
config_opts['chroot_setup_cmd'] += ' elfutils-libelf-devel'
config_opts['chroot_setup_cmd'] += ' elfutils-libelf-devel-static'
config_opts['chroot_setup_cmd'] += ' expat-devel'
config_opts['chroot_setup_cmd'] += ' file-devel'
config_opts['chroot_setup_cmd'] += ' flex-devel'
config_opts['chroot_setup_cmd'] += ' gdbm-devel'
config_opts['chroot_setup_cmd'] += ' glibc-devel'
config_opts['chroot_setup_cmd'] += ' gmp-devel'
config_opts['chroot_setup_cmd'] += ' libarchive-devel'
config_opts['chroot_setup_cmd'] += ' libassuan-devel'
config_opts['chroot_setup_cmd'] += ' libcap-devel'
config_opts['chroot_setup_cmd'] += ' libcap-ng-devel'
config_opts['chroot_setup_cmd'] += ' libffi-devel'
config_opts['chroot_setup_cmd'] += ' libgcc-devel'
config_opts['chroot_setup_cmd'] += ' libgomp-devel'
config_opts['chroot_setup_cmd'] += ' libksba-devel'
config_opts['chroot_setup_cmd'] += ' libltdl-devel'
config_opts['chroot_setup_cmd'] += ' libpipeline-devel'
config_opts['chroot_setup_cmd'] += ' libsolv-devel'
config_opts['chroot_setup_cmd'] += ' libssh2-devel'
config_opts['chroot_setup_cmd'] += ' libstdc++-devel'
config_opts['chroot_setup_cmd'] += ' libxcrypt-devel'
config_opts['chroot_setup_cmd'] += ' libxml2-devel'
config_opts['chroot_setup_cmd'] += ' mpfr-devel'
config_opts['chroot_setup_cmd'] += ' ncurses-devel'
config_opts['chroot_setup_cmd'] += ' openssl-devel'
config_opts['chroot_setup_cmd'] += ' popt-devel'
config_opts['chroot_setup_cmd'] += ' procps-ng-devel'
config_opts['chroot_setup_cmd'] += ' python3-devel'
config_opts['chroot_setup_cmd'] += ' readline-devel'
config_opts['chroot_setup_cmd'] += ' rpm-devel'
config_opts['chroot_setup_cmd'] += ' sqlite-devel'
config_opts['chroot_setup_cmd'] += ' tdnf-devel'
config_opts['chroot_setup_cmd'] += ' util-linux-devel'
config_opts['chroot_setup_cmd'] += ' xz-devel'
config_opts['chroot_setup_cmd'] += ' zlib-devel'
config_opts['chroot_setup_cmd'] += ' zstd-devel'

# HACK: Disable IMA to avoid errors running as non-admin building SRPMs
config_opts['files']['etc/rpm/macros.ima'] = "%__transaction_ima %{nil}"

# HACK: Work around issue with gpg
config_opts['environment']['GNUPGHOME'] = config_opts['environment']['HOME'] + '/.gnupg'
config_opts['files'][config_opts['environment']['GNUPGHOME'] + '/placeholder'] = ''

# Provide path to system-installed logging.ini file.
config_opts['log_config_file'] = '/etc/mock/logging.ini'

# Plugin config
config_opts['plugin_conf']['ccache_enable'] = True

# Failure behavior
config_opts['cleanup_on_success'] = False
config_opts['cleanup_on_failure'] = False

config_opts['dist'] = 'azl3'
config_opts['extra_chroot_dirs'] = ['/run/lock']
config_opts['releasever'] = '3.0'
config_opts['package_manager'] = 'dnf'
config_opts['update_before_build'] = False
config_opts['useradd'] = 'useradd -o -m -u {{chrootuid}} -g {{chrootgid}} -d {{chroothome}} -N {{chrootuser}}'
config_opts['root'] = 'azl-{{ releasever }}-{{ target_arch }}'

# Disable copying ca-trust dirs on Azure Linux 3.0 to avoid any symlinks under the host's
# ca-trust dirs from turning into non-symlink'd dirs in the root and later conflicting
# with the symlink installed by the 'ca-certificates-shared' package.
config_opts['ssl_copied_ca_trust_dirs'] = None

config_opts['dnf.conf'] = """
[main]
assumeyes=1
gpgcheck=0
install_weak_deps=False
keepcache=1
metadata_expire=0
reposdir=/dev/null
retries=20
# sslcacert=/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
sslverify=1
system_cachedir=/var/cache/dnf

[azurelinux]
name=Azure Linux Official Base 3.0 $basearch
baseurl=https://packages.microsoft.com/azurelinux/3.0/prod/base/$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/azure-linux/MICROSOFT-RPM-GPG-KEY
gpgcheck=1
pkg_gpgcheck=1
repo_gpgcheck=1

[azurelinux-extended]
name=Azure Linux Official Extended 3.0 $basearch
baseurl=https://packages.microsoft.com/azurelinux/3.0/prod/extended/$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/azure-linux/MICROSOFT-RPM-GPG-KEY
gpgcheck=1
pkg_gpgcheck=1
repo_gpgcheck=1

[azurelinux-debuginfo]
name=Azure Linux Official Base Debuginfo 3.0 $basearch
baseurl=https://packages.microsoft.com/azurelinux/3.0/prod/base/debuginfo/$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/azure-linux/MICROSOFT-RPM-GPG-KEY
gpgcheck=1
pkg_gpgcheck=1
repo_gpgcheck=1

[azurelinux-ms-oss]
name=Azure Linux Official MS OSS 3.0 $basearch
baseurl=https://packages.microsoft.com/azurelinux/3.0/prod/ms-oss/$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/azure-linux/MICROSOFT-RPM-GPG-KEY
gpgcheck=1
pkg_gpgcheck=1
repo_gpgcheck=1
"""
