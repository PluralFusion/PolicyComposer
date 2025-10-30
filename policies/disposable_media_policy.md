# Disposable Media Policy

{% if hipaa %}
## HIPAA Compliance Context
This policy implements the requirements of HIPAA § 164.310(d)(1) - Device and Media Controls, ensuring proper handling of electronic media containing ePHI throughout its lifecycle, including disposal.
{% endif %}

{% if soc2 %}
## SOC2 Compliance Context
This policy supports SOC2 Common Criteria (CC) 6.7 and CC 8.1, addressing the identification, protection, and disposal of system components containing sensitive data.
{% endif %}

{% if data_storage_vendors %}
All {{ company }} data is stored on media maintained by:
{% for vendor in data_storage_vendors %}
{%- if not loop.first -%}
    {%- if loop.last %} and {% else %}, {% endif -%}
{% endif -%}
{{ vendor }}
{%- endfor -%}.

{% for vendor in data_storage_vendors %}
{% if vendor in baa_vendors %}
{{ vendor }} has signed a BAA with {{ company }} committing to the policy below.
{% endif %}
{% endfor %}
{% endif %}

{{ company }} recognizes that media containing sensitive data may be reused when appropriate steps are taken to ensure that all stored data has been effectively rendered inaccessible. Destruction/disposal of sensitive data shall be carried out in accordance with federal and state law. The schedule for destruction/disposal shall be suspended for data involved in any open investigation, audit, or litigation.

{{ company }} implements a comprehensive approach to data storage and media management:

1. Infrastructure
{% if platform_vendors %}
   * Cloud infrastructure provided by:
{% for vendor in platform_vendors %}
     * {{ vendor }}{% if vendor in baa_vendors %} (with BAA){% endif %}
{% endfor %}
{% endif %}

2. Data Storage
{% if data_storage_vendors %}
   * Data storage services provided by:
{% for vendor in data_storage_vendors %}
     * {{ vendor }}{% if vendor in baa_vendors %} (with BAA){% endif %}
{% endfor %}
{% endif %}

3. Device Management
{% if byod.policy_enabled %}
   * BYOD devices subject to:
     * {{ byod.security_requirements.encryption_required | default(false) | string | lower }} - Device encryption requirement
     * {{ byod.security_requirements.mdm_required | default(false) | string | lower }} - Mobile Device Management
     * {{ byod.management.remote_wipe_enabled | default(false) | string | lower }} - Remote wipe capability
{% endif %}

## Applicable Standards

{% if hitrust %}
### HITRUST Common Security Framework
* 0.9o - Management of Removable Media
* 01.y - Clear Desk and Clear Screen Policy
* 09.p - Disposal of Media
{% endif %}

{% if hipaa %}
### HIPAA Security Rule
* 164.310(d)(1) - Device and Media Controls
* 164.310(d)(2)(i) - Disposal
* 164.310(d)(2)(ii) - Media Re-use
{% endif %}

{% if soc2 %}
### SOC2 Requirements
* CC6.7 - System Component Protection
* CC6.8 - Secure Disposal
* CC8.1 - Change Management
{% endif %}

## Disposable Media Policy

1. All removable media is restricted, audited, and is encrypted.
2. {{ company }} assumes all disposable media in its Platform may contain ePHI, so it treats all disposable media with the same protections and disposal policies.
3. All destruction/disposal of ePHI media will be done in accordance with federal and state laws and regulations and pursuant to the {{ company }}’s written retention policy/schedule. Records that have satisfied the period of retention will be destroyed/disposed of in an appropriate manner.
4. Records involved in any open investigation, audit or litigation should not be destroyed/disposed of. If notification is received that any of the above situations have occurred or there is the potential for such, the record retention schedule shall be suspended for these records until such time as the situation has been resolved. If the records have been requested in the course of a judicial or administrative hearing, a qualified protective order will be obtained to ensure that the records are returned to the organization or properly destroyed/disposed of by the requesting party. 
5. Before reuse of any media, for example all ePHI is rendered inaccessible, cleaned, or scrubbed. All media is formatted to restrict future access.
6. All {{ company }} Subcontractors provide that, upon termination of the contract, they will return or destroy/dispose of all patient health information. In cases where the return or destruction/disposal is not feasible, the contract limits the use and disclosure of the information to the purposes that prevent its return or destruction/disposal.
7. Any media containing ePHI is disposed using a method that ensures the ePHI could not be readily recovered or reconstructed.
8. The methods of destruction, disposal, and reuse are reassessed periodically, based on current technology, accepted practices, and availability of timely and cost-effective destruction, disposal, and reuse technologies and services.
9. Service Termination Data Handling

{% if service_types.saas %}
### SaaS Service Termination
* Customer data available for export for 30 days post-termination
* Data provided in industry-standard formats
* Secure data deletion after export period
{% endif %}

{% if service_types.paas %}
### PaaS Service Termination
* 30-day data export window
* Customer environment decommissioning
* Infrastructure cleanup procedures
{% endif %}

{% if service_types.medical_device %}
### Medical Device Service Termination
* Device data export procedures
* Compliance with FDA requirements
* Secure device decommissioning
{% endif %}

{% if service_types.mobile_app %}
### Mobile App Service Termination
* User data export capabilities
* Local data wiping procedures
* Cloud data handling process
{% endif %}

In all cases, it is the Customer's responsibility to maintain HIPAA safeguards for any data exported from {{ company }} systems.