#!/bin/bash

LOGFILE=$1

# We have a log file, some lines will contain "Failed to download". From each of these lines, extract the URL that failed to download.
# The URLs will be in the format "https://*.rpm".

# time="2025-01-13T15:53:34Z" level=info msg="Attempt 1/8: Failed to download (https://packages.microsoft.com/azurelinux/3.0/prod/base/x86_64/Packages/l/libnuma-2.0.16-1.azl3.x86_64.rpm) with error: (download error:\nrequest failed:\nGet \"https://packages.microsoft.com/azurelinux/3.0/prod/base/x86_64/Packages/l/libnuma-2.0.16-1.azl3.x86_64.rpm\": dial tcp 13.107.246.40:443: i/o timeout)"
# We would want to extract the URL "https://packages.microsoft.com/azurelinux/3.0/prod/base/x86_64/Packages/l/libnuma-2.0.16-1.azl3.x86_64.rpm"
# There are several errors that have "i/o timeout", those are transient errors, so we can ignore them.
urls=$(cat $LOGFILE | grep "Failed to download" | grep -v "i/o timeout" | grep -oP 'https://[^ \)]*.rpm' | sort | uniq)

printf '\n\n\n###################### Errors: ######################\n\n\n'
# Print the error lines here for reference
cat $LOGFILE | grep "Failed to download" | grep -v "i/o timeout"

# For each url, debug the issue by running curl -v <url>. If the curl command fails, print the error message, but continue to the next URL.
# Save the files in a directory called "debug" in the current directory.
for url in $urls; do
    printf '\n\n\n###################### Debugging %s ######################\n\n\n' "$url"
    curl -vO "$url" || true
done

echo "Done debugging"
exit 1
