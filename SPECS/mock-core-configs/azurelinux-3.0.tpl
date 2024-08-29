config_opts['chroot_setup_cmd'] = 'install'

# General packages required
config_opts['chroot_setup_cmd'] += ' autoconf'
config_opts['chroot_setup_cmd'] += ' automake'
config_opts['chroot_setup_cmd'] += ' bash'
config_opts['chroot_setup_cmd'] += ' binutils'
config_opts['chroot_setup_cmd'] += ' bzip2'
config_opts['chroot_setup_cmd'] += ' coreutils'
config_opts['chroot_setup_cmd'] += ' cpio'
config_opts['chroot_setup_cmd'] += ' diffutils'
config_opts['chroot_setup_cmd'] += ' findutils'
config_opts['chroot_setup_cmd'] += ' gawk'
config_opts['chroot_setup_cmd'] += ' gcc-c++'
config_opts['chroot_setup_cmd'] += ' gcc'
config_opts['chroot_setup_cmd'] += ' glibc-devel'
config_opts['chroot_setup_cmd'] += ' grep'
config_opts['chroot_setup_cmd'] += ' gzip'
config_opts['chroot_setup_cmd'] += ' info'
config_opts['chroot_setup_cmd'] += ' kernel-headers'
config_opts['chroot_setup_cmd'] += ' make'
config_opts['chroot_setup_cmd'] += ' azurelinux-release'
config_opts['chroot_setup_cmd'] += ' azurelinux-rpm-macros'
config_opts['chroot_setup_cmd'] += ' patch'
config_opts['chroot_setup_cmd'] += ' perl-generators'
config_opts['chroot_setup_cmd'] += ' python3'
config_opts['chroot_setup_cmd'] += ' python3-rpm-generators'
config_opts['chroot_setup_cmd'] += ' pyproject-rpm-macros'
config_opts['chroot_setup_cmd'] += ' rpm-build'
config_opts['chroot_setup_cmd'] += ' sed'
config_opts['chroot_setup_cmd'] += ' shadow-utils'
config_opts['chroot_setup_cmd'] += ' tar'
config_opts['chroot_setup_cmd'] += ' unzip'
config_opts['chroot_setup_cmd'] += ' util-linux'
config_opts['chroot_setup_cmd'] += ' which'
config_opts['chroot_setup_cmd'] += ' xz'

config_opts['dist'] = 'azl3'
config_opts['extra_chroot_dirs'] = [ '/run/lock', ]
config_opts['releasever'] = '3.0'
config_opts['package_manager'] = 'dnf'
config_opts['useradd'] = 'useradd -o -m -u {{chrootuid}} -g {{chrootgid}} -d {{chroothome}} -N {{chrootuser}}'
config_opts['root'] = 'azl-{{ releasever }}-{{ target_arch }}'

config_opts['dnf.conf'] = """
[main]
gpgcheck=0
installonly_limit=3
clean_requirements_on_remove=True
skip_if_unavailable=True
assumeyes=1
# exclude=ca-certificates-shared ca-certificates

# repos
[azurelinux-official-base]
name=Azure Linux Official Base $releasever $basearch
baseurl=https://packages.microsoft.com/azurelinux/$releasever/prod/base/$basearch
gpgkey=file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY
gpgcheck=1
repo_gpgcheck=1
enabled=1
skip_if_unavailable=True
sslverify=1

[azurelinux-official-ms-oss]
name=Azure Linux Official Microsoft Open-Source $releasever $basearch
baseurl=https://packages.microsoft.com/azurelinux/$releasever/prod/ms-oss/$basearch
gpgkey=file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY
gpgcheck=1
repo_gpgcheck=1
enabled=1
skip_if_unavailable=True
sslverify=1
"""
