Summary:        Simple configuration tool for Flatcar Container Linux
Name:           coreos-cloudinit
Version:        1.14.0

%global commit  1c1d7f4ae6b933350d7fd36e882dda170123cccc

Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://github.com/flatcar/coreos-cloudinit

Source0:        https://github.com/flatcar/coreos-cloudinit/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

Requires:       shadow-utils >= 4.1.5.1

%description
coreos-cloudinit enables a user to customize Flatcar Container Linux machines by providing
either a cloud-config document or an executable script through user-data.

%prep
%autosetup -n %{name}-%{commit}

%build
export GO111MODULE=on
export GOFLAGS="-mod=vendor"
go build -v -o %{name} .

%check
%if "%{getenv:RUN_CHECK}" == "y"
export GO111MODULE=on
export GOFLAGS="-mod=vendor"
go test ./...
%endif

%install
rm -rf %{buildroot}

install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

# Install udev rules + systemd units from upstream "units/" directory (as in ebuild)
if [ -d units ]; then
    install -d %{buildroot}%{_udevrulesdir}
    for f in units/*.rules; do
        [ -f "$f" ] && install -m 0644 "$f" %{buildroot}%{_udevrulesdir}/
    done

    install -d %{buildroot}%{_unitdir}
    for ext in mount path service target; do
        for f in units/*.${ext}; do
            [ -f "$f" ] && install -m 0644 "$f" %{buildroot}%{_unitdir}/
        done
    done

    # systemd_enable_service multi-user.target system-config.service
    # systemd_enable_service multi-user.target user-config.target
    install -d %{buildroot}%{_unitdir}/multi-user.target.wants
    for u in system-config.service user-config.target; do
        if [ -f "%{buildroot}%{_unitdir}/$u" ]; then
            ln -sf ../$u %{buildroot}%{_unitdir}/multi-user.target.wants/$u
        fi
    done
fi

# Azure Linux: ensure everything in buildroot is captured
find %{buildroot} -type f -o -type l \
  | sed "s|^%{buildroot}||" \
  | sort -u > %{name}.files

%post
%systemd_post system-config.service >/dev/null 2>&1 || :

%preun
%systemd_preun system-config.service >/dev/null 2>&1 || :

%postun
%systemd_postun system-config.service >/dev/null 2>&1 || :

%files -f %{name}.files
%license LICENSE NOTICE
%doc README.md

%changelog
* Mon Feb 02 2026 Sumit Jena (HCL Technologies Ltd) - 1.14.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.