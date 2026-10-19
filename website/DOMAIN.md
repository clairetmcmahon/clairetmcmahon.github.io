# Domain setup: clairetmcmahon.com

Hosting: GitHub Pages (free for this public repository).
Registrar: Squarespace (domain registration/renewal only; a Squarespace website subscription is unnecessary).

1. In the repository’s Settings → Pages, preserve deployment from `master` and `/ (root)`. Set the custom domain to `clairetmcmahon.com`. With branch publishing, this creates a root `CNAME` file containing that hostname.
2. In Squarespace Domains → clairetmcmahon.com → DNS, replace conflicting default website records at `@` and `www` with the records below. Preserve unrelated TXT, MX, and email records.

| Host | Type | Value |
| --- | --- | --- |
| @ | A | 185.199.108.153 |
| @ | A | 185.199.109.153 |
| @ | A | 185.199.110.153 |
| @ | A | 185.199.111.153 |
| www | CNAME | clairetmcmahon.github.io |

Use the DNS provider’s default TTL. Remove conflicting apex AAAA records if any exist; GitHub also documents optional IPv6 addresses.

3. Set `origin` in `website/content.json` to `https://clairetmcmahon.com`, rebuild, check, commit, and push. If GitHub generated the CNAME commit, synchronize it before pushing.
4. Wait for DNS and GitHub’s HTTPS certificate. Enable **Enforce HTTPS** in Pages settings once available.
5. Verify the homepage, `/research/`, `/blog/`, `/tools/`, `/cv/`, and `/files/McMahon_CV.pdf`. Check that `www.clairetmcmahon.com` redirects to the apex domain. GitHub also redirects the old github.io site once its custom domain is configured.

DNS propagation and certificate availability can take up to 24 hours.

Source: [GitHub’s custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), checked October 19, 2026.
