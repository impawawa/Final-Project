## Rate Limiting

The API implements rate limiting to prevent abuse and ensure fair usage. Rate limiting is applied per IP address.

### Rate Limit Rules
- All endpoints are limited to 5 requests per minute per IP address
- The limit resets after 60 seconds
- Rate limits are tracked separately for each endpoint

### Rate Limit Response
When the rate limit is exceeded, the API will return:
```json
{
    "error": "Rate limit exceeded",
    "detail": "Too many requests. Maximum 5 requests per 60 seconds."
}
```
Status Code: 429 Too Many Requests

### Example Rate Limit Scenarios

1. Login Attempts:
   - First 5 login attempts within a minute: Success (200 OK)
   - 6th attempt within the same minute: Rate limit error (429)

2. Car Operations:
   - First 5 requests to list/create/update/delete cars within a minute: Success
   - 6th request within the same minute: Rate limit error

3. Rental Operations:
   - First 5 requests to list/create/update/delete rentals within a minute: Success
   - 6th request within the same minute: Rate limit error

### Best Practices
- Implement exponential backoff when receiving 429 responses
- Cache responses when possible to reduce API calls
- Consider implementing request queuing for high-volume operations

## Authentication Endpoints
