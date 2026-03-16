## Overview

In this lab, you will build a complete automated test suite for your Flask application.

You will practice:

1. Unit testing pure validation helpers
2. Building reusable pytest fixtures
3. Integration testing profile API endpoints
4. Testing device authentication using API keys

The goal is to make your app testable without real Firebase credentials or network access.

---

## Quick Setup (One-Time)

1. Install dependencies:
   - pip install -r requirements.txt
   - pip install pytest pytest-cov

2. Make sure your project runs locally before starting tests.

3. Run tests with:
   - pytest tests/ -v
   - pytest tests/ --cov=utils --cov=blueprints --cov=decorators

---

## Task 1: Unit Testing Your Validators

Create tests/test_validators.py and write parametrized tests for the pure functions in utils/.

### What to test

1. validate_profile_data(first_name, last_name, student_id)
   - Cover all equivalence partitions from lecture:
     - Empty strings
     - None
     - Whitespace-only strings
     - Valid combinations
     - All-empty values

2. normalize_profile_data(first_name, last_name, student_id)
   - Whitespace stripping behavior
   - None handling
   - Conversion of student_id to string

### Key learning outcomes

1. Translate equivalence partition tables into @pytest.mark.parametrize
2. Use the AAA pattern in practice
3. Observe current behavior for whitespace-only strings in validate_profile_data (this may reveal a bug worth discussing)

### Suggested scope

1. 8 to 10 parametrized test cases for validate_profile_data
2. 4 to 5 test cases for normalize_profile_data
3. Run pytest --cov=utils and target at least 90 percent coverage for utils

---

## Task 2: Setting Up Test Infrastructure

Create tests/conftest.py with shared fixtures.

### Fixtures to build

1. client
   - Flask test client with TESTING = True

2. mock_firebase_auth
   - Patch firebase_admin.auth.verify_id_token
   - Return {"uid": "test_user_123"}

3. mock_firestore
   - Patch firebase.db with a MagicMock
   - Support chained calls used by your app, such as:
     - db.collection().document().get()
     - db.collection().document().set()
     - db.collection().document().update()

### Key learning outcomes

1. Use pytest fixtures as dependency injection
2. Patch objects at the import location your code uses
3. Build chained Firestore behavior with MagicMock

### Guidance

1. Start from a provided client fixture
2. Complete a skeleton for mock_firebase_auth
3. Build mock_firestore by inspecting your own route and helper code paths

---

## Task 3: Integration Testing API Endpoints

Create tests/test_api_profile.py and write integration tests for profile CRUD endpoints.

### Required test cases (minimum 7)

1. test_get_profile_no_auth
   - GET without Authorization header returns 401

2. test_get_profile_bad_token_format
   - Authorization header without Bearer prefix returns 401

3. test_get_profile_invalid_token
   - Mock verify_id_token to raise Exception, expect 401

4. test_get_profile_success
   - Valid mocked token + mocked Firestore, expect 200 with profile payload

5. test_create_profile_missing_fields
   - POST incomplete JSON body, expect 400

6. test_create_profile_success
   - POST valid data with mocked auth and Firestore, expect 200

7. test_update_profile_invalid_field
   - PUT {"age": 25}, expect 400 and whitelist error message

### Key learning outcomes

1. Validate auth decorators through endpoint tests
2. Combine fixtures in one test (client + mock_firebase_auth + mock_firestore)
3. Assert important mock interactions with assert_called_once_with
4. Verify JSON error structure and messages

---

## Task 4: Testing Device Authentication

Create tests/test_api_sensor.py and test the require_api_key decorator path.

### Required test cases (minimum 3)

1. test_sensor_data_no_api_key
   - Missing X-API-Key header returns 401

2. test_sensor_data_wrong_key
   - Wrong API key value returns 401

3. test_sensor_data_valid_key
   - Correct key + valid JSON returns 201

### Key learning outcomes

1. Use mocker.patch.dict(os.environ, {...}) to control API key configuration in tests
2. Compare testing patterns for JWT auth and API key auth
3. Mock Firestore writes for sensor ingestion endpoint

---

## Deliverables

Create the following files:

```
tests/
├── conftest.py              # Fixtures: client, mock_firebase_auth, mock_firestore
├── test_validators.py       # 12+ parametrized unit tests
├── test_api_profile.py      # 7+ integration tests for /api/profile
└── test_api_sensor.py       # 3+ tests for /api/sensor_data
```

---

## Success Criteria

1. All tests pass with:
   - pytest tests/ -v

2. No tests require real Firebase credentials or network calls

3. Coverage report is generated with:
   - pytest tests/ --cov=utils --cov=blueprints --cov=decorators
