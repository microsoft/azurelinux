%define commit_hash 7d9895ce55617b18a78294975197975ac17b5bc3

Name:           bootengine
Version:        0.0.38
Release:        1%{?dist}
Summary:        Flatcar bootengine dracut modules and helper utilities

License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/flatcar/bootengine
Source0:        https://github.com/flatcar/bootengine/archive/%{commit_hash}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-modify-tests.patch
BuildArch:      noarch
BuildRequires:  dracut
Requires:       util-linux

# Keep this local so the spec works even if a global dracut macro isn't defined.
%global dracutlibdir %{_prefix}/lib/dracut

%description
Flatcar bootengine content intended for initramfs usage via dracut modules.
This package installs the bootengine dracut module directory (modules.d)
and any included helper utilities/scripts from the Flatcar bootengine source.

%prep
%autosetup -p1 -n %{name}-%{commit_hash}

%build
# no build step (content is scripts/modules)

%install
rm -rf %{buildroot}

# Install dracut modules
# Adjust "dracut/modules.d/*" if upstream uses a different directory.
if [ -d dracut ]; then
  install -d -p %{buildroot}%{dracutlibdir}/modules.d
  cp -a dracut/* %{buildroot}%{dracutlibdir}/modules.d/
fi

# Optional: install any helper script if present (adjust names as needed)
# Common pattern: provide a helper in %{_sbindir} or %{_bindir}
if [ -f update-bootengine ]; then
  install -d -p %{buildroot}%{_sbindir}
  install -p -m 0755 update-bootengine %{buildroot}%{_sbindir}/update-bootengine
fi
install -p -m 0755 minimal-init %{buildroot}%{_sbindir}/minimal-init
# Ensure dracut module files are readable/executable where appropriate
# (Avoid chmod -R 0755; be conservative)
find %{buildroot}%{dracutlibdir}/modules.d -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || :
find %{buildroot}%{dracutlibdir}/modules.d -type f -name "module-setup.sh" -exec chmod +x {} \; 2>/dev/null || :

%check
set -e

./dracut/51usr-generator/testsuite.sh

%files
%license LICENSE
%doc README.md
%{dracutlibdir}/modules.d/*
%{_sbindir}/update-bootengine
%{_sbindir}/minimal-init

%changelog
* Tue Jan 27 2026 Sumit Jena <v-sumitjena@microsoft.com> - 0.0.38-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
