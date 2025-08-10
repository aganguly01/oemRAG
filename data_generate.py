import json

# Sample production incident style knowledge base
incident_docs = [
    {
        "content": "CPU usage spiking in Kubernetes pod can be due to high traffic, inefficient code loops, or memory leaks. Check pod metrics using `kubectl top pods`, review application profiling logs, and consider horizontal pod autoscaling."
    },
    {
        "content": "MongoDB connection spikes can occur when too many concurrent requests hit the database. Check connection pool settings, slow queries using `db.currentOp()`, and ensure indexes are optimized."
    },
    {
        "content": "DynamoDB read/write capacity spikes might be caused by batch jobs or sudden traffic surges. Enable auto-scaling, use caching (e.g., DAX), and optimize query patterns to reduce hot partitions."
    },
    {
        "content": "Freeze errors in services may be due to deadlocks, infinite loops, or blocking I/O calls. Use thread dumps or profiling tools to identify bottlenecks and refactor long-running operations."
    },
    {
        "content": "Endpoint timeouts often occur when backend services exceed response SLAs. Check application logs, monitor upstream service performance, and implement retries with exponential backoff."
    },
    {
        "content": "Database connection pool exhaustion often occurs when connections are not closed properly or queries are slow. Monitor connection usage, set maximum pool sizes, and investigate long-running queries."
    },
    {
        "content": "For persistent payment gateway timeouts, verify API health, network latency, and service-level agreement breaches. Escalate to the concerned SRE on-call person if external API is unresponsive."
    },
    {
        "content": "If MongoDB query latency spikes, check for slow queries with `db.currentOp()` and `explain()`. Revisit index usage, optimize aggregation pipelines, and scale vertically or horizontally."
    },
    {
        "content": "If DynamoDB throttling errors occur, review CloudWatch metrics, increase provisioned capacity or enable on-demand mode, and batch requests to reduce burst load."
    },
    {
        "content": "When Kubernetes pods OOMKill, check container memory limits, review memory usage trends, and optimize application memory footprint. Enable vertical pod autoscaling if applicable."
    }
]

# Add IDs automatically
data_with_ids = [{"id": f"doc_{i}", "content": doc["content"]} for i, doc in enumerate(incident_docs)]

# Write to incidents.json
with open("incidents.json", "w") as f:
    json.dump(data_with_ids, f, indent=2)

print("✅ incidents.json generated with production incident examples.")

