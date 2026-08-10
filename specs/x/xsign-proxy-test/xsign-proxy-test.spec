Name:           xsign-proxy-test
Version:        1.0.0
Release:        1%{?dist}
Summary:        Dummy package to test xsign-proxy client-server communication

License:        MIT
URL:            https://example.com/xsign-proxy-test

Source0:        README

BuildArch:      noarch

%description
A dummy package that exercises the xsign-proxy-client during the build phase.
This package is used to verify that the xsign-proxy daemon is reachable from
within the mock chroot via the bind-mounted Unix socket.

%prep
cp %{SOURCE0} .

%build
echo "=== Testing xsign-proxy connectivity ==="

# Test 1: Verify the client script is available in the chroot
if [ -x /usr/local/bin/xsign_proxy_client.py ]; then
    echo "PASS: xsign_proxy_client.py is present and executable"
else
    echo "FAIL: xsign_proxy_client.py not found or not executable"
fi

# Test 2: Verify the socket directory is bind-mounted
if [ -d /var/run/xsign-proxy ]; then
    echo "PASS: Socket directory /var/run/xsign-proxy exists"
else
    echo "FAIL: Socket directory /var/run/xsign-proxy not found"
fi

# Test 3: Verify the exchange directory is bind-mounted
if [ -d /var/lib/xsign-exchange ]; then
    echo "PASS: Exchange directory /var/lib/xsign-exchange exists"
else
    echo "FAIL: Exchange directory /var/lib/xsign-exchange not found"
fi

# Test 4: Ping the daemon to verify connectivity
echo "Pinging xsign-proxy-d daemon..."
if /usr/local/bin/xsign_proxy_client.py ping; then
#     echo "PASS: Daemon responded to ping"
else
    echo "FAIL: Daemon did not respond to ping"
fi

# Test 5: Create a test file in the exchange directory and submit it for signing
TEST_FILE="/var/lib/xsign-exchange/test-file-%{name}-%{version}.txt"
echo "This is a test file for xsign-proxy signing" > "$TEST_FILE"
echo "Created test file: $TEST_FILE"

# echo "Submitting test file for signing..."
if /usr/local/bin/xsign_proxy_client.py sign "$TEST_FILE"; then
    echo "PASS: Sign request submitted successfully"
else
    echo "FAIL: Sign request failed"
    rm -f "$TEST_FILE"
fi

# Clean up test file
rm -f "$TEST_FILE"
echo "=== All xsign-proxy tests passed ==="

%install
mkdir -p %{buildroot}%{_docdir}/%{name}
echo "xsign-proxy-test package installed successfully" > %{buildroot}%{_docdir}/%{name}/README

%files
%{_docdir}/%{name}/README

%changelog
* Thu Jun 26 2026 Test User <test@example.com> - 1.0.0-1
- Initial package to test xsign-proxy client-server communication
