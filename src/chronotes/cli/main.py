import typer

app = typer.Typer(no_args_is_help=True)

@app.callback()
def _root() -> None:
    """chronotes CLI."""
    pass

@app.command()
def hello() -> None:
    """Sanity check command."""
    typer.echo("chronotes: ok")

def main() -> None:
    app()

if __name__ == "__main__":
    main()
