# Disable bootstrap image for now.
config_opts['use_bootstrap_image'] = False

# General packages required
# TODO: This will be moved into a comp.xml file.
config_opts['chroot_setup_cmd'] = 'install'
config_opts['chroot_setup_cmd'] += ' azurelinux-stage1-compat'
config_opts['chroot_setup_cmd'] += ' bash'
config_opts['chroot_setup_cmd'] += ' bzip2'
config_opts['chroot_setup_cmd'] += ' coreutils'
config_opts['chroot_setup_cmd'] += ' cpio'
config_opts['chroot_setup_cmd'] += ' diffutils'
config_opts['chroot_setup_cmd'] += ' azurelinux-release-common'
config_opts['chroot_setup_cmd'] += ' findutils'
config_opts['chroot_setup_cmd'] += ' gawk'
config_opts['chroot_setup_cmd'] += ' glibc-minimal-langpack'
config_opts['chroot_setup_cmd'] += ' grep'
config_opts['chroot_setup_cmd'] += ' gzip'
config_opts['chroot_setup_cmd'] += ' info'
config_opts['chroot_setup_cmd'] += ' patch'
config_opts['chroot_setup_cmd'] += ' azurelinux-rpm-config'
config_opts['chroot_setup_cmd'] += ' rpm-build'
config_opts['chroot_setup_cmd'] += ' sed'
config_opts['chroot_setup_cmd'] += ' shadow-utils'
config_opts['chroot_setup_cmd'] += ' tar'
config_opts['chroot_setup_cmd'] += ' unzip'
config_opts['chroot_setup_cmd'] += ' util-linux'
config_opts['chroot_setup_cmd'] += ' which'
config_opts['chroot_setup_cmd'] += ' xz'

# Provide path to system-installed logging.ini file.
config_opts['log_config_file'] = '/etc/mock/logging.ini'

# Plugin config
# NOTE: We disable ccache until its dependencies are available for stage2.
config_opts['plugin_conf']['ccache_enable'] = False

# Failure behavior
config_opts['cleanup_on_success'] = False
config_opts['cleanup_on_failure'] = False

config_opts['macros']['%dist'] = '.azl4'
config_opts['macros']['%vendor'] = 'Microsoft Corporation'
config_opts['macros']['%distribution'] = 'Azure Linux'
config_opts['dist'] = 'azl4'
config_opts['extra_chroot_dirs'] = ['/run/lock']
config_opts['releasever'] = '4.0'
config_opts['package_manager'] = 'dnf5'
config_opts['update_before_build'] = False
config_opts['root'] = 'azl-4.0-stage2-{{ target_arch }}'

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

[koji]
name=koji
baseurl=http://20.88.251.114/kojifiles/repos-dist/azl4-bootstrap-rpms-tag-20260226/latest/$basearch/
cost=1
enabled=1
skip_if_unavailable=False
"""
