import com.google.webp.libwebp;

import java.lang.reflect.Method;

public class libwebp_jni_example {
  static {
    try {
      System.load("/usr/lib64/libwebp-java/libwebp_jni.so");
    } catch (UnsatisfiedLinkError e) {
      System.load("/usr/lib/libwebp-java/libwebp_jni.so");
    }
  }

  /**
   * usage: java -cp libwebp.jar:. libwebp_jni_example
   */
  public static void main(String argv[]) {
    final int version = libwebp.WebPGetDecoderVersion();
    System.out.println("libwebp version: " + Integer.toHexString(version));

    System.out.println("libwebp methods:");
    final Method[] libwebpMethods = libwebp.class.getDeclaredMethods();
    for (int i = 0; i < libwebpMethods.length; i++) {
      System.out.println(libwebpMethods[i]);
    }
  }
}
