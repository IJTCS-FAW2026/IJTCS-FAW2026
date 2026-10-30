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

The accepted-paper list, detailed programme, and confirmed tutorial details are generated as static HTML from `assets/data/conference-2026.json`. Public paper metadata was checked against [OpenReview](https://openreview.net/group?id=IJTCS-FAW/2026/Conference) on Oct 24, 2026 (`papers_verified`). The current timetable still follows **direct organizer instructions dated Oct 28, 2026** (`sources.programme`). The `updated` field records the latest overall data revision, now Oct 30 for the addition of Tutorial 2 speaker, title, and abstract; it is not the timetable-authority date or a new paper-verification date. The [shared programme document](https://docs.qq.com/sheet/DZnd1ZXBHYXVVUkRL) was an early reference only, retained as `sources.earlier_programme_draft`; it must not overwrite the directly supplied Oct 28 timetable. No new OpenReview metadata check is claimed. The current data contains 51 accepted papers, 16 paper sessions, and 35 events. Submission tracks and presentation sessions are independent; author order is preserved.

Under the Oct 28 timetable, every day starts at 09:00 and each oral presentation slot lasts 16 minutes, including questions and transition. Scheduled afternoon programmes retain their 13:30 start, while subsequent session and break times follow the revised table below. The Opening Ceremony and Group Photo remain on Nov 8; the Nov 7 poster session is 60 minutes. Additional tea breaks are scheduled on Nov 8 and Nov 9, and the Nov 9 post-forum tea break precedes S11. Session IDs, titles, paper assignments, and order are unchanged. All times are Beijing time (UTC+8):

- **Nov 7:** Tutorial 1 09:00–10:30; Tea Break 10:30–10:50; S01 10:50–11:38; S02 11:38–12:10; Lunch 12:10–13:30; Tutorial 2 13:30–15:00; Tea Break & Poster Session 15:00–16:00; S03 16:00–16:48; S04 16:48–17:36.
- **Nov 8:** Opening 09:00–09:05; Keynote 1 09:05–10:05; Tea Break & Group Photo 10:05–10:25; S05 10:25–11:13; S06 11:13–12:17; Lunch 12:17–13:30; Keynote 2 13:30–14:30; Tea Break 14:30–14:50; S07 14:50–15:54; Tea Break 15:54–16:14; S08 16:14–17:18.
- **Nov 9:** Keynote 3 09:00–10:00; Tea Break 10:00–10:20; S09 10:20–11:08; S10 11:08–12:12; Lunch 12:12–13:30; Women in TCS Forum 13:30–14:30; Tea Break 14:30–14:50; S11 14:50–15:38; S12 15:38–16:10; Tea Break 16:10–16:30; S13 16:30–17:18.
- **Nov 10:** S14 09:00–10:04; S15 10:04–10:52; Tea Break 10:52–11:12; S16 11:12–12:00.

The Oct 25 move of paper #34 from the Nov 9 **Statistical Learning and Causal Inference** session to the first presentation in the Nov 8 **Foundations and Systems of Artificial Intelligence** session remains in effect. The latter is S08 and now runs 16:14–17:18 with #34, #11, #35, and #103; #34 is presented at 16:14–16:30. Paper order within every session is preserved. Earlier timetable descriptions are superseded by the directly supplied Oct 28 [conference programme](program.html).

Run `python scripts/build-conference-pages.py` after updating the data. `--validate-only` validates data without writing pages; `--check` additionally checks generated sections. Accepted papers may be unscheduled. The current programme has 51 assigned papers in 51 presentation slots. By organizer instruction on Oct 24, the withdrawn paper #39 slot was removed and remains absent; no empty slot is retained. S04, **Fair Allocation of Goods and Chores**, takes place on Nov 7 at 16:48–17:36, with #50 at 17:04–17:20 and #64 at 17:20–17:36. To close a future withdrawn slot, remove it from the data, renumber subsequent slots, and adjust the session end and following event start. If a slot is explicitly retained with status `withdrawn`, it must have `paper_number: null` and renders only `TBA`, never a withdrawn paper title. The generator checks unique IDs, slot references/order, session lengths, and single-venue overlaps. GitHub Pages serves the committed HTML without a build step. Preserve the existing Posters navigation and Copyright Form URL.

Run `python scripts/build-programme-pdf.py` with ReportLab installed to rebuild the English printable programme at `output/pdf/IJTCS-FAW-2026-Programme.pdf`. It uses the same validated data, with one A4 landscape page per day, all paper titles and authors, and Beijing time throughout. Rebuild both HTML and PDF after any timetable or paper-metadata change, then render and inspect all four PDF pages before publication.

## Confirmed Tutorial 2

The organizers confirmed the following speaker, title, and full abstract on Oct 30, 2026. These details are stored in `talk_details["Tutorial 2"]` and rendered into the `BEGIN GENERATED TUTORIALS` / `END GENERATED TUTORIALS` block on [the tutorials page](tutorials.html#tutorial-2). The title and speaker are also shown in the programme and English programme PDF, with a link from the programme to the full abstract. The Oct 28 timetable is unchanged. Tutorial 1 and keynote speakers and titles remain TBA; no affiliation, biography, or photograph has been supplied or inferred.

- **Speaker:** Wei Tang
- **Title:** Decision-Aware Predictor Optimization
- **Time:** Nov 7, 2026, 13:30–15:00 Beijing time (UTC+8)

**Abstract**

Predictions increasingly drive operational decisions, while advances in AI, particularly large language models (LLMs), offer an expanding set of predictors. However, the best predictor depends on how its predictions are used. How should we select or combine predictors when their downstream use is only partially known?

This tutorial introduces a decision-theoretic framework for predictor selection and aggregation. We begin with the foundations of predictor comparison and the roles of predictive information and calibration in downstream decisions. We then examine how to select or aggregate multiple predictors to perform well across a family of possible tasks, measuring decision quality relative to the best task-specific predictor. We discuss structural insights and algorithmic approaches for calibrated predictors, the challenges posed by miscalibration, and applications to heterogeneous LLM-based forecasts. The tutorial concludes with open research directions in optimizing predictors for the decisions they support.
