# Systemd defaults in WSL images

WSL sets up networking, DNS, the console, and `/dev` for every distribution it
runs, so Azure Linux skips the systemd units that would duplicate or conflict
with that work when running inside WSL.

The `systemd` component (`systemd`, `systemd-udev`, `systemd-networkd`, and
`systemd-resolved` subpackages) installs vendor drop-ins under
`/usr/lib/systemd/system/<unit>.d/wsl-disable.conf` with
`ConditionVirtualization=!wsl`:

- On non-WSL systems, `ConditionVirtualization=!wsl` is satisfied and has no
  effect.
- Inside WSL, systemd skips any unit whose condition is unmet and treats the
  start job as successful, whether the unit was pulled in by a preset, a static
  `*.target.wants` symlink, a socket, or a generator.
- `/etc/systemd/system` is left to the administrator, who can re-enable any unit
  with an override such as `/etc/systemd/system/<unit>.d/zz-local.conf`.

| Units | Package | Why skipped in WSL |
| --- | --- | --- |
| `systemd-networkd.service`, `systemd-networkd.socket`, `systemd-networkd-varlink.socket`, `systemd-networkd-wait-online.service` | `systemd-networkd` | WSL configures the network interface and routing. |
| `systemd-resolved.service`, `systemd-resolved-monitor.socket`, `systemd-resolved-varlink.socket` | `systemd-resolved` | WSL provides DNS and manages `/etc/resolv.conf`. |
| `getty@.service`, `console-getty.service` | `systemd` | WSL provides the console; `systemd-getty-generator` otherwise starts `console-getty.service` in container environments. |
| `systemd-vconsole-setup.service` | `systemd-udev` | Leaves the WSL-provided console untouched. |
| `systemd-tmpfiles-setup-dev.service`, `systemd-tmpfiles-setup-dev-early.service` | `systemd-udev` | WSL initializes `/dev`. |
| `tmp.mount` | `systemd` | As WSL recommends, no `tmpfs` is mounted over `/tmp`; it stays on the distribution's disk. |

The WSL static image tests in `base/images/tests/cases/static/wsl/` verify these
drop-ins in the built image.

## Deliberate exceptions

WSL's recommendations also list the `systemd-tmpfiles` setup and cleanup units.
Azure Linux keeps both enabled:

- `systemd-tmpfiles-setup.service` creates the `/tmp/.X11-unix` symlink that
  WSLg needs to run Linux GUI apps.
- `systemd-tmpfiles-clean.timer` removes old files from `/tmp`, which is not
  cleared on restart because `tmp.mount` does not run. The WSLg symlink has its
  own tmpfiles entry (`usr/lib/tmpfiles.d/wsl-setup.conf`), so cleanup leaves it
  alone.

WSL's static image validator (`validate-modern.py`) only inspects `/dev/null`
masks and `*.target.wants` symlinks, so it does not evaluate
`ConditionVirtualization=!wsl` drop-ins. It therefore emits expected non-fatal
warnings for `systemd-resolved.service`, `systemd-networkd.service`,
`systemd-networkd-wait-online.service`, `systemd-tmpfiles-setup.service`,
`systemd-tmpfiles-setup-dev{,-early}.service`, and `tmp.mount`, while exiting
`0` with no errors.

## References

- [WSL systemd recommendations](https://learn.microsoft.com/windows/wsl/build-custom-distro#systemd-recommendations)
- [WSL distribution validator](https://github.com/microsoft/WSL/blob/master/distributions/validate-modern.py)
