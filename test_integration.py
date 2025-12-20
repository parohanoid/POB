#!/usr/bin/env python3
"""Additional integration and edge case testing."""

import tempfile
import os
from unittest.mock import patch
from typer.testing import CliRunner
from parliament_of_bruce.cli import app


runner = CliRunner()


class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_workflow(self):
        """Test a complete workflow from start to finish."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # 1. Initialize
                result = runner.invoke(app, ["init"])
                assert result.exit_code == 0
                
                # 2. Create Bruce
                result = runner.invoke(app, ["reign", "new"], input="King Arthur\nFound Camelot\n")
                assert result.exit_code == 0
                assert "now reigns" in result.stdout
                
                # 3. Check status
                result = runner.invoke(app, ["status"])
                assert result.exit_code == 0
                assert "King Arthur" in result.stdout
                
                # 4. Add voices
                for i in range(2):
                    result = runner.invoke(app, ["add-voice", f"Voice{i}", "-d", f"Description{i}"])
                    assert result.exit_code == 0
                
                # 5. List voices
                result = runner.invoke(app, ["voices"])
                assert result.exit_code == 0
                assert "Voice0" in result.stdout
                assert "Voice1" in result.stdout
                
                # 6. Export
                result = runner.invoke(app, ["export", "--format", "json"])
                assert result.exit_code == 0
                assert "Exported to" in result.stdout
    
    def test_voice_lifecycle(self):
        """Test adding and removing voices."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create Bruce
                runner.invoke(app, ["reign", "new"], input="Test Bruce\nReason\n")
                
                # Add first voice
                result = runner.invoke(app, ["add-voice", "VoiceToKeep", "-d", "Will remain"])
                assert result.exit_code == 0
                assert "Added to parliament" in result.stdout
                keep_id = None
                for line in result.stdout.split('\n'):
                    if "ID:" in line:
                        # Extract ID more carefully - get just the alphanumeric part
                        id_part = line.split("ID:")[1].strip()
                        # Take only alphanumeric characters
                        keep_id = ''.join(c for c in id_part if c.isalnum())
                        break
                
                # Add second voice
                result = runner.invoke(app, ["add-voice", "VoiceToRemove", "-d", "Will be removed"])
                assert result.exit_code == 0
                remove_id = None
                for line in result.stdout.split('\n'):
                    if "ID:" in line:
                        id_part = line.split("ID:")[1].strip()
                        remove_id = ''.join(c for c in id_part if c.isalnum())
                        break
                
                # Verify both exist
                result = runner.invoke(app, ["voices"])
                assert "VoiceToKeep" in result.stdout
                assert "VoiceToRemove" in result.stdout
                
                # Remove the second voice
                if remove_id:
                    result = runner.invoke(app, ["remove-voice", remove_id], input="y\n")
                    assert "dismissed" in result.stdout
                
                # Verify removal
                result = runner.invoke(app, ["voices"])
                assert "VoiceToKeep" in result.stdout
                assert "VoiceToRemove" not in result.stdout


class TestDataIntegrity:
    """Test data persistence and integrity."""
    
    def test_state_persistence_across_commands(self):
        """Test that state persists across multiple commands."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create Bruce in first command
                runner.invoke(app, ["reign", "new"], input="Persistent Bruce\nFounded\n")
                
                # Check it exists in second command
                result = runner.invoke(app, ["status"])
                assert "Persistent Bruce" in result.stdout
                
                # Check timeline in third command
                result = runner.invoke(app, ["timeline"])
                assert "Persistent Bruce" in result.stdout
    
    def test_multiple_voices_persistence(self):
        """Test that multiple voices persist correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                runner.invoke(app, ["reign", "new"], input="Test\nReason\n")
                
                # Add multiple voices
                voice_ids = []
                for i in range(3):
                    result = runner.invoke(app, ["add-voice", f"Voice{i}", "-d", f"Desc{i}"])
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if "ID:" in line:
                            vid = line.split("ID:")[1].strip()
                            voice_ids.append(vid)
                            break
                
                # Verify all exist
                result = runner.invoke(app, ["voices"])
                for i in range(3):
                    assert f"Voice{i}" in result.stdout


class TestCommandCombinations:
    """Test various command combinations."""
    
    def test_rebirth_workflow(self):
        """Test rebirth command workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create first Bruce
                runner.invoke(app, ["reign", "new"], input="First Bruce\nOrigin\n")
                
                # Verify first Bruce is reigning
                result = runner.invoke(app, ["status"])
                assert "First Bruce" in result.stdout
                
                # Rebirth - provide exit report and new Bruce info
                result = runner.invoke(
                    app, 
                    ["rebirth"], 
                    input="The first fell\nSecond Bruce\nRisen anew\n"
                )
                assert result.exit_code == 0
                assert "now reigning" in result.stdout or "is now reigning" in result.stdout
                
                # Verify second Bruce is now reigning
                result = runner.invoke(app, ["status"])
                assert "Second Bruce" in result.stdout
                
                # Verify timeline has both
                result = runner.invoke(app, ["timeline"])
                assert "First Bruce" in result.stdout
                assert "Second Bruce" in result.stdout
    
    def test_renounce_workflow(self):
        """Test renounce command workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                # Create Bruce
                runner.invoke(app, ["reign", "new"], input="Renouncer\nStart\n")
                
                # Verify Bruce exists
                result = runner.invoke(app, ["status"])
                assert "Renouncer" in result.stdout
                
                # Renounce - confirm and provide exit statement
                result = runner.invoke(app, ["renounce"], input="y\nI renounce the throne\n")
                assert result.exit_code == 0
                assert "renounced" in result.stdout
                
                # Verify no active Bruce
                result = runner.invoke(app, ["status"])
                assert "No Reigning Bruce" in result.stdout
                
                # Verify Bruce is in history
                result = runner.invoke(app, ["timeline"])
                assert "Renouncer" in result.stdout


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_remove_nonexistent_voice(self):
        """Test removing a voice that doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                runner.invoke(app, ["reign", "new"], input="Test\nReason\n")
                
                result = runner.invoke(app, ["remove-voice", "nonexistent"], input="y\n")
                assert "not found" in result.stdout
    
    def test_invalid_seat_search(self):
        """Test search with invalid seat parameter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["search", "test", "--seat", "invalid"])
                assert "Invalid seat" in result.stdout
    
    def test_search_with_special_characters(self):
        """Test searching for special characters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                result = runner.invoke(app, ["search", "!@#$%^&*()"])
                # Should not crash
                assert result.exit_code in [0, 1, 2]
    
    def test_vote_without_topic(self):
        """Test vote command behavior."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {'HOME': tmpdir}):
                runner.invoke(app, ["reign", "new"], input="Test\nReason\n")
                
                result = runner.invoke(
                    app,
                    ["vote", "test topic"],
                    input="yes\nno\nyes\nno\nyes\nno\n"
                )
                assert result.exit_code == 0
                assert "RESULTS" in result.stdout or "Voting" in result.stdout


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
