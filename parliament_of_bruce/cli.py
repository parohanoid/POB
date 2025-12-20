import typer
from rich.console import Console
from rich.panel import Panel
from datetime import datetime, timedelta
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
    """Conduct a parliament session with rotating discussion."""
    service = get_service()
    
    if not service.state.reigning_bruce:
        console.print("[yellow]⚠️  No Reigning Bruce active. Create one first:[/yellow]")
        console.print("  pob reign new")
        return
    
    console.print(Panel.fit(
        f"[bold cyan]{session_type.upper()} PARLIAMENT SESSION[/bold cyan]\n"
        f"Reigning Bruce: {service.state.reigning_bruce.name}\n\n"
        f"[yellow]Parliament Discussion (Rotating)[/yellow]\n"
        f"Each seat will speak. After all have spoken, you can continue the discussion\n"
        f"or move to final policy. Press [bold]Ctrl+D[/bold] or type [bold]'stop'[/bold] to end rotation.",
        title="🏛️  Parliament Convenes"
    ))
    
    permanent_responses = {}
    temporary_responses = {}
    round_num = 1
    stop_rotation = False
    
    # Get seat order
    permanent_order = [
        ("short_term", "Short-Term Bruce", "What does your immediate self need today?"),
        ("mid_term", "Mid-Term Bruce", "What should you focus on this week/month?"),
        ("long_term", "Long-Term Bruce", "What moves you toward your 5-year vision?"),
        ("purpose", "Purpose Bruce", "How does today align with your deepest values?"),
        ("ultimate", "Ultimate Bruce", "What truth must be spoken from the end of your life?"),
    ]
    
    temp_bruces = service.get_active_temporary_bruces()
    
    while not stop_rotation:
        console.print(f"\n[bold magenta]━━━ ROUND {round_num} ━━━[/bold magenta]")
        round_had_responses = False
        
        # Permanent seats
        for key, name, prompt in permanent_order:
            console.print(f"\n[bold cyan]{name}[/bold cyan]")
            try:
                response = typer.prompt(prompt)
                if response.lower() in ["stop", "exit", "done"]:
                    stop_rotation = True
                    break
                
                if round_num == 1:
                    permanent_responses[key] = response
                else:
                    if permanent_responses[key]:
                        permanent_responses[key] += f"\n\n[Round {round_num}] {response}"
                    else:
                        permanent_responses[key] = response
                round_had_responses = True
            except EOFError:
                # Handle Ctrl+D
                stop_rotation = True
                break
        
        if stop_rotation:
            break
        
        # Temporary bruces
        for temp_id, temp_bruce in temp_bruces:
            console.print(f"\n[bold yellow]{temp_bruce.name}[/bold yellow]")
            console.print(f"[dim][{temp_bruce.description}][/dim]")
            try:
                response = typer.prompt(f"Response from {temp_bruce.name}")
                if response.lower() in ["stop", "exit", "done"]:
                    stop_rotation = True
                    break
                
                if temp_id not in temporary_responses:
                    temporary_responses[temp_id] = response
                else:
                    temporary_responses[temp_id] += f"\n\n[Round {round_num}] {response}"
                round_had_responses = True
            except EOFError:
                stop_rotation = True
                break
        
        if stop_rotation:
            break
        
        # Ask if user wants to continue discussion
        if round_had_responses:
            console.print(f"\n[dim]All seats have spoken in Round {round_num}.[/dim]")
            continue_discussion = typer.confirm("Continue discussion for another round?", default=False)
            if not continue_discussion:
                stop_rotation = True
            else:
                round_num += 1
        else:
            stop_rotation = True
    
    # Get Reigning Bruce synthesis
    console.print(f"\n[bold green]Reigning Bruce ({service.state.reigning_bruce.name})[/bold green]")
    reigning_response = typer.prompt("Synthesize the parliament's wisdom")
    
    # Final policy
    console.print(f"\n[bold green]Final Policy[/bold green]")
    final_policy = typer.prompt("What is today's governing policy?")
    
    # Create entry
    permanent_responses["reigning"] = reigning_response
    permanent_responses["final_policy"] = final_policy
    
    entry = service.create_session(session_type, permanent_responses, temporary_responses)
    
    console.print("\n[green]✓ Session recorded successfully[/green]")
    console.print(f"[dim]Entry saved: {datetime.fromisoformat(entry.date).strftime('%Y-%m-%d %H:%M')}[/dim]")
    if temporary_responses:
        console.print(f"[dim]Temporary Bruces contributed: {len(temporary_responses)}[/dim]")


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
def add_voice(
    name: str = typer.Argument(..., help="Name of the temporary Bruce"),
    description: str = typer.Option(..., "--description", "-d", help="Description of this voice")
):
    """Add a temporary Bruce voice to parliament (discussion only, no voting)."""
    service = get_service()
    
    temp_bruce = service.add_temporary_bruce(name, description)
    
    console.print(Panel.fit(
        f"[bold cyan]{name}[/bold cyan]\n\n"
        f"[dim]{description}[/dim]\n\n"
        f"[green]✓ Added to parliament[/green]\n"
        f"[dim]ID: {temp_bruce.id}[/dim]",
        title="🗣️  New Voice"
    ))


@app.command()
def remove_voice(voice_id: str = typer.Argument(..., help="ID of the temporary Bruce to remove")):
    """Remove a temporary Bruce voice from parliament."""
    service = get_service()
    
    # Find the voice
    if voice_id not in service.state.temporary_bruces:
        console.print(f"[red]✗ Voice '{voice_id}' not found[/red]")
        return
    
    voice = service.state.temporary_bruces[voice_id]
    confirm = typer.confirm(f"Remove '{voice.name}' from parliament?")
    
    if confirm:
        service.dismiss_temporary_bruce(voice_id)
        console.print(f"[green]✓ '{voice.name}' has been dismissed[/green]")


@app.command()
def voices():
    """List all active temporary Bruce voices in parliament."""
    service = get_service()
    
    temp_bruces = service.get_active_temporary_bruces()
    
    if not temp_bruces:
        console.print("[yellow]No temporary voices currently active[/yellow]")
        console.print("Add one with: [cyan]pob add-voice <name> -d <description>[/cyan]")
        return
    
    console.print(Panel.fit(
        "[bold cyan]Active Temporary Voices in Parliament[/bold cyan]",
        title="🗣️  Voices"
    ))
    
    for temp_id, temp_bruce in temp_bruces:
        console.print(f"\n[bold]{temp_bruce.name}[/bold]")
        console.print(f"  ID: {temp_id}")
        console.print(f"  Description: {temp_bruce.description}")
        if temp_bruce.last_statement:
            statement_preview = temp_bruce.last_statement[:100] + "..." if len(temp_bruce.last_statement) > 100 else temp_bruce.last_statement
            console.print(f"  Last: {statement_preview}")



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
def read(
    date: str = typer.Option(None, help="Specific date (YYYY-MM-DD) or 'latest'"),
    count: int = typer.Option(10, help="Number of recent entries to show"),
    full: bool = typer.Option(False, help="Show full entries (default shows summaries)")
):
    """Read journal entries."""
    service = get_service()
    
    if not service.state.journal_entries:
        console.print("[yellow]No journal entries yet. Create one with 'pob session daily'[/yellow]")
        return
    
    entries = []
    
    # Filter by date if specified
    if date:
        if date.lower() == "latest":
            entries = [service.state.journal_entries[-1]]
        else:
            # Parse date and find matching entries
            target_date = date
            entries = [e for e in service.state.journal_entries 
                      if e.date.startswith(target_date)]
            
            if not entries:
                console.print(f"[yellow]No entries found for {date}[/yellow]")
                return
    else:
        # Show most recent entries
        entries = service.state.journal_entries[-count:]
    
    # Display entries
    for i, entry in enumerate(entries):
        date_obj = datetime.fromisoformat(entry.date)
        date_str = date_obj.strftime('%Y-%m-%d %H:%M')
        
        if full:
            # Full detailed view
            console.print("\n" + "="*70)
            console.print(Panel.fit(
                f"[bold cyan]{entry.session_type.upper()} SESSION[/bold cyan]\n"
                f"Date: {date_str}\n"
                f"Reigning Bruce: {entry.reigning_bruce_name}",
                title=f"📔 Entry {len(service.state.journal_entries) - len(entries) + i + 1}"
            ))
            
            console.print(f"\n[bold cyan]Short-Term Bruce:[/bold cyan]")
            console.print(entry.short_term)
            
            console.print(f"\n[bold cyan]Mid-Term Bruce:[/bold cyan]")
            console.print(entry.mid_term)
            
            console.print(f"\n[bold cyan]Long-Term Bruce:[/bold cyan]")
            console.print(entry.long_term)
            
            console.print(f"\n[bold cyan]Purpose Bruce:[/bold cyan]")
            console.print(entry.purpose)
            
            console.print(f"\n[bold cyan]Ultimate Bruce:[/bold cyan]")
            console.print(entry.ultimate)
            
            console.print(f"\n[bold green]Reigning Bruce ({entry.reigning_bruce_name}):[/bold green]")
            console.print(entry.reigning)
            
            console.print(f"\n[bold yellow]Final Policy:[/bold yellow]")
            console.print(entry.final_policy)
            
            # Show temporary Bruce responses if any
            if entry.temporary_bruce_entries:
                console.print(f"\n[bold yellow]Temporary Voices:[/bold yellow]")
                for temp_id, response in entry.temporary_bruce_entries.items():
                    if temp_id in service.state.temporary_bruces:
                        temp_bruce = service.state.temporary_bruces[temp_id]
                        console.print(f"\n[yellow]{temp_bruce.name}:[/yellow]")
                        console.print(response)
            
            if entry.decisions_voted_on:
                console.print(f"\n[bold]Decisions Voted:[/bold]")
                for dec in entry.decisions_voted_on:
                    console.print(f"  • {dec.topic}: {'PASSED' if dec.passed else 'FAILED'}")
        else:
            # Summary view
            console.print(f"\n[bold]{date_str}[/bold] - {entry.session_type}")
            console.print(f"  Bruce: {entry.reigning_bruce_name}")
            console.print(f"  Policy: {entry.final_policy[:80]}{'...' if len(entry.final_policy) > 80 else ''}")
    
    # Show usage tip if in summary mode
    if not full and entries:
        console.print(f"\n[dim]Showing {len(entries)} entries (summaries). Use --full flag for complete entries.[/dim]")
        console.print(f"[dim]Examples:[/dim]")
        console.print(f"[dim]  pob read --date 2025-12-14 --full[/dim]")
        console.print(f"[dim]  pob read --date latest --full[/dim]")
        console.print(f"[dim]  pob read --count 20[/dim]")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search term to find in entries"),
    seat: str = typer.Option(None, help="Search specific seat: short_term, mid_term, long_term, purpose, ultimate, reigning, policy")
):
    """Search journal entries for specific content."""
    service = get_service()
    
    if not service.state.journal_entries:
        console.print("[yellow]No journal entries to search[/yellow]")
        return
    
    query_lower = query.lower()
    matches = []
    
    for entry in service.state.journal_entries:
        fields_to_search = {}
        
        if seat:
            # Search specific seat
            if seat == "short_term":
                fields_to_search = {"Short-Term": entry.short_term}
            elif seat == "mid_term":
                fields_to_search = {"Mid-Term": entry.mid_term}
            elif seat == "long_term":
                fields_to_search = {"Long-Term": entry.long_term}
            elif seat == "purpose":
                fields_to_search = {"Purpose": entry.purpose}
            elif seat == "ultimate":
                fields_to_search = {"Ultimate": entry.ultimate}
            elif seat == "reigning":
                fields_to_search = {"Reigning": entry.reigning}
            elif seat == "policy":
                fields_to_search = {"Policy": entry.final_policy}
        else:
            # Search all fields
            fields_to_search = {
                "Short-Term": entry.short_term,
                "Mid-Term": entry.mid_term,
                "Long-Term": entry.long_term,
                "Purpose": entry.purpose,
                "Ultimate": entry.ultimate,
                "Reigning": entry.reigning,
                "Policy": entry.final_policy
            }
        
        # Check for matches
        found_in = []
        for field_name, field_content in fields_to_search.items():
            if query_lower in field_content.lower():
                # Get context around match
                index = field_content.lower().index(query_lower)
                start = max(0, index - 40)
                end = min(len(field_content), index + len(query) + 40)
                context = field_content[start:end]
                if start > 0:
                    context = "..." + context
                if end < len(field_content):
                    context = context + "..."
                
                found_in.append((field_name, context))
        
        if found_in:
            matches.append((entry, found_in))
    
    # Display results
    if not matches:
        console.print(f"[yellow]No matches found for '{query}'[/yellow]")
        return
    
    console.print(f"\n[bold]Found {len(matches)} entries containing '{query}':[/bold]\n")
    
    for entry, found_in in matches:
        date_obj = datetime.fromisoformat(entry.date)
        date_str = date_obj.strftime('%Y-%m-%d')
        
        console.print(f"[cyan]{date_str}[/cyan] - {entry.session_type} - {entry.reigning_bruce_name}")
        for field_name, context in found_in:
            console.print(f"  [{field_name}] {context}")
        console.print()


@app.command()
def stats():
    """Show statistics about your parliament usage."""
    service = get_service()
    
    total_entries = len(service.state.journal_entries)
    total_decisions = len(service.state.decisions)
    total_bruces = len(service.state.bruce_history) + (1 if service.state.reigning_bruce else 0)
    
    if total_entries == 0:
        console.print("[yellow]No data yet. Start with 'pob session daily'[/yellow]")
        return
    
    # Calculate date range
    first_entry = service.state.journal_entries[0]
    last_entry = service.state.journal_entries[-1]
    first_date = datetime.fromisoformat(first_entry.date)
    last_date = datetime.fromisoformat(last_entry.date)
    days_active = (last_date - first_date).days + 1
    
    # Session type breakdown
    session_types = {}
    for entry in service.state.journal_entries:
        session_types[entry.session_type] = session_types.get(entry.session_type, 0) + 1
    
    # Decision success rate
    passed = sum(1 for d in service.state.decisions if d.passed)
    failed = total_decisions - passed
    
    # Current streak (consecutive days with entries)
    streak = 0
    current_date = datetime.now().date()
    for entry in reversed(service.state.journal_entries):
        entry_date = datetime.fromisoformat(entry.date).date()
        if entry_date == current_date:
            streak += 1
            current_date -= timedelta(days=1)
        elif entry_date < current_date:
            break
    
    # Display stats
    console.print(Panel.fit(
        f"[bold cyan]Parliament Statistics[/bold cyan]\n\n"
        f"📊 Overall:\n"
        f"  • Total Sessions: {total_entries}\n"
        f"  • Total Decisions: {total_decisions}\n"
        f"  • Identity Versions: {total_bruces}\n"
        f"  • Days Active: {days_active}\n"
        f"  • Current Streak: {streak} days\n\n"
        f"📝 Session Types:\n" +
        "\n".join(f"  • {k}: {v}" for k, v in session_types.items()) +
        f"\n\n🗳️  Decision Record:\n"
        f"  • Passed: {passed}\n"
        f"  • Failed: {failed}\n"
        f"  • Success Rate: {(passed/total_decisions*100) if total_decisions > 0 else 0:.1f}%",
        title="📈 Your Journey"
    ))
    
    # Most productive Bruce
    if service.state.bruce_history:
        most_sessions = max(service.state.bruce_history, key=lambda b: b.session_count)
        console.print(f"\n[bold]Most Productive Bruce:[/bold] {most_sessions.name} ({most_sessions.session_count} sessions)")
    
    # Recent activity
    if total_entries >= 7:
        recent_7 = service.state.journal_entries[-7:]
        console.print(f"\n[bold]Last 7 Days Activity:[/bold]")
        for entry in recent_7:
            date = datetime.fromisoformat(entry.date).strftime('%Y-%m-%d')
            console.print(f"  {date}: {entry.session_type}")


@app.command()
def export(format: str = typer.Option("markdown", help="Export format: markdown or json")):
    """Export all parliament data."""
    service = get_service()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format == "json":
        filename = f"parliament_export_{timestamp}.json"
        import json
        with open(filename, 'w') as f:
            json.dump(service.state.dict(), f, indent=2)
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
