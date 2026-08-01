# IJTCS-FAW 2026 Website Draft

This repository is a static GitHub Pages draft for **IJTCS-FAW 2026**, hosted by Renmin University of China, Beijing, China.

## Current status

This is a draft. The website intentionally contains `TBA` placeholders and a visible draft banner.

Do not treat the following items as confirmed until the organizers approve them:

- conference dates;
- exact venue;
- committee names and affiliations;
- submission system and paper-format requirements;
- proceedings and special-issue arrangements;
- registration fees and payment channel;
- keynote speakers;
- contact email;
- sponsor/supporting-organization logos.

## Recommended GitHub Pages deployment

### Option A: project site under the IJTCS-FAW GitHub organization

1. Create a repository named `2026` under the `ijtcs-faw` organization.
2. Upload all files in this folder to the repository root.
3. In GitHub, open `Settings` -> `Pages`.
4. Select `Deploy from a branch`.
5. Select branch `main` and folder `/root`.
6. The site should be served as `https://ijtcs-faw.github.io/2026/`.

### Option B: temporary project site under a personal or lab account

1. Create a repository, for example `ijtcs-faw-2026`.
2. Upload all files to the repository root.
3. Enable GitHub Pages from branch `main`, folder `/root`.
4. The temporary address will be similar to `https://USERNAME.github.io/ijtcs-faw-2026/`.

## Before formal launch

1. Replace all `TBA` placeholders.
2. Remove or edit the draft banner in each HTML file.
3. Remove the noindex metadata from each HTML file:

```html
<meta name="robots" content="noindex, nofollow">
```

4. Replace `robots.txt` with:

```txt
User-agent: *
Allow: /
```

5. Add official logos only after permission is confirmed.
6. Check all links manually.

## File map

- `index.html`: homepage / overview
- `cfp.html`: Call for Papers
- `submission.html`: submission information
- `committees.html`: committees
- `program.html`: conference program placeholder
- `keynotes.html`: keynote speaker placeholder
- `registration.html`: registration placeholder
- `attending.html`: venue, travel, accommodation, visa
- `accepted-papers.html`: accepted papers placeholder
- `previous.html`: previous editions
- `contact.html`: contact information
- `assets/css/style.css`: website styling
- `assets/js/main.js`: mobile navigation script
- `assets/img/ruc-lide.jpg`: Lide Building photograph used in the shared page banner and on the homepage
- `assets/img/IMAGE-CREDITS.md`: image sources, authors, licenses, and modification notes
- `assets/img/hero-campus.svg`: original abstract campus illustration retained as a fallback asset
- `.nojekyll`: disables Jekyll processing on GitHub Pages
- `robots.txt`: currently disallows indexing because this is a draft

## Maintenance note

This is a dependency-free static website. Editing can be done directly in GitHub or locally with any text editor. No build step is required.

Draft generated on 2026-05-29.
