# Install
1. Put *collectd_saltmaster.py* into your `/usr/local/bin/`
2. Put *read_salt-master.conf* into your collectd configs folder (`/etc/collectd.d/`) and make sure it gets included from `/etc/collectd.conf`.
3. Restart collectd

# Requirements
- Saltstack master running
- Collectd run as root (otherwise we'd need to use any way of external_auth to be able to run salt runners... thats nasty!)
- colletd Python plugin (usually not a problem because this comes with every collectd for years)

# Metrics
Currently only
- number of currently **online** minions
- number of currently **offline** minions

are reported.

# Troubleshooting

To test the plugin:
```
/usr/sbin/collectd -C /etc/collectd.conf -T
```

To run collectd in foreground to see if any warnings are reported:
```
/usr/sbin/collectd -C /etc/collectd.conf -f
```

