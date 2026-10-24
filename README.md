# IJTCS-FAW 2026 Official Website

This repository contains the official static website for **IJTCS-FAW 2026**, organized by the China Computer Federation and Renmin University of China in Beijing, China.

The conference will be held from **Nov 7 to 10, 2026**, at the Culture Building of Renmin University of China. Items that have not yet been announced are explicitly marked `TBA`.

## Published website

The GitHub Pages site is available at:

<https://ijtcs-faw2026.github.io/IJTCS-FAW2026/>

GitHub Pages deploys the `main` branch from the repository root. The site is dependency-free and does not require a build step.

## Search indexing

- Public pages use `index, follow` metadata and canonical URLs.
- `robots.txt` permits crawling and points to `sitemap.xml`.
- The error page remains `noindex, follow` as expected for a 404 page.

## Main files

- `index.html`: overview and important dates
- `cfp.html`: Call for Papers and track descriptions
- `posters.html`: Call for Posters, email submission, and brief organizer review
- `tutorials.html`: Call for Tutorials, proposal guidelines, and tutorial submission details
- `submission.html`: submission information and OpenReview link
- `committees.html`: conference committees and track chairs
- `program.html`: conference programme
- `keynotes.html`: keynote speakers
- `registration.html`: registration information
- `attending.html`: venue, travel, accommodation, and visa information
- `accepted-papers.html`: accepted papers
- `special-issue.html`: journal special issues
- `previous.html`: previous editions
- `support.html`: supporting organizations
- `contact.html`: conference contacts
- `assets/css/style.css`: shared site styling
- `assets/js/main.js`: mobile navigation
- `assets/img/IMAGE-CREDITS.md`: image sources and usage notes

## Maintenance

Replace `TBA` items as information becomes available, preserve the shared page shell, and verify local links before pushing changes to `main`.

The accepted-paper list and detailed programme are generated as static HTML from `assets/data/conference-2026.json`. Public paper metadata was checked against [OpenReview](https://openreview.net/group?id=IJTCS-FAW/2026/Conference), and the timetable against the [organizers' programme document](https://docs.qq.com/sheet/DZnd1ZXBHYXVVUkRL), on Oct 24, 2026. The current data contains 51 accepted papers, 16 paper sessions, and 33 events. Submission tracks and presentation sessions are independent; author order is preserved.

Run `python scripts/build-conference-pages.py` after updating the data. `--validate-only` validates data without writing pages; `--check` additionally checks generated sections. Accepted papers may be unscheduled. A withdrawn presentation slot must have `paper_number: null`: its 18-minute time remains reserved and is displayed only as `TBA`, with no withdrawn paper title. The current programme has 51 assigned papers and one such anonymous slot. The generator checks unique IDs, slot references/order, session lengths, and single-venue overlaps. GitHub Pages serves the committed HTML without a build step. Preserve the existing Posters navigation and Copyright Form URL.
