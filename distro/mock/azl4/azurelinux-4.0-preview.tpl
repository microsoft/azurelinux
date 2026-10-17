include('azurelinux-4.0.tpl')

config_opts['root'] = 'azl-4.0-preview-{{ target_arch }}'

config_opts['dnf.conf'] += """
[azurelinux-preview-base]
name=Azure Linux 4 Preview Base
baseurl=https://packages.microsoft.com/azurelinux/4/preview/base/$basearch
enabled=1
skip_if_unavailable=False
excludepkgs=rpmautospec-0.8.4*

[azurelinux-preview-builddeps]
name=Azure Linux 4 Preview Build Dependencies
baseurl=https://packages.microsoft.com/azurelinux/4/preview/builddeps/$basearch
enabled=1
skip_if_unavailable=False
excludepkgs=rpmautospec-0.8.4*

"""
