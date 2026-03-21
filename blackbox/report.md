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

**Bug 2: Pincode Datatype Validation Missing**
- **Endpoint tested**: `POST /api/v1/addresses`
- **Request payload**:
  - Method: `POST`
  - URL: `http://localhost:8080/api/v1/addresses`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
  - Body: `{"label": "HOME", "street": "123 Main St", "city": "Springfield", "pincode": "abcdef", "is_default": true}`
- **Expected result**: Status `400 Bad Request` based on API rule "The pincode must be exactly 6 digits."
- **Actual result observed**: Status `200 OK`. The system accepted a 6-character string of alphabetical letters instead of validating that it was strictly numeric digits.

**Bug 3: Default Address Override Failed**
- **Endpoint tested**: `POST /api/v1/addresses`
- **Request payload**:
  - Method: `POST`
  - URL: `http://localhost:8080/api/v1/addresses`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
  - Body: `{"label": "OFFICE", "street": "Street 2", "city": "City", "pincode": "222222", "is_default": true}` *(Called after another address was already set to default)*
- **Expected result**: The newly created address should be the unique default, and all pre-existing addresses marked `is_default: true` should have it set to `false`.
- **Actual result observed**: The historical address retained its `is_default: true` flag, creating conflicting defaults in the database.

**Bug 4: Cart Subtotal Integer Overflow**
- **Endpoint tested**: `GET /api/v1/cart`
- **Request payload**:
  - Method: `POST` Add Item (Price 120, Quantity 2), then `GET` Cart
  - URL: `http://localhost:8080/api/v1/cart`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
- **Expected result**: Mathematical accuracy. Subtotal should read `240` (120 * 2).
- **Actual result observed**: Subtotal returned as `-16`. The internal server logic suffers from Signed 8-bit Integer Overflow, preventing proper calculation.

**Bug 5: Cart Accepts Zero and Negative Quantities**
- **Endpoint tested**: `POST /api/v1/cart/add`
- **Request payload**:
  - Method: `POST`
  - URL: `http://localhost:8080/api/v1/cart/add`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
  - Body: `{"product_id": 1, "quantity": 0}` (Also tested `-5`)
- **Expected result**: Status `400 Bad Request` based on API rule "When adding an item, the quantity must be at least 1. Sending 0 or a negative number must be rejected."
- **Actual result observed**: Status `200 OK`. Internal validation limits missing entirely on addition quantities.

**Bug 6: Cart Total Sum Always Asserts ZERO**
- **Endpoint tested**: `GET /api/v1/cart`
- **Request payload**:
  - Method: `POST` Add Item (Price 120), then `GET` Cart
  - URL: `http://localhost:8080/api/v1/cart`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
- **Expected result**: Cart dictionary contains `"total": 120`.
- **Actual result observed**: The API forcibly returned `"total": 0`. The iteration logic for calculating total across dynamic cart configurations is completely broken, triggering downstream coupon validation failures.

**Bug 7: Absence of Discount Payload Return Field**
- **Endpoint tested**: `GET /api/v1/cart`
- **Request payload**:
  - Method: `POST` `/coupon/apply` with valid Code, then `GET` `/cart`
  - URL: `http://localhost:8080/api/v1/cart`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
- **Expected result**: The GET endpoint should return a `"discount"` variable denoting the sum saved.
- **Actual result observed**: Handlers threw `KeyError: 'discount'`, demonstrating the server completely omits providing this required structural UI field back to the caller.

**Bug 8: COD Payments Logged as PAID Initially**
- **Endpoint tested**: `POST /api/v1/checkout`
- **Request payload**:
  - Method: `POST` Checkout Cart
  - URL: `http://localhost:8080/api/v1/checkout`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
  - Body: `{"payment_method": "COD", "address_id": 1}`
- **Expected result**: Dictionary payload sets `"payment_status": "PENDING"`.
- **Actual result observed**: The system forced `"payment_status": "PAID"`, defeating the purpose of Cash on Delivery protocols entirely.

**Bug 9: Missing Single Deposit Threshold for Wallets**
- **Endpoint tested**: `POST /api/v1/wallet/add`
- **Request payload**:
  - Method: `POST` Adding Funds
  - URL: `http://localhost:8080/api/v1/wallet/add`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
  - Body: `{"amount": 5001}`
- **Expected result**: Status `400 Bad Request` according to "A user cannot add an amount greater than 5000 in a single request."
- **Actual result observed**: Status `200 OK`. Rule enforcement is functionally absent.

**Bug 10: Missing Absolute Global Wallet Cap Enforcement**
- **Endpoint tested**: `POST /api/v1/wallet/add`
- **Request payload**:
  - Method: `POST` Sequentially over-depositing beyond $10,000 threshold.
  - URL: `http://localhost:8080/api/v1/wallet/add`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
  - Body: `{"amount": 4000}` run sequentially 4 times.
- **Expected result**: Status `400 Bad Request` once the user's total active sum exceeds $10,000.
- **Actual result observed**: Status `200 OK`. Accounts can balloon well past $10,000.

**Bug 11: Orders Privacy Enforcement Yields 404**
- **Endpoint tested**: `GET /api/v1/orders/{order_id}`
- **Request payload**:
  - Method: `GET` User 2 requesting User 1's Order
  - URL: `http://localhost:8080/api/v1/orders/{order_id}`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '2'}`
- **Expected result**: Status `403 Forbidden` according to "If they try to view an order that belongs to another user, the server must return a 403 error."
- **Actual result observed**: Status `404 Not Found`.

**Bug 12: Missing Add Review POST Endpoint**
- **Endpoint tested**: `POST /api/v1/products/{product_id}/reviews/add`
- **Request payload**:
  - Method: `POST` Adding product review
  - URL: `http://localhost:8080/api/v1/products/1/reviews/add`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
  - Body: `{"rating": 4, "review_text": "Good"}`
- **Expected result**: Status codes `200` or `400` depending on input values and bounds validations.
- **Actual result observed**: Status `404 Not Found`. The endpoint is completely unimplemented or improperly routed.

**Bug 13: Support Tickets APIs Entirely Unimplemented**
- **Endpoint tested**: `GET /api/v1/tickets` and `POST /api/v1/tickets/create`
- **Request payload**:
  - Method: `GET` and `POST`
  - URL: `http://localhost:8080/api/v1/tickets/create`
  - Headers: `{'X-Roll-Number': '<your_roll_number>', 'X-User-ID': '1'}`
- **Expected result**: Status `200 OK` or structural rule validation responses.
- **Actual result observed**: Status `404 Not Found`. The Support Tickets logic mapping is absent from the API.
