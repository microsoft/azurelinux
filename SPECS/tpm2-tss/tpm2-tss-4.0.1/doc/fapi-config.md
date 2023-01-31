# FAPI configuration

The FAPI parameters which can be adjusted via the configuration file are:

* profile_name: Name of the default cryptographic profile chosen from the profile_dir directory.
* profile_dir: Directory that contains all cryptographic profiles known to FAPI.
* user_dir: The directory where user objects are stored.
* system_dir: The directory where system objects, policies, and imported
  objects are stored.
* tcti: The TCTI interface which will be used.
* system_pcrs: The PCR registers which are used by the system.
* log_dir: The directory for the event log.
* ek_cert_less: A switch to disable certificate verification (optional).
* ek_fingerprint: The fingerprint of the endorsement key (optional).
* firmware_log_file: The binary bios measuerments.
* ima_log_file: The binary IMA measuerments (Integrity Measurement Architecture).

If not otherwise specified during TSS installation, the default location for the
exemplary profiles is /etc/tpm2-tss/profiles/ and /etc/tpm2-tss/ for the FAPI
configuration file. The environment variable TSS2_FAPICONF can be used to set
an alternative pathname for the FAPI configuration file.
If the system measurement files (IMA and bios) do not exist /dev/null will
be used for firmware_log_file and ima_log_file.

# EXAMPLES
The FAPI configuration file is JSON encoded:

```
{
     "profile_name": "P_ECCP256SHA256",
     "profile_dir": "/etc/tpm2-tss/fapi-profiles/",
     "user_dir": "~/.local/share/tpm2-tss/user/keystore/",
     "system_dir": "/home/myhome/keystore/system/keystore",
     "tcti": "",
     "system_pcrs" : [0, 1, 2, 3, 4, 5, 6, 7],
     "log_dir" : "/home/myhome/eventlog/",
     "firmware_log_file": "/sys/kernel/security/tpm0/binary_bios_measurements",
     "ima_log_file": "/sys/kernel/security/ima/binary_runtime_measurements"
}
```

 For this example the default TCTI of the system will be used. The certificates
 for the stored endorsement keys will be checked.
 If the certificate checking is not needed the option:

 ```
    "ek_cert_less": "yes"
 ```
can be added to the config file. Alternative to the standard certificate checking a
fingerprint (hash of the public key) for the stored endorsement key can be defined
in the config file:

```
"ek_fingerprint":  {
    "hashAlg" : "sha256",
    "digest" : "9e56...214d"
    }
 ```