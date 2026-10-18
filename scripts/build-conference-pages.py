"""Render the static paper list and programme; --check verifies without writing.

Only marked sections of the two pages are generated; the shared shell stays editable.
"""

import argparse
from collections import Counter
from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def minutes(value):
    hour, minute = map(int, value.split(":"))
    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise ValueError(f"Invalid time: {value}")
    return hour * 60 + minute


def clock(value):
    return f"{value // 60:02d}:{value % 60:02d}"


def title_markup(value):
    # These are the only inline mathematical expressions in the supplied titles.
    value = escape(value)
    for source, markup in {
        "$k$": "<var>k</var>",
        "$b$": "<var>b</var>",
        "$l_p$": "<var>l</var><sub>p</sub>",
        r"\(k\)": "<var>k</var>",
    }.items():
        value = value.replace(source, markup)
    return value


def load_data():
    data = json.loads((ROOT / "assets/data/conference-2026.json").read_text(encoding="utf-8"))
    papers = [dict(zip(data["paper_fields"], p, strict=True)) for p in data["papers"]]
    sessions = {s[0]: dict(zip(data["session_fields"], s, strict=True)) for s in data["sessions"]}
    events = [dict(zip(data["programme_fields"], e, strict=True)) for e in data["programme"]]
    if len({p["number"] for p in papers}) != len(papers):
        raise ValueError("Duplicate paper numbers")
    if len({p["forum_id"] for p in papers}) != len(papers):
        raise ValueError("Duplicate OpenReview forum IDs")
    if len(sessions) != len(data["sessions"]):
        raise ValueError("Duplicate session IDs")
    for p in papers:
        if p["track"] not in data["tracks"] or p["session"] not in sessions:
            raise ValueError(f"Unknown track or session for paper {p['number']}")
        if not re.fullmatch(r"[A-Za-z0-9]+", p["forum_id"]):
            raise ValueError(f"Invalid forum ID for paper {p['number']}")
    session_events = [e for e in events if e["type"] == "Session"]
    if Counter(e["session"] for e in session_events) != Counter({s: 1 for s in sessions}):
        raise ValueError("Every session must appear exactly once in the programme")
    for e in session_events:
        group = sorted((p for p in papers if p["session"] == e["session"]), key=lambda p: p["order"])
        if not group or [p["order"] for p in group] != list(range(1, len(group) + 1)):
            raise ValueError(f"Incomplete or duplicate paper order in {e['session']}")
        if minutes(e["end"]) - minutes(e["start"]) != len(group) * data["talk_minutes"]:
            raise ValueError(f"Paper slots do not fill session {e['session']}")
        if e["title"] != sessions[e["session"]]["title"]:
            raise ValueError(f"Session title mismatch: {e['session']}")
    for i, e in enumerate(events):
        if not date(2026, 11, 7) <= date.fromisoformat(e["date"]) <= date(2026, 11, 10):
            raise ValueError("Event outside conference dates")
        if minutes(e["start"]) >= minutes(e["end"]):
            raise ValueError(f"Non-positive event duration: {e}")
        if i and (events[i - 1]["date"], events[i - 1]["end"]) > (e["date"], e["start"]):
            raise ValueError(f"Overlapping or unsorted event: {e}")
    return data, papers, sessions, events


def accepted_html(data, papers, sessions):
    counts = Counter(p["track"] for p in papers)
    out = [
        '<p>Listed by track and alphabetically by title. Author names retain their submitted order. Paper numbers are the OpenReview submission numbers.</p>',
        '<nav class="conference-jump-links" aria-label="Accepted paper tracks">',
    ]
    for code in data["tracks"]:
        out.append(f'  <a href="#track-{code}">Track {code} &middot; {counts[code]} papers</a>')
    out += ['</nav>', '<p><a href="program.html">View the conference programme and presentation times</a> &middot; <a href="submission.html#camera-ready">Camera-ready instructions</a></p>']
    for code, name in data["tracks"].items():
        out += [f'<section aria-labelledby="track-{code}">', f'<h2 id="track-{code}">Track {code}: {escape(name)}</h2>', '<ol class="accepted-paper-list">']
        for p in sorted((p for p in papers if p["track"] == code), key=lambda p: p["title"].casefold()):
            sid = p["session"]
            out += [
                f'  <li class="accepted-paper" id="paper-{p["number"]}">',
                f'    <h3 class="paper-heading"><span class="paper-number">#{p["number"]}</span> <a href="https://openreview.net/forum?id={p["forum_id"]}">{title_markup(p["title"])}</a></h3>',
                f'    <p class="paper-authors">{escape(p["authors"])}</p>',
                f'    <p class="paper-meta">Oral presentation &middot; <a href="program.html#session-{sid}">{sid}: {escape(sessions[sid]["title"])}</a></p>',
                '  </li>',
            ]
        out += ['</ol>', '</section>']
    out += ['<h2>Proceedings</h2>', '<p>Proceedings publication details: <span class="placeholder">TBA</span>. Please follow the <a href="submission.html#camera-ready">camera-ready instructions</a> for final files and the Copyright Form.</p>']
    return "\n".join(out)


def programme_html(data, papers, sessions, events):
    out = [
        f'<p>All times are <strong>{escape(data["timezone"])}</strong>. Paper presentations are in a single venue; each {data["talk_minutes"]}-minute slot includes the talk, questions, and transition.</p>',
        '<p>Session chairs and presenting authors: <span class="placeholder">TBA</span>. Keynote and tutorial speakers and talk titles: <span class="placeholder">TBA</span>. Further forum and poster details: <span class="placeholder">TBA</span>.</p>',
        f'<div class="conference-summary"><span>{len(papers)} papers</span><span>{len(sessions)} paper sessions</span><span>3 keynotes</span><span>2 tutorials</span></div>',
        '<nav class="conference-jump-links" aria-label="Programme days">',
    ]
    dates = sorted({e["date"] for e in events})
    for value in dates:
        day = date.fromisoformat(value)
        out.append(f'  <a href="#nov-{day.day}">Nov {day.day} &middot; {day:%a}</a>')
    out += ['</nav>', '<p><a href="accepted-papers.html">Browse all accepted papers by track</a></p>']
    for value in dates:
        day = date.fromisoformat(value)
        out += [
            f'<section class="programme-day" aria-labelledby="nov-{day.day}">',
            f'<h2 id="nov-{day.day}">Nov {day.day}, 2026 &middot; {day:%A}</h2>',
            '<table class="simple-table programme-table">',
            f'  <caption>Nov {day.day} schedule &middot; {escape(data["timezone"])}</caption>',
            '  <thead><tr><th scope="col">Time</th><th scope="col">Activity</th><th scope="col">Details</th></tr></thead>',
            '  <tbody>',
        ]
        for e in (e for e in events if e["date"] == value):
            sid = e["session"]
            ident = f' id="session-{sid}"' if sid else ''
            title = 'Schedule Buffer' if e["type"] == 'Buffer' else escape(e["title"])
            out += [
                f'    <tr{ident}>',
                f'      <th class="programme-time" scope="row"><time datetime="{value}T{e["start"]}:00+08:00">{e["start"]}</time>&ndash;<time datetime="{value}T{e["end"]}:00+08:00">{e["end"]}</time></th>',
                f'      <td class="programme-session"><span class="programme-type">{sid or escape(e["type"])}</span>{title}</td>',
                '      <td>',
            ]
            if sid:
                group = sorted((p for p in papers if p["session"] == sid), key=lambda p: p["order"])
                out += [f'        <details class="programme-details"><summary>{len(group)} paper presentations &middot; View titles and authors</summary>', '          <ol class="programme-paper-list">']
                for p in group:
                    start = minutes(e["start"]) + (p["order"] - 1) * data["talk_minutes"]
                    end = start + data["talk_minutes"]
                    out += [
                        '            <li>',
                        f'              <span class="paper-time">{clock(start)}&ndash;{clock(end)}</span> <a href="accepted-papers.html#paper-{p["number"]}">#{p["number"]} &middot; {title_markup(p["title"])}</a>',
                        f'              <p class="paper-authors">{escape(p["authors"])}</p>',
                        '            </li>',
                    ]
                out += ['          </ol>', '        </details>']
            elif e["type"] in ('Keynote', 'Tutorial'):
                target = 'keynotes.html' if e["type"] == 'Keynote' else 'tutorials.html'
                out.append(f'        Speaker and title: <span class="placeholder">TBA</span>. <a href="{target}">More information</a>.')
            elif e["type"] == 'Forum':
                out.append('        Speakers and session details: <span class="placeholder">TBA</span>.')
            elif e["type"] == 'Poster':
                out.append('        Poster lineup and presentation details: <span class="placeholder">TBA</span>.')
            elif e["type"] == 'Break':
                out.append('        Tea break.')
            else:
                out.append('        Reserved for session overruns and transitions.')
            out += ['      </td>', '    </tr>']
        out += ['  </tbody>', '</table>', '</section>']
    return "\n".join(out)


def replace_section(path, label, content, check):
    source = path.read_text(encoding="utf-8")
    start = f"<!-- BEGIN GENERATED {label} -->"
    end = f"<!-- END GENERATED {label} -->"
    if source.count(start) != 1 or source.count(end) != 1:
        raise ValueError(f"Missing or duplicate generation markers in {path.name}")
    before, remainder = source.split(start)
    _, after = remainder.split(end)
    updated = f"{before}{start}\n{content}\n{end}{after}"
    if check:
        if updated != source:
            raise ValueError(f"Generated content is out of date: {path.name}")
    elif updated != source:
        path.write_text(updated, encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data, papers, sessions, events = load_data()
    replace_section(ROOT / "accepted-papers.html", "ACCEPTED PAPERS", accepted_html(data, papers, sessions), args.check)
    replace_section(ROOT / "program.html", "PROGRAMME", programme_html(data, papers, sessions, events), args.check)
    print(f"Validated {len(papers)} papers, {len(sessions)} sessions, {len(events)} events; no schedule overlaps.")


if __name__ == "__main__":
    main()
