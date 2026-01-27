import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def hello():
    """Sanity check command."""
    typer.echo("chronotes: ok")

if __name__ == "__main__":
    app()
