from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from schema import AuditLog
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import time

async def mask_sensitive(data):
    # sensitive_fields = [
    #     'password', 'token', 'email', 'phone_number',
    #     'address', 'credit_card_number', 'social_security_number',
    #     'national_identification_number', 'date_of_birth',
    #     'driver_license_number', 'passport_number', 'bank_account_number',
    #     'health_insurance_number', 'biometric_data', 'ethnicity',
    #     'gender', 'sexual_orientation', 'marital_status', 'religion',
    #     # ... add more sensitive fields as needed
    # ]
    sensitive_fields = ["password"]
    if isinstance(data, dict):
        return {
            key: mask_sensitive(value) if key.lower() not in sensitive_fields else '**SENSITIVE**'
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [mask_sensitive(item) for item in data]
    else:
        return data

class APILogger:
    def __init__(self, app: FastAPI, mongodb_connection_string: str, database_name: str):
        self.app = app
        self.mongodb_connection_string = mongodb_connection_string
        self.database_name = database_name
    
    # async def __call__(self, request: Request, call_next: Callable) -> JSONResponse:
    async def __call__(self, scope, receive, send) -> JSONResponse:
        if scope["type"] == "http":
            await self.process_request(scope, receive, send)
        else:
            await self.app(scope, receive, send)
    

    async def process_request(self, scope, receive, send):
        client = AsyncIOMotorClient(self.mongodb_connection_string, maxPoolSize=50)
        database = client[self.database_name]
        start_time = time.time()
        # Get request and response attributes from the scope
        request = Request(scope, receive)
        request_method = scope.get("method")
        request_url = str(request.url)
        request_headers = dict(request.headers)
        client_ip_address = request.client.host
        if request_method not in ["GET", "DELETE", "HEAD"]:
            # Access request body through the scope
            request_payload_before = await receive()
            request_payload_before = await mask_sensitive(request_payload_before)
        else:
            request_payload_before = None
        
        async def capture_response(received_scope):
            global response_started, response_status_code
            global response_body
            if received_scope["type"] == "http.response.start":
                response_started = True
                response_status_code = received_scope["status"]

            if received_scope["type"] == "http.response.body":
                response_body = received_scope.get("body", b"")

            await send(received_scope)

        await self.app(scope, receive, capture_response)
        response_body_str = response_body.decode("utf-8")
        end_time = time.time()


        audit_log = AuditLog(
            added_on= datetime.utcnow(),
            http_method= request_method,
            api= request_url,
            headers= dict(request_headers),
            payload= request_payload_before,
            response= response_body_str,
            client_ip_address= client_ip_address,
            status_code= response_status_code,
            execution_time= end_time - start_time
            )
        audit_db = database.get_collection("api_logger")
        audit_db.insert_one(audit_log.model_dump())