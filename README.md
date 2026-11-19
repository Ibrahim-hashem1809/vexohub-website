# VEXO Hub Official Website

Pure HTML5, CSS3 and vanilla JavaScript website for `https://vexohub.app`.

## Pages

- `index.html` — homepage
- `features.html` — product features
- `about.html` — mission, vision and values
- `faq.html` — accessible interactive FAQ
- `contact.html` — support, privacy and release access
- `privacy.html` — Privacy Policy
- `terms.html` — Terms of Service
- `404.html` — GitHub Pages error page

## Structure

### Hekaya Tanya — Arabic fiction

- `stories/index.html` — standalone RTL library at `/stories/`
- `stories/the-last-page/index.html` — complete first story and reader
- `stories/assets/` — isolated styles, script, brand and story illustration
- `stories/stories.json` — source text for the first story

The section uses static HTML and relative assets, so the existing GitHub Pages
root deployment serves it without DNS changes or a build step. Reading works
without JavaScript; JavaScript adds title/category search, browser-local
bookmarks, font size, day/night reading, progress and sharing. No account,
database or additional analytics service is used in the stories section.
Saved stories and reader preferences stay in the current browser.

The two public identities have independent navigation and branding. No public
page links from the main site to stories or from stories to the main site.
Stories have their own sitemap and error page; unknown story paths are sent
to that error page by the shared GitHub Pages fallback when JavaScript is enabled.
The shared domain remains visible in browser addresses and canonical URLs.

To add another story, create a new directory with an `index.html`, add a
library card and update `sitemap.xml`. The JSON is an editing source, not a
live content management system; editing JSON alone does not update the HTML.

- `css/style.css` — all website styling
- `js/script.js` — mobile navigation, FAQ behavior and current year
- `images/` — real VEXO Hub application captures
- `robots.txt` and `sitemap.xml` — search-engine discovery
- `CNAME` — GitHub Pages custom domain (`vexohub.app`)
- `.nojekyll` — direct static-file publishing

## Preview

Serve the folder through any static HTTP server. Opening the files directly also works, but an HTTP server more closely matches GitHub Pages behavior.

## GitHub Pages

Publish the repository root from the `main` branch, or deploy the folder through a Pages workflow. No build command is required.

Before public launch:

1. Confirm that all `@vexohub.app` mailboxes are active.
2. Have qualified counsel approve `privacy.html` and `terms.html` for the operating entity and launch regions.
3. Replace the private-testing download route only after a production-signed application is available from an approved channel.
4. Configure the `vexohub.app` custom domain and HTTPS in GitHub Pages.
