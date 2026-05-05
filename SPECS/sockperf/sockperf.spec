%global version 3.1

Name:           sockperf
Version:        %{version}
Release:        1%{?dist}
Summary:        Network benchmarking utility for testing latency and throughput
Group:          Applications/Internet
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/mellanox/%{name}
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.2.2/SOURCES/mlnx_ofed/OFED-internal-25.10-2.4.1.tgz
Source0:        %{_distro_sources_url}/%{name}-%{version}-3.2.2.tar.gz
ExclusiveArch:   x86_64

BuildRequires:  doxygen
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc-c++
BuildRequires:  make

# can't use _pkgdocdir neither _docdir since it is not the same even where it is defined
%global _my_pkgdocdir /usr/share/doc/%{name} 


%description
sockperf is a network benchmarking utility over socket API that was designed
for testing performance (latency and throughput) of high-performance systems
(it is also good for testing performance of regular networking systems as
well). It covers most of the socket API calls and options.

Specifically, in addition to the standard throughput tests, sockperf, does the
following:

* Measure latency of each discrete packet at sub-nanosecond resolution (using
  TSC register that counts CPU ticks with very low overhead).

* Does the above for both ping-pong mode and for latency under load mode. This
  means that we measure latency of single packets even under load of millions
  Packets Per Second (without waiting for reply of packet before sending
  subsequent packet on time)

* Enable spike analysis by providing histogram, with various percentiles of the
  packets' latencies (for example: median, min, max, 99% percentile, and more),
  (this is in addition to average and standard deviation). Also, sockperf
  provides full log with all packet's tx/rx times that can be further analyzed
  with external tools, such as MS-Excel or matplotlib - All this without
  affecting the benchmark itself.

* Support MANY optional settings for good coverage of socket API and network
  configurations, while still keeping very low overhead in the fast path to
  allow cleanest results.

%prep
#%setup -q -n %{name}-%{git_ref}
%setup -q -n %{name}-%{version}


%build

# Upstream wants and defaults to "-O3 --param inline-unit-growth=200".
# The Fedora optflags would override the former, so let's put it back.
# Avner wrote:
# > I reached that in the past after fine tuning the performance of sockperf.
# > We used sockperf for measuring latency of extremely fast networks.
# > Sometimes at sub microsecond resolution. This parameter helps us keeping
# > the entire fast path of the application as "one big function" with no
# > calls to other functions because it helps the compiler to respect all our
# > "inline" directive for other functions that we call (while still keeping
# > the "one big function" at a reasonable size for good performance at run
# > time).
export CXXFLAGS='%{optflags} -O3'
if [ ! -f configure ]; then
    ./autogen.sh
fi
%configure --enable-doc
# --enable-tool --enable-test
make %{?_smp_mflags}

%install
make install DESTDIR="%{?buildroot}"

%files
%defattr(-,root,root,-)
%license copying
%{_bindir}/%{name}
%{_mandir}/man3/%{name}.3.*
%{_my_pkgdocdir}

%changelog
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com>
* Thu Apr 17 2026 Azure Linux Team - 3.1-1
- Upgrade to DOCA 3.2.2 (OFED 25.10-2.4.1)

- Initial Azure Linux import from NVIDIA (license: BSD).
- License verified
