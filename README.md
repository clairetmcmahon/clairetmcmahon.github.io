# Claire McMahon’s academic website

A responsive static website hosted free on GitHub Pages. No Squarespace website plan, JavaScript framework, analytics service, or paid hosting is needed. The domain remains registered with Squarespace.

## Update content

- Research and blog entries: `website/content.json`
- Bio, navigation, tools, and shared page layout: `website/build.py`
- Appearance: `assets/site/style.css`
- CV: replace `files/McMahon_CV.pdf` at the same path
- Portrait: `images/headshot.png`

After editing, run from this repository:

```sh
python3 website/build.py
python3 website/check.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Preview at http://127.0.0.1:8765. Commit both the source and generated HTML, then push `master`. GitHub Pages publishes from `master`, `/ (root)`. `.nojekyll` tells GitHub to serve these generated files directly. No build dependencies are required.

The earlier AcademicPages/Jekyll sources remain in the repository for reference and recovery; they are no longer used to build the public site. Edit `website/` for the current site. The original AcademicPages license remains in `LICENSE`.

## Custom domain

The final domain is `clairetmcmahon.com`. See `website/DOMAIN.md` for the DNS values, migration order, and verification steps. Set `origin` in `website/content.json` to the final HTTPS origin and rebuild when connecting the domain so canonical links and the sitemap agree.

Paper titles link directly to their publisher, NBER, or SSRN landing page. Do not prepend the site origin or a local path to an external URL. Local publication and blog aliases redirect to the original work, and `/research/`, `/blog/`, `/cv/`, and the existing CV URL remain available.
