/* TestECDSA -- Ensure ECDSA signatures are working.
   Copyright (C) 2016 Red Hat, Inc.

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

import java.math.BigInteger;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

/**
 * @test
 */
public class TestECDSA {

    public static void main(String[] args) throws Exception {
        KeyPairGenerator keyGen = KeyPairGenerator.getInstance("EC");
        KeyPair key = keyGen.generateKeyPair();
        
        byte[] data = "This is a string to sign".getBytes("UTF-8");
        
        Signature dsa = Signature.getInstance("NONEwithECDSA");
        dsa.initSign(key.getPrivate());
        dsa.update(data);
        byte[] sig = dsa.sign();
        System.out.println("Signature: " + new BigInteger(1, sig).toString(16));
        
        Signature dsaCheck = Signature.getInstance("NONEwithECDSA");
        dsaCheck.initVerify(key.getPublic());
        dsaCheck.update(data);
        boolean success = dsaCheck.verify(sig);
        if (!success) {
            throw new RuntimeException("Test failed. Signature verification error");
        }
        System.out.println("Test passed.");
    }
}
