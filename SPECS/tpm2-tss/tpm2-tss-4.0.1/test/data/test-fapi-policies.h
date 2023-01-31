/* SPDX-License-Identifier: BSD-2-Clause */
#ifndef TEST_FAPI_POLICIES_H
#define TEST_FAPI_POLICIES_H

typedef struct policy_digests policy_digests;
struct policy_digests {
    char *path;
    char *sha1;
    char *sha256;
};

/*
 * Table with expected policy digests.
 * If computation is not possible sha1 and sha256 has to be set to NULL.
 * If a policy digest will be computed for these cases an error will be signalled.
 */
static policy_digests _test_fapi_policy_policies[] = {
    { .path = "/policy/pol_action",
      .sha1 = "0000000000000000000000000000000000000000",
      .sha256 = "0000000000000000000000000000000000000000000000000000000000000000" },
    { .path = "/policy/pol_pcr16_0_ecc_authorized",
      .sha1 = "eab0d71ae6088009cbd0b50729fde69eb453649c",
      .sha256 = "bff2d58e9813f97cefc14f72ad8133bc7092d652b7c877959254af140c841f36" },
    { .path = "/policy/pol_authorize_ecc_pem",
      .sha1 = "9d2c365dd9ccba3962041d7f9b3e276588338c94",
      .sha256 = "b9b370c6b4f84887518634ab408ce23dfc092ae42281a1b8438b3f34d9ceb18e" },
    { .path = "/policy/pol_nv_counter", .sha1 = NULL, .sha256 = NULL },
    { .path = "/policy/pol_authorize_rsa_pem",
      .sha1 = "33e656768aa977ff42cdc60799c48f1a8ab6c1ec",
      .sha256 = "5164b89fcfdc398806c0fde7a3eb52371595fcbec1b1fcea57524c56fff67f46" },
    { .path = "/policy/pol_locality",
      .sha1 = "9d2af7c7235047d90719bb07e699bc266554997f",
      .sha256 = "ddee6af14bf3c4e8127ced87bcf9a57e1c0c8ddb5e67735c8505f96f07b8dbb8" },
    { .path = "/policy/pol_nv_change_auth",
      .sha1 = "9ebf6fd0f5547da6c57280ae4032c2de62b773da",
      .sha256 = "363ac945b6457c47c31f3355dba0db27de8db213d6250c6bf79685003f9fe7ab" },
    { .path = "/policy/pol_password",
      .sha1 = "af6038c78c5c962d37127e319124e3a8dc582e9b",
      .sha256 = "8fcd2169ab92694e0c633f1ab772842b8241bbc20288981fc7ac1eddc1fddb0e" },
    { .path = "/policy/pol_pcr16_0_or",
      .sha1 = "be5ea4b5e7de56f883968667f1f12f02b7c3c99b",
      .sha256 = "04b01d728fc1ea060d943b3ca6e3e5ea9d3bbb61126542677ad7591c092eafba" },
    { .path = "/policy/pol_physical_presence",
      .sha1 = "9acb06395f831f88e89eeac29442cb0ebe9485ab",
      .sha256 = "0d7c6747b1b9facbba03492097aa9d5af792e5efc07346e05f9daa8b3d9e13b5" },
    { .path = "/policy/pol_secret", .sha1 = NULL, .sha256 = NULL },
    { .path = "/policy/pol_authorize", .sha1 = NULL, .sha256 = NULL },
    { .path = "/policy/pol_authorize_nv", .sha1 = NULL, .sha256 = NULL },
    { .path = "/policy/pol_auth_value",
      .sha1 = "af6038c78c5c962d37127e319124e3a8dc582e9b",
      .sha256 = "8fcd2169ab92694e0c633f1ab772842b8241bbc20288981fc7ac1eddc1fddb0e" },
    { .path = "/policy/pol_command_code",
      .sha1 = "2a2a1493809bbc1b4b46fc325dc54a815cbb980e",
      .sha256 = "cc6918b226273b08f5bd406d7f10cf160f0a7d13dfd83b7770ccbcd1aa80d811" },
    { .path = "/policy/pol_duplicate", .sha1 = NULL, .sha256 = NULL },
    { .path = "/policy/pol_pcr16_0",
      .sha1 = "eab0d71ae6088009cbd0b50729fde69eb453649c",
      .sha256 = "bff2d58e9813f97cefc14f72ad8133bc7092d652b7c877959254af140c841f36" },
    { .path = "/policy/pol_nv", .sha1 = NULL, .sha256 = NULL },
    { .path = "/policy/pol_authorize_outer", .sha1 = NULL, .sha256 = NULL },
    { .path = "/policy/pol_countertimer",
      .sha1 = "969a04fb820cc4a3aa4436e02cd5a71a87fd95b9",
      .sha256 = "7c67802209683d17c1d94f3fc9df7afb2a0d7955c3c5d0fa3f602d58ffdaf984" },
    { .path = "/policy/pol_cphash",
      .sha1 = "b2b2763b9a638a8e4f38897a47468e09fe0a0853",
      .sha256 = "2d7038734b12258ae7108ab70d0e7ee36f4e64c64d53f8adb6c2bed602c95d09" },
    { .path = "/policy/pol_name_hash", .sha1 = NULL, .sha256 = NULL },
    { .path = "/policy/pol_nv_written",
      .sha1 = "5a91e7105386bd547a15aad40369b1e25e462873",
      .sha256 = "3c326323670e28ad37bd57f63b4cc34d26ab205ef22f275c58d47fab2485466e" },
    { .path = "/policy/pol_pcr16_0_fail",
      .sha1 = "904fbcef1d6cb3ecaf085259b40b55fa3025232f",
      .sha256 = "b740077197d46009b9c18f5ad181b7a3ac5bef1d9a881cc5dde808f1a6b8c787" },
    { .path = "/policy/pol_pcr16_read",
      .sha1 = "eab0d71ae6088009cbd0b50729fde69eb453649c",
      .sha256 = "bff2d58e9813f97cefc14f72ad8133bc7092d652b7c877959254af140c841f36" },
    { .path = "/policy/pol_pcr8_0",
      .sha1 = "d6756ffbe88b1d082ee7048500ff9cc1a718de40",
      .sha256 = "2a90ac03196573f129e70a9e04485bff581d2890fe5882d3c2667290d84b497b" },
    { .path = "/policy/pol_signed_ecc",
      .sha1 = "c18fc6f175bd17e41c257184443a81c99ced9225",
      .sha256 = "07aefc36fb098f5f59f2f74d8854235a29d1f93b4ddd488f6ec667d9c1d716b6" },
    { .path = "/policy/pol_signed",
      .sha1 = "85bf0403e87d3c29c3daa5c87efb111cb717875d",
      .sha256 = "b1969529af7796c5b4f5e4781713f4525049f36cb12ec63f996dad1c4401c068" },
    { .path = "/policy/pol_ek_high_range_sha256",
      .sha1 = "23694f69a8f33f588a93879021a294f3ed73b361",
      .sha256 = "ca3d0a99a2b93906f7a3342414efcfb3a385d44cd1fd459089d19b5071c0b7a0" },
    { .path = "/policy/pol_template",
      .sha1 = "acfec8114dee366fa5451cfcbfe2111cf324e18d",
      .sha256 = "4f94fe9a608e6efc376ee1589f43581b8eb1fea60fe6ae94d60f88b67312825d" },
};
#endif
