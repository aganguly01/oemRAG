import json
import os

def generate_data():
    docs = [
        {
            "id": "doc1",
            "content": "New Relic alerts when CPU usage exceeds 85% for more than 5 minutes."
        },
        {
            "id": "doc2",
            "content": "MongoDB replica set sync issues can cause read delays."
        },
        {
            "id": "doc3",
            "content": "Splunk logs indicate service availability with uptime percentages."
        },
        {
            "id": "doc4",
            "content": "Confluence page on escalation process during database outages."
        },
        {
            "id": "doc5",
            "content": "Response time spikes tracked via Splunk APM can highlight bottlenecks."
        },
        {
            "id": "doc6",
            "content": "Tracking client IP address helps in identifying suspicious activities."
        },
        {
            "id": "doc7",
            "content": "Payload encryption is enabled to secure sensitive data transmission."
        },
        {
            "id": "doc8",
            "content": "Service availability is monitored 24/7 using multiple monitoring tools."
        },
        {
            "id": "doc9",
            "content": "Database connection pool exhaustion can lead to application slowdowns."
        },
        {
            "id": "doc10",
            "content": "VPN access requests follow an approval workflow documented in Confluence."
        },
    ]

    questions = [
        "Why is CPU usage spiking in my Kubernetes pod?",
        "How can I troubleshoot payment gateway timeouts?",
        "Show logs for database connection pool exhaustion.",
        "How do I monitor service availability effectively?",
        "What are the common causes of response time spikes in Splunk?",
        "How can I track client IP address suspicious activity?",
        "What is the process to enable payload encryption?",
        "How to resolve MongoDB replica set sync issues?",
        "Where can I find escalation steps for outages in Confluence?",
        "What alerts are configured in New Relic for CPU and memory?",
    ]

    # Save documents and questions to files for the app to consume
    os.makedirs("data", exist_ok=True)
    with open("data/documents.json", "w") as f_docs:
        json.dump(docs, f_docs, indent=2)

    with open("data/questions.json", "w") as f_q:
        json.dump(questions, f_q, indent=2)

if __name__ == "__main__":
    generate_data()

