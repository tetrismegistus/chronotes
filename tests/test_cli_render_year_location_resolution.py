from __future__ import annotations

from typer.testing import CliRunner

from chronotes.cli.main import app

runner = CliRunner()


def _out(result) -> str:
    # Typer/CliRunner can split output between stdout/stderr depending on version/config.
    return (result.stdout or "") + (result.stderr or "")


def test_cli_render_year_accepts_coords_without_city() -> None:
    # Coord override path should succeed without --city.
    result = runner.invoke(
        app,
        [
            "render-year",
            "--tz",
            "America/Indiana/Indianapolis",
            "--lat",
            "39.7684",
            "--lon",
            "-86.1581",
            "--year",
            "2026",
        ],
    )

    assert result.exit_code == 0, _out(result)
    assert result.stdout.strip() != ""


def test_cli_render_year_errors_if_only_one_coord_is_provided() -> None:
    result = runner.invoke(
        app,
        [
            "render-year",
            "--tz",
            "America/Indiana/Indianapolis",
            "--lat",
            "39.7684",
            "--year",
            "2026",
        ],
    )

    assert result.exit_code != 0, _out(result)
    assert "Provide both --lat and --lon" in _out(result)


def test_cli_render_year_requires_city_or_coords() -> None:
    result = runner.invoke(
        app,
        [
            "render-year",
            "--tz",
            "America/Indiana/Indianapolis",
            "--year",
            "2026",
        ],
    )

    assert result.exit_code != 0, _out(result)
    assert "Provide --city" in _out(result)


def test_cli_render_year_city_requires_user_agent_when_no_coords() -> None:
    result = runner.invoke(
        app,
        [
            "render-year",
            "--city",
            "Indianapolis, IN",
            "--tz",
            "America/Indiana/Indianapolis",
            "--year",
            "2026",
        ],
    )

    # Depending on your current CLI wiring, this can fail either:
    # - in our own logic (BadParameter with a specific message), or
    # - at Typer parsing/validation time (generic "Usage: ... Error ...").
    #
    # We assert the invariant: city-without-coords requires a user agent.
    assert result.exit_code != 0, _out(result)

    msg = _out(result)
    assert "user-agent" in msg.lower()
    assert "--city" in msg or "city" in msg.lower()
