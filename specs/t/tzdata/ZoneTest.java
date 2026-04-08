/* Smoke test to ensure that tzdb.data can be loaded.
   Copyright (c) 2024 Red Hat, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */


import java.time.zone.ZoneRulesProvider;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.Locale;
import java.util.Set;
import java.util.TimeZone;

public class ZoneTest {
    public static void main(String[] args) {
        // This is what failed in OpenJDK's build.tools.cldrconverter.
        new GregorianCalendar(TimeZone.getTimeZone("America/Los_Angeles"),
            Locale.US).get(Calendar.YEAR);

        // In some OpenJDK versions, this exercises a different parser.
        Set<String> available = ZoneRulesProvider.getAvailableZoneIds();
        boolean errors = false;
        if (available.contains("ROC"))
            System.out.println("error: ROC zone is present");
        if (!available.contains("America/New_York"))
            System.out.println("error: America/New_York is missing");
        if (errors)
            System.exit(1);
    }
}

