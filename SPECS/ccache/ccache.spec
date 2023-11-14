Summary:        Compiler Cache
Name:           ccache
Version:        4.8.3
Release:        1%{?dist}
License:        BeOpen AND BSD AND GPLv3+ AND (Patrick Powell's AND Holger Weiss' license) AND Public Domain AND Python AND zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://ccache.dev
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  cmake

%description
Ccache (or “ccache”) is a compiler cache. It speeds up recompilation by caching previous
compilations and detecting when the same compilation is being done again.

%prep
%setup -q

%build
mkdir build
pushd build
%cmake .. -DREDIS_STORAGE_BACKEND=OFF -DENABLE_TESTING=ON
make %{?_smp_mflags}
popd

%install
pushd build
%make_install
popd
install -dm 755 %{buildroot}%{_libdir}/ccache
for n in cc gcc g++ c++ ; do
    ln -sf ../../bin/ccache %{buildroot}%{_libdir}/ccache/$n
    ln -sf ../../bin/ccache %{buildroot}%{_libdir}/ccache/%{_host}-$n
done
ln -sf ../../bin/ccache %{buildroot}%{_libdir}/ccache/clang
ln -sf ../../bin/ccache %{buildroot}%{_libdir}/ccache/clang++

%check
pushd build
make check
popd

%post
# Remove ccache symlinks for clang if not installed
for n in clang clang++ ; do
if ! command -v $n ; then
    rm -rvf %{_libdir}/ccache/$n
fi
done

%files
%license LICENSE.adoc
%doc README.md
%{_bindir}/ccache
%dir %{_libdir}/ccache/
%{_libdir}/*

%changelog
* Fri Nov 10 2023 Andrew Phelps <anphel@microsoft.com> - 4.8.3-1
- Upgrade to version 4.8.3

* Thu Mar 23 2023 Andrew Phelps <anphel@microsoft.com> - 4.8-1
- Update to 4.8
- Remove missing clang symlinks if detected in post install section

* Mon Aug 22 2022 Andrew Phelps <anphel@microsoft.com> - 4.6-2
- Create symlinks to ccache
- Lint spec

* Mon Mar 07 2022 Andrew Phelps <anphel@microsoft.com> - 4.6-1
- Upgrade to version 4.6
- Enable check tests

* Mon Oct 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6-2
- License verified.
- Added 'Vendor' and 'Distribution' tags.

* Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> - 3.6-1
- Original version for CBL-Mariner.
