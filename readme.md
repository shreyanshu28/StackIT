1. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Service

1. **Start the FastAPI application**:
   ```bash
   uvicorn app:app --reload
   ```
   - The application should be available at `http://127.0.0.1:8000`.

2. **Interact with the API**:
   - Use `http://127.0.0.1:8000/docs` to test using CURL (commands below)

---

## Testing the Service
1. **Run the tests**:
   ```bash
   pytest test_api.py
   ```
   - This will execute all the test cases and verify the API functionality.

2. **Interact with the API**:
    - Use `http://127.0.0.1:8000/docs` to test using CURL

### Including `curl` Commands
Here are the `curl` commands you can use to test each of the API endpoints:

---

#### **1. POST `/notifications`**
Send a "Warning" notification:
```bash
curl -X POST http://127.0.0.1:8000/notifications \
-H "Content-Type: application/json" \
-d '{
    "Type": "Warning",
    "Name": "Backup Failure",
    "Description": "The backup failed due to a database problem"
}'
```

Send an "Info" notification:
```bash
curl -X POST http://127.0.0.1:8000/notifications \
-H "Content-Type: application/json" \
-d '{
    "Type": "Info",
    "Name": "Quota Exceeded",
    "Description": "Compute quota exceeded the allowed limit"
}'
```

Send an invalid notification type:
```bash
curl -X POST http://127.0.0.1:8000/notifications \
-H "Content-Type: application/json" \
-d '{
    "Type": "Critical",
    "Name": "Security Breach",
    "Description": "Unauthorized access detected"
}'
```