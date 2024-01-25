Name: amdsev-qemu-ovmf
Version: 1.0
Release: 1
Summary: QEMU and OVMF from AMDSEV GitHub repo
License: (whatever applies)
URL: https://github.com/AMDESE/AMDSEV/tree/snp-latest
Source0: %{name}-%{version}.tar.gz

# Define Build Dependencies
BuildRequires: libattr-devel
BuildRequires: libcap-ng-devel
BuildRequires: liburing-devel

%description
This package includes QEMU and OVMF from the AMDSEV GitHub repository.

%prep
mkdir -p %{_builddir}/%{name}-%{version}
tar -xzf %{SOURCE0} -C %{_builddir}/%{name}-%{version}
cd %{_builddir}/%{name}-%{version}


%build
# Builds ovmf, we don't need qemu from here because we want to disable virtiofsd 
pushd %{_builddir}/%{name}-%{version}
./build qemu
./build ovmf
popd

pushd %{_builddir}/%{name}-%{version}/qemu
./configure --enable-virtfs --disable-virtiofsd --target-list=x86_64-softmmu --enable-debug --prefix=/usr/local --enable-io-uring
make -j$(nproc)
popd

%install
make install DESTDIR=%{buildroot}/usr/local/bin

%files
/usr/local/bin/qemu        # Define paths to QEMU binaries
# List other files to be included in the package

%changelog
* Tue Dec 26 2023 Archana Choudhary <archana1@microsoft.com>
- Initial package setup
