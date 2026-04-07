#
# Exim ACL for greylisting. David Woodhouse <dwmw2@infradead.org>
#
# For full background on the logic behind greylisting and how this
# ACL works, see https://github.com/Exim/exim/wiki/SimpleGreylisting
#

# UPDATING TO EXIM 4.94+
# ======================
#
# Previous versions of this ACL specified the sqlite database filename 
# in the sqlite lookup strings directly, but since Exim 4.94 is it no 
# longer permitted to mix "tainted" text which comes from the message 
# itself, with the filename. Thus, you now have to set
#
# sqlite_dbfile = /var/spool/exim/db/greylist.db
#
# ... in the main configuration because it can't be specified within
# the ACL in this file any more.

# USING THIS ACL
# ==============
#
# First set sqlite_dbfile in the main configuration file to point to
# the greylist sqlite database, as described above.
#
# In your main ACLs, gather reason(s) for greylisting into a variable 
# named $acl_m_greylistreasons before invoking this ACL with
# 'require acl = greylist_mail'. The reasons should be separate lines
# of text, and will be reported in the SMTP rejection message as well
# as the log message. Anything "suspicious" about the email can be
# used as criteria here — being HTML, having even a few SpamAssassin
# points, even lacking SPF authorisation (which is OK for greylisting
# although you should never reject outright for an SPF "failure"
# because of the flaws in SPF).
#
# Obviously you need to .include this file too in order to be able
# to invoke this greylist_mail ACL.

# HOW IT WORKS
# ============
#
# When a suspicious mail is seen, we temporarily reject it and wait to see
# if the sender tries again. Most spam robots won't bother. Real mail hosts
# _will_ retry, and we'll accept it the second time. For hosts which are
# observed to retry, we don't bother greylisting again in the future --
# it's obviously pointless. We remember such hosts, or 'known resenders',
# by a tuple of their IP address and the name they used in HELO.
#
# We also include the time of listing for 'known resenders', just in case
# someone wants to expire them after a certain amount of time. So the 
# database table for these 'known resenders' looks like this:
#
# CREATE TABLE resenders (
#        host            TEXT,
#        helo            TEXT,
#        time            INTEGER,
#    PRIMARY KEY (host, helo) );
#
# To remember mail we've rejected, we create an 'identity' from its sender
# and recipient addresses and its Message-ID: header. We don't include the
# sending IP address in the identity, because sometimes the second and 
# subsequent attempts may come from a different IP address to the original.
#
# We do record the original IP address and HELO name though, because if
# the message _is_ retried from another machine, it's the _first_ one we
# want to record as a 'known resender'; not just its backup path.
#
# Obviously we record the time too, so the main table of greylisted mail
# looks like this:
#
# CREATE TABLE greylist (
#        id              TEXT,
#        expire          INTEGER,
#        host            TEXT,
#        helo            TEXT);
#

greylist_mail:
  # Firstly,  accept if it was generated locally or by authenticated clients.
  accept hosts = :
  accept authenticated = *

  # Secondly, there's _absolutely_ no point in greylisting mail from
  # hosts which are known to resend their mail. Just accept it.
  accept condition = ${lookup sqlite {SELECT host from resenders \
			       WHERE helo='${quote_sqlite:$sender_helo_name}' \
			       AND host='$sender_host_address';} {1}}

  # Generate a hashed 'identity' for the mail, as described above.
  warn set acl_m_greyident = ${hash{20}{62}{$sender_address$recipients$h_message-id:}}

  # Attempt to look up this mail in the greylist database. If it's there,
  # remember the expiry time for it; we need to make sure they've waited
  # long enough.
  warn set acl_m_greyexpiry = ${lookup sqlite {SELECT expire FROM greylist \
				WHERE id='${quote_sqlite:$acl_m_greyident}';}{$value}}


  # If there's absolutely nothing suspicious about the email, accept it. BUT...
  accept condition = ${if eq {$acl_m_greylistreasons}{} {1}}
         condition = ${if eq {$acl_m_greyexpiry}{} {1}}

  # ..if this same mail was greylisted before (perhaps because it came from a
  # host which *was* suspicious), then we still want to mark that original host
  # as a "known resender". If we don't, then hosts which attempt to deliver from
  # a dodgy Legacy IP address but then fall back to using IPv6 after greylisting
  # will *never* see their Legacy IP address added to the 'known resenders' list.
  accept condition = ${if eq {$acl_m_greylistreasons}{} {1}}
         acl = write_known_resenders

  # If the mail isn't already the database -- i.e. if the $acl_m_greyexpiry
  # variable we just looked up is empty -- then try to add it now. This is 
  # where the 5 minute timeout is set ($tod_epoch + 300), should you wish
  # to change it.
  warn  condition = ${if eq {$acl_m_greyexpiry}{} {1}}
	set acl_m_dontcare = ${lookup sqlite {INSERT INTO greylist \
					VALUES ( '${quote_sqlite:$acl_m_greyident}', \
						 '${eval10:$tod_epoch+300}', \
						 '$sender_host_address', \
						 '${quote_sqlite:$sender_helo_name}' );}}

  # Be paranoid, and check if the insertion succeeded (by doing another lookup).
  # Otherwise, if there's a database error we might end up deferring for ever.
  defer condition = ${if eq {$acl_m_greyexpiry}{} {1}}
        condition = ${lookup sqlite {SELECT expire FROM greylist \
				WHERE id='${quote_sqlite:$acl_m_greyident}';} {1}}
        message = Your mail was considered suspicious for the following reason(s):\n$acl_m_greylistreasons \
		  The mail has been greylisted for 5 minutes, after which it should be accepted. \
		  We apologise for the inconvenience. Your mail system should keep the mail on \
		  its queue and retry. When that happens, your system will be added to the list \
		  genuine mail systems, and mail from it should not be greylisted any more. \
		  In the event of problems, please contact postmaster@$qualify_domain
	log_message = Greylisted <$h_message-id:> from <$sender_address> for offences: ${sg {$acl_m_greylistreasons}{\n}{,}}

  # Handle the error case (which should never happen, but would be bad if it did).
  # First by whining about it in the logs, so the admin can deal with it...
  warn   condition = ${if eq {$acl_m_greyexpiry}{} {1}}
         log_message = Greylist insertion failed. Bypassing greylist.
  # ... and then by just accepting the message.
  accept condition = ${if eq {$acl_m_greyexpiry}{} {1}}

  # OK, we've dealt with the "new" messages. Now we deal with messages which
  # _were_ already in the database...

  # If the message was already listed but its time hasn't yet expired, keep rejecting it
  defer condition = ${if > {$acl_m_greyexpiry}{$tod_epoch}}
	message = Your mail was previously greylisted and the time has not yet expired.\n\
		  You should wait another ${eval10:$acl_m_greyexpiry-$tod_epoch} seconds.\n\
		  Reason(s) for greylisting: \n$acl_m_greylistreasons

  accept acl = write_known_resenders

write_known_resenders:
  # The message was listed but it's been more than five minutes. Accept it now and whitelist
  # the _original_ sending host by its { IP, HELO } so that we don't delay its mail again.
  warn set acl_m_orighost = ${lookup sqlite {SELECT host FROM greylist \
				WHERE id='${quote_sqlite:$acl_m_greyident}';}{$value}}
       set acl_m_orighelo = ${lookup sqlite {SELECT helo FROM greylist \
				WHERE id='${quote_sqlite:$acl_m_greyident}';}{$value}}
       set acl_m_dontcare = ${lookup sqlite {INSERT INTO resenders \
				VALUES ( '$acl_m_orighost', \
					 '${quote_sqlite:$acl_m_orighelo}', \
					 '$tod_epoch' ); }}
       logwrite = Added host $acl_m_orighost with HELO '$acl_m_orighelo' to known resenders

  accept
