// Default download directory.
pref("browser.download.dir", "/config/downloads");
pref("browser.download.folderList", 2);
// Disable the privacy notice page.
pref("toolkit.telemetry.reportingpolicy.firstRun", false);
// Disable some warning messages.
pref("security.sandbox.warn_unprivileged_namespaces", false);
// Prevent closing Firefox when closing the last tab.
pref("browser.tabs.closeWindowWithLastTab", false);
// Disable confirmation before quitting with Ctrl+Q.  Needed to allow Firefox
// to quit cleanly when container is shutted down.
pref("browser.warnOnQuitShortcut", false);


// i2p Proxy Configuration
pref("network.proxy.type", 1); // Manual proxy configuration

// HTTP Proxy (for .i2p sites)
pref("network.proxy.http", "127.0.0.1");
pref("network.proxy.http_port", 4444);

// HTTPS Proxy  
pref("network.proxy.ssl", "127.0.0.1");
pref("network.proxy.ssl_port", 4444);

// SOCKS Proxy (backup)
pref("network.proxy.socks", "127.0.0.1");
pref("network.proxy.socks_port", 4447);
pref("network.proxy.socks_version", 5);

// Share proxy settings for all protocols
pref("network.proxy.share_proxy_settings", true);

// No proxy for local addresses
pref("network.proxy.no_proxies_on", "localhost, 127.0.0.1");

// DNS over SOCKS (important for .i2p domains)
pref("network.proxy.socks_remote_dns", true);

// Disable DNS prefetching to prevent leaks
pref("network.dns.disablePrefetch", true);

// Disable speculative connections
pref("network.http.speculative-parallel-limit", 0);

// Disable WebRTC to prevent IP leaks
pref("media.peerconnection.enabled", false);

// Disable geolocation
pref("geo.enabled", false);

// Disable safe browsing (can leak data)
pref("browser.safebrowsing.enabled", false);
pref("browser.safebrowsing.malware.enabled", false);
pref("browser.safebrowsing.phishing.enabled", false);


pref("browser.aboutwelcome.enabled", false);
pref("startup.homepage_welcome_url", "");
pref("startup.homepage_welcome_url.additional", "");

// Disable import bookmarks/login prompt
pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);
pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false);
pref("browser.newtabpage.activity-stream.asrouter.userprefs.onboarding", false);

// Ensure homepage loads on first launch
pref("browser.startup.page", 1); // 1 = homepage

// Set homepage to i2p status
pref("browser.startup.homepage", "http://7tbay5p4kzeekxvyvbf6v7eauazemsnnl2aoyqhg5jzpr5eke7tq.b32.i2p/home.html");

// Disable automatic updates
pref("app.update.enabled", false);

// Disable extension updates
pref("extensions.update.enabled", false);

// Disable search suggestions
pref("browser.search.suggest.enabled", false);
pref("browser.urlbar.suggest.searches", false);

// Increase connection timeout for slow i2p
pref("network.http.connection-timeout", 120);
pref("network.http.response.timeout", 120);

// Allow unsigned extensions (useful for i2p extensions)
pref("xpinstall.signatures.required", false);
pref("browser.fixup.domainsuffixwhitelist.i2p", true);
