# C/C++ (autotools, CMake, Meson, make) idioms

Source: [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/) (main page § as
`#_<section>`), [CMake](https://docs.fedoraproject.org/en-US/packaging-guidelines/CMake/),
[Meson](https://docs.fedoraproject.org/en-US/packaging-guidelines/Meson/), build flags:
[buildflags.md](../../../../specs/a/azurelinux-rpm-config/buildflags.md) (AZL copy of redhat-rpm-config's).
Live examples: `grep -l '%cmake_build' specs/*/*/*.spec | head`, same for `%meson_build`, `%configure`.

## Canonical shape

```spec
%build
%configure --disable-static          # or: %cmake / %meson  (they apply distro flags)
%make_build                          # or: %cmake_build / %meson_build
%install
%make_install                        # or: %cmake_install / %meson_install
find %{buildroot} -name '*.la' -delete
%check
%make_build check                    # or: %ctest / %meson_test
%files
%{_libdir}/libfoo.so.1{,.*}          # SONAME visible
%files devel
%{_includedir}/foo.h
%{_libdir}/libfoo.so
%{_libdir}/pkgconfig/foo.pc
```

## Anti-patterns

| Seen | Fix | Level (§) |
| --- | --- | --- |
| `CFLAGS="..."`/`make CFLAGS=...` without `%{optflags}`/`%{build_cflags}`; `-O3` | Use the macros (they set flags); append extras via `%{optflags} -foo`; document reason | MUST honor (Compiler Flags) |
| Raw `./configure`, `cmake`, `meson setup`, `make install DESTDIR=` | `%configure`/`%cmake`/`%meson`, `%make_install` etc. | SHOULD (Compiler Flags: use flag macros) |
| `%{_libdir}/libfoo.so*` / `libfoo.so.*` in main package | `libfoo.so.N{,.*}` so a SONAME change is noticed | SHOULD NOT glob SONAME (Listing Shared Library Files) |
| Development-only unversioned `libfoo.so` linker files, headers, `.pc` in main package | `-devel`; keep runtime-loaded plugins/extension modules in runtime packages | MUST (Devel Packages) |
| `.la` shipped; static `.a` shipped without `-static` subpackage or a permitted exception | Delete `.la`; avoid static, else use `-static`. Static-only libraries and static libraries required by shared libraries may live in `-devel` with a versioned `Provides: %{name}-static = %{version}-%{release}` | SHOULD NOT / MUST (Packaging Static Libraries) |
| rpath in binaries | Remove (`chrpath`, `--disable-rpath`, CMake `-DCMAKE_SKIP_RPATH`) | MUST remove flagged rpath (Beware of rpath) |
| `BuildRequires: foo-devel` where a `.pc` exists | `pkgconfig(foo)` | SHOULD (BuildRequires Based on pkg-config) |
| Bundled copy of a system library (zlib, openssl...) | Build against the system one | MUST/SHOULD (`#bundling`) |

Not a finding: `%ldconfig_scriptlets`/`%ldconfig` (no-ops now; "not necessary to call ldconfig") in inherited specs.

## ABI checklist for library changes

- Removing/renaming an exported function, changing a public struct/enum, or changing a function signature is an
  ABI break even if the SONAME is unchanged. Grep consumers (`BuildRequires: <name>-devel` / `pkgconfig(<name>)`)
  and check whether they use the symbol; prefer not to diverge from upstream ABI at all.
- A SONAME bump requires rebuilding every consumer in the same change (or a compat package).
- Disabling a configure feature can change installed headers/`.pc` `Requires`/plugins: re-check `-devel`.
