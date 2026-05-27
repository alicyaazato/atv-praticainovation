"""
Unit Tests for calculate_progress module

Tests validators, helper functions, and core logic.
"""

import unittest
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import (
    validate_user_id,
    validate_subject_id,
    validate_date_format,
    validate_date_range,
)


class TestValidateUserId(unittest.TestCase):
    """Tests for validate_user_id function."""
    
    def test_valid_positive_integer(self):
        """Test with valid positive integer."""
        self.assertTrue(validate_user_id(1))
        self.assertTrue(validate_user_id(100))
        self.assertTrue(validate_user_id(999999))
    
    def test_string_integer(self):
        """Test with string that can be converted to integer."""
        self.assertTrue(validate_user_id("42"))
    
    def test_invalid_zero(self):
        """Test with zero."""
        with self.assertRaises(ValueError) as context:
            validate_user_id(0)
        self.assertIn("positive integer", str(context.exception))
    
    def test_invalid_negative(self):
        """Test with negative integer."""
        with self.assertRaises(ValueError) as context:
            validate_user_id(-1)
        self.assertIn("positive integer", str(context.exception))
    
    def test_invalid_non_integer(self):
        """Test with non-integer type."""
        with self.assertRaises(ValueError) as context:
            validate_user_id("abc")
        self.assertIn("must be an integer", str(context.exception))
    
    def test_invalid_none(self):
        """Test with None."""
        with self.assertRaises(ValueError):
            validate_user_id(None)


class TestValidateSubjectId(unittest.TestCase):
    """Tests for validate_subject_id function."""
    
    def test_valid_positive_integer(self):
        """Test with valid positive integer."""
        self.assertTrue(validate_subject_id(1))
        self.assertTrue(validate_subject_id(5))
        self.assertTrue(validate_subject_id(100000))
    
    def test_string_integer(self):
        """Test with string that can be converted to integer."""
        self.assertTrue(validate_subject_id("7"))
    
    def test_invalid_zero(self):
        """Test with zero."""
        with self.assertRaises(ValueError) as context:
            validate_subject_id(0)
        self.assertIn("positive integer", str(context.exception))
    
    def test_invalid_negative(self):
        """Test with negative integer."""
        with self.assertRaises(ValueError):
            validate_subject_id(-5)
    
    def test_invalid_non_integer(self):
        """Test with non-integer type."""
        with self.assertRaises(ValueError):
            validate_subject_id("not_a_number")


class TestValidateDateFormat(unittest.TestCase):
    """Tests for validate_date_format function."""
    
    def test_valid_date_format(self):
        """Test with valid YYYY-MM-DD format."""
        self.assertTrue(validate_date_format("2026-05-26"))
        self.assertTrue(validate_date_format("2026-01-01"))
        self.assertTrue(validate_date_format("2025-12-31"))
    
    def test_none_value(self):
        """Test with None (should be valid)."""
        self.assertTrue(validate_date_format(None))
    
    def test_invalid_format_dmy(self):
        """Test with DD-MM-YYYY format."""
        with self.assertRaises(ValueError) as context:
            validate_date_format("26-05-2026")
        self.assertIn("YYYY-MM-DD", str(context.exception))
    
    def test_invalid_format_mdy(self):
        """Test with MM-DD-YYYY format."""
        with self.assertRaises(ValueError):
            validate_date_format("05-26-2026")
    
    def test_invalid_date_value(self):
        """Test with invalid date value (e.g., month 13)."""
        with self.assertRaises(ValueError) as context:
            validate_date_format("2026-13-01")
        self.assertIn("not a valid date", str(context.exception))
    
    def test_invalid_day_value(self):
        """Test with invalid day value (e.g., day 32)."""
        with self.assertRaises(ValueError):
            validate_date_format("2026-05-32")
    
    def test_non_string_type(self):
        """Test with non-string type."""
        with self.assertRaises(ValueError) as context:
            validate_date_format(12345)
        self.assertIn("must be a string", str(context.exception))
    
    def test_empty_string(self):
        """Test with empty string."""
        with self.assertRaises(ValueError):
            validate_date_format("")
    
    def test_leap_year_date(self):
        """Test with valid leap year date."""
        self.assertTrue(validate_date_format("2024-02-29"))
    
    def test_non_leap_year_feb_29(self):
        """Test with February 29 in non-leap year."""
        with self.assertRaises(ValueError):
            validate_date_format("2025-02-29")


class TestValidateDateRange(unittest.TestCase):
    """Tests for validate_date_range function."""
    
    def test_valid_range(self):
        """Test with valid date range."""
        self.assertTrue(
            validate_date_range("2026-01-01", "2026-05-26")
        )
        self.assertTrue(
            validate_date_range("2026-01-01", "2026-01-01")
        )
    
    def test_both_none(self):
        """Test with both dates None."""
        self.assertTrue(validate_date_range(None, None))
    
    def test_start_date_only(self):
        """Test with only start_date."""
        self.assertTrue(validate_date_range("2026-01-01", None))
    
    def test_end_date_only(self):
        """Test with only end_date."""
        self.assertTrue(validate_date_range(None, "2026-05-26"))
    
    def test_invalid_range_start_after_end(self):
        """Test with start_date after end_date."""
        with self.assertRaises(ValueError) as context:
            validate_date_range("2026-05-26", "2026-01-01")
        self.assertIn("start_date must be before end_date", str(context.exception))
    
    def test_invalid_start_format(self):
        """Test with invalid start_date format."""
        with self.assertRaises(ValueError):
            validate_date_range("26-05-2026", "2026-05-26")
    
    def test_invalid_end_format(self):
        """Test with invalid end_date format."""
        with self.assertRaises(ValueError):
            validate_date_range("2026-01-01", "26-05-2026")


class TestProgressCalculation(unittest.TestCase):
    """Tests for progress calculation logic."""
    
    def test_calculate_progress_zero_tasks(self):
        """Test progress calculation with zero tasks."""
        from calculate_progress import _calculate_progress_from_tasks
        
        tasks = []
        result = _calculate_progress_from_tasks(tasks)
        
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["completed"], 0)
        self.assertEqual(result["progress_percentage"], 0.0)
    
    def test_calculate_progress_all_completed(self):
        """Test progress calculation with all tasks completed."""
        from calculate_progress import _calculate_progress_from_tasks
        
        tasks = [
            {"id": 1, "status": "completed"},
            {"id": 2, "status": "completed"},
            {"id": 3, "status": "completed"},
        ]
        result = _calculate_progress_from_tasks(tasks)
        
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["completed"], 3)
        self.assertEqual(result["progress_percentage"], 100.0)
    
    def test_calculate_progress_mixed_statuses(self):
        """Test progress calculation with mixed task statuses."""
        from calculate_progress import _calculate_progress_from_tasks
        
        tasks = [
            {"id": 1, "status": "completed"},
            {"id": 2, "status": "completed"},
            {"id": 3, "status": "pending"},
            {"id": 4, "status": "in_progress"},
            {"id": 5, "status": "overdue"},
        ]
        result = _calculate_progress_from_tasks(tasks)
        
        self.assertEqual(result["total"], 5)
        self.assertEqual(result["completed"], 2)
        self.assertEqual(result["pending"], 1)
        self.assertEqual(result["in_progress"], 1)
        self.assertEqual(result["overdue"], 1)
        self.assertEqual(result["progress_percentage"], 40.0)
    
    def test_calculate_progress_percentage_rounding(self):
        """Test that progress percentage is rounded to 2 decimal places."""
        from calculate_progress import _calculate_progress_from_tasks
        
        tasks = [
            {"status": "completed"},
            {"status": "completed"},
            {"status": "pending"},
        ]
        result = _calculate_progress_from_tasks(tasks)
        
        self.assertEqual(result["progress_percentage"], 66.67)
    
    def test_build_success_response(self):
        """Test building a success response."""
        from calculate_progress import build_response
        
        progress_data = {
            "completed": 10,
            "pending": 2,
            "in_progress": 1,
            "overdue": 0,
            "total": 13,
            "progress_percentage": 76.92,
        }
        
        response = build_response(
            user_id=1,
            subject_id=5,
            progress_data=progress_data,
            subject_name="Mathematics",
            period={"start_date": "2026-01-01", "end_date": "2026-05-26"},
        )
        
        self.assertTrue(response["success"])
        self.assertIsNone(response["error"])
        self.assertEqual(response["data"]["user_id"], 1)
        self.assertEqual(response["data"]["subject_id"], 5)
        self.assertEqual(response["data"]["subject_name"], "Mathematics")
        self.assertEqual(response["data"]["progress_percentage"], 76.92)
        self.assertEqual(response["data"]["tasks"]["total"], 13)
        self.assertEqual(response["data"]["tasks"]["completed"], 10)
        self.assertIn("calculated_at", response["data"])
    
    def test_build_error_response(self):
        """Test building an error response."""
        from calculate_progress import build_error_response
        
        response = build_error_response(
            error_code="USER_NOT_FOUND",
            error_message="User with ID 999 not found",
            status_code=400,
        )
        
        self.assertFalse(response["success"])
        self.assertIsNone(response["data"])
        self.assertEqual(response["error"]["code"], "USER_NOT_FOUND")
        self.assertEqual(response["error"]["message"], "User with ID 999 not found")
        self.assertEqual(response["error"]["status_code"], 400)


if __name__ == "__main__":
    unittest.main()
