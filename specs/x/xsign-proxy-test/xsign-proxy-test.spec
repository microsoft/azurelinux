Name:           xsign-proxy-test
Version:        1.0.0
Release:        1%{?dist}
Summary:        Dummy package to test xsign-proxy client-server communication

License:        MIT
URL:            https://example.com/xsign-proxy-test

Source0:        README

BuildArch:      noarch
BuildRequires:  python3

%description
A dummy package that exercises the xsign-proxy-client during the build phase.
This package is used to verify that the xsign-proxy daemon is reachable from
within the mock chroot via the bind-mounted Unix socket.

%prep
cp %{SOURCE0} .

%build

echo "=== Building the binary ==="
TEST_FILE="%{_builddir}/%{name}-%{version}/test-file-%{name}-%{version}.txt"
mkdir -p %{_builddir}/%{name}-%{version}
echo "This is a test file for xsign-proxy signing" > "$TEST_FILE"
echo "Created test file: $TEST_FILE"

# Check if pesign is available for direct signing
PESIGN_CLIENT=/usr/bin/pesign

# Are we running on a secure-boot image?
if [ -x "$PESIGN_CLIENT" ]; then

    SIGNED_TEST_FILE="%{_builddir}/%{name}-%{version}/test-file-%{name}-%{version}.txt"

    echo "=== Using pesign for secure-boot signing ==="
    
    # Sign using pesign-client
    echo "=== signing the test file with pesign ==="
    pesign pesign-client \
        --sign \
        --token "OpenSC Card" \
        --certificate "IPL" \
        --infile "$TEST_FILE" \
        --outfile "$SIGNED_TEST_FILE"
    echo "PASS: pesign sign request completed successfully"

    ls -la "$TEST_FILE"
    ls -la "$SIGNED_TEST_FILE"

    echo "=== secure boot signing completed ==="
else
    echo "=== skipped secure boot signing ==="
fi

%install
TEST_FILE="%{_builddir}/%{name}-%{version}/test-file-%{name}-%{version}.txt"
SIGNED_TEST_FILE="%{_builddir}/%{name}-%{version}/test-file-%{name}-%{version}.txt"

if [ -f "$SIGNED_TEST_FILE" ]; then
    install -D -m 0644 "$SIGNED_TEST_FILE" \
        %{buildroot}%{_sysconfdir}/xsign-proxy-test.txt
else
    install -D -m 0644 "$TEST_FILE" \
        %{buildroot}%{_sysconfdir}/xsign-proxy-test.txt
fi

%files
%config(noreplace) %{_sysconfdir}/xsign-proxy-test.txt

%changelog
* Fri Jun 26 2026 Test User <test@example.com> - 1.0.0-1
- Initial package to test xsign-proxy client-server communication
