# Approved Tools Policy

{% if hipaa %}
## HIPAA Compliance Context
This policy establishes controls for tools and systems that may process or store Protected Health Information (PHI), ensuring compliance with HIPAA Security Rule requirements for access control and data protection.
{% endif %}

{% if soc2 %}
## SOC2 Compliance Context
This policy supports SOC2 Common Criteria related to logical access controls, system operations, and change management by defining approved tools and their security requirements.
{% endif %}

{% if hitrust %}
## HITRUST Compliance Context
This policy aligns with HITRUST CSF controls for system configuration, access management, and data protection through defined tool standards and security requirements.
{% endif %}

{{ company }} maintains a comprehensive list of approved software tools for business operations. {% if hipaa %}For tools that may interact with Protected Health Information (PHI), additional security controls and business associate agreements are required.{% endif %} All tools are either self-hosted and managed by {{ company }} or provided by approved vendors with appropriate security agreements in place.

## Approved Collaboration Tools

{% for tool in approved_tools.collaboration %}
* **{{ tool.name }}** ({{ tool.type }}). Approved for: {{ tool.approved_for|join(", ") }}.
{% endfor %}

## Approved Development Tools

{% for tool in approved_tools.development %}
* **{{ tool.name }}** ({{ tool.type }}). Approved for: {{ tool.approved_for|join(", ") }}.
{% endfor %}

## Approved Productivity Tools

{% for tool in approved_tools.productivity %}
* **{{ tool.name }}** ({{ tool.type }}). Approved for: {{ tool.approved_for|join(", ") }}.
{% endfor %}

## Approved Operating Systems

### Workstations
{% for os_type, versions in approved_os.workstations.items() %}
#### {{ os_type|title }}
{% for version in versions %}
* {{ version.name }}
{% endfor %}
{% endfor %}

### Servers
{% for os_type, versions in approved_os.servers.items() %}
#### {{ os_type|title }}
{% for version in versions %}
* {{ version.name }}
{% endfor %}
{% endfor %}

## Security Requirements

### General Requirements
1. All approved tools must be kept up-to-date with the latest security patches
2. Access to these tools must be protected with strong authentication mechanisms
3. When available, Multi-Factor Authentication (MFA) must be enabled
4. Data sharing through these tools must follow {{ company }}'s data classification and handling policies
5. Users must report any security concerns or unexpected behavior to the Security Officer immediately

{% if hipaa %}
### HIPAA-Specific Requirements
1. Tools processing PHI must maintain detailed access logs
2. Business Associate Agreements (BAA) required for third-party tools handling PHI
3. PHI transmission must use encrypted channels
4. Regular security assessments of PHI-handling tools
{% endif %}

{% if soc2 %}
### SOC2-Specific Requirements
1. Tools must support audit logging capabilities
2. Access reviews conducted quarterly
3. Change management procedures for tool updates
4. Vendor security assessments required
{% endif %}

{% if hitrust %}
### HITRUST-Specific Requirements
1. Tools must meet HITRUST encryption standards
2. Regular security configuration reviews
3. Detailed incident response procedures
4. Vendor compliance verification
{% endif %}
