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

The accepted-paper list and detailed programme are generated as static HTML from `assets/data/conference-2026.json`. Public paper metadata was checked against [OpenReview](https://openreview.net/group?id=IJTCS-FAW/2026/Conference) on Oct 24, 2026 (`papers_verified`). The timetable was initially checked against the [organizers' programme document](https://docs.qq.com/sheet/DZnd1ZXBHYXVVUkRL) on Oct 24 and most recently amended by organizer instruction on Oct 27 (`updated`). A timetable amendment does not imply a new OpenReview metadata check. The current data contains 51 accepted papers, 16 paper sessions, and 33 events. Submission tracks and presentation sessions are independent; author order is preserved.

The Oct 27 organizer timetable amendment changes the placement of the keynote/tutorial blocks and exchanges the Nov 7 positions of the **Fair Allocation of Goods and Chores** and **Auctions and Bilateral Trade** sessions. The opening ceremony is shortened to five minutes and the Nov 7 poster session to 45 minutes. All scheduled afternoon programmes retain their 13:30 start. Nov 7 lunch absorbs the morning timing difference, running 11:55–13:30 for 95 minutes; all remaining event durations are preserved, with subsequent events shifted continuously. Paper sessions, keynotes, and tutorials were subsequently renumbered in chronological order across the four days; this numbering-only update changes no times, titles, content, or paper order. Current numbering and affected-day timings (Beijing time, UTC+8) are:

- **Nov 7:** Opening 08:30–08:35; Tutorial 1 08:35–10:05; Tea Break & Group Photo 10:05–10:25; S01 10:25–11:19; S02 11:19–11:55; Lunch 11:55–13:30; Tutorial 2 13:30–15:00; Tea Break & Poster Session 15:00–15:45; S03 15:45–16:39; S04 16:39–17:33.
- **Nov 8:** The morning times and lunch are unchanged; Keynote 2 13:30–14:30; Tea Break 14:30–14:50; S07 14:50–16:02; S08 16:02–17:14.

The Oct 25 move of paper #34 from the Nov 9 **Statistical Learning and Causal Inference** session to the first presentation in the Nov 8 **Foundations and Systems of Artificial Intelligence** session remains in effect. The latter is now S08 and runs 16:02–17:14 with #34, #11, #35, and #103; #34 is presented at 16:02–16:20. Nov 9 and Nov 10 times are unchanged by the Oct 27 amendment: under the current numbering, Nov 9 S11 contains #59, #78, and #58 at 14:30–15:24, followed by the tea break at 15:24–15:44, S12 at 15:44–16:20, and S13 at 16:20–17:14. Paper order within every session is preserved. Earlier timetable descriptions are superseded by the current [conference programme](program.html).

Run `python scripts/build-conference-pages.py` after updating the data. `--validate-only` validates data without writing pages; `--check` additionally checks generated sections. Accepted papers may be unscheduled. The current programme has 51 assigned papers in 51 presentation slots. By organizer instruction on Oct 24, the withdrawn paper #39 slot was removed and remains absent; no empty slot is retained. S04, **Fair Allocation of Goods and Chores**, takes place on Nov 7 at 16:39–17:33, with #50 at 16:57–17:15 and #64 at 17:15–17:33. To close a future withdrawn slot, remove it from the data, renumber subsequent slots, and adjust the session end and following event start. If a slot is explicitly retained with status `withdrawn`, it must have `paper_number: null` and renders only `TBA`, never a withdrawn paper title. The generator checks unique IDs, slot references/order, session lengths, and single-venue overlaps. GitHub Pages serves the committed HTML without a build step. Preserve the existing Posters navigation and Copyright Form URL.

Run `python scripts/build-programme-pdf.py` with ReportLab installed to rebuild the English printable programme at `output/pdf/IJTCS-FAW-2026-Programme.pdf`. It uses the same validated data, with one A4 landscape page per day, all paper titles and authors, and Beijing time throughout. Rebuild both HTML and PDF after any timetable or paper-metadata change, then render and inspect all four PDF pages before publication.
