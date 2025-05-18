"""
Tests for error handling in rule generators.
"""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from airulefy.config import SyncMode, ToolConfig
from airulefy.generator.base import RuleGenerator


class TestGeneratorErrorHandling:
    """Test error handling in RuleGenerator."""

    class TestGenerator(RuleGenerator):
        """Test implementation of RuleGenerator."""
        
        def transform_content(self, content: str) -> str:
            """Implement required abstract method."""
            return content

    def test_generate_no_files(self, tmp_path):
        """Test generate method with no input files."""
        # Create a generator
        config = ToolConfig()
        generator = self.TestGenerator("test", config, tmp_path)
        
        # Call generate with empty list
        result = generator.generate([])
        
        # Check result
        assert result is False

    def test_generate_temporary_file_error(self, tmp_path):
        """Test generate method when temporary file creation fails."""
        # Create a test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Content")
        
        # Create a generator
        config = ToolConfig()
        generator = self.TestGenerator("test", config, tmp_path)
        
        # ケース1: 単一ファイルでsymlink以外の場合に例外処理が機能するか確認
        with patch('airulefy.generator.base.NamedTemporaryFile',
                   side_effect=IOError("Mocked temporary file error")):
            with patch('builtins.print') as mock_print:
                # Call generate with COPY mode to ensure we go into the try block
                result = generator.generate([test_file], force_mode=SyncMode.COPY)
                
                # Check that error was printed and result is False
                mock_print.assert_called_once()
                assert result is False

    def test_generate_sync_failure(self, tmp_path):
        """Test generate method when sync_file fails."""
        # Create a test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Content")
        
        # Create a generator
        config = ToolConfig()
        generator = self.TestGenerator("test", config, tmp_path)
        
        # Mock sync_file to return False
        with patch('airulefy.generator.base.sync_file', return_value=False):
            # Call generate
            result = generator.generate([test_file])
            
            # Check result
            assert result is False

    def test_generate_exception_handling(self, tmp_path):
        """Test generate method handles exceptions gracefully."""
        # Create a test file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Content")
        test_file2 = tmp_path / "test2.md"
        test_file2.write_text("# Test Content 2")
        
        # Create a generator
        config = ToolConfig()
        generator = self.TestGenerator("test", config, tmp_path)
        
        # Mock combining function to raise an exception
        with patch('airulefy.generator.base.combine_markdown_files', 
                   side_effect=Exception("Unexpected error")):
            # Capture output to verify error message
            with patch('builtins.print') as mock_print:
                # Call generate with multiple files to ensure combine_markdown_files is called
                result = generator.generate([test_file, test_file2], force_mode=SyncMode.COPY)
                
                # Check result
                assert result is False
                
                # Verify error message was printed
                mock_print.assert_called_once()
