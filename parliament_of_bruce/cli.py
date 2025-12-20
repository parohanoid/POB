"""Parliament of Bruce CLI - Internal Republic Journaling System."""

import json
import os
from datetime import datetime
from typing import Optional

import typer
from rich.console import Console

from .config import DEFAULT_CONSTITUTION_PATH
from .db import (
    Base,
    Constitution,
    CustomBruce,
    ReigningBruce,
    Seat,
    Session,
    get_engine,
    get_session,
)
from .services.analytics_service import AnalyticsService
from .services.custom_bruce_service import CustomBruceService
from .services.session_service import SessionService
from .services.vote_service import VoteService
from .storage import check_and_migrate_json, ensure_data_dir, get_db_path
from .ui.prompts import (
    SEAT_CONFIG,
    print_emergency_mode,
    print_error,
    print_grounding_steps,
    print_header,
    print_info,
    print_session_header,
    print_success,
    print_vote_results,
    print_warning,
    prompt_seat_statement,
    prompt_vote,
)

app = typer.Typer(
    help="Parliament of Bruce - Internal Republic Journaling & Governance",
    no_args_is_help=True,
)
console = Console()


@app.command()
def init(db: Optional[str] = typer.Option(None, "--db", help="Database path")):
    """Initialize the Parliament of Bruce system."""
    db_path = get_db_path(db)
    ensure_data_dir()

    # Check for migration
    check_and_migrate_json(db_path)

    # Create tables
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)

    session = get_session(db_path)

    # Check if already initialized
    existing_seats = session.query(Seat).count()
    if existing_seats > 0:
        print_info("System already initialized")
        session.close()
        return

    # Create default seats
    seats_data = [
        {
            "name": "Short-Term Bruce",
            "votes": 1,
            "description": "Focused on immediate needs, pleasure, survival instincts",
        },
        {
            "name": "Mid-Term Bruce",
            "votes": 2,
            "description": "Planning weeks/months ahead, career moves, relationships",
        },
        {
            "name": "Long-Term Bruce",
            "votes": 3,
            "description": "Years-ahead vision, legacy building, strategic positioning",
        },
        {
            "name": "Purpose Bruce",
            "votes": 4,
            "description": "Life meaning, values alignment, existential direction",
        },
        {
            "name": "Ultimate Bruce",
            "votes": 5,
            "description": "Death-aware wisdom, final chapter perspective, truth above all",
        },
        {
            "name": "Reigning Bruce",
            "votes": 3,
            "description": "Current identity version, executive and synthesizer",
        },
    ]

    for seat_data in seats_data:
        seat = Seat(
            name=seat_data["name"],
            votes=seat_data["votes"],
            description=seat_data["description"],
            is_permanent=True,
            active=True,
        )
        session.add(seat)

    # Load and create constitution
    try:
        with open(DEFAULT_CONSTITUTION_PATH, "r") as f:
            const_data = json.load(f)
            constitution = Constitution(
                core_values=const_data["core_values"],
                rights=const_data["rights"],
                prohibited_actions=const_data["prohibited_actions"],
                amendment_rules=const_data["amendment_rules"],
                emergency_powers=const_data["emergency_powers"],
            )
            session.add(constitution)
    except FileNotFoundError:
        console.print("[yellow]Warning: default_constitution.json not found[/yellow]")

    session.commit()
    session.close()

    print_header("Parliament of Bruce Initialized", f"Database: {db_path}")
    print_success("System ready for first session")


@app.command()
def status(db: Optional[str] = typer.Option(None, "--db", help="Database path")):
    """Show current parliament status."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)
    reigning = db_session.query(ReigningBruce).filter(ReigningBruce.end_date == None).first()
    if not reigning:
        print_warning("No Reigning Bruce currently active")
        db_session.close()
        return

    print_header("Current Parliament Status", reigning.name)
    console.print("\n[bold cyan]Reigning Bruce:[/bold cyan]")
    console.print(f"  Name: {reigning.name}")
    console.print(f"  Started: {reigning.start_date[:10]}")

    recent_sessions = db_session.query(Session).order_by(Session.id.desc()).limit(3).all()
    if recent_sessions:
        console.print("\n[bold cyan]Recent Sessions:[/bold cyan]")
        for s in reversed(recent_sessions):
            console.print(f"  • {s.date[:10]} ({s.session_type})")

    custom_bruces = db_session.query(CustomBruce).filter_by(active=True).all()
    if custom_bruces:
        console.print("\n[bold cyan]Active Custom Bruces:[/bold cyan]")
        for cb in custom_bruces:
            console.print(f"  • {cb.name} (votes: {cb.votes})")

    db_session.close()


@app.command()
def timeline(db: Optional[str] = typer.Option(None, "--db", help="Database path")):
    """Display timeline of all Bruce identities."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)
    all_bruces = db_session.query(ReigningBruce).order_by(ReigningBruce.start_date).all()

    if not all_bruces:
        print_warning("No Bruce history")
        db_session.close()
        return

    print_header("Timeline of Bruce Identities")
    for i, bruce in enumerate(all_bruces, 1):
        console.print(f"\n{i}. [bold]{bruce.name}[/bold]")
        console.print(f"   Started: {bruce.start_date[:10]}")
        if bruce.end_date:
            console.print(f"   Ended: {bruce.end_date[:10]}")
        else:
            console.print("[green]   Currently Reigning[/green]")

    db_session.close()


@app.command()
def reign_new(
    name: str = typer.Option(..., "--name", help="Name for new Bruce"),
    reason: str = typer.Option(..., "--reason", help="Reason for new Bruce"),
    db: Optional[str] = typer.Option(None, "--db", help="Database path"),
):
    """Create a new Reigning Bruce."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)
    new_bruce = ReigningBruce(
        name=name,
        start_date=datetime.now().isoformat(),
        reason_born=reason,
    )
    db_session.add(new_bruce)
    db_session.commit()
    print_success(f"{new_bruce.name} now reigns")
    db_session.close()


@app.command()
def session_cmd(
    session_type: str = typer.Argument("daily", help="daily or weekly"),
    db: Optional[str] = typer.Option(None, "--db", help="Database path"),
):
    """Conduct a parliament session."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)
    reigning = db_session.query(ReigningBruce).filter(ReigningBruce.end_date == None).first()
    if not reigning:
        print_error("No Reigning Bruce active. Create one with 'pob reign new'")
        db_session.close()
        return

    print_session_header(session_type, reigning.name)

    statements = {}
    for seat_name, cfg in SEAT_CONFIG.items():
        if seat_name != "Reigning Bruce":
            statements[seat_name.lower().replace(" ", "_")] = prompt_seat_statement(seat_name)

    console.print("[cyan]● Reigning Bruce[/cyan]")
    console.print("[dim]Synthesize the parliament's wisdom:[/dim]")
    reigning_statement = input("> ").strip()
    statements["reigning"] = reigning_statement

    console.print("\n[green]Final Policy[/green]")
    console.print("[dim]What is today's governing policy?[/dim]")
    final_policy = input("> ").strip()

    session_service = SessionService(db_session)
    full_text = " ".join(statements.values()) + " " + final_policy
    
    if session_service.check_emergency_trigger(full_text):
        print_emergency_mode()
        session_service.log_emergency(
            trigger_text=full_text[:200],
            actions_taken="Emergency mode activated",
            who_initiated="System (keyword detection)",
        )

    session_id = session_service.create_session(
        date=datetime.now().isoformat(),
        session_type=session_type,
        statements=statements,
        final_policy=final_policy,
        reigning_bruce_id=reigning.id,
    )

    print_success(f"Session recorded (ID: {session_id})")
    db_session.close()


@app.command()
def vote(
    topic: str = typer.Argument(..., help="Topic to vote on"),
    options: Optional[str] = typer.Option(None, "--options", help="Comma-separated options"),
    db: Optional[str] = typer.Option(None, "--db", help="Database path"),
):
    """Conduct a vote on a decision."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)

    print_header("Vote", topic)

    votes = {}
    seats_to_vote = [
        ("Short-Term Bruce", 1),
        ("Mid-Term Bruce", 2),
        ("Long-Term Bruce", 3),
        ("Purpose Bruce", 4),
        ("Ultimate Bruce", 5),
        ("Reigning Bruce", 3),
    ]

    for seat_name, weight in seats_to_vote:
        vote_val = prompt_vote(seat_name, weight)
        votes[seat_name] = vote_val

    vote_service = VoteService(db_session)
    result = vote_service.calculate_vote_result(votes)

    vote_service.create_decision(
        topic=topic,
        options=options.split(",") if options else ["yes", "no"],
        votes=votes,
    )

    print_vote_results(
        topic=topic,
        votes=votes,
        passed=result["passed"],
        total_yes=result["total_yes"],
        total_no=result["total_no"],
    )

    db_session.close()


@app.command()
def rebirth(db: Optional[str] = typer.Option(None, "--db", help="Database path")):
    """Trigger a rebirth (major identity shift)."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)

    print_header("Rebirth Protocol", "🔄")

    current_reigning = db_session.query(ReigningBruce).filter(ReigningBruce.end_date == None).first()

    if current_reigning:
        console.print(f"\n[bold]Current Bruce:[/bold] {current_reigning.name}")
        console.print("[dim]Prepare exit report for this identity...[/dim]")
        exit_report = input("Exit Report: ").strip()

        current_reigning.end_date = datetime.now().isoformat()
        current_reigning.exit_report = exit_report
        db_session.commit()

        print_success("Previous Bruce has been archived")

    console.print("\n[bold cyan]Birth of New Bruce[/bold cyan]")
    new_name = input("Name for new Bruce: ").strip()
    reason = input("Reason for this rebirth: ").strip()

    new_bruce = ReigningBruce(
        name=new_name,
        start_date=datetime.now().isoformat(),
        reason_born=reason,
    )
    db_session.add(new_bruce)
    db_session.commit()

    print_success(f"{new_bruce.name} is now reigning")

    db_session.close()


@app.command()
def renounce(db: Optional[str] = typer.Option(None, "--db", help="Database path")):
    """Voluntarily renounce the current Reigning Bruce."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)

    reigning = db_session.query(ReigningBruce).filter(ReigningBruce.end_date == None).first()
    if not reigning:
        print_warning("No Reigning Bruce to renounce")
        db_session.close()
        return

    console.print(f"[bold]Renouncing:[/bold] {reigning.name}")
    final_statement = input("Final statement: ").strip()

    reigning.end_date = datetime.now().isoformat()
    reigning.exit_report = final_statement
    db_session.commit()

    print_success("Bruce renounced")

    db_session.close()


@app.command()
def emergency(db: Optional[str] = typer.Option(None, "--db", help="Database path")):
    """Trigger emergency mode."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    print_emergency_mode()
    print_grounding_steps()

    db_session = get_session(db_path)
    session_service = SessionService(db_session)
    session_service.log_emergency(
        trigger_text="Manual emergency activation",
        actions_taken="Emergency mode initiated by user",
        who_initiated="User command",
    )
    db_session.close()


@app.command()
def custom_create(db: Optional[str] = typer.Option(None, "--db", help="Database path")):
    """Create a custom Bruce."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)

    print_header("Create Custom Bruce")

    console.print("\n[bold]Fill out the custom Bruce template:[/bold]")
    name = input("Name: ").strip()
    primary_function = input("Primary function: ").strip()
    problem_statement = input("Problem statement: ").strip()
    values = input("Values (comma-separated): ").strip()
    deliberately_ignore = input("Deliberately ignore: ").strip()
    tone_of_voice = input("Tone of voice: ").strip()
    allowed_emotional_range = input("Allowed emotional range: ").strip()
    decision_bias = input("Decision bias: ").strip()
    votes = int(input("Voting power (0-3): ").strip() or "2")
    expiry_condition = input("Expiry condition (manual/time-based/event-based): ").strip() or "manual"
    expiry_value = input("Expiry value (e.g., '14' for 14 days): ").strip()

    service = CustomBruceService(db_session)

    try:
        custom_id = service.create_custom_bruce(
            name=name,
            primary_function=primary_function,
            problem_statement=problem_statement,
            values=values,
            deliberately_ignore=deliberately_ignore,
            tone_of_voice=tone_of_voice,
            allowed_emotional_range=allowed_emotional_range,
            decision_bias=decision_bias,
            votes=votes,
            expiry_condition=expiry_condition,
            expiry_value=expiry_value,
        )
        print_success(f"Custom Bruce '{name}' created (ID: {custom_id})")
    except ValueError as e:
        print_error(str(e))

    db_session.close()


@app.command()
def custom_list(db: Optional[str] = typer.Option(None, "--db", help="Database path")):
    """List active custom Bruces."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)
    service = CustomBruceService(db_session)

    customs = service.list_active_customs()
    if not customs:
        print_warning("No active custom Bruces")
        db_session.close()
        return

    print_header("Active Custom Bruces")

    for custom in customs:
        console.print(f"\n[bold]{custom.name}[/bold]")
        console.print(f"  Function: {custom.primary_function}")
        console.print(f"  Voting power: {custom.votes}")
        console.print(f"  Expiry: {custom.expiry_condition} ({custom.expiry_value})")

    db_session.close()


@app.command()
def custom_dismiss(
    name: str = typer.Argument(..., help="Name of custom Bruce"),
    db: Optional[str] = typer.Option(None, "--db", help="Database path"),
):
    """Dismiss a custom Bruce."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)
    service = CustomBruceService(db_session)

    if service.dismiss_by_name(name):
        print_success(f"Custom Bruce '{name}' dismissed")
    else:
        print_error(f"Custom Bruce '{name}' not found")

    db_session.close()


@app.command()
def analytics(
    days: int = typer.Option(7, "--days", help="Period in days"),
    db: Optional[str] = typer.Option(None, "--db", help="Database path"),
):
    """Show analytics and dominance scores."""
    db_path = get_db_path(db)
    if not os.path.exists(db_path):
        print_error("System not initialized. Run 'pob init' first")
        return

    db_session = get_session(db_path)
    service = AnalyticsService(db_session)

    analytics_data = service.get_analytics_summary(days=days)

    print_header(f"Analytics ({days} days)")

    console.print("\n[bold cyan]Dominance Scores:[/bold cyan]")
    for seat, score in analytics_data["dominance_scores"].items():
        console.print(f"  {seat}: {score}")

    console.print("\n[bold cyan]Speaking Frequency:[/bold cyan]")
    for seat, freq in analytics_data["speaking_frequency"].items():
        console.print(f"  {seat}: {freq} sessions")

    console.print("\n[bold cyan]Trends:[/bold cyan]")
    for seat, trend in analytics_data["trends"].items():
        direction = "↑" if trend["direction"] == "up" else ("↓" if trend["direction"] == "down" else "→")
        console.print(f"  {seat}: {direction} ({trend['change']:+d})")

    db_session.close()


if __name__ == "__main__":
    app()
