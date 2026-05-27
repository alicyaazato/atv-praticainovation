"""
Input Validators Module

This module provides validation functions for the calculate_progress script.
Validates user IDs, subject IDs, date formats, and date ranges.
"""

import re
from typing import Optional
from datetime import datetime


def validate_user_id(user_id: int) -> bool:
    """
    Validate that user_id is a valid positive integer.
    
    Args:
        user_id: The user ID to validate
    
    Returns:
        bool: True if valid, raises ValueError otherwise
    
    Raises:
        ValueError: If user_id is invalid
    
    Example:
        >>> validate_user_id(1)
        True
        >>> validate_user_id(-1)
        Traceback (most recent call last):
            ...
        ValueError: user_id must be a positive integer, got: -1
    """
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise ValueError(f"user_id must be an integer, got: {type(user_id).__name__}")
    
    if user_id <= 0:
        raise ValueError(f"user_id must be a positive integer, got: {user_id}")
    
    return True


def validate_subject_id(subject_id: int) -> bool:
    """
    Validate that subject_id is a valid positive integer.
    
    Args:
        subject_id: The subject ID to validate
    
    Returns:
        bool: True if valid, raises ValueError otherwise
    
    Raises:
        ValueError: If subject_id is invalid
    
    Example:
        >>> validate_subject_id(5)
        True
        >>> validate_subject_id(0)
        Traceback (most recent call last):
            ...
        ValueError: subject_id must be a positive integer, got: 0
    """
    try:
        subject_id = int(subject_id)
    except (TypeError, ValueError):
        raise ValueError(f"subject_id must be an integer, got: {type(subject_id).__name__}")
    
    if subject_id <= 0:
        raise ValueError(f"subject_id must be a positive integer, got: {subject_id}")
    
    return True


def validate_date_format(date_str: Optional[str]) -> bool:
    """
    Validate that date_str is in YYYY-MM-DD format.
    
    Args:
        date_str: The date string to validate (can be None)
    
    Returns:
        bool: True if valid or None, raises ValueError otherwise
    
    Raises:
        ValueError: If date format is invalid
    
    Example:
        >>> validate_date_format("2026-05-26")
        True
        >>> validate_date_format(None)
        True
        >>> validate_date_format("26-05-2026")
        Traceback (most recent call last):
            ...
        ValueError: Date must be in YYYY-MM-DD format, got: 26-05-2026
    """
    if date_str is None:
        return True
    
    if not isinstance(date_str, str):
        raise ValueError(
            f"date must be a string in YYYY-MM-DD format, got: {type(date_str).__name__}"
        )
    
    # Pattern: YYYY-MM-DD
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_pattern, date_str):
        raise ValueError(
            f"Date must be in YYYY-MM-DD format, got: {date_str}"
        )
    
    # Verify it's a valid date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date value: {date_str} is not a valid date"
        )
    
    return True


def validate_date_range(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> bool:
    """
    Validate that start_date and end_date form a valid range.
    
    Args:
        start_date: Optional start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format
    
    Returns:
        bool: True if valid, raises ValueError otherwise
    
    Raises:
        ValueError: If date range is invalid
    
    Example:
        >>> validate_date_range("2026-01-01", "2026-05-26")
        True
        >>> validate_date_range("2026-05-26", "2026-01-01")
        Traceback (most recent call last):
            ...
        ValueError: start_date must be before end_date, got: 2026-05-26 > 2026-01-01
    """
    # Both None is valid
    if start_date is None and end_date is None:
        return True
    
    # Validate individual formats first
    validate_date_format(start_date)
    validate_date_format(end_date)
    
    # If both provided, check the range
    if start_date is not None and end_date is not None:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start > end:
            raise ValueError(
                f"start_date must be before end_date, got: {start_date} > {end_date}"
            )
    
    return True
