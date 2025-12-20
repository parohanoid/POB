"""Rich prompts and styled output for Parliament of Bruce CLI."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Seat colors and prompts
SEAT_CONFIG = {
    "Short-Term Bruce": {
        "color": "red",
        "prompt": "What do you want RIGHT NOW?",
    },
    "Mid-Term Bruce": {
        "color": "yellow",
        "prompt": "What can realistically be done this week/month?",
    },
    "Long-Term Bruce": {
        "color": "blue",
        "prompt": "Does this compound over 5 years?",
    },
    "Purpose Bruce": {
        "color": "magenta",
        "prompt": "Why does this matter to your deepest self?",
    },
    "Ultimate Bruce": {
        "color": "white",
        "prompt": "Will you regret this at the end of your life?",
    },
    "Reigning Bruce": {
        "color": "cyan",
        "prompt": "Synthesize the parliament's wisdom into policy:",
    },
}


def print_header(title: str, subtitle: str = ""):
    """Print a styled header."""
    panel_text = f"[bold cyan]{title}[/bold cyan]"
    if subtitle:
        panel_text += f"\n[dim]{subtitle}[/dim]"
    console.print(Panel.fit(panel_text, style="bold blue"))


def print_session_header(session_type: str, reigning_bruce_name: str = ""):
    """Print a session header."""
    title = f"{session_type.upper()} PARLIAMENT SESSION"
    subtitle = f"Reigning Bruce: {reigning_bruce_name}" if reigning_bruce_name else ""
    print_header(title, subtitle)


def prompt_seat_statement(seat_name: str) -> str:
    """
    Prompt for a statement from a seat with styled input.
    """
    cfg = SEAT_CONFIG.get(seat_name, {"color": "white", "prompt": "Speak:"})
    color = cfg["color"]
    prompt_text = cfg["prompt"]

    console.print(f"\n[{color}]● {seat_name}[/{color}]")
    console.print(f"[dim]{prompt_text}[/dim]")
    return input("> ").strip()


def print_vote_header(topic: str):
    """Print a voting session header."""
    print_header(
        "🗳️  VOTING SESSION",
        f"Topic: {topic}\n\nVote YES or NO for each seat",
    )


def prompt_vote(seat_name: str, weight: int) -> str:
    """Prompt for a vote from a seat."""
    cfg = SEAT_CONFIG.get(seat_name, {"color": "white"})
    color = cfg["color"]

    console.print(f"\n[{color}]● {seat_name}[/{color}] ({weight} votes)")
    return input("Vote (yes/no/abstain): ").strip().lower()


def print_vote_results(
    topic: str,
    votes: dict,
    passed: bool,
    total_yes: int,
    total_no: int,
    threshold: int = 10,
):
    """Print voting results."""
    result_color = "green" if passed else "red"
    result_text = "✓ DECISION PASSED" if passed else "✗ DECISION FAILED"

    table = Table(title="Vote Breakdown")
    table.add_column("Seat", style="cyan")
    table.add_column("Vote", style="yellow")
    table.add_column("Weight", justify="right")

    from ..config import VOTE_WEIGHTS

    for seat, vote in votes.items():
        weight = VOTE_WEIGHTS.get(seat, 0)
        table.add_row(seat, vote.upper(), str(weight))

    console.print(table)

    console.print("\n[bold]Results:[/bold]")
    console.print(f"  Yes: {total_yes}/{18}")
    console.print(f"  No: {total_no}/{18}")
    console.print(f"  Threshold: {threshold}")
    console.print(f"\n[bold {result_color}]{result_text}[/bold {result_color}]")


def print_emergency_mode():
    """Print emergency mode activation."""
    console.print(
        Panel.fit(
            "[bold red]EMERGENCY MODE ACTIVATED[/bold red]\n\n"
            "Ultimate Bruce has absolute veto.\n"
            "Long-Term weight doubled.\n"
            "Short-Term cannot initiate.\n"
            "System in crisis containment.",
            style="bold red",
        )
    )


def print_grounding_steps():
    """Print grounding and de-escalation steps."""
    steps = [
        "🫁 Take 5 deep breaths",
        "🚶 Move your body (walk, stretch)",
        "💧 Drink water or splash cold water on face",
        "📞 Call a trusted person",
        "⏸️  Delay any major decision for 24 hours",
    ]

    console.print("\n[bold yellow]Grounding Steps:[/bold yellow]")
    for step in steps:
        console.print(f"  {step}")


def print_success(message: str):
    """Print a success message."""
    console.print(f"[bold green]✓ {message}[/bold green]")


def print_error(message: str):
    """Print an error message."""
    console.print(f"[bold red]✗ {message}[/bold red]")


def print_warning(message: str):
    """Print a warning message."""
    console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")


def print_info(message: str):
    """Print an info message."""
    console.print(f"[bold cyan]ℹ️  {message}[/bold cyan]")
