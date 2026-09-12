<h1>
  <img src="assets/azurelinux-logo-48.png" alt="Azure Linux logo" align="left" height="44" /> Azure Linux 4
</h1>

**An open-source Linux distribution built and optimized for [Azure](https://azure.microsoft.com/), with sources derived from [Fedora Linux](https://fedoraproject.org/).** Azure Linux provides a secured, reliable operating system for virtual machines, containers, and bare-metal platforms.

Azure Linux is built on a robust open-source foundation from the Fedora ecosystem and enhanced with Azure-specific innovations. This provides the familiarity of the RPM package ecosystem, while adding Azure-native security, compliance, and operational capabilities.

Key features of Azure Linux include: hardened security posture, an Azure-optimized kernel, supply chain security, native Azure integration, and a predictable lifecycle.

> **This branch holds the in-development sources for Azure Linux 4.** For Azure Linux 3, see the [`3.0` branch](https://github.com/microsoft/azurelinux/tree/3.0).

## Getting started

The links below will help you get started with Azure Linux:

| | |
|---|---|
| **Product documentation** | <https://aka.ms/azurelinux> |
| **Release information** | [GitHub Releases](https://github.com/microsoft/azurelinux/releases) |
| **File a bug / feedback** | [GitHub Issues](https://github.com/microsoft/azurelinux/issues) |
| **Ask a question / get help** | [SUPPORT.md](SUPPORT.md) |
| **Get started as a distro developer** | [DEVELOPING.md](DEVELOPING.md) |
| **Contribution guidelines** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Report a security issue** | [SECURITY.md](SECURITY.md) |

## Using Azure Linux

*Note: Azure Linux 4 is still in development*

<details open>
<summary><b>🖥️ Azure VM</b></summary>

To try Azure Linux in an Azure VM, please visit [our Azure Linux 4.0 page](https://aka.ms/azure-linux-4-marketplace) on the Microsoft Marketplace.

</details>

<details open>
<summary><b>📦 Container</b></summary>

To try Azure Linux base container, please use the following image reference: `mcr.microsoft.com/azurelinux-beta/base/core:4.0`

</details>

<details>
<summary><b>💿 ISO Installer</b></summary>

To try Azure Linux in a local VM, please download the ISO Installer: [x86_64](https://aka.ms/azurelinux-4.0-x86_64.iso) / [ARM64](https://aka.ms/azurelinux-4.0-aarch64.iso)

Before using a downloaded ISO, [verify the checksum and signature of the ISO](./docs/verify-iso-signature-and-checksum.md).

After downloading and verifying the ISO, follow the [ISO installer instructions](./docs/iso-installer-in-local-vm.md) to install and use Azure Linux in a local VM (Hyper-V on Windows or QEMU/KVM on Linux). The ISO runs the [Anaconda](https://anaconda-installer.readthedocs.io/) installer.

_Note: Support for the ISO is community based. Before filing a new bug or feature request, please search the list of Github Issues. If you are unable to find a matching issue, please report new bugs by clicking [here](https://github.com/microsoft/azurelinux/issues). For additional information, refer to the [SUPPORT.md](./SUPPORT.md) file._

</details>

<details>
<summary><b>🐧 Windows Subsystem for Linux (WSL)</b></summary>

To try Azure Linux on the Windows Subsystem for Linux, please download the `.wsl` distribution package for your architecture:

- [x86_64](https://aka.ms/azurelinux-4.0-x86_64.wsl)
- [ARM64](https://aka.ms/azurelinux-4.0-aarch64.wsl)

Before installing a downloaded package, [verify the checksum and signature of the `.wsl` package](./docs/verify-wsl-signature-and-checksum.md).

Install the distribution using `wsl`:

```powershell
wsl --install --from-file "C:\Path\To\AzureLinux-4.0-ARCH.wsl"
```

To list all the installed distributions:

```powershell
wsl --list
```

To use the distro:

```powershell
wsl -d AzureLinux-4
```

</details>

## What's in this branch?

Azure Linux 4 is an RPM-based distribution optimized for Azure and modern cloud workloads. It is defined by a set of TOML configuration files and targeted *overlays* applied to [Fedora Linux](https://fedoraproject.org/), its upstream base.

Deviations from upstream are declaratively defined and scoped to avoid unnecessary divergence or forking. This repository contains a mechanically rendered set of RPM package spec files derived from applying this layer to Fedora's upstream packaging sources.

### Core userland in the VM image

Azure Linux builds a broad set of RPM packages, but each image includes only the packages it needs. The standard VM image uses these components for common system roles:

| Role | Component |
|---|---|
| C library | glibc (`glibc`) |
| Core command-line utilities | GNU coreutils (`coreutils`) |
| Shell | Bash (`bash`) |
| Init, services, and networking | `systemd`, `systemd-networkd`, and `systemd-resolved` |
| Package management | DNF5 (`dnf5`) over the RPM package format |
| Privilege delegation | `sudo` |
| Time synchronization | `chrony` |
| DNS command-line tools | BIND utilities (`bind-utils`) |

The wider package set also contains `mimalloc` and `uutils-coreutils`, but no image selects them to replace glibc's allocator or GNU coreutils. Container, distroless, minimal OS, WSL, and installer images select different package sets.

This table records which implementation is chosen for each role, not the packages an image contains. For exact contents, see the [VM](base/images/vm-base/vm-base.kiwi), [container and distroless](base/images/container-base/container-base.kiwi), [minimal OS](base/images/minimal-os/minimal-os.kiwi), [WSL](base/images/wsl/wsl.kiwi), and [installer](base/images/vm-iso-installer/vm-iso-installer.kiwi) image definitions, which remain the source of truth.

## How Azure Linux is defined

The distro is described almost entirely in TOML-based configuration files. Our open-source development tool, [`azldev`](https://github.com/microsoft/azure-linux-dev-tools), is used to apply this configuration to upstream Fedora spec files and packaging sources.

```text
azldev.toml        # Top-level entry point
├── distro/        # Distro-wide configs (e.g., sources, mock configs)
└── base/          # The "base" project: components, images, tests
    └── comps/     # Component definitions (one per source package)
    └── images/    # Base image definitions
```

### Concepts/terms

- **Components** (also known as source packages) are the unit of packaging.
  Most are imported in source form from Fedora's upstream dist-git repositories; each component produces one or more RPMs. Azure Linux builds all components from sources to produce a full set of installable RPM packages.
- **Overlays** are declarative modifications to upstream specs and sources
  (e.g., patches, additions/removals, build parameters). They live alongside the component definition and always carry a `description` explaining *why* the change is needed. Overlays let us avoid forking upstream specs and are more flexible than plain textual patches.
- **Rendered specs** are the final `.spec` files produced by applying overlays to upstream sources. They are mechanically generated by `azldev`, checked in for visibility and auditability, and live under [`specs/`](specs/). Treat them as derived output and not sources for editing. We use them as the input to standard RPM building services/tools (`mock` + `rpmbuild`, `koji`).

For a deeper tour of the tooling, the overlay system, and how to get started developing within this distro, please see
[DEVELOPING.md](DEVELOPING.md).

## Repository layout

| Path | What's there |
|---|---|
| [`azldev.toml`](azldev.toml) | Top-level config — includes `distro/` and `base/`. |
| [`distro/`](distro/) | Distro definitions (Azure Linux + upstream Fedora), shared `mock` configs. |
| [`base/`](base/) | The `base` project: components, images, tests. |
| [`base/comps/`](base/comps/) | **Component definitions** — the heart of the distro. |
| [`base/images/`](base/images/) | Image definitions (VM, container, etc.) built from the component set using [`KIWI NG`](https://osinside.github.io/kiwi/). |
| [`specs/`](specs/) | **Rendered specs** — generated `.spec` files after overlays are applied. Checked in for visibility; do not hand-edit. |
| [`locks/`](locks/) | Per-component lock files pinning upstream commits + input fingerprints; do not hand-edit. |
| [`external/schemas/`](external/schemas/) | Cached copy of the JSON Schema for TOML config files; mirrored from `azldev`. |
| [`.github/`](.github/) | CI workflows, plus Copilot prompts, skills, and agent instructions used by AI-assisted development. |

## Getting started as a distro developer

If you want to build or develop within the distro, start with **[DEVELOPING.md](DEVELOPING.md)**. Don't worry about this if you're primarily looking to *use* the distro.

## Engagement & support

- **Bugs and feature requests:** file a
  [GitHub issue](https://github.com/microsoft/azurelinux/issues). Please search existing issues first to avoid duplicates. Share as much as you can with us regarding what you tried and what you're seeing.
- **Support:** see [SUPPORT.md](SUPPORT.md) for the full set of channels.
- **Security vulnerabilities:** do **not** open a public issue. Follow the process in [SECURITY.md](SECURITY.md) to report privately to the Microsoft Security Response Center.
- **Pull requests:** see [CONTRIBUTING.md](CONTRIBUTING.md) for the patch-series workflow, commit-message conventions, and review expectations.
- **Community calls:** Azure Linux hosts community calls where users can connect with our product and support teams, discuss new features, share feedback, and learn how others are using Azure Linux.
  Each session also includes a featured demo. Upcoming community calls (08:00–09:00 PT):
  - 2026-07-23 — [Click to join][community-call-join]
  - 2026-09-24 — [Click to join][community-call-join]
  - 2026-11-19 — [Click to join][community-call-join]
  - 2027-01-28 — [Click to join][community-call-join]
  - 2027-03-25 — [Click to join][community-call-join]
  - 2027-05-27 — [Click to join][community-call-join]

[community-call-join]: https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZDcyZjRkYWMtOWQxYS00OTk3LWFhNmMtMTMwY2VhMTA4OTZi%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2271a6ce92-58a5-4ea0-96f4-bd4a0401370a%22%7d
This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions
or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general). Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos is subject to those third parties' policies.

## Acknowledgments

Any Linux distribution, including Azure Linux, benefits from contributions by the open-source software community. We gratefully acknowledge all contributions made from the broader community.

We specifically want to thank [the Fedora Project](https://start.fedoraproject.org/) for providing us with a strong foundation across components, spec files, tools, services, and community. We are proud to participate and contribute to this community.

The Azure Linux penguin icon is inspired by the Linux mascot ("Tux"), created by Larry Ewing.

## License

Unless otherwise specified, the content of the Azure Linux distribution and this repository are distributed under an [MIT license](LICENSE).

Individual packages within the distribution are distributed under licenses specified in their package spec files and sources.

This repository contains files derived from Fedora Linux. For details on the licensing terms for the Fedora Project, please consult [fedoraproject.org](https://docs.fedoraproject.org/en-US/legal/fedora-linux-license/).
