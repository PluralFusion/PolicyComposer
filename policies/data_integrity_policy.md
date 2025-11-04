# Data Integrity Policy

{% if hipaa %}
## HIPAA Compliance Context
This policy implements the requirements of HIPAA § 164.308(a)(8) - Evaluation, ensuring that technical controls maintain the integrity and availability of ePHI throughout its lifecycle.
{% endif %}

{% if soc2 %}
## SOC2 Compliance Context
This policy supports SOC2 Processing Integrity criteria (PI 1.1, PI 1.2, PI 1.3) and Common Criteria (CC 6.1), ensuring data processing integrity, accuracy, and completeness through system configuration and monitoring.
{% endif %}

{% if vendors %}
All {{ company }} data exchanges occur on platforms maintained by our infrastructure vendors.
{% for vendor in vendors if 'Platform' in vendor.services and vendor.baa_signed %}
{{ vendor.name }} has signed a BAA with {{ company }} committing to the policy below.
{% endfor %}
{% endif %}

{{ company }} takes data integrity very seriously. As stewards and partners of {{ company }} Customers, we strive to assure data is protected from unauthorized access and that it is available when needed. The following policies drive many of our procedures and technical settings in support of the {{ company }} mission of data protection.

## Applicable Standards

{% if hitrust %}
### HITRUST Common Security Framework
* 10.b - Input Data Validation
* 06.d - Data Integrity Controls
* 09.aa - Audit Logging
{% endif %}

{% if hipaa %}
### HIPAA Security Rule
* 164.308(a)(8) - Evaluation
* 164.312(c)(1) - Data Integrity
* 164.312(e)(2)(i) - Transmission Security
{% endif %}

{% if soc2 %}
### SOC2 Trust Services Criteria
* CC6.7 - System Changes
* PI1.1 - System Processing Integrity
* CC8.1 - Change Management Process
{% endif %}

## Access Monitoring and Control

* All access to Production Systems must be logged. This is done following the {{ company }} Auditing Policy.
{% for vendor in vendors if 'Security' in vendor.services %}
* All Production Systems must have {{ vendor.name }} deployed for continuous threat detection and prevention
{% endfor %}
### Malware Prevention

* All Production Systems must have {{ security_vendors[0] }} deployed for continuous threat detection and prevention
* Regular malware scans are performed using {{ vulnerability_scanner.name }} by {{ vulnerability_scanner.provider }}
* All Production Systems are restricted to {{ company }} business operations only

### Patch Management

{% if soc2 %}
* Patch management follows SOC2 change management requirements
* All changes are documented and approved before implementation
{% endif %}

* Operating system and application patches are regularly tested and applied
* System administrators maintain awareness of security updates through vendor notifications
* Approved operating systems for servers are limited to:
{% for os_type, versions in approved_os.servers.items() %}
{% for version in versions %}
  * {{ version.name }}
{% endfor %}
{% endfor %}

### Intrusion Detection and Vulnerability Scanning

* Production Systems are monitors using IDS systems. Suspicious activity is logged and alerts are generated.
* Vulnerability scanning of Production Systems must occur on a predetermined, regular basis, no less than annually. Currently it is weekly. Scans are reviewed by Security Officer, with defined steps for risk mitigation, and retained for future reference.

### Production System Security

* System, network, and server security is managed and maintained by the VP of Engineering and the Security Officer.
* Up to date system lists and architecture diagrams are kept for all Production environments.
* Access to Production Systems is controlled using centralized tools and two-factor authentication.

### Production Data Security

* Reduce the risk of compromise of Production Data.
* Implement and/or review controls designed to protect Production Data from improper alteration or destruction.
* Ensure that Confidential data is stored in a manner that supports user access logs and automated monitoring for potential security incidents.
* Ensure {{ company }} customer Production Data is segmented and only accessible to customer authorized to access data.
* All Production Data at rest is stored on encrypted volumes.

### Transmission Security

* All data transmission is encrypted end to end. Encryption is not terminated at the network end point, and is carried through to the application.
* Encryption keys and machines that generate keys are protected from unauthorized access.
* Encryption keys are limited to use for one year and then must be regenerated.
* In the case of {{ company }} provided APIs, provide mechanisms to assure person sending or receiving data is authorized to send and save data.
* System logs of all transmissions of Production Data access. These logs must be available for audit.
