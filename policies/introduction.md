# Introduction

{{ company_name }} ("{{ company }}") is committed to ensuring the confidentiality, privacy, integrity, and availability of all electronic protected health information (ePHI) it receives, maintains, processes and/or transmits on behalf of its Customers. As providers of compliant, {{ company_service }} used by {{ company_service_user_types }}, {{ company }} strives to maintain compliance, proactively address information security, mitigate risk for its Customers, and assure known breaches are completely and effectively communicated in a timely manner.

{% if service_types.paas.enabled %}
## Platform as a Service (PaaS)

PaaS Customers utilized hosted software and infrastructure from {{ company }} to deploy, host, and scale custom developed applications and configured databases. These customers are deployed into compliant containers run on systems secured and managed by {{ company }}. {{ company }} does not have insight or access into application level data of PaaS Customers and, as such, does not have the ability to secure or manage risk associated with application level vulnerabilities and security weaknesses. {{ company }} makes every effort to reduce the risk of unauthorized disclosure, access, and/or breach of PaaS Customer data through network (firewalls, dedicated IP spaces, etc) and server settings (encryption at rest and in transit, OSSEC throughout the Platform, etc).
{% endif %}

{% if service_types.saas.enabled or service_types.baas.enabled %}
## Platform Add-ons

Add-ons are compliant API-driven services that are offered as part of the {{ company }} Platform. These services currently include our Backend as a Service and secure Messaging Service. With Add-ons, {{ company }} has access to data models and manages all application level configurations and security.

In the future there may be 3rd party Add-on services available as part of the {{ company }} Platform. These 3rd party, or Partner, Services will be fully reviewed by {{ company }} to assure they do not have a negative impact on {{ company }}'s information security and compliance posture.
{% endif %}

## Compliance Inheritance

{{ company }} provides compliant hosted software infrastructure for its Customers.
{% if compliance_frameworks.hipaa.supported and compliance_frameworks.hipaa.audit.completed %}
{{ company }} has been through a HIPAA compliance audit by a national, 3rd party compliance firm, to validate and map organizational policies and technical settings to HIPAA rules. This audit was last completed on {{ compliance_frameworks.hipaa.audit.completed_date }}.
{% elif compliance_frameworks.hipaa.supported and compliance_frameworks.hipaa.audit.in_progress %}
{{ company }} is currently undergoing a HIPAA compliance audit.
{% endif %}
{% if compliance_frameworks.hitrust.supported and compliance_frameworks.hitrust.audit.completed %}
{{ company }} has been through a HITRUST audit and achieved HITRUST Certification on {{ compliance_frameworks.hitrust.audit.completed_date }}.
{% elif compliance_frameworks.hitrust.supported and compliance_frameworks.hitrust.audit.in_progress %}
{{ company }} is currently undergoing a HITRUST audit to achieve HITRUST Certification.
{% endif %}

{{ company }} signs business associate agreements (BAAs) with its Customers. These BAAs outline {{ company }} obligations and Customer obligations, as well as liability in the case of a breach. In providing infrastructure and managing security configurations that are a part of the technology requirements that exist in HIPAA and HITRUST, as well as future compliance frameworks, {{ company }} manages various aspects of compliance for Customers. The aspects of compliance that {{ company }} manages for Customers are inherited by Customers, and {{ company }} assumes the risk associated with those aspects of compliance. In doing so, {{ company }} helps Customers achieve and maintain compliance, as well as mitigates Customers risk.

Certain aspects of compliance cannot be inherited. Because of this, {{ company }} Customers, in order to achieve full compliance or HITRUST Certification, must implement certain organizational policies. These policies and aspects of compliance fall outside of the services and obligations of {{ company }}.