# Azure Linux traps (verified; read for every review)

Each entry: rule → evidence → false/missed finding it prevents.

1. **`%rhel` can be defined on AZL.** `macros.dist` defines `%fedora`/`%azurelinux`, not `%rhel`
   ([azurelinux-release.spec](../../../../specs/a/azurelinux-release/azurelinux-release.spec), `macros.dist`), but a
   component's generated `specs/<x>/<name>/<name>.azl.macros` can set it (e.g.
   [mesa.azl.macros](../../../../specs/m/mesa/mesa.azl.macros) has `%rhel 10`). Check the sidecar before
   calling a `%if 0%{?rhel}` branch dead or live. A `rhel` build define flips *every* `%rhel` branch.
2. **Weak deps aren't installed in the buildroot**: `install_weak_deps=0` in
   [azurelinux-4.0.tpl](../../../../distro/mock/azl4/azurelinux-4.0.tpl). `Recommends:` doesn't put a package
   in the build environment.
3. **`check.skip` vs `build.without`**: `check.skip` prepends `exit 0` to `%check`; `without = ["check"]` only
   passes `--without check` ([schema](../../../../external/schemas/azldev.schema.json)). Retained test lines
   after a skip are not evidence tests ran.
4. **Product scope**: AZL4 is a headless cloud distro; respect documented pruning in overlay descriptions /
   `build.without` ([copilot-instructions](../../../../.github/copilot-instructions.md)). Don't ask to restore a
   pruned upstream feature; do check that retained packages still have coherent deps/files.
5. **Hyper-V PTP time source** ships in `azurelinux-release-identity-cloud`
   ([chrony-azure.conf](../../../../base/comps/azurelinux-release/chrony-azure.conf)) via chrony's confdir;
   don't flag chrony for lacking it.
6. **Signature verification**: only the legacy `%gpgverify` provider is packaged
   ([macros.gpgverify.in](../../../../specs/g/gpgverify/macros.gpgverify.in)); don't demand a migration to a
   helper AZL doesn't ship.
7. **Publish channels** (`rpm-sdk` default, `rpm-base`;
   [components-publish-channels.toml](../../../../base/comps/components-publish-channels.toml)) are not image
   membership and don't downgrade defects.
