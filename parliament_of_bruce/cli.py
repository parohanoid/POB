import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime
from pathlib import Path
from .storage import Storage
from .services import ParliamentService

app = typer.Typer(help="Parliament of Bruce - Psychological journaling and decision-making system")
console = Console()


def get_service() -> ParliamentService:
    """Get parliament service instance."""
    storage = Storage()
    return ParliamentService(storage)


@app.command()
def init():
    """Initialize the Parliament of Bruce system."""
    service = get_service()
    
    console.print(Panel.fit(
        "[bold cyan]Parliament of Bruce Initialized[/bold cyan]\n\n"
        "Five permanent seats established:\n"
        "  • Short-Term Bruce (1 vote)\n"
        "  • Mid-Term Bruce (2 votes)\n"
        "  • Long-Term Bruce (3 votes)\n"
        "  • Purpose Bruce (4 votes)\n"
        "  • Ultimate Bruce (5 votes)\n\n"
        "[yellow]No Reigning Bruce yet. Create one with:[/yellow]\n"
        "  pob reign new",
        title="🏛️  Parliament Established"
    ))
    
    console.print(f"\n[dim]Data stored in: {service.storage.data_dir}[/dim]")


@app.command()
def status():
    """Show current parliament status."""
    service = get_service()
    
    if not service.state.reigning_bruce:
        console.print("[yellow]⚠️  No Reigning Bruce currently active[/yellow]")
        console.print("Create one with: [cyan]pob reign new[/cyan]")
        return
    
    bruce = service.state.reigning_bruce
    start = datetime.fromisoformat(bruce.start_date)
    duration = (datetime.now() - start).days
    
    # Status panel
    console.print(Panel.fit(
        f"[bold cyan]{bruce.name}[/bold cyan]\n\n"
        f"Born: {start.strftime('%Y-%m-%d')}\n"
        f"Reason: {bruce.reason_born}\n"
        f"Duration: {duration} days\n"
        f"Sessions: {bruce.session_count}",
        title="👑 Current Reigning Bruce"
    ))
    
    # Recent entries
    recent = service.get_recent_entries(3)
    if recent:
        console.print("\n[bold]Recent Sessions:[/bold]")
        for entry in recent:
            date = datetime.fromisoformat(entry.date).strftime('%Y-%m-%d')
            console.print(f"  • {date} - {entry.session_type}")
    
    # Warnings
    warnings = service.generate_warnings()
    console.print("\n[bold]Psychological Analysis:[/bold]")
    for warning in warnings:
        console.print(f"  {warning}")


@app.command()
def session(
    session_type: str = typer.Argument("daily", help="Session type: daily, weekly, monthly")
):
    """Conduct a parliament session."""
    service = get_service()
    
    if not service.state.reigning_bruce:
        console.print("[yellow]⚠️  No Reigning Bruce active. Create one first:[/yellow]")
        console.print("  pob reign new")
        return
    
    console.print(Panel.fit(
        f"[bold cyan]{session_type.upper()} PARLIAMENT SESSION[/bold cyan]\n"
        f"Reigning Bruce: {service.state.reigning_bruce.name}",
        title="🏛️  Parliament Convenes"
    ))
    
    responses = {}
    
    # Collect from each seat
    seats = [
        ("short_term", "Short-Term Bruce", "What does your immediate self need today?"),
        ("mid_term", "Mid-Term Bruce", "What should you focus on this week/month?"),
        ("long_term", "Long-Term Bruce", "What moves you toward your 5-year vision?"),
        ("purpose", "Purpose Bruce", "How does today align with your deepest values?"),
        ("ultimate", "Ultimate Bruce", "What truth must be spoken from the end of your life?"),
    ]
    
    for key, name, prompt in seats:
        console.print(f"\n[bold cyan]{name}[/bold cyan]")
        response = typer.prompt(prompt)
        responses[key] = response
    
    # Reigning Bruce summary
    console.print(f"\n[bold cyan]Reigning Bruce ({service.state.reigning_bruce.name})[/bold cyan]")
    responses["reigning"] = typer.prompt("Synthesize the parliament's wisdom")
    
    # Final policy
    console.print(f"\n[bold green]Final Policy[/bold green]")
    responses["final_policy"] = typer.prompt("What is today's governing policy?")
    
    # Create entry
    entry = service.create_session(session_type, responses)
    
    console.print("\n[green]✓ Session recorded successfully[/green]")
    console.print(f"[dim]Entry saved: {datetime.fromisoformat(entry.date).strftime('%Y-%m-%d %H:%M')}[/dim]")


@app.command()
def vote(topic: str = typer.Argument(..., help="Topic to vote on")):
    """Vote on a decision through parliament."""
    service = get_service()
    
    if not service.state.reigning_bruce:
        console.print("[yellow]⚠️  No Reigning Bruce active[/yellow]")
        return
    
    console.print(Panel.fit(
        f"[bold cyan]VOTING SESSION[/bold cyan]\n\n"
        f"Topic: {topic}\n\n"
        f"[yellow]Vote YES or NO for each seat[/yellow]",
        title="🗳️  Parliament Votes"
    ))
    
    votes = {}
    seats = [
        ("ShortTerm", "Short-Term Bruce", 1),
        ("MidTerm", "Mid-Term Bruce", 2),
        ("LongTerm", "Long-Term Bruce", 3),
        ("Purpose", "Purpose Bruce", 4),
        ("Ultimate", "Ultimate Bruce", 5),
        ("Reigning", f"Reigning Bruce ({service.state.reigning_bruce.name})", 3),
    ]
    
    for key, name, weight in seats:
        console.print(f"\n[cyan]{name}[/cyan] ({weight} votes)")
        vote = typer.prompt("Vote (yes/no)").strip().lower()
        votes[key] = vote
    
    # Process decision
    decision = service.vote_on_decision(topic, ["Yes", "No"], votes)
    
    # Display results
    yes_score = sum(service.VOTE_WEIGHTS[k] for k, v in votes.items() if v in ["yes", "y", "1"])
    no_score = service.MAX_SCORE - yes_score
    
    console.print("\n" + "="*60)
    console.print(f"\n[bold]RESULTS:[/bold]")
    console.print(f"  Yes: {yes_score}/{service.MAX_SCORE}")
    console.print(f"  No: {no_score}/{service.MAX_SCORE}")
    console.print(f"  Threshold: {service.PASSING_THRESHOLD}")
    
    if decision.passed:
        console.print(f"\n[bold green]✓ DECISION PASSED[/bold green]")
    else:
        console.print(f"\n[bold red]✗ DECISION FAILED[/bold red]")
    
    console.print("\n" + "="*60)


@app.command()
def rebirth():
    """Trigger a Bruce rebirth (identity death and renewal)."""
    service = get_service()
    
    if not service.state.reigning_bruce:
        console.print("[yellow]No Bruce to rebirth. Create first Bruce with 'pob reign new'[/yellow]")
        return
    
    console.print(Panel.fit(
        "[bold red]REBIRTH PROTOCOL[/bold red]\n\n"
        "A significant event has triggered identity death.\n"
        "The current Bruce must exit with a final report.",
        title="💀 Identity Transition"
    ))
    
    # Exit report
    console.print(f"\n[bold]Current Bruce:[/bold] {service.state.reigning_bruce.name}")
    console.print(f"Duration: {service.state.reigning_bruce.session_count} sessions")
    
    exit_report = typer.prompt("\nExit Report: What killed this version of Bruce?")
    service.end_reigning_bruce(exit_report)
    
    console.print("\n[green]✓ Bruce has been laid to rest[/green]")
    
    # Create new Bruce
    console.print("\n[bold cyan]Birth of New Bruce[/bold cyan]")
    new_name = typer.prompt("Name for new Bruce")
    reason = typer.prompt("What event birthed this new identity?")
    
    new_bruce = service.create_reigning_bruce(new_name, reason)
    
    console.print(f"\n[bold green]✓ {new_bruce.name} is now reigning[/bold green]")


@app.command()
def renounce():
    """Voluntarily end current Bruce's reign."""
    service = get_service()
    
    if not service.state.reigning_bruce:
        console.print("[yellow]No Bruce to renounce[/yellow]")
        return
    
    console.print(f"[bold]Current Bruce:[/bold] {service.state.reigning_bruce.name}")
    confirm = typer.confirm("Are you sure you want to renounce this identity?")
    
    if not confirm:
        console.print("Renunciation cancelled")
        return
    
    exit_report = typer.prompt("Final statement for this Bruce")
    service.end_reigning_bruce(exit_report)
    
    console.print("[green]✓ Bruce renounced[/green]")


@app.command()
def reign(action: str = typer.Argument("new", help="Action: new")):
    """Create a new Reigning Bruce."""
    service = get_service()
    
    if action != "new":
        console.print("[red]Unknown action. Use: pob reign new[/red]")
        return
    
    if service.state.reigning_bruce:
        console.print(f"[yellow]Current Bruce:[/yellow] {service.state.reigning_bruce.name}")
        replace = typer.confirm("Replace current Bruce?")
        if replace:
            exit_report = typer.prompt("Exit report for current Bruce")
            service.end_reigning_bruce(exit_report)
    
    name = typer.prompt("Name for new Reigning Bruce")
    reason = typer.prompt("Reason for this new identity")
    
    new_bruce = service.create_reigning_bruce(name, reason)
    console.print(f"\n[bold green]✓ {new_bruce.name} now reigns[/bold green]")


@app.command()
def timeline():
    """Show timeline of all Bruce identities."""
    service = get_service()
    
    if not service.state.bruce_history and not service.state.reigning_bruce:
        console.print("[yellow]No Bruce history yet[/yellow]")
        return
    
    console.print(Panel.fit("[bold cyan]Timeline of Bruce Identities[/bold cyan]", title="📜 History"))
    
    all_bruces = service.state.bruce_history.copy()
    if service.state.reigning_bruce:
        all_bruces.append(service.state.reigning_bruce)
    
    for i, bruce in enumerate(all_bruces, 1):
        start = datetime.fromisoformat(bruce.start_date).strftime('%Y-%m-%d')
        
        if bruce.end_date:
            end = datetime.fromisoformat(bruce.end_date).strftime('%Y-%m-%d')
            status = f"[dim]{start} → {end}[/dim]"
        else:
            status = f"[green]{start} → Present[/green]"
        
        console.print(f"\n{i}. [bold]{bruce.name}[/bold]")
        console.print(f"   {status}")
        console.print(f"   Reason: {bruce.reason_born}")
        console.print(f"   Sessions: {bruce.session_count}")
        
        if bruce.exit_report:
            console.print(f"   Exit: {bruce.exit_report}")


@app.command()
def export(format: str = typer.Option("markdown", help="Export format: markdown or json")):
    """Export all parliament data."""
    service = get_service()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format == "json":
        filename = f"parliament_export_{timestamp}.json"
        import json
        with open(filename, 'w') as f:
            json.dump(service.state.model_dump(), f, indent=2)
        console.print(f"[green]✓ Exported to {filename}[/green]")
    
    elif format == "markdown":
        filename = f"parliament_export_{timestamp}.md"
        
        with open(filename, 'w') as f:
            f.write("# Parliament of Bruce - Complete Export\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Bruce timeline
            f.write("## Bruce Identity Timeline\n\n")
            all_bruces = service.state.bruce_history.copy()
            if service.state.reigning_bruce:
                all_bruces.append(service.state.reigning_bruce)
            
            for bruce in all_bruces:
                f.write(f"### {bruce.name}\n")
                f.write(f"- Start: {bruce.start_date}\n")
                if bruce.end_date:
                    f.write(f"- End: {bruce.end_date}\n")
                f.write(f"- Reason: {bruce.reason_born}\n")
                f.write(f"- Sessions: {bruce.session_count}\n")
                if bruce.exit_report:
                    f.write(f"- Exit: {bruce.exit_report}\n")
                f.write("\n")
            
            # Journal entries
            f.write("## Journal Entries\n\n")
            for entry in service.state.journal_entries:
                date = datetime.fromisoformat(entry.date).strftime('%Y-%m-%d')
                f.write(f"### {date} - {entry.session_type}\n")
                f.write(f"**Bruce:** {entry.reigning_bruce_name}\n\n")
                f.write(f"**Short-Term:** {entry.short_term}\n\n")
                f.write(f"**Mid-Term:** {entry.mid_term}\n\n")
                f.write(f"**Long-Term:** {entry.long_term}\n\n")
                f.write(f"**Purpose:** {entry.purpose}\n\n")
                f.write(f"**Ultimate:** {entry.ultimate}\n\n")
                f.write(f"**Reigning:** {entry.reigning}\n\n")
                f.write(f"**Policy:** {entry.final_policy}\n\n")
                f.write("---\n\n")
        
        console.print(f"[green]✓ Exported to {filename}[/green]")
    
    else:
        console.print("[red]Unknown format. Use: markdown or json[/red]")


if __name__ == "__main__":
    app()
