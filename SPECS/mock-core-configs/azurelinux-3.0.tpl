config_opts['root'] = 'azl-{{ releasever }}-{{ target_arch }}'

config_opts['chroot_setup_cmd'] = 'install azurelinux-tools-package-build'
config_opts['dist'] = 'azl3'
config_opts['package_manager'] = 'dnf'
config_opts['description'] = 'Azure Linux 3.0'
config_opts['releasever'] = '3.0'

config_opts['ssl_extra_certs'] = ['/etc/pki/tls/certs/ca-bundle.trust.crt', '/etc/pki/tls/certs/']

config_opts['extra_chroot_dirs'] = [ '/run/lock', ]
config_opts['useradd'] = 'useradd -o -m -u {{chrootuid}} -g {{chrootgid}} -d {{chroothome}} -N {{chrootuser}}'

config_opts['dnf.conf'] = """
[main]
reposdir=/dev/null
gpgcheck=0
assumeyes=1
install_weak_deps=0
clean_requirements_on_remove=True
skip_if_unavailable=True

[azurelinux-official-base]
name=Azure Linux Official Base $releasever $basearch
baseurl=https://packages.microsoft.com/azurelinux/$releasever/prod/base/$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/azure-linux/MICROSOFT-RPM-GPG-KEY
gpgcheck=1
repo_gpgcheck=1
enabled=1
sslverify=1

[azurelinux-official-ms-oss]
name=Azure Linux Official Microsoft Open-Source $releasever $basearch
baseurl=https://packages.microsoft.com/azurelinux/$releasever/prod/ms-oss/$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/azure-linux/MICROSOFT-RPM-GPG-KEY
gpgcheck=1
repo_gpgcheck=1
enabled=1
sslverify=1
"""
