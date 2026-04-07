/* TestCryptoLevel -- Ensure unlimited crypto policy is in use.
   Copyright (C) 2012 Red Hat, Inc.

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

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;

import java.security.Permission;
import java.security.PermissionCollection;

public class TestCryptoLevel
{
  public static void main(String[] args)
    throws NoSuchFieldException, ClassNotFoundException,
           IllegalAccessException, InvocationTargetException
  {
    Class<?> cls = null;
    Method def = null, exempt = null;

    try
      {
        cls = Class.forName("javax.crypto.JceSecurity");
      }
    catch (ClassNotFoundException ex)
      {
        System.err.println("Running a non-Sun JDK.");
        System.exit(0);
      }
    try
      {
        def = cls.getDeclaredMethod("getDefaultPolicy");
        exempt = cls.getDeclaredMethod("getExemptPolicy");
      }
    catch (NoSuchMethodException ex)
      {
        System.err.println("Running IcedTea with the original crypto patch.");
        System.exit(0);
      }
    def.setAccessible(true);
    exempt.setAccessible(true);
    PermissionCollection defPerms = (PermissionCollection) def.invoke(null);
    PermissionCollection exemptPerms = (PermissionCollection) exempt.invoke(null);
    Class<?> apCls = Class.forName("javax.crypto.CryptoAllPermission");
    Field apField = apCls.getDeclaredField("INSTANCE");
    apField.setAccessible(true);
    Permission allPerms = (Permission) apField.get(null);
    if (defPerms.implies(allPerms) && (exemptPerms == null || exemptPerms.implies(allPerms)))
      {
        System.err.println("Running with the unlimited policy.");
        System.exit(0);
      }
    else
      {
        System.err.println("WARNING: Running with a restricted crypto policy.");
        System.exit(-1);
      }
  }
}
