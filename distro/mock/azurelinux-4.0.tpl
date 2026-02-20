# Disable bootstrap image for now.
config_opts['use_bootstrap_image'] = False

# General packages required
config_opts['chroot_setup_cmd'] = 'install @{% if mirrored %}buildsys-{% endif %}build'

# Provide path to system-installed logging.ini file.
config_opts['log_config_file'] = '/etc/mock/logging.ini'

# Plugin config
config_opts['plugin_conf']['ccache_enable'] = True

# Failure behavior
config_opts['cleanup_on_success'] = False
config_opts['cleanup_on_failure'] = False

config_opts['dist'] = 'azl4'
config_opts['extra_chroot_dirs'] = ['/run/lock']
config_opts['releasever'] = '43'
config_opts['package_manager'] = 'dnf5'
config_opts['update_before_build'] = False
config_opts['root'] = 'azl-4.0-{{ target_arch }}'

# When rpmautospec is enabled,
# the %autorelease and %autochangelog macros can be used in spec files
# to automatically generate release numbers and changelog entries based
# on the git history, eliminating the need to manually maintain them.
config_opts['plugin_conf']['rpmautospec_enable'] = True
config_opts['plugin_conf']['rpmautospec_opts'] = {
    'requires': ['rpmautospec'],
    'cmd_base': ['/usr/bin/rpmautospec', 'process-distgit'],
}

config_opts['dnf.conf'] = """
[main]
zchunk=true
keepcache=1
system_cachedir=/var/cache/dnf
debuglevel=2
reposdir=/dev/null
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
syslog_ident=mock
syslog_device=
install_weak_deps=0
metadata_expire=0
best=1
module_platform_id=platform:f{{ releasever }}
protected_packages=
user_agent={{ user_agent }}

# repos

[local]
name=local
baseurl=https://kojipkgs.fedoraproject.org/repos/f{{ releasever }}-build/latest/$basearch/
cost=2000
enabled={{ not mirrored }}
skip_if_unavailable=False

{% if mirrored %}
[fedora]
name=fedora
metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-$releasever&arch=$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
skip_if_unavailable=False

[updates]
name=updates
metalink=https://mirrors.fedoraproject.org/metalink?repo=updates-released-f$releasever&arch=$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
skip_if_unavailable=False
{% endif %}
"""
