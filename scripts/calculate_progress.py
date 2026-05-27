"""
Calculate Progress Script

This module provides functionality to calculate student progress in academic subjects
by computing the percentage of completed tasks out of total tasks.

Main Function:
    calculate_progress: Calculate progress percentage for a student in a subject

Author: EduTrack AI
Version: 1.0.0
"""

import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from utils.validators import (
    validate_user_id,
    validate_subject_id,
    validate_date_format,
    validate_date_range,
)
from utils.database import (
    fetch_tasks_by_user_subject,
    fetch_subject_info,
    check_user_access,
    XanoDatabaseError,
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def calculate_progress(
    user_id: int,
    subject_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    include_metadata: bool = True,
) -> Dict[str, Any]:
    """
    Calculate the progress percentage for a student in a subject.
    
    Args:
        user_id: ID of the student user
        subject_id: ID of the subject
        start_date: Optional start date filter (YYYY-MM-DD format)
        end_date: Optional end date filter (YYYY-MM-DD format)
        include_metadata: Whether to include metadata in response (default: True)
    
    Returns:
        dict: Success response with progress data or error response
        
    Raises:
        ValueError: If inputs are invalid
        ConnectionError: If database connection fails
        PermissionError: If user doesn't have access to subject
    
    Example:
        >>> result = calculate_progress(user_id=1, subject_id=5)
        >>> print(result['data']['progress_percentage'])
        75.5
    """
    logger.info(f"Calculating progress for user {user_id} in subject {subject_id}")
    
    try:
        # Phase 1: Validate inputs
        validate_user_id(user_id)
        validate_subject_id(subject_id)
        validate_date_format(start_date)
        validate_date_format(end_date)
        validate_date_range(start_date, end_date)
        logger.debug("Input validation passed")
        
        # Phase 2: Check user access and fetch subject info
        if not check_user_access(user_id, subject_id):
            raise PermissionError(
                f"User {user_id} does not have access to subject {subject_id}"
            )
        logger.debug(f"Access verified for user {user_id}")
        
        subject_info = fetch_subject_info(subject_id)
        subject_name = subject_info.get("name", "Unknown Subject")
        logger.debug(f"Retrieved subject: {subject_name}")
        
        # Phase 3: Fetch tasks and calculate progress
        tasks = fetch_tasks_by_user_subject(user_id, subject_id, start_date, end_date)
        logger.debug(f"Retrieved {len(tasks)} tasks")
        
        progress_data = _calculate_progress_from_tasks(tasks)
        logger.debug(f"Progress calculated: {progress_data}")
        
        # Phase 4: Build and return response
        period = None
        if include_metadata:
            period = {
                "start_date": start_date,
                "end_date": end_date,
            }
        
        response = build_response(
            user_id=user_id,
            subject_id=subject_id,
            progress_data=progress_data,
            subject_name=subject_name,
            period=period,
        )
        
        logger.info(
            f"Progress calculation complete for user {user_id} in subject {subject_id}: "
            f"{progress_data['progress_percentage']}%"
        )
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return build_error_response("VALIDATION_ERROR", str(e), 400)
    except PermissionError as e:
        logger.error(f"Access denied: {str(e)}")
        return build_error_response("ACCESS_DENIED", str(e), 403)
    except XanoDatabaseError as e:
        logger.error(f"Database error: {str(e)}")
        return build_error_response("DATABASE_ERROR", str(e), 500)
    except ConnectionError as e:
        logger.error(f"Database connection error: {str(e)}")
        return build_error_response("DATABASE_CONNECTION_ERROR", str(e), 500)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return build_error_response("INTERNAL_ERROR", str(e), 500)


def _calculate_progress_from_tasks(tasks: list) -> Dict[str, Any]:
    """
    Count tasks by status and calculate progress percentage.
    
    Args:
        tasks: List of task dictionaries with 'status' field
    
    Returns:
        dict: Task counts and progress percentage
              {
                  "completed": 15,
                  "pending": 3,
                  "in_progress": 2,
                  "overdue": 1,
                  "total": 21,
                  "progress_percentage": 71.43
              }
    
    Example:
        >>> tasks = [
        ...     {"id": 1, "status": "completed"},
        ...     {"id": 2, "status": "pending"},
        ... ]
        >>> result = _calculate_progress_from_tasks(tasks)
        >>> print(result['progress_percentage'])
        50.0
    """
    # Initialize counters
    completed = 0
    pending = 0
    in_progress = 0
    overdue = 0
    total = len(tasks)
    
    logger.debug(f"Counting tasks from {total} tasks")
    
    # Count tasks by status
    for task in tasks:
        status = task.get("status", "").lower()
        
        if status == "completed":
            completed += 1
        elif status == "pending":
            pending += 1
        elif status == "in_progress":
            in_progress += 1
        elif status == "overdue":
            overdue += 1
        else:
            # Unknown status, count as pending
            logger.warning(f"Unknown task status: {status}, counting as pending")
            pending += 1
    
    # Calculate progress percentage
    # Division by zero handled: if total is 0, progress is 0
    if total == 0:
        progress_percentage = 0.0
        logger.debug("No tasks found, progress is 0%")
    else:
        progress_percentage = round((completed / total) * 100, 2)
        logger.debug(f"Progress: {completed}/{total} = {progress_percentage}%")
    
    return {
        "completed": completed,
        "pending": pending,
        "in_progress": in_progress,
        "overdue": overdue,
        "total": total,
        "progress_percentage": progress_percentage,
    }


def build_response(
    user_id: int,
    subject_id: int,
    progress_data: Dict[str, Any],
    subject_name: str,
    period: Optional[Dict[str, Optional[str]]] = None,
) -> Dict[str, Any]:
    """
    Build a success response JSON object following the specification schema.
    
    Args:
        user_id: ID of the student
        subject_id: ID of the subject
        progress_data: Dictionary with progress calculation data
        subject_name: Name of the subject
        period: Optional dict with start_date and end_date
    
    Returns:
        dict: Properly formatted success response with structure:
              {
                  "success": true,
                  "data": {
                      "user_id": 1,
                      "subject_id": 5,
                      "subject_name": "Matemática",
                      "progress_percentage": 75.5,
                      "tasks": {
                          "completed": 15,
                          "pending": 3,
                          "in_progress": 2,
                          "overdue": 1,
                          "total": 21
                      },
                      "calculated_at": "2026-05-26T14:30:00Z",
                      "period": {...}
                  },
                  "error": null
              }
    
    Example:
        >>> progress_data = {
        ...     "completed": 10,
        ...     "pending": 2,
        ...     "in_progress": 1,
        ...     "overdue": 0,
        ...     "total": 13,
        ...     "progress_percentage": 76.92
        ... }
        >>> response = build_response(1, 5, progress_data, "Math")
        >>> print(response['data']['progress_percentage'])
        76.92
    """
    logger.debug("Building success response")
    
    # Build tasks object
    tasks_obj = {
        "completed": progress_data.get("completed", 0),
        "pending": progress_data.get("pending", 0),
        "in_progress": progress_data.get("in_progress", 0),
        "overdue": progress_data.get("overdue", 0),
        "total": progress_data.get("total", 0),
    }
    
    # Build data object
    data = {
        "user_id": user_id,
        "subject_id": subject_id,
        "subject_name": subject_name,
        "progress_percentage": progress_data.get("progress_percentage", 0.0),
        "tasks": tasks_obj,
        "calculated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    
    # Add period if provided
    if period is not None:
        data["period"] = period
    
    # Build final response
    response = {
        "success": True,
        "data": data,
        "error": None,
    }
    
    logger.debug(f"Response built successfully")
    return response


def build_error_response(
    error_code: str,
    error_message: str,
    status_code: int,
) -> Dict[str, Any]:
    """
    Build an error response JSON object following the specification schema.
    
    Args:
        error_code: Error code identifier (e.g., 'USER_NOT_FOUND')
        error_message: Human-readable error message
        status_code: HTTP status code (400, 403, 500, etc.)
    
    Returns:
        dict: Properly formatted error response with structure:
              {
                  "success": false,
                  "data": null,
                  "error": {
                      "code": "USER_NOT_FOUND",
                      "message": "User with ID 999 not found",
                      "status_code": 400
                  }
              }
    
    Example:
        >>> response = build_error_response("USER_NOT_FOUND", "User 999 not found", 400)
        >>> print(response['success'])
        False
        >>> print(response['error']['code'])
        'USER_NOT_FOUND'
    """
    logger.debug(f"Building error response: {error_code}")
    
    response = {
        "success": False,
        "data": None,
        "error": {
            "code": error_code,
            "message": error_message,
            "status_code": status_code,
        },
    }
    
    return response


if __name__ == "__main__":
    # Example usage will be added in documentation phase
    pass
