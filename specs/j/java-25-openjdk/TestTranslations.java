/* TestTranslations -- Ensure translations are available for new timezones
   Copyright (C) 2022 Red Hat, Inc.

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

import java.text.DateFormatSymbols;

import java.time.ZoneId;
import java.time.format.TextStyle;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Locale;
import java.util.Objects;
import java.util.TimeZone;

public class TestTranslations {

    private static Map<Locale,String[]> KYIV, CIUDAD_JUAREZ;

    static {
        Map<Locale,String[]> map = new HashMap<Locale,String[]>();
        map.put(Locale.US, new String[] { "Eastern European Standard Time", "GMT+02:00", "EET",
                                          "Eastern European Summer Time", "GMT+03:00", "EEST",
                                          "Eastern European Time", "GMT+02:00", "EET"});
        map.put(Locale.FRANCE, new String[] { "heure normale d\u2019Europe de l\u2019Est", "UTC+02:00", "EET",
                                              "heure d\u2019\u00e9t\u00e9 d\u2019Europe de l\u2019Est", "UTC+03:00", "EEST",
                                              "heure d\u2019Europe de l\u2019Est", "UTC+02:00", "EET"});
        map.put(Locale.GERMANY, new String[] { "Osteurop\u00e4ische Normalzeit", "OEZ", "OEZ",
                                               "Osteurop\u00e4ische Sommerzeit", "OESZ", "OESZ",
                                               "Osteurop\u00e4ische Zeit", "OEZ", "OEZ"});
        KYIV = Collections.unmodifiableMap(map);

        map = new HashMap<Locale,String[]>();
        map.put(Locale.US, new String[] { "Mountain Standard Time", "MST", "MST",
                                          "Mountain Daylight Time", "MDT", "MDT",
                                          "Mountain Time", "MT", "MT"});
        map.put(Locale.FRANCE, new String[] { "heure normale des Rocheuses", "UTC\u221207:00", "MST",
                                              "heure d\u2019\u00e9t\u00e9 des Rocheuses", "UTC\u221206:00", "MDT",
                                              "heure des Rocheuses", "UTC\u221207:00", "MT"});
        map.put(Locale.GERMANY, new String[] { "Rocky-Mountain-Normalzeit", "GMT-07:00", "MST",
                                               "Rocky-Mountain-Sommerzeit", "GMT-06:00", "MDT",
                                               "Rocky-Mountain-Zeit", "GMT-07:00", "MT"});
        CIUDAD_JUAREZ = Collections.unmodifiableMap(map);
    }


    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Test must be started with the name of the locale provider.");
            System.exit(1);
        }

        System.out.println("Checking sanity of full zone string set...");
        boolean invalid = Arrays.stream(Locale.getAvailableLocales())
            .peek(l -> System.out.println("Locale: " + l))
            .map(l -> DateFormatSymbols.getInstance(l).getZoneStrings())
            .flatMap(zs -> Arrays.stream(zs))
            .flatMap(names -> Arrays.stream(names))
            .filter(name -> Objects.isNull(name) || name.isEmpty())
            .findAny()
            .isPresent();
        if (invalid) {
            System.err.println("Zone string for a locale returned null or empty string");
            System.exit(2);
        }

        String localeProvider = args[0];
        testZone(localeProvider, KYIV,
                 new String[] { "Europe/Kiev", "Europe/Kyiv", "Europe/Uzhgorod", "Europe/Zaporozhye" });
        testZone(localeProvider, CIUDAD_JUAREZ,
                 new String[] { "America/Cambridge_Bay", "America/Ciudad_Juarez" });
    }

    private static void testZone(String localeProvider, Map<Locale,String[]> exp, String[] ids) {
        for (Locale l : exp.keySet()) {
            String[] expected = exp.get(l);
            System.out.printf("Expected values for %s are %s\n", l, Arrays.toString(expected));
            for (String id : ids) {
                String expectedShortStd = null;
                String expectedShortDST = null;
                String expectedShortGen = null;

                System.out.printf("Checking locale %s for %s...\n", l, id);

                if ("JRE".equals(localeProvider)) {
                    expectedShortStd = expected[2];
                    expectedShortDST = expected[5];
                    expectedShortGen = expected[8];
                } else if ("CLDR".equals(localeProvider)) {
                    expectedShortStd = expected[1];
                    expectedShortDST = expected[4];
                    expectedShortGen = expected[7];
                } else {
                    System.err.printf("Invalid locale provider %s\n", localeProvider);
                    System.exit(3);
                }
                System.out.printf("Locale Provider is %s, using short values %s, %s and %s\n",
                                  localeProvider, expectedShortStd, expectedShortDST, expectedShortGen);

                String longStd = TimeZone.getTimeZone(id).getDisplayName(false, TimeZone.LONG, l);
                String shortStd = TimeZone.getTimeZone(id).getDisplayName(false, TimeZone.SHORT, l);
                String longDST = TimeZone.getTimeZone(id).getDisplayName(true, TimeZone.LONG, l);
                String shortDST = TimeZone.getTimeZone(id).getDisplayName(true, TimeZone.SHORT, l);
                String longGen = ZoneId.of(id).getDisplayName(TextStyle.FULL, l);
                String shortGen = ZoneId.of(id).getDisplayName(TextStyle.SHORT, l);

                if (!expected[0].equals(longStd)) {
                    System.err.printf("Long standard display name for %s in %s was %s, expected %s\n",
                                      id, l, longStd, expected[0]);
                    System.exit(4);
                }

                if (!expectedShortStd.equals(shortStd)) {
                    System.err.printf("Short standard display name for %s in %s was %s, expected %s\n",
                                      id, l, shortStd, expectedShortStd);
                    System.exit(5);
                }

                if (!expected[3].equals(longDST)) {
                    System.err.printf("Long DST display name for %s in %s was %s, expected %s\n",
                                      id, l, longDST, expected[3]);
                    System.exit(6);
                }

                if (!expectedShortDST.equals(shortDST)) {
                    System.err.printf("Short DST display name for %s in %s was %s, expected %s\n",
                                      id, l, shortDST, expectedShortDST);
                    System.exit(7);
                }

                if (!expected[6].equals(longGen)) {
                    System.err.printf("Long generic display name for %s in %s was %s, expected %s\n",
                                      id, l, longGen, expected[6]);
                    System.exit(8);
                }

                if (!expectedShortGen.equals(shortGen)) {
                    System.err.printf("Short generic display name for %s in %s was %s, expected %s\n",
                                      id, l, shortGen, expectedShortGen);
                    System.exit(9);
                }
            }
        }
    }
}
