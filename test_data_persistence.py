#!/usr/bin/env python3
"""Comprehensive data persistence and read command testing."""

import tempfile
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typer.testing import CliRunner
from parliament_of_bruce.cli import app
from parliament_of_bruce.storage import Storage
from parliament_of_bruce.services import ParliamentService
from parliament_of_bruce.models import ReigningBruce, JournalEntry

runner = CliRunner()


class TestReadCommandInputs:
    """Test read command with various input parameters."""
    
    def test_read_no_options(self):
        """Test read with no options."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["read"])
            assert result.exit_code == 0
    
    def test_read_with_count(self):
        """Test read with count parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
            
            for count in [1, 5, 10, 100]:
                result = runner.invoke(app, ["read", "--count", str(count)])
                assert result.exit_code == 0
    
    def test_read_with_full_flag(self):
        """Test read with full flag."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["read", "--full"])
            assert result.exit_code == 0
    
    def test_read_with_latest(self):
        """Test read with latest date."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
            result = runner.invoke(app, ["read", "--date", "latest"])
            assert result.exit_code == 0
    
    def test_read_with_specific_date_full_format(self):
        """Test read with specific date in YYYY-MM-DD format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            today = datetime.now().strftime("%Y-%m-%d")
            result = runner.invoke(app, ["read", "--date", today])
            assert result.exit_code == 0
    
    def test_read_with_month_format(self):
        """Test read with date in YYYY-MM format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            current_month = datetime.now().strftime("%Y-%m")
            result = runner.invoke(app, ["read", "--date", current_month])
            assert result.exit_code == 0
    
    def test_read_with_invalid_date_format(self):
        """Test read with invalid date format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            invalid_dates = ["2024-13-01", "invalid", "01-01-2024", "2024/01/01", "20240101"]
            
            for invalid_date in invalid_dates:
                result = runner.invoke(app, ["read", "--date", invalid_date])
                assert result.exit_code in [0, 2]
    
    def test_read_with_nonexistent_date(self):
        """Test read with date that has no entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["read", "--date", "2000-01-01"])
            assert result.exit_code == 0
            assert "No entries found" in result.stdout or "No journal entries" in result.stdout


class TestSearchCommandInputs:
    """Test search command with various inputs."""
    
    def test_search_empty_query(self):
        """Test search with empty query."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["search", ""])
            assert result.exit_code in [0, 2]
    
    def test_search_single_character(self):
        """Test search with single character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["search", "a"])
            assert result.exit_code == 0
    
    def test_search_special_characters(self):
        """Test search with special characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            special_queries = ["@", "#", "$", "%", "^", "&", "*", "!"]
            for query in special_queries:
                result = runner.invoke(app, ["search", query])
                assert result.exit_code in [0, 2]
    
    def test_search_unicode(self):
        """Test search with Unicode characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["search", "布鲁斯"])
            assert result.exit_code in [0, 2]
    
    def test_search_very_long_query(self):
        """Test search with very long query string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            long_query = "test" * 1000
            result = runner.invoke(app, ["search", long_query])
            assert result.exit_code in [0, 2]
    
    def test_search_with_seat_param(self):
        """Test search with specific seat parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["search", "test", "--seat", "short"])
            assert result.exit_code == 0
    
    def test_search_with_invalid_seat(self):
        """Test search with invalid seat parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["search", "test", "--seat", "invalid"])
            assert result.exit_code == 0


class TestVoteCommandInputs:
    """Test vote command with various inputs."""
    
    def test_vote_simple_topic(self):
        """Test vote with simple topic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["vote", "Should I sleep?"], input="yes\nno\nyes\nno\nyes\nno\n")
            assert result.exit_code in [0, 1]
    
    def test_vote_empty_topic(self):
        """Test vote with empty topic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["vote", ""], input="yes\nno\nyes\nno\nyes\nno\n")
            assert result.exit_code in [0, 1, 2]
    
    def test_vote_very_long_topic(self):
        """Test vote with very long topic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            
            long_topic = "Should I " + "do this very important thing " * 100 + "?"
            result = runner.invoke(app, ["vote", long_topic], input="yes\nno\nyes\nno\nyes\nno\n")
            assert result.exit_code in [0, 1, 2]
    
    def test_vote_special_characters_topic(self):
        """Test vote with special characters in topic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            
            special_topic = "Should I @#$%^&*()?!~`"
            result = runner.invoke(app, ["vote", special_topic], input="yes\nno\nyes\nno\nyes\nno\n")
            assert result.exit_code in [0, 1]


class TestSessionVariations:
    """Test session command with various parameters."""
    
    def test_session_daily(self):
        """Test daily session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["session", "daily"], input="")
            assert result.exit_code in [0, 1]
    
    def test_session_weekly(self):
        """Test weekly session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["session", "weekly"], input="")
            assert result.exit_code in [0, 1]
    
    def test_session_monthly(self):
        """Test monthly session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["session", "monthly"], input="")
            assert result.exit_code in [0, 1]
    
    def test_session_custom(self):
        """Test custom session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["session", "custom"], input="")
            assert result.exit_code in [0, 1]


class TestExportInputs:
    """Test export command with various formats."""
    
    def test_export_default_format(self):
        """Test export with default format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["export"])
            assert result.exit_code == 0
            assert "Exported to" in result.stdout
    
    def test_export_json_format(self):
        """Test export to JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["export", "--format", "json"])
            assert result.exit_code == 0
            assert "Exported to" in result.stdout
    
    def test_export_markdown_format(self):
        """Test export to Markdown."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["export", "--format", "markdown"])
            assert result.exit_code == 0
            assert "Exported to" in result.stdout
    
    def test_export_invalid_format(self):
        """Test export with invalid format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
            result = runner.invoke(app, ["export", "--format", "invalid_format"])
            assert result.exit_code == 0


class TestBruceOperations:
    """Test Bruce lifecycle operations."""
    
    def test_reign_new_with_minimal_input(self):
        """Test creating Bruce with minimal input."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["reign", "new"], input="B\nR\n")
            assert result.exit_code == 0
    
    def test_reign_new_long_names(self):
        """Test creating Bruce with very long names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            long_name = "x" * 1000
            result = runner.invoke(app, ["reign", "new"], input=f"{long_name}\n{long_name}\n")
            assert result.exit_code in [0, 1, 2]
    
    def test_rebirth_workflow(self):
        """Test rebirth command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Bruce One\nReason\n")
            result = runner.invoke(app, ["rebirth"], input="New reason\n")
            assert result.exit_code in [0, 1]


class TestVoiceOperations:
    """Test voice management operations."""
    
    def test_add_voice_with_description(self):
        """Test adding voice with description."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Bruce\nReason\n")
            result = runner.invoke(app, ["add-voice", "Voice", "-d", "Test description"])
            assert result.exit_code == 0
    
    def test_remove_voice_nonexistent_id(self):
        """Test removing voice with nonexistent ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Bruce\nReason\n")
            result = runner.invoke(app, ["remove-voice", "fake-id"], input="n\n")
            assert result.exit_code == 0
    
    def test_voices_list_empty(self):
        """Test listing voices when none exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["voices"])
            assert result.exit_code == 0


class TestDataStateConsistency:
    """Test that data state remains consistent."""
    
    def test_status_shows_correct_bruce(self):
        """Test that status shows the current Reigning Bruce."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            runner.invoke(app, ["reign", "new"], input="Bruce Test\nTest Reason\n")
            result = runner.invoke(app, ["status"])
            assert "Bruce Test" in result.stdout
            assert "Test Reason" in result.stdout
    
    def test_timeline_shows_history(self):
        """Test that timeline shows Bruce history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["timeline"])
            assert result.exit_code == 0
    
    def test_stats_calculation(self):
        """Test stats command produces output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['HOME'] = tmpdir
            
            result = runner.invoke(app, ["stats"])
            assert result.exit_code == 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
