from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import NAMESPACE_URL, uuid5

from chronotes.domain.models import DailyPageData, PlanetaryHour


def _ics_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", r"\n")
    )


def _fold_ical_line(line: str, limit: int = 75) -> list[str]:
    if len(line) <= limit:
        return [line]
    out: list[str] = []
    s = line
    out.append(s[:limit])
    s = s[limit:]
    while s:
        out.append(" " + s[: limit - 1])
        s = s[limit - 1 :]
    return out


def _fmt_dt(dt: datetime) -> str:
    if dt.tzinfo is None:
        return dt.strftime("%Y%m%dT%H%M%S")
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _fmt_dtstamp(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _stable_uid(*, calendar_id: str, start: datetime, end: datetime, summary: str) -> str:
    seed = "|".join([calendar_id, _fmt_dt(start), _fmt_dt(end), summary])
    return f"{uuid5(NAMESPACE_URL, seed)}@chronotes"


@dataclass(frozen=True, slots=True)
class IcsEvent:
    uid: str
    dtstamp: datetime
    start: datetime
    end: datetime
    summary: str
    description: str = ""
    location: str = ""


def _event_to_vevent_lines(e: IcsEvent) -> list[str]:
    lines: list[str] = [
        "BEGIN:VEVENT",
        f"UID:{e.uid}",
        f"DTSTAMP:{_fmt_dtstamp(e.dtstamp)}",
        f"DTSTART:{_fmt_dt(e.start)}",
        f"DTEND:{_fmt_dt(e.end)}",
        f"SUMMARY:{_ics_escape(e.summary)}",
    ]
    if e.description:
        lines.append(f"DESCRIPTION:{_ics_escape(e.description)}")
    if e.location:
        lines.append(f"LOCATION:{_ics_escape(e.location)}")
    lines.append("END:VEVENT")

    folded: list[str] = []
    for ln in lines:
        folded.extend(_fold_ical_line(ln))
    return folded


def _planetary_hour_events_for_day(
    day: DailyPageData,
    *,
    calendar_id: str,
    dtstamp: datetime,
) -> list[IcsEvent]:
    events: list[IcsEvent] = []

    def mk(ph: PlanetaryHour, *, period: str, index_1: int) -> IcsEvent:
        summary = f"{ph.ruler.name} — {period} Hour {index_1}"

        sun_sign_label = getattr(day.sun_sign, "name", None)
        if sun_sign_label is None and day.sun_sign is not None:
            # fallback if sun_sign is a plain string
            sun_sign_label = str(day.sun_sign)

        sun_sign_line = (
            f"Sun sign: {sun_sign_label}\n" if sun_sign_label else ""
        )

        desc = (
            f"City: {day.city}\n"
            f"Date: {day.day.isoformat()}\n"
            f"Day ruler: {day.day_ruler.name}\n"
            f"{sun_sign_line}"
            f"Moon phase: {day.moon_phase}\n"
            f"Period: {period}\n"
            f"Hour: {index_1}/12\n"
            f"Planet: {ph.ruler.name} ({ph.ruler.key})\n"
            f"Sunrise: {day.markers.sunrise.isoformat()}\n"
            f"Solar noon: {day.markers.solar_noon.isoformat()}\n"
            f"Sunset: {day.markers.sunset.isoformat()}\n"
            f"Next sunrise: {day.markers.next_sunrise.isoformat()}"
        )
        uid = _stable_uid(
            calendar_id=calendar_id,
            start=ph.start,
            end=ph.end,
            summary=summary,
        )
        return IcsEvent(
            uid=uid,
            dtstamp=dtstamp,
            start=ph.start,
            end=ph.end,
            summary=summary,
            description=desc,
            location=day.city,
        )

    for i, ph in enumerate(day.hours.day, start=1):
        events.append(mk(ph, period="Day", index_1=i))
    for i, ph in enumerate(day.hours.night, start=1):
        events.append(mk(ph, period="Night", index_1=i))

    return events


def render_calendar_from_days(
    days: Sequence[DailyPageData],
    *,
    prodid: str = "-//chronotes//EN",
    calendar_id: str = "chronotes",
    dtstamp: datetime | None = None,
) -> str:
    stamp = dtstamp or datetime.now(timezone.utc)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)

    vevents: list[str] = []
    for day in days:
        for e in _planetary_hour_events_for_day(day, calendar_id=calendar_id, dtstamp=stamp):
            vevents.extend(_event_to_vevent_lines(e))

    cal_lines: list[str] = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{prodid}",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        *vevents,
        "END:VCALENDAR",
        "",
    ]
    return "\r\n".join(cal_lines)
