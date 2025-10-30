# Facility Access Policy

{% if compliance_frameworks.hipaa %}
## HIPAA Compliance Context
This policy implements HIPAA physical safeguard requirements (45 CFR §164.310) for facilities and controlled areas that may contain systems or media holding ePHI.
{% endif %}

{% if compliance_frameworks.soc2 %}
## SOC2 Compliance Context
This policy supports SOC2 physical security criteria for access control, environmental protection, and asset management.
{% endif %}

# {{ company }} Facility Access Policy

This policy works in conjunction with the Physical and Environmental Security Policy and the Workspace Security and Privacy Policy to provide comprehensive facility security controls.

{{ company }} works with Subcontractors to assure restriction of physical access to systems used as part of the {{ company }} Platform. {{ company }} and its Subcontractors control access to the physical buildings/facilities that house these systems/applications, or in which {{ company }} workforce members operate, in accordance to the HIPAA Security Rule 164.310 and its implementation specifications. Physical Access to all of {{ company }} facilities is limited to only those authorized in this policy. In an effort to safeguard ePHi from unauthorized access, tampering, and theft, access is allowed to areas only to those persons authorized to be in them and with escorts for unauthorized persons. All workforce members are responsible for reporting an incident of unauthorized visitor and/or unauthorized access to {{ company }}’s facility.

{# Render this block only when the configuration indicates the company does NOT have PHI access.
	Using a single canonical flag `ephi_access` simplifies templates and avoids undefined-variable issues. #}
{% if not (ephi_access | default(false)) %}
Of note, {{ company }} does not have ready access to ePHI; it provides cloud-based, compliant infrastructure to covered entities and business associates. {{ company }} does not physically house any systems used by its Platform in {{ company }} facilities. Physical security of our Platform servers is outlined [here](http://broadcast.rackspace.com/downloads/pdfs/RackspaceSecurityApproach.pdf).
{% endif %}

## Applicable Standards from the HITRUST Common Security Framework

* 08.b - Physical Entry Controls
* 08.d - Protecting Against External and Environmental Threats
* 08.j - Equipment Maintenance
* 08.l - Secure Disposal or Re-Use of Equipment
* 09.p - Disposal of Media

## Applicable Standards from the HIPAA Security Rule

* 164.310(a)(2)(ii) Facility Security Plan
* 164.310(a)(2)(iii) Access Control & Validation Procedures
* 164.310(b-c) Workstation Use & Security

## {{ company }}-controlled Facility Access Policies

1. Visitor and third party support access is recorded and supervised. All visitors are escorted.
5. Electronic and physical media containing covered information is securely destroyed (or the information securely removed) prior to disposal.
6. The organization securely disposes media with sensitive information.
7. Physical access is restricted using smart locks that track all access.
	* Restricted areas and facilities are locked and when unattended (where feasible).
	* Only authorized workforce members receive access to restricted areas (as determined by the Security Officer).
	* Access and keys are revoked upon termination of workforce members.
	* Workforce members must report a lost and/or stolen key(s) to the Security Officer.
	* The Security Officer facilitates the changing of the lock(s) within 7 days of a key being reported lost/stolen
8. Enforcement of Facility Access Policies
	* Report violations of this policy to the restricted area’s department team leader, supervisor, manager, or director, or the Privacy Officer.
	* Workforce members in violation of this policy are subject to disciplinary action, up to and including termination.
	* Visitors in violation of this policy are subject to loss of vendor privileges and/or termination of services from {{ company }}. 
9. Workstation Security
## Workstation Security and Management

### Approved Operating Systems
Workstations must use one of the following approved operating systems:
{% for os_type, versions in approved_os.workstations.items() %}
#### {{ os_type|title }}
{% for version in versions %}
* {{ version.name }}
{% endfor %}
{% endfor %}

### Device Management
{% if byod.policy_enabled %}
#### BYOD Requirements
* Approved device types:
{% if byod.allowed_devices.computers %}  - Personal computers{% endif %}
{% if byod.allowed_devices.phones %}  - Mobile phones{% endif %}
{% if byod.allowed_devices.other_devices %}  - Other approved devices{% endif %}

* Security Requirements:
{% if byod.security_requirements.mdm_required %}  - Mobile Device Management (MDM) enrollment required{% endif %}
{% if byod.security_requirements.encryption_required %}  - Device encryption mandatory{% endif %}
{% if byod.security_requirements.password_policy_enforced %}  - Password policy compliance required{% endif %}
{% if byod.security_requirements.screen_lock_required %}  - Screen lock configuration mandatory{% endif %}

* Management Controls:
{% if byod.management.app_restrictions %}  - Application restrictions enforced{% endif %}
{% if byod.management.data_backup_required %}  - Regular data backup required{% endif %}
{% if byod.management.remote_wipe_enabled %}  - Remote wipe capability enabled{% endif %}
{% if byod.management.security_scanning %}  - Security scanning enabled{% endif %}
{% endif %}

### Security Controls
* Workstations may only be accessed by authorized personnel
* All access attempts must be monitored and logged
* Security patches must be kept current
* Endpoint protection required on all devices
* Regular vulnerability scans using {{ vulnerability_scanner.name }}
* Full disk encryption mandatory
* Automated security monitoring enabled