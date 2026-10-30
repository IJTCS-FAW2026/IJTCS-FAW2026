"""Render marked static paper/programme sections from verified public metadata.

--validate-only checks data without touching pages; --check also verifies that
generated HTML is current. Accepted papers may have no presentation slot.
Only slots explicitly present in the data are rendered. To close a withdrawn
slot, remove it, renumber subsequent slots, and adjust the session end time.
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
    if not isinstance(value, str) or not re.fullmatch(r"\d{2}:\d{2}", value):
        raise ValueError(f"Invalid time format: {value}")
    hour, minute = map(int, value.split(":"))
    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise ValueError(f"Invalid time: {value}")
    return hour * 60 + minute


def clock(value):
    return f"{value // 60:02d}:{value % 60:02d}"


def title_markup(value):
    value = escape(value)
    for source, markup in {
        "$k$": "<var>k</var>",
        "$b$": "<var>b</var>",
        "$l_p$": "<var>l</var><sub>p</sub>",
        r"\\(k\\)": "<var>k</var>",
        r"\(k\)": "<var>k</var>",
    }.items():
        value = value.replace(source, markup)
    return value


def records(data, name):
    fields = data[f"{name}_fields"]
    if len(fields) != len(set(fields)):
        raise ValueError(f"Duplicate field names: {name}")
    plural = {"paper": "papers", "session": "sessions", "slot": "slots", "programme": "programme"}[name]
    return [dict(zip(fields, row, strict=True)) for row in data[plural]]


def validate_data(data):
    date.fromisoformat(data["updated"])
    date.fromisoformat(data.get("papers_verified", data["updated"]))
    if data["programme_status"] not in ("pending", "confirmed"):
        raise ValueError("Unknown programme status")
    if type(data["talk_minutes"]) is not int or data["talk_minutes"] <= 0:
        raise ValueError("Paper slot duration must be a positive integer")
    papers = records(data, "paper")
    session_rows = records(data, "session")
    slots = records(data, "slot")
    events = records(data, "programme")
    sessions = {s["id"]: s for s in session_rows}
    if len(sessions) != len(session_rows):
        raise ValueError("Duplicate session IDs")
    for code in data["tracks"]:
        if not re.fullmatch(r"[A-Z]", code):
            raise ValueError(f"Invalid track code: {code}")
    for sid, session in sessions.items():
        if not re.fullmatch(r"S\d{2}", sid) or not session["title"].strip():
            raise ValueError(f"Invalid session: {sid}")
    if len({p["number"] for p in papers}) != len(papers):
        raise ValueError("Duplicate paper numbers")
    if len({p["forum_id"] for p in papers}) != len(papers):
        raise ValueError("Duplicate OpenReview forum IDs")
    by_number = {p["number"]: p for p in papers}
    for p in papers:
        if type(p["number"]) is not int or p["number"] <= 0:
            raise ValueError("Invalid paper number")
        if p["track"] not in data["tracks"] or not p["title"].strip() or not p["authors"].strip():
            raise ValueError(f"Missing metadata for paper {p['number']}")
        if not re.fullmatch(r"[A-Za-z0-9]+", p["forum_id"]):
            raise ValueError(f"Invalid forum ID for paper {p['number']}")
    scheduled = []
    for slot in slots:
        if slot["session"] not in sessions or type(slot["order"]) is not int or slot["order"] < 1:
            raise ValueError(f"Invalid presentation slot: {slot}")
        if slot["status"] == "accepted":
            if type(slot["paper_number"]) is not int or slot["paper_number"] not in by_number:
                raise ValueError(f"Slot references a non-accepted paper: {slot}")
            scheduled.append(slot["paper_number"])
        elif slot["status"] == "withdrawn":
            if slot["paper_number"] is not None:
                raise ValueError("Withdrawn slots must be anonymous (paper_number=null)")
        else:
            raise ValueError(f"Unknown slot status: {slot['status']}")
    if len(scheduled) != len(set(scheduled)):
        raise ValueError("A paper has more than one presentation slot")
    for sid in sessions:
        group = sorted((s for s in slots if s["session"] == sid), key=lambda s: s["order"])
        if group and [s["order"] for s in group] != list(range(1, len(group) + 1)):
            raise ValueError(f"Incomplete or duplicate slot order in {sid}")
    allowed_types = {"Opening", "Keynote", "Break", "Lunch", "Tutorial", "Poster", "Forum", "Buffer", "Session"}
    for i, event in enumerate(events):
        day = date.fromisoformat(event["date"])
        if not date(2026, 11, 7) <= day <= date(2026, 11, 10):
            raise ValueError("Event outside conference dates")
        if event["type"] not in allowed_types or not event["title"].strip():
            raise ValueError(f"Invalid programme event: {event}")
        if minutes(event["start"]) >= minutes(event["end"]):
            raise ValueError(f"Non-positive event duration: {event}")
        if i and (events[i - 1]["date"], events[i - 1]["end"]) > (event["date"], event["start"]):
            raise ValueError(f"Overlapping or unsorted event: {event}")
        if event["type"] == "Session":
            sid = event["session"]
            if sid not in sessions or event["title"] != sessions[sid]["title"]:
                raise ValueError(f"Session title or ID mismatch: {sid}")
            group = [s for s in slots if s["session"] == sid]
            if not group or minutes(event["end"]) - minutes(event["start"]) != len(group) * data["talk_minutes"]:
                raise ValueError(f"Presentation slots do not fill session {sid}")
        elif event["session"]:
            raise ValueError("Non-session events cannot reference a paper session")
    session_counts = Counter(e["session"] for e in events if e["type"] == "Session")
    if any(count != 1 for count in session_counts.values()):
        raise ValueError("A paper session appears more than once")
    if data["programme_status"] == "confirmed" and session_counts != Counter({sid: 1 for sid in sessions}):
        raise ValueError("Every confirmed session must appear once in the programme")
    talk_events = {e["title"] for e in events if e["type"] in ("Keynote", "Tutorial")}
    for event_title, detail in data.get("talk_details", {}).items():
        if event_title not in talk_events:
            raise ValueError(f"Talk details reference an unknown invited talk: {event_title}")
        for key in ("speaker", "title", "source"):
            if not isinstance(detail.get(key), str) or not detail[key].strip():
                raise ValueError(f"Missing {key} for {event_title}")
        date.fromisoformat(detail["updated"])
        abstract = detail.get("abstract", [])
        if not isinstance(abstract, list) or any(not isinstance(p, str) or not p.strip() for p in abstract):
            raise ValueError(f"Invalid abstract for {event_title}")
    return data, papers, sessions, slots, events


def load_data():
    return validate_data(json.loads((ROOT / "assets/data/conference-2026.json").read_text(encoding="utf-8")))


def accepted_html(data, papers, sessions, slots):
    counts = Counter(p["track"] for p in papers)
    scheduled = {s["paper_number"]: s for s in slots if s["status"] == "accepted"}
    verified = data.get("papers_verified", data["updated"])
    out = [
        '<p>Listed by track and alphabetically by title. Author names retain their submitted order. Paper numbers are the OpenReview submission numbers; presentation sessions may span multiple tracks.</p>',
        f'<p>Paper metadata verified on <time datetime="{escape(verified)}">{escape(verified)}</time> against <a href="https://openreview.net/group?id=IJTCS-FAW/2026/Conference">OpenReview</a>.</p>',
        f'<div class="conference-summary"><span>{len(papers)} accepted papers</span></div>',
        '<nav class="conference-jump-links" aria-label="Accepted paper tracks">',
    ]
    for code in data["tracks"]:
        out.append(f'  <a href="#track-{code}">Track {code} &middot; {counts[code]} papers</a>')
    out += ['</nav>', '<p><a href="program.html">View the conference programme and presentation times</a> &middot; <a href="submission.html#camera-ready">Camera-ready instructions</a></p>']
    for code, name in data["tracks"].items():
        out += [f'<section aria-labelledby="track-{code}">', f'<h2 id="track-{code}">Track {code}: {escape(name)}</h2>', '<ol class="accepted-paper-list">']
        for paper in sorted((p for p in papers if p["track"] == code), key=lambda p: p["title"].casefold()):
            slot = scheduled.get(paper["number"])
            if slot:
                sid = slot["session"]
                meta = f'<a href="program.html#session-{sid}">{sid}: {escape(sessions[sid]["title"])}</a>'
            else:
                meta = 'Presentation schedule: <span class="placeholder">TBA</span>'
            out += [
                f'  <li class="accepted-paper" id="paper-{paper["number"]}">',
                f'    <h3 class="paper-heading"><span class="paper-number">#{paper["number"]}</span> <a href="https://openreview.net/forum?id={paper["forum_id"]}">{title_markup(paper["title"])}</a></h3>',
                f'    <p class="paper-authors">{escape(paper["authors"])}</p>',
                f'    <p class="paper-meta">{meta}</p>',
                '  </li>',
            ]
        out += ['</ol>', '</section>']
    out += ['<h2>Proceedings</h2>', '<p>Proceedings publication details: <span class="placeholder">TBA</span>. Please follow the <a href="submission.html#camera-ready">camera-ready instructions</a> for final files and the Copyright Form.</p>']
    return "\n".join(out)


def programme_html(data, papers, sessions, slots, events):
    if data["programme_status"] != "confirmed":
        raise ValueError("Cannot publish an unconfirmed programme")
    by_number = {p["number"]: p for p in papers}
    types = Counter(e["type"] for e in events)
    out = [
        '<p><a href="output/pdf/IJTCS-FAW-2026-Programme.pdf" class="text-link" download>Download the English programme (PDF)</a></p>',
        f'<p>All times are <strong>{escape(data["timezone"])}</strong>. Paper presentations are in a single venue; each {data["talk_minutes"]}-minute slot includes the talk, questions, and transition.</p>',
        '<p>Session chairs and presenting authors: <span class="placeholder">TBA</span>. Unannounced keynote and tutorial speakers and talk titles: <span class="placeholder">TBA</span>; confirmed talks are listed below. Further forum and poster details: <span class="placeholder">TBA</span>.</p>',
        f'<div class="conference-summary"><span>{len(papers)} accepted papers</span><span>{len(sessions)} paper sessions</span><span>{types["Keynote"]} keynotes</span><span>{types["Tutorial"]} tutorials</span></div>',
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
        for event in (e for e in events if e["date"] == value):
            sid = event["session"]
            ident = f' id="session-{sid}"' if sid else ''
            out += [
                f'    <tr{ident}>',
                f'      <th class="programme-time" scope="row"><time datetime="{value}T{event["start"]}:00+08:00">{event["start"]}</time>&ndash;<time datetime="{value}T{event["end"]}:00+08:00">{event["end"]}</time></th>',
                f'      <td class="programme-session"><span class="programme-type">{escape(sid or event["type"])}</span>{escape(event["title"])}</td>',
                '      <td>',
            ]
            if sid:
                group = sorted((s for s in slots if s["session"] == sid), key=lambda s: s["order"])
                count = sum(s["status"] == "accepted" for s in group)
                pending = len(group) - count
                summary = f'{count} paper presentations' + (f' &middot; {pending} slot TBA' if pending else '')
                out += [f'        <details class="programme-details"><summary>{summary} &middot; View presentation slots</summary>', '          <ol class="programme-paper-list">']
                for slot in group:
                    start = minutes(event["start"]) + (slot["order"] - 1) * data["talk_minutes"]
                    end = start + data["talk_minutes"]
                    time = f'<span class="paper-time"><time datetime="{value}T{clock(start)}:00+08:00">{clock(start)}</time>&ndash;<time datetime="{value}T{clock(end)}:00+08:00">{clock(end)}</time></span>'
                    out += ['            <li>', f'              {time}']
                    if slot["status"] == "accepted":
                        paper = by_number[slot["paper_number"]]
                        out += [f'              <a href="accepted-papers.html#paper-{paper["number"]}">#{paper["number"]} &middot; {title_markup(paper["title"])}</a>', f'              <p class="paper-authors">{escape(paper["authors"])}</p>']
                    else:
                        out.append('              <span class="placeholder">TBA</span>')
                    out.append('            </li>')
                out += ['          </ol>', '        </details>']
            elif event["type"] in ("Keynote", "Tutorial"):
                target = 'keynotes.html' if event["type"] == 'Keynote' else 'tutorials.html'
                detail = data.get("talk_details", {}).get(event["title"])
                if detail:
                    anchor = event["title"].lower().replace(" ", "-")
                    out += [f'        <strong>{escape(detail["title"])}</strong>',
                            f'        <p>Speaker: {escape(detail["speaker"])}</p>',
                            f'        <a href="{target}#{anchor}">Abstract and details</a>.']
                else:
                    out.append(f'        Speaker and title: <span class="placeholder">TBA</span>. <a href="{target}">More information</a>.')
            elif event["type"] == "Forum":
                out.append('        Speakers and session details: <span class="placeholder">TBA</span>.')
            elif event["type"] == "Poster":
                out.append('        Poster lineup and display instructions: <span class="placeholder">TBA</span>. See the <a href="posters.html">Call for Posters</a>.')
            elif event["type"] == "Break":
                out.append('        Tea break and group photo.' if 'Group Photo' in event["title"] else '        Tea break.')
            elif event["type"] == "Lunch":
                out.append('        Lunch break.')
            elif event["type"] == "Opening":
                out.append('        Conference opening.')
            else:
                out.append('        Reserved for session overruns and transitions.')
            out += ['      </td>', '    </tr>']
        out += ['  </tbody>', '</table>', '</section>']
    return "\n".join(out)


def tutorials_html(data, events):
    out = []
    for event in events:
        if event["type"] != "Tutorial":
            continue
        detail = data.get("talk_details", {}).get(event["title"])
        if not detail:
            continue
        anchor = event["title"].lower().replace(" ", "-")
        day = date.fromisoformat(event["date"])
        out += [f'<section aria-labelledby="{anchor}">',
                f'<h3 id="{anchor}">{escape(event["title"])}: {escape(detail["title"])}</h3>',
                f'<p><strong>Speaker:</strong> {escape(detail["speaker"])}</p>',
                f'<p><strong>Time:</strong> <time datetime="{event["date"]}">Nov {day.day}, {day.year}</time>, {event["start"]}&ndash;{event["end"]}, {escape(data["timezone"])}.</p>',
                '<h4>Abstract</h4>']
        out += [f'<p>{escape(paragraph)}</p>' for paragraph in detail.get("abstract", [])]
        out.append('</section>')
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
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    data, papers, sessions, slots, events = load_data()
    if not args.validate_only:
        replace_section(ROOT / "accepted-papers.html", "ACCEPTED PAPERS", accepted_html(data, papers, sessions, slots), args.check)
        replace_section(ROOT / "program.html", "PROGRAMME", programme_html(data, papers, sessions, slots, events), args.check)
        replace_section(ROOT / "tutorials.html", "TUTORIALS", tutorials_html(data, events), args.check)
    scheduled = sum(s["status"] == "accepted" for s in slots)
    print(f"Validated {len(papers)} accepted papers ({scheduled} scheduled), {len(sessions)} sessions, {len(slots)} slots and {len(events)} events; no schedule overlaps.")


if __name__ == "__main__":
    main()
