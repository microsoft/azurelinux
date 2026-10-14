# Systemd defaults in WSL images

WSL sets up networking, DNS, the console and `/dev` for every distribution it
runs, so the Azure Linux WSL image turns off the systemd units that would do the
same work. These settings ship in the `azurelinux-release-identity-wsl` package
and apply only to the WSL image.

Two mechanisms are used, each where it fits:

- **A preset** (`80-wsl.preset`) sets the default enablement for optional daemons.
  It is a default, so an administrator can still `systemctl enable` them.
- **Vendor drop-ins** under `/usr/lib/systemd/system/<unit>.d/wsl-disable.conf` carry
  `ConditionVirtualization=!wsl` for units a preset cannot reach — those pulled in by
  a generator or by a static `*.target.wants` symlink. systemd skips a unit whose
  condition is unmet and treats the job as successful, so dependent units are not
  failed. `/etc/systemd/system` is left to the administrator, who can override any of
  this with `/etc/systemd/system/<unit>.d/zz-local.conf`.

| Units | Setting | Why |
| --- | --- | --- |
| `systemd-networkd` (service, sockets, `-wait-online`) | preset: disabled | WSL configures the network. |
| `systemd-resolved` (service, sockets) | preset: disabled | WSL provides DNS and writes `/etc/resolv.conf`. |
| `getty@*.service` | preset: disabled | WSL provides the console. |
| `console-getty.service` | drop-in | systemd's getty generator starts it in containers, and systemd counts WSL as one. Generators ignore presets, so the condition is what stops it. |
| `systemd-vconsole-setup.service` | drop-in | Leaves the console WSL provides alone. |
| `systemd-tmpfiles-setup-dev{,-early}.service` | drop-in | WSL initializes `/dev`. Both ship as static `sysinit.target.wants` symlinks. |
| `tmp.mount` | drop-in | As WSL recommends, no tmpfs is mounted over `/tmp`; it stays on the distribution's disk. Ships as a static `local-fs.target.wants` symlink. |

The WSL static image tests in `base/images/tests/cases/static/wsl/` check these
settings in the built image.

## Deliberate exceptions

WSL's recommendations also list the systemd-tmpfiles setup and cleanup units.
Azure Linux keeps both:

- `systemd-tmpfiles-setup.service` creates the `/tmp/.X11-unix` link that WSLg
  needs to run Linux GUI apps.
- `systemd-tmpfiles-clean.timer` removes old files from `/tmp`, which is not
  cleared on restart because `tmp.mount` does not run. The WSLg link has its own
  tmpfiles entry, so cleanup leaves it alone.

WSL's image validator only recognises masked units and `*.target.wants` symlinks, so
it cannot see these drop-ins. It therefore warns about `systemd-tmpfiles-setup.service`,
`systemd-tmpfiles-setup-dev{,-early}.service` and `tmp.mount`. These warnings are
expected and do not fail validation, which exits non-zero only on errors.

## References

- [WSL systemd recommendations](https://learn.microsoft.com/windows/wsl/build-custom-distro#systemd-recommendations)
- [WSL distribution validator](https://github.com/microsoft/WSL/blob/master/distributions/validate-modern.py)
