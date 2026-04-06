#!/bin/sh
if [ -f /etc/redis/redis.conf ]; then
  cp /etc/redis/redis.conf /etc/valkey/valkey.conf
  mv /etc/redis/redis.conf /etc/redis/redis.conf.rpmsave
  chown valkey:root /etc/valkey/valkey.conf
  sed -i 's|^dir\s.*|dir /var/lib/valkey|g' /etc/valkey/valkey.conf
  sed -i 's|logfile /var/log/redis/redis.log|logfile /var/log/valkey/valkey.log|' /etc/valkey/valkey.conf
  echo "/etc/redis/redis.conf has been copied to /etc/valkey/valkey.conf.  Manual review of valkey.conf is strongly suggested especially if you had modified redis.conf."
fi
if [ -f /etc/redis/sentinel.conf ]; then
  cp /etc/redis/sentinel.conf /etc/valkey/sentinel.conf
  mv /etc/redis/sentinel.conf /etc/redis/sentinel.conf.rpmsave
  chown valkey:root /etc/valkey/sentinel.conf
  sed -i 's|logfile /var/log/redis/sentinel.log|logfile /var/log/valkey/sentinel.log|' /etc/valkey/sentinel.conf
  echo "/etc/redis/sentinel.conf has been copied to /etc/valkey/sentinel.conf.  Manual review of sentinel.conf is strongly suggested especially if you had modified sentinel.conf."
fi
if [ -d /var/lib/redis ]; then
  # cp could take a while, and this is a one-way move anyway
  mv /var/lib/redis/* /var/lib/valkey/
  # don't leave garbage behind, plus we check if this dir exists when running this script
  rm -rf /var/lib/redis
  chown -R valkey. /var/lib/valkey
  echo "On-disk redis dumps moved from /var/lib/redis/ to /var/lib/valkey"
fi
