# Systemd defaults in WSL images

The `azurelinux-release-identity-wsl` package owns the WSL-specific systemd
policy. Other Azure Linux variants do not ship its presets or masks. The WSL
identity requires `azurelinux-release-wsl`, not the container release variant.

## Enablement is not activation

`80-wsl.preset` sorts before `90-default.preset` and `90-systemd.preset`.
Systemd applies the first matching preset rule when packages are initially
installed. A disabled preset removes installation-time enablement links; it
does not prevent a unit from being started through a dependency, socket,
generator, or an explicit administrator request.

| Unit group | WSL policy | Reason |
| --- | --- | --- |
| `systemd-networkd.service`, its sockets, and `systemd-networkd-wait-online.service` | Disable by preset | Leave default network configuration to WSL; do not enable a second network manager or wait for networkd to configure interfaces. |
| `systemd-resolved.service` and its sockets | Disable by preset | Leave default DNS configuration to WSL, including its generated `/etc/resolv.conf`. |
| `getty@*.service` | Disable by preset | Avoid the vendor preset's `DefaultInstance=tty1` console login. WSL's listing review explicitly requested this. |
| `console-getty.service` | Disable by preset and mask | The getty generator adds this unit in containers independently of its preset. A mask prevents that generated dependency from starting a console login. |
| `systemd-vconsole-setup.service` | Mask | Avoid reconfiguring the WSL-provided virtual console. Udev restarts this static unit when a `vtconsole` device appears. |
| `tmp.mount` | Mask | Follow WSL's recommendation not to mount a new tmpfs over the distribution's existing `/tmp` tree. |
| `systemd-tmpfiles-setup-dev{,-early}.service` | Mask | These units run `systemd-tmpfiles --prefix=/dev --create --boot` to initialize device nodes and permissions. Leave WSL device initialization alone, as recommended. |
| `systemd-tmpfiles-setup.service` | Keep available and scheduled at boot | The packaged WSLg X11 integration uses system tmpfiles to create its socket-directory link. |
| `systemd-tmpfiles-clean.service` and `.timer` | Keep available and scheduled | Retain periodic cleanup of ordinary temporary files without removing the WSLg link. |

The [getty generator][getty-source] taking its container path does **not** prove that
`getty@tty1.service` is disabled: an earlier package preset can already have
enabled that instance. Likewise, `ConditionPathExists=/dev/tty0` is a runtime
condition, not an enablement policy. Neither condition results nor concurrent
distribution failures should be inferred from a preset listing.

The early device rules include mode/ownership adjustments for paths such as
`/dev/net/tun`, `/dev/fuse`, and `/dev/kvm`. Their exclusion is a WSL device-policy
choice; it is not a claim that every such adjustment causes a demonstrated
failure. These masks do not disable general system or user tmpfiles processing.

## Guidance and its limits

The [WSL systemd recommendations][wsl-docs], the
[distribution validator][wsl-validator], and the
[Azure Linux listing review][wsl-review] are separate sources. Their unit lists
are not identical. In particular, the maintainer review calls out
`getty@tty1.service`, whereas the validator lists `console-getty.service`.
The review explains the network/DNS ownership concerns and reports console
conflicts when several distributions configure the device concurrently.

The validator inspects `*.target.wants` links in the image and recognizes masks
under `/etc/systemd/system/`. It reports discouraged units as **warnings**, not
errors. It neither interprets presets nor models boot-time generators, so
passing this part of the validator is not evidence that a unit cannot start.

Keeping `systemd-tmpfiles-setup.service` produces an intentional discouraged-unit
warning. Keeping cleanup adds no additional **unit** warning with the cited
validator: the service has no `*.target.wants` link, and the timer is not on its
discouraged-unit list. Both cleanup units nevertheless appear in the prose
recommendations, so retaining them is a deliberate policy exception, not full
compliance with that list. Other validator diagnostics are independent of this
unit policy.

## Temporary files and WSLg

The system tmpfiles configuration shipped by `wsl-setup` contains:

```text
L+ /tmp/.X11-unix - - - - /mnt/wslg/.X11-unix
```

When cleaning a parent directory, [systemd-tmpfiles skips paths with a separate
tmpfiles entry][tmpfiles-source]. Thus the `/tmp` age rule does not remove this
link or recursively clean its WSLg target. No additional exclusion rule is needed.

WSL 2 distributions have [separate mount namespaces][wsl-architecture]. Ordinary
`/tmp` contents are not a shared directory across distributions; the WSLg socket
directory is a distinct integration path reached through the link above.

With `tmp.mount` masked, retain the daily cleanup timer rather than assuming the
host will age the distribution's ordinary `/tmp` contents. Disabling both the
mount and the cleaner would remove the package's normal temporary-file cleanup.
The `tmpfiles-setup` and `tmpfiles-clean` exceptions to the broad WSL
recommendations are intentional.

The system setup service creates the **X11** link. Wayland and PulseAudio use the
separate user tmpfiles configuration in `/usr/share/user-tmpfiles.d/`; they are
not created by `systemd-tmpfiles-setup.service`.

## WSL registration

`wsl-setup` registers the image as `AzureLinux-4.0` and uses the real
`/usr/share/pixmaps/azurelinux-logo.ico` asset. The registration identifier should
remain stable across prerelease and release images; it is separate from the
release status recorded in `/etc/os-release`.

The Azure Linux entry in WSL's `distributions/DistributionInfo.json` must use the
same name when it is published. Otherwise installation from the online catalog
and installation from the downloaded `.wsl` file can register different names.

## Other distributions and upstreaming

Ubuntu Noble's WSL setup uses unit-specific condition drop-ins, including
[`ConditionVirtualization=!wsl` for `systemd-binfmt.service`][ubuntu-binfmt].
[Fedora's `wsl-setup`][fedora-wsl-setup] uses the same kind of condition for
`systemd-firstboot.service` and explicitly retains tmpfiles-based X11
integration. These are examples of selective adaptations, not evidence that
every unit in the WSL recommendations must be masked.

Differences in package enablement alone do not establish that Ubuntu or Fedora
is broken, that a condition succeeds at runtime, or that concurrent
distributions fail. Azure Linux's policy is based on its own packaged units,
the listing feedback, and the activation paths described above.

The common policy is suitable to propose to Fedora's WSL variant packaging.
The discussion in [microsoft/WSL#41120][wsl-listing] expresses intent to make
similar Fedora changes; it should not be described as an upstream patch having
landed. Azure-specific names and icon paths remain downstream branding.

## Image coverage

The existing `static-image-checks` suite discovers the WSL-specific cases in
`base/images/tests/cases/static/wsl/`. They inspect the assembled image's masks
and dependency links, required release packages, registration configuration,
icon, and tmpfiles setup/cleanup scheduling. Inspecting only the `PRESET` column
does not establish the image's actual enablement state or its boot behavior.

```bash
azldev image test wsl --test-suite static-image-checks --image-path /path/to/image.wsl
```

[wsl-docs]: https://learn.microsoft.com/windows/wsl/build-custom-distro#systemd-recommendations
[wsl-validator]: https://github.com/microsoft/WSL/blob/74c6ac9abb77f336bd4c796146c23cdb90877ed7/distributions/validate-modern.py
[wsl-review]: https://github.com/microsoft/WSL/pull/41120#pullrequestreview-4756854396
[wsl-listing]: https://github.com/microsoft/WSL/pull/41120
[wsl-architecture]: https://learn.microsoft.com/windows/wsl/about
[tmpfiles-source]: https://github.com/systemd/systemd/blob/9457f81485bfe8e09d45c0376fe02ebce7c15872/src/tmpfiles/tmpfiles.c
[getty-source]: https://github.com/systemd/systemd/blob/9457f81485bfe8e09d45c0376fe02ebce7c15872/src/getty-generator/getty-generator.c
[ubuntu-binfmt]: https://git.launchpad.net/ubuntu/+source/wsl-setup/plain/systemd/system/systemd-binfmt.service.d/wsl.conf?id=6aa0aa20245d84c9ac932a430f7b870ae466149f
[fedora-wsl-setup]: https://src.fedoraproject.org/rpms/wsl-setup/raw/a24b96bded1174191b9c997d097f7864d98ab878/f/wsl-setup.spec
