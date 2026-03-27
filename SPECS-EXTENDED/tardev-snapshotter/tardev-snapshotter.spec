%global debug_package %{nil}

Summary: Tardev Snapshotter for containerd
Name: tardev-snapshotter
Version: 3.2.0.tardev1
Release: 7%{?dist}
License: ASL 2.0
Group: Tools/Container
Vendor: Microsoft Corporation
Distribution: Azure Linux

Source0:https://github.com/microsoft/kata-containers/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Note: the %%{name}-%%{name}-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache run regenerate-archives.sh
Source1:  %{_distro_sources_url}/%{name}-%{version}-cargo.tar.gz

%{?systemd_requires}

BuildRequires: clang-devel
BuildRequires: cmake
BuildRequires: device-mapper-devel
BuildRequires: git
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: pkgconfig(libudev)
BuildRequires: protobuf-compiler
BuildRequires: rust

%description
tardev-snapshotter is a snapshotter for containerd that uses tar archives to store snapshots.

%prep
# Setup .cargo directory
mkdir -p $HOME
pushd $HOME
tar xf %{SOURCE1} --no-same-owner
popd

%autosetup -p1

%build
export CARGO_NET_OFFLINE=true
make

%install
mkdir -p %{buildroot}/%{_unitdir}
install -D -p -m 0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -D -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%post
%systemd_post %{name}.service

if [ $1 -eq 1 ]; then # Package install
	systemctl enable %{name}.service > /dev/null 2>&1 || :
	systemctl start %{name}.service > /dev/null 2>&1 || :
fi

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%{_bindir}/%{name}
%config(noreplace) %{_unitdir}/%{name}.service

%changelog
* Wed Feb 11 2026 BinduSri Adabala <v-badabala@microsoft.com> - 3.2.0.tardev1-7
- Bump release to rebuild with rust

* Mon Feb 02 2026 Archana Shettigar <v-shettigara@microsoft.com> - 3.2.0.tardev1-6
- Bump release to rebuild with rust

* Wed Oct 15 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 3.2.0.tardev1-5
- Bump release to rebuild with rust

* Fri Aug 08 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.2.0.tardev1-4
- Bump release to rebuild with rust

* Mon Jul 21 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 3.2.0.tardev1-3
- Bump release to rebuild with rust

* Fri Jun 13 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 3.2.0.tardev1-2
- Bump release to rebuild with rust

* Fri Mar 28 2025 Dallas Delaney <dadelan@microsoft.com> - 3.2.0.tardev1-1
- Add package to specs-extended
- License verified
- Original version for Azure Linux

* Tue Dec 31 2024 Jiri Appl <jiria@microsoft.com> - 0.0.13-1
- Initial version
