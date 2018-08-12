=============
Rate Limiting
=============

All endpoints are rate-limited. Switcheo uses a dynamic algorithm for determining these limits. The HTTP error code 429 will be returned if this limit is exceeded. You should implement an exponential backoff strategy when encountering this error code.
