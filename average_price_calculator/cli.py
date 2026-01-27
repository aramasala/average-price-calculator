"""Command-line interface for the calculator."""

from rich import print as rprint
from rich.console import Console
from rich.table import Table
import typer

from . import __version__
from .calculator import calculate_average_price_safe
from .models import PriceData

app = typer.Typer(
    name="avg-price-calc",
    help="Calculate weighted average prices for investments",
    add_completion=False,
)
console = Console()


@app.command()
def calculate(
    initial_qty: float = typer.Option(
        ...,
        "--initial-qty",
        "-iq",
        help="Initial quantity",
        prompt="Initial quantity",
    ),
    initial_price: float = typer.Option(
        ...,
        "--initial-price",
        "-ip",
        help="Initial price per unit",
        prompt="Initial price",
    ),
    new_qty: float = typer.Option(
        ...,
        "--new-qty",
        "-nq",
        help="New quantity to purchase",
        prompt="New quantity",
    ),
    new_price: float = typer.Option(
        ...,
        "--new-price",
        "-np",
        help="New price per unit",
        prompt="New price",
    ),
    precision: int = typer.Option(
        6, "--precision", "-p", help="Decimal precision for results", min=0, max=10
    ),
) -> None:
    """
    Calculate weighted average price after additional purchase.

    Example:
        avg-price-calc calculate
        --initial-qty 100 --initial-price 10.5
        --new-qty 50 --new-price 12.0
    """
    try:
        data = PriceData(
            initial_quantity=initial_qty,
            initial_price=initial_price,
            new_quantity=new_qty,
            new_price=new_price,
        )

        result = calculate_average_price_safe(data, precision)

        # Display results in a table
        table = Table(title="📊 Average Price Calculation Results", show_header=True)
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Value", style="green", justify="right")
        table.add_column("Description", style="white")

        table.add_row(
            "Average Price",
            f"{result.average_price:.{precision}f}",
            "Weighted average price per unit",
        )
        table.add_row(
            "Total Quantity",
            f"{result.total_quantity:.{precision}f}",
            "Total units after purchase",
        )
        table.add_row(
            "Total Investment",
            f"{result.total_investment:.{precision}f}",
            "Total money invested",
        )

        console.print(table)

        # Show formula
        console.print("\n[bold]Formula:[/bold]")
        console.print(f"  ({initial_qty} x {initial_price}) + ({new_qty} x {new_price})")
        console.print("  ------------------------------------")
        console.print(f"          {initial_qty} + {new_qty}")

    except (ValueError, ZeroDivisionError) as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from e


@app.command()
def version() -> None:
    """Show version information."""
    rprint(f"[bold green]Average Price Calculator[/bold green] v{__version__}")


@app.command()
def example() -> None:
    """Run an example calculation."""
    rprint("[yellow]Running example calculation...[/yellow]")

    data = PriceData(
        initial_quantity=4.37562,
        initial_price=3.602,
        new_quantity=2.93867,
        new_price=2.11,
    )

    result = calculate_average_price_safe(data)

    rprint("[cyan]Input:[/cyan]")
    rprint(f"  Initial: {data.initial_quantity} units at ${data.initial_price}")
    rprint(f"  New: {data.new_quantity} units at ${data.new_price}")

    rprint("[cyan]Results:[/cyan]")
    rprint(f"  Average Price: ${result.average_price:.6f}")
    rprint(f"  Total Quantity: {result.total_quantity:.6f}")
    rprint(f"  Total Investment: ${result.total_investment:.6f}")


if __name__ == "__main__":
    app()
