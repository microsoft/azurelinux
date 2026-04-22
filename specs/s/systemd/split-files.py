import re, sys, os, collections

buildroot = sys.argv[1]
no_bootloader = '--no-bootloader' in sys.argv

known_files = '''
%ghost %config(noreplace) /etc/crypttab
%ghost %attr(0444,root,root) /etc/udev/hwdb.bin
/etc/inittab
# This directory is owned by openssh-server, but we don't want to introduce
# a dependency. So let's copy the config and co-own the directory.
%dir %attr(0700,root,root) /etc/ssh/sshd_config.d
%ghost %config(noreplace) /etc/vconsole.conf
%ghost %config(noreplace) /etc/X11/xorg.conf.d/00-keyboard.conf
%ghost %attr(0664,root,root) %verify(not group) /run/utmp
%ghost %attr(0664,root,root) %verify(not group) /var/log/wtmp
%ghost %attr(0660,root,root) %verify(not group) /var/log/btmp
%ghost %attr(0664,root,root) %verify(not md5 size mtime group) /var/log/lastlog
%ghost %config(noreplace) /etc/hostname
%ghost %config(noreplace) /etc/localtime
%ghost %config(noreplace) /etc/locale.conf
%ghost %attr(0444,root,root) %config(noreplace) /etc/machine-id
%ghost %config(noreplace) /etc/machine-info
%ghost %attr(0700,root,root) %dir /var/cache/private
%ghost %attr(0700,root,root) %dir /var/lib/private
%ghost %dir /var/lib/private/systemd
%ghost %dir /var/lib/private/systemd/journal-upload
%ghost /var/lib/private/systemd/journal-upload/state
%ghost %dir /var/lib/systemd/timesync
%ghost /var/lib/systemd/timesync/clock
%ghost %dir /var/lib/systemd/backlight
%ghost /var/lib/systemd/catalog/database
%ghost %dir /var/lib/systemd/coredump
%ghost /var/lib/systemd/journal-upload
%ghost %dir /var/lib/systemd/linger
%ghost %attr(0600,root,root) /var/lib/systemd/random-seed
%ghost %dir /var/lib/systemd/rfkill
%ghost %dir %verify(not mode group) /var/log/journal
%ghost %dir /var/log/journal/remote
%ghost %attr(0700,root,root) %dir /var/log/private
'''

known_files = {line.split()[-1]:line for line in known_files.splitlines()
               if line and not line.startswith('#')}

def files(root):
    os.chdir(root)
    todo = collections.deque(['.'])
    while todo:
        n = todo.pop()
        files = os.scandir(n)
        for file in files:
            yield file
            if file.is_dir() and not file.is_symlink():
                todo.append(file)

outputs = {suffix: open(f'.file-list-{suffix}', 'w')
           for suffix in (
                   'shared',
                   'libs',
                   'udev',
                   'ukify',
                   'boot',
                   'pam',
                   'rpm-macros',
                   'sysusers',
                   'devel',
                   'container',
                   'networkd',
                   'networkd-defaults',
                   'oomd-defaults',
                   'remote',
                   'resolve',
                   'tests',
                   'standalone-repart',
                   'standalone-tmpfiles',
                   'standalone-sysusers',
                   'standalone-shutdown',
                   'main',
           )}

for file in files(buildroot):
    n = file.path[1:]
    if re.match(r'''/usr/(share|include)$|
                    /usr/share/man(/man.|)$|
                    /usr/share/zsh(/site-functions|)$|
                    /usr/share/dbus-1$|
                    /usr/share/dbus-1/system.d$|
                    /usr/share/dbus-1/(system-|)services$|
                    /usr/share/polkit-1(/actions|/rules.d|)$|
                    /usr/share/pkgconfig$|
                    /usr/share/bash-completion(/completions|)$|
                    /usr(/lib|/lib64|/bin|/sbin|)$|
                    /usr/lib.*/(security|pkgconfig)$|
                    /usr/lib/rpm(/macros.d|)$|
                    /usr/lib/firewalld(/services|)$|
                    /usr/share/(locale|licenses|doc)|             # no $
                    /etc(/pam\.d|/xdg|/X11|/X11/xinit|/X11.*\.d|)$|
                    /etc/(dnf|dnf/protected.d)$|
                    /usr/(src|lib/debug)|                         # no $
                    /run$|
                    /var(/cache|/log|/lib|/run|)$
    ''', n, re.X):
        continue

    if n.endswith('.standalone'):
        if 'repart' in n:
            o = outputs['standalone-repart']
        elif 'tmpfiles' in n:
            o = outputs['standalone-tmpfiles']
        elif 'sysusers' in n:
            o = outputs['standalone-sysusers']
        elif 'shutdown' in n:
            o = outputs['standalone-shutdown']
        else:
            assert False, 'Found .standalone not belonging to known packages'

    elif '/security/pam_' in n or '/man8/pam_' in n:
        o = outputs['pam']
    elif '/rpm/' in n:
        o = outputs['rpm-macros']
    elif '/usr/lib/systemd/tests' in n:
        o = outputs['tests']
    elif 'ukify' in n and '/man/' not in n:
        o = outputs['ukify']
    elif re.search(r'/libsystemd-core-.*\.so$', n):
        o = outputs['main']
    elif re.search(r'/libsystemd-shared-.*\.so$', n):
        o = outputs['shared']
    elif re.search(r'/libcryptsetup-token-systemd-.*\.so$', n):
        o = outputs['udev']
    elif re.search(r'/lib.*\.pc$|/man3/|/usr/include|\.so$', n):
        o = outputs['devel']
    elif re.search(r'''journal-(remote|gateway|upload)|
                       systemd-remote\.conf|
                       /usr/share/systemd/gatewayd|
                       /var/log/journal/remote
    ''', n, re.X):
        o = outputs['remote']

    # Just the binary, the dir, and the man page.
    elif re.search(r'''systemd-sysusers$|
                       sysusers\.d$|
                       man/.*sysusers\.d\.5|
                       man/.*systemd-sysusers\.8
    ''', n, re.X):
        o = outputs['sysusers']

    elif re.search(r'''mymachines|
                       machinectl|
                       mount.ddi|
                       importctl|
                       portablectl|
                       systemd-nspawn|
                       systemd\.nspawn|
                       systemd-vmspawn|
                       systemd-dissect|
                       import-pubring|
                       systemd-machined|
                       systemd-import|
                       systemd-export|
                       systemd-pull|
                       systemd-mountfsd|
                       systemd-mountwork|
                       systemd-nsresource|
                       /machine.slice|
                       /machines.target|
                       var-lib-machines.mount|
                       org.freedesktop.(import|machine)1
    ''', n, re.X):
        o = outputs['container']

    # .network.example files go into systemd-networkd, and the matching files
    # without .example go into systemd-networkd-defaults
    elif (re.search(r'''/usr/lib/systemd/network/.*\.network$''', n)
          and os.path.exists(f'./{n}.example')):
        o = outputs['networkd-defaults']

    # Files that are "consumed" by systemd-networkd go into the -networkd
    # subpackage. As a special case, network-generator is co-owned also by
    # the -udev subpackage because systemd-udevd reads .link files.
    elif re.search(r'''/usr/lib/systemd/network/.*\.network|
                       networkd|
                       networkctl|
                       org.freedesktop.network1|
                       sysusers\.d/systemd-network.conf|
                       tmpfiles\.d/systemd-network.conf|
                       systemd\.network|
                       systemd\.netdev
    ''', n, re.X):
        o = outputs['networkd']
    elif 'network-generator' in n:
        o = (outputs['networkd'], outputs['udev'])

    elif '.so.' in n:
        o = outputs['libs']

    elif re.search(r'10-oomd-.*defaults.conf|lib/systemd/oomd.conf.d', n, re.X):
        o = outputs['oomd-defaults']

    elif re.search(r'''udev(?!\.pc)|
                       hwdb|
                       ac-power|
                       bootctl|
                       boot-update|
                       bless-boot|
                       boot-system-token|
                       bsod|
                       kernel-install|
                       installkernel|
                       vconsole|
                       backlight|
                       rfkill|
                       random-seed|
                       modules-load|
                       timesync|
                       crypttab|
                       cryptenroll|
                       cryptsetup|
                       kmod|
                       quota|
                       pstore|
                       sleep|suspend|hibernate|
                       systemd-tmpfiles-setup-dev|
                       network/98-default-mac-none.link|
                       network/99-default.link|
                       growfs|makefs|makeswap|mkswap|
                       fsck|
                       repart|
                       gpt-auto|
                       volatile-root|
                       veritysetup|
                       integritysetup|
                       integritytab|
                       remount-fs|
                       /initrd|
                       systemd[.-]pcr|
                       /pcrlock\.d|
                       systemd-measure|
                       /boot$|
                       /kernel/|
                       /kernel$|
                       /modprobe.d|
                       binfmt|
                       sysctl|
                       coredump|
                       homed|home1|
                       sysupdate|updatctl|
                       oomd|
                       portabled|portable1
    ''', n, re.X):     # coredumpctl, homectl, portablectl are included in the main package because
                       # they can be used to interact with remote daemons. Also, the user could be
                       # confused if those user-facing binaries are not available.
        o = outputs['udev']

    elif re.search(r'''/boot/efi|
                       /usr/lib/systemd/boot|
                       sd-boot|systemd-boot\.|loader.conf
    ''', n, re.X):
        o = outputs['boot']

    elif re.search(r'''resolved|resolve1|
                       systemd-resolve|
                       resolvconf|
                       systemd\.(positive|negative)
    ''', n, re.X):     # resolvectl and nss-resolve are in the main package.
        o = outputs['resolve']

    else:
        o = outputs['main']

    if n in known_files:
        prefix = known_files[n].split()[:-1]
    elif file.is_dir(follow_symlinks=False):
        prefix = ['%dir']
    elif 'README' in n:
        prefix = ['%doc']
    elif n.startswith('/etc'):
        prefix = ['%config(noreplace)']
        if not file.is_symlink() and file.stat().st_size == 0:
            prefix += ['%ghost']
    else:
        prefix = []
    prefix = ' '.join(prefix + ['']) if prefix else ''

    suffix = '*' if '/man/' in n else ''

    if not isinstance(o, tuple):
        o = (o,)
    for file in o:
        print(f'{prefix}{n}{suffix}', file=file)

if [print(f'ERROR: no file names were written to {o.name}')
    for name, o in outputs.items()
    if (o.tell() == 0 and
        not (no_bootloader and name == 'boot'))
    ]:
    sys.exit(1)
