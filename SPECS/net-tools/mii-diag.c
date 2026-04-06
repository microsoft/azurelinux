/* Mode: C;
 * mii-diag.c: Examine and set the MII registers of a network interfaces.

	Usage:	mii-diag [-vw] interface.

	This program reads and writes the Media Independent Interface (MII)
	management registers on network transceivers.  The registers control
	and report network link settings and errors.  Examples are link speed,
	duplex, capabilities advertised to the link partner, status LED
	indications and link error counters.

	Notes:
	The compile-command is at the end of this source file.
	This program works with drivers that implement MII ioctl() calls.

	Written/copyright 1997-2003 by Donald Becker <becker@scyld.com>

	This program is free software; you can redistribute it
	and/or modify it under the terms of the GNU General Public
	License as published by the Free Software Foundation.

	The author may be reached as becker@scyld.com, or C/O
	 Scyld Computing Corporation
	 914 Bay Ridge Road, Suite 220
	 Annapolis MD 21403

	References
	http://scyld.com/expert/mii-status.html
	http://scyld.com/expert/NWay.html
	http://www.national.com/pf/DP/DP83840.html
*/

static char version[] =
"mii-diag.c:v2.11 3/21/2005 Donald Becker (becker@scyld.com)\n"
" http://www.scyld.com/diag/index.html\n";

static const char usage_msg[] =
"Usage: %s [--help] [-aDfrRvVw] [-AF <speed+duplex>] [--watch] <interface>\n";
static const char long_usage_msg[] =
"Usage: %s [-aDfrRvVw] [-AF <speed+duplex>] [--watch] <interface>\n\
\n\
  This program configures and monitors the transceiver management registers\n\
  for network interfaces.  It uses the Media Independent Interface (MII)\n\
  standard with additional Linux-specific controls to communicate with the\n\
  underlying device driver.  The MII registers control and report network\n\
  link settings and errors.  Examples are link speed, duplex, capabilities\n\
  advertised to the link partner, status LED indications and link error\n\
  counters.\n\
\n\
   The common usage is\n\
      mii-diag eth0\n\
\n\
 Frequently used options are\n\
   -A  --advertise <speed|setting>\n\
   -F  --fixed-speed <speed>\n\
	Speed is one of: 100baseT4, 100baseTx, 100baseTx-FD, 100baseTx-HD,\n\
	                 10baseT, 10baseT-FD, 10baseT-HD\n\
   -s  --status     Return exit status 2 if there is no link beat.\n\
\n\
 Less frequently used options are\n\
   -a  --all-interfaces  Show the status all interfaces\n\
              (Not recommended with options that change settings.)\n\
   -D  --debug\n\
   -g  --read-parameters 	Get driver-specific parameters.\n\
   -G  --set-parameters PARMS	Set driver-specific parameters.\n\
       Parameters are comma separated, missing parameters retain\n\
       their previous values.\n\
   -M  --msg-level LEVEL 	Set the driver message bit map.\n\
   -p  --phy ADDR		Set the PHY (MII address) to report.\n\
   -r  --restart	Restart the link autonegotiation.\n\
   -R  --reset		Reset the transceiver.\n\
   -v  --verbose	Report each action taken.\n\
   -V  --version	Emit version information.\n\
   -w  --watch		Continuously monitor the transceiver and report changes.\n\
\n\
   This command returns success (zero) if the interface information can be\n\
   read.  If the --status option is passed, a zero return means that the\n\
   interface has link beat.\n\
";

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <getopt.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <net/if.h>
#ifdef use_linux_libc5
#include <linux/if_arp.h>
#include <linux/if_ether.h>
#endif

typedef u_int32_t u32;
typedef u_int16_t u16;
typedef u_int8_t u8;

#if defined(SIOCGPARAMS)  && SIOCGPARAMS != SIOCDEVPRIVATE+3
#error Changed definition for SIOCGPARAMS
#else
#define SIOCGPARAMS (SIOCDEVPRIVATE+3) 		/* Read operational parameters. */
#define SIOCSPARAMS (SIOCDEVPRIVATE+4) 		/* Set operational parameters. */
#endif

const char shortopts[] = "aA:C:DfF:gG:hmM:p:rRsvVw?";
struct option longopts[] = {
 /* { name  has_arg  *flag  val } */
    {"all-interfaces", 0, 0, 'a'},	/* Show all interfaces. */
	{"advertise",	1, 0, 'A'},		/* Change the capabilities advertised. */
	{"BMCR",		1, 0, 'C'},		/* Set the control register. */
    {"debug",       0, 0, 'D'},		/* Increase the debug level. */
    {"force",       0, 0, 'f'},		/* Force the operation. */
    {"fixed-speed", 1, 0, 'F'},		/* Fixed speed name. */
    {"read-parameters", 0, 0, 'g'}, /* Show general settings values. */
    {"set-parameters",  1, 0, 'G'},	/* Write general settings values. */
    {"help", 		0, 0, 'h'},		/* Print a long usage message. */
    {"monitor",		0, 0, 'm'},		/* Monitor status register. */
    {"msg-level",	1, 0, 'M'},		/* Set the driver message level. */
    {"phy",			1, 0, 'p'},		/* Set the PHY (MII address) to report. */
    {"restart",		0, 0, 'r'},		/* Restart the link negotiation */
    {"reset",		0, 0, 'R'},		/* Reset the transceiver. */
    {"status",		0, 0, 's'},		/* Non-zero exit status w/ no link beat. */
    {"verbose", 	0, 0, 'v'},		/* Report each action taken.  */
    {"version", 	0, 0, 'V'},		/* Emit version information.  */
    {"watch", 		0, 0, 'w'},		/* Constantly monitor the port.  */
    {"error", 		0, 0, '?'},		/* Return the error message. */
    { 0, 0, 0, 0 }
};

/* Usually in libmii.c, but trivial substitions are below. */
extern int  show_mii_details(long ioaddr, int phy_id);
extern void monitor_mii(long ioaddr, int phy_id);
int  show_mii_details(long ioaddr, int phy_id) __attribute__((weak));
void monitor_mii(long ioaddr, int phy_id) __attribute__((weak));


/* Command-line flags. */
unsigned int opt_a = 0,					/* Show-all-interfaces flag. */
	opt_f = 0,					/* Force the operation. */
	opt_g = 0,
	opt_G = 0,
	verbose = 0,				/* Verbose flag. */
	debug = 0,
	opt_version = 0,
	opt_restart = 0,
	opt_reset = 0,
	opt_status = 0,
	opt_watch = 0;
static int msg_level = -1;
static int set_BMCR = -1;
static int nway_advertise = 0;
static int fixed_speed = -1;
static int override_phy = -1;
char *opt_G_string = NULL;

/* Internal values. */
int new_ioctl_nums;
int skfd = -1;					/* AF_INET socket for ioctl() calls.	*/
struct ifreq ifr;

int do_one_xcvr(int skfd);
int show_basic_mii(long ioaddr, int phy_id);
int mdio_read(int skfd, int phy_id, int location);
void mdio_write(int skfd, int phy_id, int location, int value);
static int parse_advertise(const char *capabilities);
static void monitor_status(long ioaddr, int phy_id);


int
main(int argc, char **argv)
{
	int c, errflag = 0;
	char **spp, *ifname;
    char *progname = rindex(argv[0], '/') ? rindex(argv[0], '/')+1 : argv[0];

	while ((c = getopt_long(argc, argv, shortopts, longopts, 0)) != EOF)
		switch (c) {
		case 'a': opt_a++; break;
		case 'A': nway_advertise |= parse_advertise(optarg);
			if (nway_advertise == -1) errflag++;
			break;
		case 'C': set_BMCR = strtoul(optarg, NULL, 16); break;
		case 'D': debug++;			break;
		case 'f': opt_f++; break;
		case 'F': fixed_speed = parse_advertise(optarg);
			if (fixed_speed == -1) errflag++;
			break;
		case 'g': opt_g++; break;
		case 'G': opt_G++; opt_G_string = strdup(optarg); break;
		case 'm': opt_watch++; opt_status++; break;
		case 'M': msg_level = strtoul(optarg, NULL, 0); break;
		case 'h': fprintf(stderr, long_usage_msg, progname); return 0;
		case 'p': override_phy = atoi(optarg); break;
		case 'r': opt_restart++;	break;
		case 'R': opt_reset++;		break;
		case 's': opt_status++;		break;
		case 'v': verbose++;		break;
		case 'V': opt_version++;	break;
		case 'w': opt_watch++;		break;
		case '?': errflag++;		break;
		}
	if (errflag) {
		fprintf(stderr, usage_msg, progname);
		return 2;
	}

	if (verbose || opt_version)
		printf("%s", version);

	/* Open a basic socket. */
	if ((skfd = socket(AF_INET, SOCK_DGRAM,0)) < 0) {
		perror("socket");
		return 1;
	}

	if (debug)
		fprintf(stderr, "DEBUG: argc=%d, optind=%d and argv[optind] is %s.\n",
				argc, optind, argv[optind]);

	/* No remaining args means interface wasn't specified. */
	if (optind == argc) {
		fprintf(stderr, "No interface specified.\n");
		fprintf(stderr, usage_msg, progname);
		(void) close(skfd);
		return 2;
	} else {
		/* Copy the interface name. */
		spp = argv + optind;
		ifname = *spp++;
	}

	if (ifname == NULL) {
		fprintf(stderr, "No ifname.\n");
		(void) close(skfd);
		return -1;
	}

	/* Verify that the interface supports the ioctl(), and if
	   it is using the new or old SIOCGMIIPHY value (grrr...).
	 */
	{
		u16 *data = (u16 *)(&ifr.ifr_data);

		strncpy(ifr.ifr_name, ifname, IFNAMSIZ);
		ifr.ifr_name[IFNAMSIZ-1] = '\0';
		data[0] = 0;

		if (ioctl(skfd, 0x8947, &ifr) >= 0) {
			new_ioctl_nums = 1;
		} else if (ioctl(skfd, SIOCDEVPRIVATE, &ifr) >= 0) {
			new_ioctl_nums = 0;
		} else {
			fprintf(stderr, "SIOCGMIIPHY on %s failed: %s\n", ifname,
					strerror(errno));
			(void) close(skfd);
			return 1;
		}
		if (verbose)
			printf("  Using the %s SIOCGMIIPHY value on PHY %d "
				   "(BMCR 0x%4.4x).\n",
				   new_ioctl_nums ? "new" : "old", data[0], data[3]);
	}

	do_one_xcvr(skfd);

	(void) close(skfd);
	return 0;
}

int do_one_xcvr(int skfd)
{
	u16 *data = (u16 *)(&ifr.ifr_data);
	u32 *data32 = (u32 *)(&ifr.ifr_data);
	unsigned phy_id = data[0];

	if (override_phy >= 0) {
		printf("Using the specified MII PHY index %d.\n", override_phy);
		phy_id = override_phy;
	}

	if (opt_g || opt_G || msg_level >= 0) {
		if (ioctl(skfd, SIOCGPARAMS, &ifr) < 0) {
			fprintf(stderr, "SIOCGPARAMS on %s failed: %s\n", ifr.ifr_name,
					strerror(errno));
			return -1;
		}
	}
	if (opt_g) {
		int i;
		printf("Driver general parameter settings:");
		for (i = 0; i*sizeof(u32) < sizeof(ifr.ifr_ifru); i++) {
			printf(" %d", data32[i]);
		}
		printf(".\n");
	}
	if (opt_G) {
		/* Set up to four arbitrary driver parameters from the -G parameter.
		   The format is comma separated integers, with a missing element
		   retaining the previous value.
		*/
		char *str = opt_G_string;
		int i;
		for (i = 0; str && i < 4; i++) {
			char *endstr;
			u32 newval = strtol(str, &endstr, 0);
			if (debug)
				printf(" parse string '%s'  value %d end '%s'.\n",
					   str, newval, endstr);
			if (str == endstr) {
				if (endstr[0] == ',') /* No parameter */
					str = endstr+1;
				else {
					fprintf(stderr, "Invalid driver parameter '%s'.\n", str);
					str = index(str, ',');
				}
			} else if (endstr[0] == ',') {
				data32[i] = newval;
				str = endstr + 1;
			} else if (endstr[0] == 0) {
				data32[i] = newval;
				break;
			}
		}
		printf("Setting new driver general parameters:");
		for (i = 0; i*sizeof(u32) < sizeof(ifr.ifr_ifru); i++) {
			printf(" %d", data32[i]);
		}
		printf(".\n");
		if (ioctl(skfd, SIOCSPARAMS, &ifr) < 0) {
			fprintf(stderr, "SIOCSPARAMS on %s failed: %s\n", ifr.ifr_name,
					strerror(errno));
			return -1;
		}
	}
	if (msg_level >= 0) {
		data32[0] = msg_level;
		if (ioctl(skfd, SIOCSPARAMS, &ifr) < 0) {
			fprintf(stderr, "SIOCSPARAMS on %s failed: %s\n", ifr.ifr_name,
					strerror(errno));
			return -1;
		}
	}

	if (opt_reset) {
		printf("Resetting the transceiver...\n");
		mdio_write(skfd, phy_id, 0, 0x8000);
	}
	/* Note: PHY addresses > 32 are pseudo-MII devices, usually built-in. */
	if (phy_id < 64  &&  nway_advertise > 0) {
		printf(" Setting the media capability advertisement register of "
			   "PHY #%d to 0x%4.4x.\n", phy_id, nway_advertise | 1);
		mdio_write(skfd, phy_id, 4, nway_advertise | 1);
		mdio_write(skfd, phy_id, 0, 0x1000);
	}

	if (opt_restart) {
		printf("Restarting negotiation...\n");
		mdio_write(skfd, phy_id, 0, 0x0000);
		mdio_write(skfd, phy_id, 0, 0x1200);
	}
	/* To force 100baseTx-HD do  mdio_write(skfd, phy_id, 0, 0x2000); */
	if (fixed_speed >= 0) {
		int reg0_val = 0;
		if (fixed_speed & 0x0180) 		/* 100mpbs */
			reg0_val |=  0x2000;
		if ((fixed_speed & 0x0140) &&		/* A full duplex type and */
			! (fixed_speed & 0x0820)) 		/* no half duplex types. */
			reg0_val |= 0x0100;
		printf("Setting the speed to \"fixed\", Control register %4.4x.\n",
			   reg0_val);
		mdio_write(skfd, phy_id, 0, reg0_val);
	}
	if (set_BMCR >= 0) {
		printf("Setting the Basic Mode Control Register to 0x%4.4x.\n",
			   set_BMCR);
		mdio_write(skfd, phy_id, 0, set_BMCR);
	}

	if (opt_watch && opt_status)
		monitor_status(skfd, phy_id);

	show_basic_mii(skfd, phy_id);
#ifdef LIBMII
	if (verbose)
		show_mii_details(skfd, phy_id);
#else
	if (verbose || debug) {
		int mii_reg, mii_val;
		printf(" MII PHY #%d transceiver registers:", phy_id);
		for (mii_reg = 0; mii_reg < 32; mii_reg++) {
			mii_val = mdio_read(skfd, phy_id, mii_reg);
			printf("%s %4.4x", (mii_reg % 8) == 0 ? "\n  " : "",
				   mii_val);
		}
		printf("\n");
	}
#endif

	if (opt_watch)
		monitor_mii(skfd, phy_id);
	if (opt_status &&
		(mdio_read(skfd, phy_id, 1) & 0x0004) == 0)
		exit(2);
	return 0;
}

int mdio_read(int skfd, int phy_id, int location)
{
	u16 *data = (u16 *)(&ifr.ifr_data);

	data[0] = phy_id;
	data[1] = location;

	if (ioctl(skfd, new_ioctl_nums ? 0x8948 : SIOCDEVPRIVATE+1, &ifr) < 0) {
		fprintf(stderr, "SIOCGMIIREG on %s failed: %s\n", ifr.ifr_name,
				strerror(errno));
		return -1;
	}
	return data[3];
}

void mdio_write(int skfd, int phy_id, int location, int value)
{
	u16 *data = (u16 *)(&ifr.ifr_data);

	data[0] = phy_id;
	data[1] = location;
	data[2] = value;

	if (ioctl(skfd, new_ioctl_nums ? 0x8949 : SIOCDEVPRIVATE+2, &ifr) < 0) {
		fprintf(stderr, "SIOCSMIIREG on %s failed: %s\n", ifr.ifr_name,
				strerror(errno));
	}
}

/* Parse the command line argument for advertised capabilities. */
static int parse_advertise(const char *capabilities)
{
	const char *mtypes[] = {
		"100baseT4", "100baseTx", "100baseTx-FD", "100baseTx-HD",
		"10baseT", "10baseT-FD", "10baseT-HD", 0,
	};
	char *endptr;
	int cap_map[] = { 0x0200, 0x0180, 0x0100, 0x0080, 0x0060, 0x0040, 0x0020,};
	int i;
	if ( ! capabilities) {
		fprintf(stderr, "You passed -A 'NULL'.  You must provide a media"
				" list to advertise!\n");
		return -1;
	}
	if (debug)
		fprintf(stderr, "Advertise string is '%s'.\n", capabilities);
	for (i = 0; mtypes[i]; i++)
		if (strcasecmp(mtypes[i], capabilities) == 0)
			return cap_map[i];
	if ((i = strtol(capabilities, &endptr, 16)) <= 0xffff  &&  endptr[0] == 0)
		return i;
	fprintf(stderr, "Invalid media advertisement value '%s'.\n"
			"  Either pass a numeric value or one of the following names:\n",
			capabilities);
	for (i = 0; mtypes[i]; i++)
		fprintf(stderr, "   %-14s %3.3x\n", mtypes[i], cap_map[i]);
	return -1;
}

/* Trivial versions if we don't link against libmii.c */
static const char *media_names[] = {
	"10baseT", "10baseT-FD", "100baseTx", "100baseTx-FD", "100baseT4",
	"Flow-control", 0,
};
/* Various non-good bits in the command register. */
static const char *bmcr_bits[] = {
	"  Internal Collision-Test enabled!\n", "",		/* 0x0080,0x0100 */
	"  Restarted auto-negotiation in progress!\n",
	"  Transceiver isolated from the MII!\n",
	"  Transceiver powered down!\n", "", "",
	"  Transceiver in loopback mode!\n",
	"  Transceiver currently being reset!\n",
};

int show_basic_mii(long ioaddr, int phy_id)
{
	int mii_reg, i;
	u16 mii_val[32];
	u16 bmcr, bmsr, new_bmsr, nway_advert, lkpar;

	for (mii_reg = 0; mii_reg < 8; mii_reg++)
		mii_val[mii_reg] = mdio_read(ioaddr, phy_id, mii_reg);
	if ( ! verbose) {
		printf("Basic registers of MII PHY #%d: ", phy_id);
		for (mii_reg = 0; mii_reg < 8; mii_reg++)
			printf(" %4.4x", mii_val[mii_reg]);
		printf(".\n");
	}

	if (mii_val[0] == 0xffff  ||  mii_val[1] == 0x0000) {
		printf("  No MII transceiver present!.\n");
		if (! opt_f) {
			printf("  Use '--force' to view the information anyway.\n");
			return -1;
		}
	}
	/* Descriptive rename. */
	bmcr = mii_val[0];
	bmsr = mii_val[1];
	nway_advert = mii_val[4];
	lkpar = mii_val[5];

	if (lkpar & 0x4000) {
		int negotiated = nway_advert & lkpar & 0x3e0;
		int max_capability = 0;
		/* Scan for the highest negotiated capability, highest priority
		   (100baseTx-FDX) to lowest (10baseT-HDX). */
		int media_priority[] = {8, 9, 7, 6, 5}; 	/* media_names[i-5] */
		printf(" The autonegotiated capability is %4.4x.\n", negotiated);
		for (i = 0; media_priority[i]; i++)
			if (negotiated & (1 << media_priority[i])) {
				max_capability = media_priority[i];
				break;
			}
		if (max_capability)
			printf("The autonegotiated media type is %s.\n",
				   media_names[max_capability - 5]);
		else
			printf("No common media type was autonegotiated!\n"
				   "This is extremely unusual and typically indicates a "
				   "configuration error.\n" "Perhaps the advertised "
				   "capability set was intentionally limited.\n");
	}
	printf(" Basic mode control register 0x%4.4x:", bmcr);
	if (bmcr & 0x1000)
		printf(" Auto-negotiation enabled.\n");
	else
		printf(" Auto-negotiation disabled, with\n"
			   " Speed fixed at 10%s mbps, %s-duplex.\n",
			   bmcr & 0x2000 ? "0" : "",
			   bmcr & 0x0100 ? "full":"half");
	for (i = 0; i < 9; i++)
		if (bmcr & (0x0080<<i))
			printf("%s", bmcr_bits[i]);

	new_bmsr = mdio_read(ioaddr, phy_id, 1);
	if ((bmsr & 0x0016) == 0x0004)
		printf( " You have link beat, and everything is working OK.\n");
	else
		printf(" Basic mode status register 0x%4.4x ... %4.4x.\n"
			   "   Link status: %sestablished.\n",
			   bmsr, new_bmsr,
			   bmsr & 0x0004 ? "" :
			   (new_bmsr & 0x0004) ? "previously broken, but now re" : "not ");
	if (verbose) {
		printf("   This transceiver is capable of ");
		if (bmsr & 0xF800) {
			for (i = 15; i >= 11; i--)
				if (bmsr & (1<<i))
					printf(" %s", media_names[i-11]);
		} else
			printf("<Warning! No media capabilities>");
		printf(".\n");
		printf("   %s to perform Auto-negotiation, negotiation %scomplete.\n",
			   bmsr & 0x0008 ? "Able" : "Unable",
			   bmsr & 0x0020 ? "" : "not ");
	}

	if (bmsr & 0x0010)
		printf(" Remote fault detected!\n");
	if (bmsr & 0x0002)
		printf("   *** Link Jabber! ***\n");

	if (lkpar & 0x4000) {
		printf(" Your link partner advertised %4.4x:",
			   lkpar);
		for (i = 5; i >= 0; i--)
			if (lkpar & (0x20<<i))
				printf(" %s", media_names[i]);
		printf("%s.\n", lkpar & 0x0400 ? ", w/ 802.3X flow control" : "");
	} else if (lkpar & 0x00A0)
		printf(" Your link partner is generating %s link beat  (no"
			   " autonegotiation).\n",
			   lkpar & 0x0080 ? "100baseTx" : "10baseT");
	else if ( ! (bmcr & 0x1000))
		printf(" Link partner information is not exchanged when in"
			   " fixed speed mode.\n");
	else if ( ! (new_bmsr & 0x004))
							;	/* If no partner, do not report status. */
	else if (lkpar == 0x0001  ||  lkpar == 0x0000) {
		printf(" Your link partner does not do autonegotiation, and this "
			   "transceiver type\n  does not report the sensed link "
			   "speed.\n");
	} else
		printf(" Your link partner is strange, status %4.4x.\n", lkpar);

	printf("   End of basic transceiver information.\n\n");
	return 0;
}

static void monitor_status(long ioaddr, int phy_id)
{
	unsigned int baseline_1 = 0x55555555; 	/* Always show initial status. */

	while (1) {
		unsigned int new_1 = mdio_read(ioaddr, phy_id, 1);
		if (new_1 != baseline_1) {
			printf("%-12s 0x%4.4x 0x%4.4x\n",
				   new_1 & 0x04 ? (new_1==0xffff ? "unknown" : "up") :
				   new_1 & 0x20 ? "negotiating" : "down",
				   new_1, mdio_read(ioaddr, phy_id, 5));
			fflush(stdout);
			baseline_1 = new_1;
		}
		sleep(1);
	}
}

int  show_mii_details(long ioaddr, int phy_id)
{
	int mii_reg, mii_val;
	printf(" MII PHY #%d transceiver registers:", phy_id);
	for (mii_reg = 0; mii_reg < 32; mii_reg++) {
		mii_val = mdio_read(skfd, phy_id, mii_reg);
		printf("%s %4.4x", (mii_reg % 8) == 0 ? "\n  " : "",
			   mii_val);
	}
	printf("\nThis version of 'mii-diag' has not been linked with "
			"the libmii.c library.\n"
			"  That library provides extended transceiver status reports.\n");
	return 0;
}

void monitor_mii(long ioaddr, int phy_id)
{
	fprintf(stderr, "\nThis version of 'mii-diag' has not been linked with "
			"the libmii.c library \n"
			"  required for the media monitor option.\n");
}



/*
 * Local variables:
 *  version-control: t
 *  kept-new-versions: 5
 *  c-indent-level: 4
 *  c-basic-offset: 4
 *  tab-width: 4
 *  compile-command: "gcc -Wall -Wstrict-prototypes -O mii-diag.c -DLIBMII libmii.c -o mii-diag"
 *  simple-compile-command: "gcc mii-diag.c -o mii-diag"
 * End:
 */
