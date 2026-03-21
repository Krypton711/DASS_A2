# QuickCart Black Box API Testing Report

## 1. Profile API
*Tests implemented covering boundary, missing, type mismatch, and valid scenarios for GET and PUT `/api/v1/profile`.*

### Test Cases
- **test_get_profile_valid**: Input headers. Expected 200 OK. Justification: Core valid path for retrieving a profile.
- **test_get_profile_missing_roll_number**: Missing X-Roll-Number header. Expected 401. Justification: Authentication strictness checks.
- **test_get_profile_invalid_roll_number**: Invalid X-Roll-Number string. Expected 400. Justification: Testing type/value casting rules for headers.
- **test_get_profile_missing_user_id**: Missing X-User-ID header. Expected 400. Justification: Testing standard validation boundary.
- **test_put_profile_valid**: Valid payload `{name: <2-50chars>, phone: <10digits>}`. Expected 200 OK. Justification: Valid state mutation.
- **test_put_profile_invalid_name_short**: Payload `{name: "A", phone...}`. Expected 400. Justification: Name lower boundary enforcement (< 2 chars).
- **test_put_profile_invalid_name_long**: Payload `{name: "A"*51, phone...}`. Expected 400. Justification: Name upper boundary enforcement (> 50 chars).
- **test_put_profile_valid_name_boundary**: Payload `{name: "A"*50, phone...}`. Expected 200. Justification: Ensuring exactly 50 chars is strictly accepted.
- **test_put_profile_invalid_phone_short**: Payload `{phone: 9 digits}`. Expected 400. Justification: Phone lower boundary constraint validation.
- **test_put_profile_wrong_datatype_phone**: Payload `{phone: "abcdefghij"}`. Expected 400. Justification: Validating server strictness against casting arbitrary strings to numeric sequences.
- **test_put_profile_missing_field**: Missing `name` key. Expected 400. Justification: Incomplete PUT payloads should be forcefully rejected.

### Bugs Discovered
**Bug 1: Phone Datatype Validation Missing**
- **Endpoint tested**: `PUT /api/v1/profile`
- **Request payload**:
  - Method: `PUT`
  - URL: `http://localhost:8080/api/v1/profile`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
  - Body: `{"name": "John", "phone": "abcdefghij"}`
- **Expected result**: Status `400 Bad Request` based on API rule "The phone number must be exactly 10 digits."
- **Actual result observed**: Status `200 OK`. The system accepted a 10-character string of letters instead of validating that it contains only numeric digits.
