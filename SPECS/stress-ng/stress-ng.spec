Name:		stress-ng
Version:	0.17.01
Release:	1%{?dist}
Summary:	Stress test a computer system in various ways

License:	GPLv2+
URL:		https://github.com/ColinIanKing/stress-ng
Source0:	https://github.com/ColinIanKing/stress-ng/archive/V%{version}/%{name}-%{version}.tar.gz

BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	glibc-devel
BuildRequires:	kernel-headers
BuildRequires:	keyutils-libs-devel
BuildRequires:	libaio-devel
BuildRequires:	libattr-devel
BuildRequires:	libcap-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libatomic
BuildRequires:	zlib-devel

%description
Stress test a computer system in various ways. It was designed to exercise
various physical subsystems of a computer as well as the various operating
system kernel interfaces.

%prep
%autosetup -n %{name}-%{version}

%build
%make_build

%install
install -p -m 755 -D %{name} %{buildroot}%{_bindir}/%{name}
install -p -m 644 -D %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
install -pm 644 bash-completion/%{name} \
    %{buildroot}%{_datadir}/bash-completion/completions/%{name}

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}

%changelog
* Thu Feb 29 2024 Stephen Carlson <stcarlso@microsoft.com> - 0.17.01-1
- Initial CBL-Mariner import from Fedora 37 (license: GPLv2)
- License verified

