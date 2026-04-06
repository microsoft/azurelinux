/* CheckVendor -- Check the vendor properties match specified values.
   Copyright (C) 2020 Red Hat, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/**
 * @test
 */
public class CheckVendor {

    public static void main(String[] args) {
        if (args.length < 4) {
            System.err.println("CheckVendor <VENDOR> <VENDOR-URL> <VENDOR-BUG-URL> <VENDOR-VERSION-STRING>");
	    System.exit(1);
	}

	String vendor = System.getProperty("java.vendor");
	String expectedVendor = args[0];
	String vendorURL = System.getProperty("java.vendor.url");
	String expectedVendorURL = args[1];
	String vendorBugURL = System.getProperty("java.vendor.url.bug");
	String expectedVendorBugURL = args[2];
        String vendorVersionString = System.getProperty("java.vendor.version");
        String expectedVendorVersionString = args[3];

	if (!expectedVendor.equals(vendor)) {
	    System.err.printf("Invalid vendor %s, expected %s\n",
			      vendor, expectedVendor);
	    System.exit(2);
	}

	if (!expectedVendorURL.equals(vendorURL)) {
	    System.err.printf("Invalid vendor URL %s, expected %s\n",
			      vendorURL, expectedVendorURL);
	    System.exit(3);
	}

	if (!expectedVendorBugURL.equals(vendorBugURL)) {
            System.err.printf("Invalid vendor bug URL %s, expected %s\n",
			      vendorBugURL, expectedVendorBugURL);
	    System.exit(4);
	}

        if (!expectedVendorVersionString.equals(vendorVersionString)) {
            System.err.printf("Invalid vendor version string %s, expected %s\n",
                              vendorVersionString, expectedVendorVersionString);
	    System.exit(5);
        }

        System.err.printf("Vendor information verified as %s, %s, %s, %s\n",
                          vendor, vendorURL, vendorBugURL, vendorVersionString);
    }
}
