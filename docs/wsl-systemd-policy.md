# Systemd defaults in WSL images

WSL sets up networking, DNS, the console and `/dev` for every distribution it
runs, so the Azure Linux WSL image turns off the systemd units that would do the
same work. These settings ship in the `azurelinux-release-identity-wsl` package
and apply only to the WSL image.

| Units | Setting | Why |
| --- | --- | --- |
| `systemd-networkd` (service, sockets, `-wait-online`) | disabled | WSL configures the network. |
| `systemd-resolved` (service, sockets) | disabled | WSL provides DNS and writes `/etc/resolv.conf`. |
| `getty@*.service` | disabled | WSL provides the console. |
| `console-getty.service` | disabled and masked | systemd's getty generator starts it in containers, and systemd counts WSL as one. A preset can't stop that, so the unit is masked as well. |
| `systemd-vconsole-setup.service` | masked | Leaves the console WSL provides alone. |
| `systemd-tmpfiles-setup-dev{,-early}.service` | masked | WSL initializes `/dev`. |
| `tmp.mount` | masked | As WSL recommends, no tmpfs is mounted over `/tmp`; it stays on the distribution's disk. |

The WSL static image tests in `base/images/tests/cases/static/wsl/` check these
settings in the built image.

## Deliberate exceptions

WSL's recommendations also list the systemd-tmpfiles setup and cleanup units.
Azure Linux keeps both:

- `systemd-tmpfiles-setup.service` creates the `/tmp/.X11-unix` link that WSLg
  needs to run Linux GUI apps.
- `systemd-tmpfiles-clean.timer` removes old files from `/tmp`, which is not
  cleared on restart because `tmp.mount` is masked. The WSLg link has its own
  tmpfiles entry, so cleanup leaves it alone.

WSL's image validator warns about `systemd-tmpfiles-setup.service`; this is expected.

## References

- [WSL systemd recommendations](https://learn.microsoft.com/windows/wsl/build-custom-distro#systemd-recommendations)
- [WSL distribution validator](https://github.com/microsoft/WSL/blob/master/distributions/validate-modern.py)
