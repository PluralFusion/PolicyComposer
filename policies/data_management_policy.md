# Data Management Policy

{% if compliance_frameworks.hipaa %}
## HIPAA Compliance Context
This policy addresses HIPAA Security Rule requirements relevant to data backup, retention, and recoverability of ePHI.
{% endif %}

{% if compliance_frameworks.soc2 %}
## SOC2 Compliance Context
This policy supports the SOC2 Trust Services Criteria for Availability, Confidentiality, and Processing Integrity as they relate to backup and recovery.
{% endif %}

# {{ company }} Data Management Policy

{% if vendors %}
All {{ company }} data backups are maintained by:
{% for vendor in vendors if 'Data Storage' in vendor.services or 'Data Backup' in vendor.services %}
* {{ vendor.name }}{% if vendor.baa_signed %} (with signed BAA){% endif %}
{% endfor %}
{% endif %}

{{ company }} has procedures to create and maintain retrievable exact copies of electronic protected health information (ePHI) across all our service offerings. The scope and implementation of these procedures vary based on the service type:

{% if service_types.saas.enabled %}
## SaaS Platform Data Management
For our Software-as-a-Service platform, {{ company }} maintains complete control and responsibility for all data backup and recovery procedures. All ePHI stored within our SaaS platform is automatically backed up according to our defined schedule and retention policies.
{% endif %}

{% if service_types.paas.enabled %}
## PaaS Customer Data Management
For Platform-as-a-Service customers utilizing our Backup Service, {{ company }} provides automated backup solutions integrated with our platform. Customers who do not opt for our Backup Service are responsible for implementing their own backup procedures in compliance with HIPAA requirements.
{% endif %}

{% if service_types.medical_device.enabled %}
## Medical Device Data Management
For medical device implementations, {{ company }} ensures:
* All device-generated ePHI is securely backed up to our HIPAA-compliant storage infrastructure
* Backup procedures comply with both HIPAA requirements and FDA medical device regulations
* Device-specific backup protocols are documented and validated
{% endif %}

{% if service_types.mobile_app.enabled %}
## Mobile Application Data Management
For our mobile applications:
* All ePHI is encrypted both in transit and at rest
* Local data on mobile devices is minimized and temporary
* Cloud-based backups of mobile app data are automatically maintained in our secure infrastructure
{% endif %}

This policy and associated procedures assure that complete, accurate, retrievable, and tested backups are available for all systems used by {{ company }}.
  
Data backup is an important part of the day-to-day operations of {{ company }}. To protect the confidentiality, integrity, and availability of ePHI, both for {{ company }} and {{ company }} Customers, completes backups are done daily to assure that data remains available when it needed and in case of disaster.

Violation of this policy and its procedures by workforce members may result in corrective disciplinary action, up to and including termination of employment.

## Applicable Standards from the HITRUST Common Security Framework

* 01.v - Information Access Restriction

## Applicable Standards from the HIPAA Security Rule

* 164.308(a)(7)(ii)(A) - Data Backup Plan
* 164.310(d)(2)(iii) - Accountability
* 164.310(d)(2)(iv) - Data Backup and Storage

{% if compliance_frameworks.soc2 %}
## SOC2 Trust Services Criteria

### Availability
* A1.1 - Data Backup and Recovery Procedures
* A1.2 - Business Continuity Planning
* A1.3 - Disaster Recovery Testing

### Confidentiality
* C1.1 - Data Classification and Handling
* C1.2 - Data Retention and Disposal
* C1.3 - Data Access Controls

### Processing Integrity
* PI1.1 - Data Accuracy and Completeness
* PI1.2 - Data Validation Procedures
* PI1.3 - Error Handling and Resolution

### Data Lifecycle Management Controls
* Data classification and inventory
* Data retention schedules
* Data disposal procedures
* Access review and monitoring
* Encryption key management
* Backup verification procedures
{% endif %}

## Backup Policy and Procedures

1. Perform daily snapshot backups of all systems that process, store, or transmit ePHI for {{ company }} Customers, including PaaS Customers that utilize the {{ company }} Backup Service
2. {{ company }} Ops Team, lead by VP of Engineering, is designated to be in charge of backups.
3. Dev Ops Team members are trained and assigned assigned to complete backups and manage the backup media.
4. Document backups 
	* Name of the system
	* Date & time of backup
	* Where backup stored (or to whom it was provided)
5. Securely encrypt stored backups in a manner that protects them from loss or environmental damage.
6. Test backups and document that files have been completely and accurately restored from the backup media.