# Go idioms (vendored, current guidelines)

Source: [Fedora Golang Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/Golang/)
(§ = section), [Go Vendor Tools](https://fedora.gitlab.io/sigs/go/go-vendor-tools/).
Local providers: [go-rpm-macros](../../../../specs/g/go-rpm-macros/), [go-vendor-tools](../../../../specs/g/go-vendor-tools/).
Live example (AZL local spec): [telegraf](../../../../base/comps/telegraf/telegraf.spec).
Old-style `golang-*` library packages (`%gopkg`, `-devel` source packages) are legacy: new packages MUST vendor.

## Canonical shape

```spec
%global goipath github.com/org/foo
%global gomodulesmode GO111MODULE=on
Version:        1.2.3
%gometa -L -f
# MUST NOT use golang- prefix for vendored apps
Name:           foo
License:        <cumulative SPDX of project + all vendored modules>
Source0:        %{gosource}
Source1:        %{archivename}-vendor.tar.bz2
Source2:        go-vendor-tools.toml
BuildRequires:  go-vendor-tools
%prep
%goprep -p1
tar -xf %{S:1}                           # unpack the vendor archive
%generate_buildrequires
%go_vendor_license_buildrequires -c %{S:2}
%build
export GO_BUILDTAGS="..."               # never BUILDTAGS; never LDFLAGS (use GO_LDFLAGS)
%gobuild -o %{gobuilddir}/bin/foo %{goipath}/cmd/foo
%install
%go_vendor_license_install -c %{S:2}
install -Dpm 0755 %{gobuilddir}/bin/foo %{buildroot}%{_bindir}/foo
%check
%go_vendor_license_check -c %{S:2}
%gocheck2                                 # never legacy %gocheck
%files -f %{go_vendor_license_filelist}
%{_bindir}/foo
```

## Anti-patterns / change hazards

| Seen | Fix | Level (§) |
| --- | --- | --- |
| Version bump without regenerating the vendor archive (`go_vendor_archive create`, or the component's custom source script + its hard-coded version/hash) and updating its hash | Regenerate; vendor archive must match the new `go.mod`/`go.sum` | MUST vendor (Vendored dependencies) |
| `License:` not recomputed after a bump/vendor change | `go_vendor_license report expression` | MUST cumulative SPDX (Licensing) |
| `%go_vendor_license_check` removed/commented, or `go_vendor_license` errors ignored | Fix licenses / `go-vendor-tools.toml` (overrides are keyed by path + sha256) | MUST address errors; SHOULD run in `%check` (Checking licenses) |
| Vendored module without a license file kept | Not allowed (temporary in-repo license only with upstream report) | MUST NOT (In case of missing licenses) |
| `bundled(golang(...))` Provides missing | Ship `vendor/modules.txt` as `%license` (filelist does it) | MUST (Bundled provides) |
| `BUILDTAGS`/`LDFLAGS` env, `go build` direct | `GO_BUILDTAGS`, `GO_LDFLAGS`, `%gobuild` (preserves distro flags) | MUST NOT / MUST preserve flags (Go compiler flags) |
| `%gocheck` | `%gocheck2`; skipped tests need a comment + upstream link | MUST NOT / SHOULD (Testing) |
| Missing build dependency on `go-rpm-macros` / `go-vendor-tools` | Check automatically supplied dependencies first (`%gometa` supplies `go-rpm-macros`); add explicit `BuildRequires` only for missing dependencies | MUST (Macro dependencies) |
| Build-tag list edited, or upstream bump renames plugins/tags | Go ignores tags nothing uses, so a renamed tag silently drops the feature; verify each tag still exists | correctness |
