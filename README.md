# LetsEncrypt-DNSPOD-update
第一次申请

    /usr/local/bin/certbot-auto certonly  -d *.oamplus.com    --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory --manual-auth-hook  ./dnspodau.sh  --email admin@oamplus.com

更新证书

    /usr/local/bin/certbot-auto renew --cert-name  oamplus.com  --manual-auth-hook  ./dnspodau.sh  --dry-run  

说明：

    不支持多个域名同时申请或者是更新

参考： https://github.com/ywdblog/certbot-letencrypt-wildcardcertificates-alydns-au 编写
