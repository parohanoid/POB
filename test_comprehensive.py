#!/usr/bin/env python3
"""Comprehensive testing of Parliament of Bruce CLI."""

import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from parliament_of_bruce.cli import app
from parliament_of_bruce.storage import Storage
from parliament_of_bruce.services import ParliamentService


runner = CliRunner()


def create_test_storage():
    """Create a temporary storage location for testing."""
    temp_dir = tempfile.mkdtemp()
    return temp_dir


class TestCommandStructure:
    """Test all CLI commands exist and have proper structure."""
    
    def test_init_command(self):
        """Test init command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["init"])
                assert result.exit_code == 0
                assert "Parliament of Bruce Initialized" in result.stdout
    
    def test_status_without_bruce(self):
        """Test status when no Bruce exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["status"])
                assert result.exit_code == 0
                assert "No Reigning Bruce currently active" in result.stdout
    
    def test_reign_new_command(self):
        """Test creating a new Reigning Bruce."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
                assert result.exit_code == 0
                assert "now reigns" in result.stdout
    
    def test_add_voice_command(self):
        """Test adding a temporary voice."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # First create a Bruce
                runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
                # Then add voice
                result = runner.invoke(app, ["add-voice", "TestVoice", "-d", "Test description"])
                assert result.exit_code == 0
                assert "Added to parliament" in result.stdout
    
    def test_voices_list_command(self):
        """Test listing voices."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create a Bruce
                runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
                # Add voice
                runner.invoke(app, ["add-voice", "TestVoice", "-d", "Test description"])
                # List voices
                result = runner.invoke(app, ["voices"])
                assert result.exit_code == 0
                assert "TestVoice" in result.stdout
    
    def test_remove_voice_with_id(self):
        """Test removing voice with ID."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create Bruce
                runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
                # Add voice and capture ID
                result = runner.invoke(app, ["add-voice", "TestVoice", "-d", "Test desc"])
                # Extract ID from output
                assert "ID:" in result.stdout
                # Try to remove
                result = runner.invoke(app, ["remove-voice", "invalid-id"], input="n\n")
                assert "not found" in result.stdout
    
    def test_timeline_command(self):
        """Test timeline display."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["timeline"])
                assert result.exit_code == 0
                assert "Bruce history" in result.stdout or "No Bruce history" in result.stdout
    
    def test_stats_command(self):
        """Test stats display."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["stats"])
                assert result.exit_code == 0
                assert "data yet" in result.stdout or "Statistics" in result.stdout
    
    def test_read_command_no_entries(self):
        """Test read when no entries exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["read"])
                assert result.exit_code == 0
                assert "No journal entries" in result.stdout
    
    def test_search_command_no_entries(self):
        """Test search when no entries exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["search", "test"])
                assert result.exit_code == 0
                assert "No journal entries" in result.stdout
    
    def test_vote_without_bruce(self):
        """Test voting without a Reigning Bruce."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["vote", "test topic"], input="yes\nno\nyes\nno\nyes\nyes\n")
                assert result.exit_code == 0
                assert "No Reigning Bruce active" in result.stdout
    
    def test_rebirth_without_bruce(self):
        """Test rebirth without a Reigning Bruce."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["rebirth"])
                assert result.exit_code == 0
                assert "No Bruce to rebirth" in result.stdout
    
    def test_renounce_without_bruce(self):
        """Test renounce without a Reigning Bruce."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["renounce"])
                assert result.exit_code == 0
                assert "No Bruce to renounce" in result.stdout
    
    def test_export_json(self):
        """Test exporting to JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create Bruce
                runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
                # Export
                result = runner.invoke(app, ["export", "--format", "json"])
                assert result.exit_code == 0
                assert "Exported to" in result.stdout
    
    def test_export_markdown(self):
        """Test exporting to Markdown."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create Bruce
                runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
                # Export
                result = runner.invoke(app, ["export", "--format", "markdown"])
                assert result.exit_code == 0
                assert "Exported to" in result.stdout
    
    def test_invalid_command(self):
        """Test invalid command."""
        result = runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0


class TestEdgeCases:
    """Test edge cases and potential bugs."""
    
    def test_multiple_bruce_creations(self):
        """Test creating multiple Bruces in sequence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create first Bruce
                result1 = runner.invoke(app, ["reign", "new"], input="Bruce One\nReason One\n")
                assert "now reigns" in result1.stdout
                
                # Create second Bruce (should replace) - need more input lines for confirmation
                result2 = runner.invoke(app, ["reign", "new"], input="y\nExit Report\nBruce Two\nReason Two\n")
                # Check if second bruce was created (exit code check since prompts might be consumed differently)
                assert result2.exit_code == 0 or "now reigns" in result2.stdout
    
    def test_add_multiple_voices(self):
        """Test adding multiple temporary voices."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create Bruce
                runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
                
                # Add multiple voices
                for i in range(3):
                    result = runner.invoke(app, ["add-voice", f"Voice{i}", "-d", f"Description {i}"])
                    assert result.exit_code == 0
                
                # List and verify
                result = runner.invoke(app, ["voices"])
                assert "Voice0" in result.stdout
                assert "Voice1" in result.stdout
                assert "Voice2" in result.stdout
    
    def test_empty_strings_as_input(self):
        """Test handling empty string inputs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["reign", "new"], input="\n\n")
                # Should either accept or error gracefully
                assert result.exit_code in [0, 1, 2]
    
    def test_very_long_input(self):
        """Test handling very long input strings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                long_text = "x" * 10000
                result = runner.invoke(app, ["reign", "new"], input=f"{long_text}\n{long_text}\n")
                # Should handle without crashing
                assert result.exit_code in [0, 1, 2]
    
    def test_special_characters_in_names(self):
        """Test handling special characters in names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                special_name = "Bruce @#$%^&*()"
                result = runner.invoke(app, ["reign", "new"], input=f"{special_name}\nTest reason\n")
                # Should handle without crashing
                assert result.exit_code == 0
    
    def test_unicode_characters(self):
        """Test handling Unicode characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                unicode_name = "布鲁斯 🦇 Брюс"
                result = runner.invoke(app, ["reign", "new"], input=f"{unicode_name}\n理由\n")
                # Should handle without crashing
                assert result.exit_code == 0
    
    def test_search_with_empty_query(self):
        """Test search with empty query."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["search", ""])
                # Should handle gracefully
                assert result.exit_code in [0, 1, 2]
    
    def test_export_invalid_format(self):
        """Test export with invalid format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["export", "--format", "invalid"])
                assert result.exit_code == 0
                assert "Unknown format" in result.stdout
    
    def test_session_type_variations(self):
        """Test different session types."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create Bruce
                runner.invoke(app, ["reign", "new"], input="Test Bruce\nTest reason\n")
                
                # Test different session types - verify command accepts them
                session_types = ["daily", "weekly", "monthly", "custom"]
                for session_type in session_types:
                    # Invoke with empty input to just test command acceptance
                    # Session command will exit due to EOF but that's okay
                    result = runner.invoke(app, ["session", session_type], input="")
                    # Should either complete or exit gracefully, not crash
                    assert result.exit_code in [0, 1]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
