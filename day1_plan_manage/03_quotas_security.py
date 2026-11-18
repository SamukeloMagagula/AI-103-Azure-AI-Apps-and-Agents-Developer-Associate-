"""Day 1 · Script 3 — Quotas, scaling, and security.

Exam objective → "Manage quotas, scaling, rate limits, cost footprints"
                 + "Configure security: managed identity, private networking,
                   keyless credentials, role policies"
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show

show("Quota units", {
    "TPM": "tokens per minute (Azure OpenAI deployments)",
    "RPM": "requests per minute — derived (TPM/1000 * 6)",
    "PTU": "Provisioned Throughput Units — reserved capacity, predictable latency",
    "SKUs": ["Standard", "GlobalStandard", "DataZoneStandard", "ProvisionedManaged"],
})

show("429 troubleshooting checklist", [
    "Raise TPM for the deployment (per region limit)",
    "Add a second deployment in another region + load-balance",
    "Switch high-volume workloads to Provisioned (PTU)",
    "Add client-side backoff + x-ms-retry-after-ms header respect",
])

show("Keyless auth (recommended)", {
    "credential": "DefaultAzureCredential()",
    "aoai_scope": "https://cognitiveservices.azure.com/.default",
    "project_scope": "https://ai.azure.com/.default",
    "roles": [
        "Cognitive Services OpenAI User",
        "Cognitive Services OpenAI Contributor",
        "Azure AI Developer",            # Foundry project
        "Azure AI Project Manager",
        "Search Index Data Reader",
        "Search Index Data Contributor",
    ],
})

show("Private networking", {
    "private_endpoint_subresources": ["account", "search", "blob"],
    "disable_public_access": True,
    "custom_subdomain_required": True,
    "data_exfil_control": "Configure 'Allowed Virtual Networks' + Private DNS zone",
})

print("\nExam trap → managed identity needs the role assigned on the TARGET")
print("            resource (Search, Storage), not on the Foundry project.")
