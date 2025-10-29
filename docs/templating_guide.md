# Examples of Jinja2 support in these documents

The configuration values for the [Jinja2](https://jinja.palletsprojects.com/en/stable/) portions of these documents are found in `/conf/config.yaml`

The github workflow/action script also supports Jinja2 for filenames. For example, if `/conf/config.yaml` contains:  
```yaml
company: Acme
```
then changing the filename:

   `/policies/introduction.md` 

to 

  `/policies/{{ company }}_introduction.md` 

should create the following output filenames:

* `/pdf/Acme_introduction.pdf`
* `/md/Acme_introduction.md`

## Example Content Formatting

{% if hipaa %}
## HIPAA Requirements
This policy supports 45 CFR § 164.312(a)(1) \- Access Control.  
All ePHI access must be logged and reviewed.  
{% endif %}  

{% if hitRUST %}
## HITRUST CSF Requirements
This policy maps to control vX.Y of the HITRUST Common Security Framework.  
{% endif %}  

{% if soc2 %}
## SOC2 Trust Criteria
This policy addresses Common Criteria (CC) 6.1.  
{% endif %}

## Compliance (notice nested jinja)
{{ company }} provides compliant hosted software infrastructure for its Customers.  

{% if hipaa %}  
{{ company }} is HIPAA compliant.  
{% if hipaa_audit_inprogress %}  
{{ company }} undergoing a HIPAA compliance audit by a 3rd party compliance firm to validate and map organizational policies and technical settings to HIPAA rules.  
{% endif %}  
{% if hipaa_audit_completed %}   
{{ company }} has been through a HIPAA compliance audit by a national, 3rd party compliance firm, to validate and map organizational policies and technical settings to HIPAA rules. This audit was last completed on {{ hipaa_audit_completed_date }}.  
{% endif %}
{% endif %}  

{% if hitRUST %}  
{{ company }} is compliant with the HITRUST CSF.  
{% if hitRUST_audit_inprogress %}  
{{ company }} is currently undergoing a HITRUST audit to achieve HITRUST Certification.  
{% endif %}  
{% if hitRUST_audit_completed %}  
{{ company }} has been through a HITRUST audit and achieved HITRUST Certification on {{ hitRUST_certification_date }}.  
{% endif %}
{% endif %}  

{% if show_internal_notes %}  
Internal Note: This section must be reviewed by {{ security_officer_name }}  
by Q4. This note will only appear if show_internal_notes is true in the config.  
{% endif %}

# **Basic Intro Example (with Jinja2 variables)**
{{ company_name }} "{{ company }}" is committed to ensuring the confidentiality, privacy, integrity, and availability of all electronic protected health information (ePHI) it receives, maintains, processes and/or transmits on behalf of its Customers. As providers of compliant, {{ company_service }} used by {{ company_service_user_types }}, {{ company }} strives to maintain compliance, proactively address information security, mitigate risk for its Customers, and assure known breaches are completely and effectively communicated in a timely manner. 

{% if PaaS %}
## **Platform as a Service (PaaS)**
PaaS Customers utilized hosted software and infrastructure from {{ company }} to deploy, host, and scale custom developed applications and configured databases. These customers are deployed into compliant containers run on systems secured and managed by {{ company }}. {{ company }} does not have insight or access into application level data of PaaS Customers and, as such, does not have the ability to secure or manage risk associated with application level vulnerabilities and security weaknesses. {{ company }} makes every effort to reduce the risk of unauthorized disclosure, access, and/or breach of PaaS Customer data through network (firewalls, dedicated IP spaces, etc) and server settings (encryption at rest and in transit, OSSEC throughout the Platform, etc)....  
{% endif %}

## Example of Jinja Loop

{% if show\_review\_committee %}

## Policy Review Committee
This policy has been reviewed and approved by the following members:  
{% for member in review_committee %}

* {{ member }}  
  {% endfor %}

{% endif %}