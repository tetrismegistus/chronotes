from __future__ import annotations

from typer.testing import CliRunner

from chronotes.cli.main import app

runner = CliRunner()


def test_cli_render_year_accepts_coords_without_city() -> None:
    # This should succeed without --city when --lat/--lon are provided.
    # We avoid asserting on astronomical content; just that it runs and emits something.
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

    assert result.exit_code == 0, result.stdout
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

    assert result.exit_code != 0
    # Typer typically writes parameter errors to stdout in CliRunner captures.
    assert "Provide both --lat and --lon" in (result.stdout + result.stderr)


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

    assert result.exit_code != 0
    assert "Provide --city" in (result.stdout + result.stderr)


def test_cli_render_year_city_without_geocode_is_an_error() -> None:
    # With your default-off geocoding policy, --city alone should error unless --geocode is enabled.
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

    assert result.exit_code != 0
    assert "Geocoding is not configured" in (result.stdout + result.stderr)


def test_cli_render_year_geocode_requires_user_agent() -> None:
    result = runner.invoke(
        app,
        [
            "render-year",
            "--city",
            "Indianapolis, IN",
            "--tz",
            "America/Indiana/Indianapolis",
            "--geocode",
            "--year",
            "2026",
        ],
    )

    assert result.exit_code != 0
    assert "--user-agent is required" in (result.stdout + result.stderr)
