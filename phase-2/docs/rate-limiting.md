# Rate Limiting Considerations

## Current Status
Rate limiting is **not implemented** in the current version of the Phase 2 Todo API. This is intentional for the MVP scope but should be considered for production deployment.

## Why Rate Limiting Matters
- **DoS Protection**: Prevents denial-of-service attacks
- **Resource Management**: Protects database and server resources
- **Fair Usage**: Ensures equitable access for all users
- **Cost Control**: Limits API costs for cloud-hosted databases

## Recommended Implementation

### Option 1: FastAPI Rate Limiting Middleware
Use `slowapi` library for simple rate limiting:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/tasks")
@limiter.limit("100/minute")
def get_tasks(...):
    ...
```

### Option 2: Nginx Rate Limiting
Configure rate limiting at the reverse proxy level:

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://backend;
}
```

### Option 3: Cloud Provider Rate Limiting
- **AWS API Gateway**: Built-in throttling
- **Cloudflare**: Rate limiting rules
- **Kong**: Rate limiting plugin

## Recommended Limits

### Authentication Endpoints
- `/auth/register`: 5 requests/hour per IP
- `/auth/login`: 10 requests/minute per IP
- `/auth/logout`: 20 requests/minute per user

### Task Endpoints
- `GET /tasks`: 100 requests/minute per user
- `POST /tasks`: 50 requests/minute per user
- `PUT/PATCH /tasks/{id}`: 50 requests/minute per user
- `DELETE /tasks/{id}`: 30 requests/minute per user

### Health Check
- `/health`: No limit (needed for monitoring)

## Implementation Priority
**Priority**: Medium (P2)
**Effort**: 2-4 hours
**Dependencies**: None

## Testing Rate Limits
Once implemented, test with:
```bash
# Test rate limiting with Apache Bench
ab -n 200 -c 10 http://localhost:8000/tasks

# Test with custom script
for i in {1..150}; do
  curl -X GET http://localhost:8000/tasks \
    -H "Authorization: Bearer $TOKEN"
  sleep 0.1
done
```

## Monitoring
Track rate limit metrics:
- Number of rate-limited requests
- Top rate-limited IPs
- Rate limit violations by endpoint
- Average requests per user

## Future Enhancements
- Per-user rate limits (not just per-IP)
- Dynamic rate limits based on user tier
- Rate limit headers in responses (X-RateLimit-Limit, X-RateLimit-Remaining)
- Graceful degradation instead of hard blocks
