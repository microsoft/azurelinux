#!/bin/bash

LOGFILE=$1

# We have a log file, some lines will contain "Failed to download". From each of these lines, extract the URL that failed to download.
# The URLs will be in the format "https://*.rpm".

# time="2025-01-13T15:53:34Z" level=info msg="Attempt 1/8: Failed to download (https://packages.microsoft.com/azurelinux/3.0/prod/base/x86_64/Packages/l/libnuma-2.0.16-1.azl3.x86_64.rpm) with error: (download error:\nrequest failed:\nGet \"https://packages.microsoft.com/azurelinux/3.0/prod/base/x86_64/Packages/l/libnuma-2.0.16-1.azl3.x86_64.rpm\": dial tcp 13.107.246.40:443: i/o timeout)"
# We would want to extract the URL "https://packages.microsoft.com/azurelinux/3.0/prod/base/x86_64/Packages/l/libnuma-2.0.16-1.azl3.x86_64.rpm"
urls=$(cat $LOGFILE | grep "Failed to download" | grep -oP 'https://[^ \)]*.rpm' | sort | uniq)

# For each url, debug the issue by running curl -v <url>. If the curl command fails, print the error message, but continue to the next URL.
# Save the files in a directory called "debug" in the current directory.
for url in $urls; do
    printf '\n\n\n###################### Debugging %s ######################\n\n\n' "$url"
    curl -vO "$url"
done

echo "Done debugging"
exit 1
