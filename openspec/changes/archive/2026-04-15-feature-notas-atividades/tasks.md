## 1. Database Setup

- [ ] 1.1 Create `activity_grades` table in Xano with fields: id, activity_id, user_id (student), professor_id, grade (numeric), created_at, updated_at
- [ ] 1.2 Create foreign key relationships to `academic_tasks`, `users` (student), and `users` (professor)
- [ ] 1.3 Add index on (activity_id, user_id) to prevent duplicates and optimize queries

## 2. API Implementation

- [ ] 2.1 Create authorization function to validate professor owns the activity's subject
- [ ] 2.2 Create POST `/activity_grades` endpoint with request validation (activity_id, user_id, grade)
- [ ] 2.3 Implement error handling: 403 for unauthorized, 400 for invalid input, 201 on success
- [ ] 2.4 Auto-populate created_at and professor_id from authenticated user

## 3. Testing

- [ ] 3.1 Test POST /activity_grades with valid professor and activity
- [ ] 3.2 Test 403 Forbidden when professor doesn't own the subject
- [ ] 3.3 Test 400 Bad Request with missing or invalid fields
- [ ] 3.4 Verify record created correctly in database with all fields populated
