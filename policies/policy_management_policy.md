# Policy Management Policy

{% if hipaa %}
## HIPAA Compliance Context
This policy addresses the requirements of HIPAA § 164.316(a) - Policies and Procedures and § 164.316(b)(1)(i) - Documentation. It establishes a framework for maintaining, updating, and managing all organizational policies in a compliant manner.
{% endif %}

{% if soc2 %}
## SOC2 Compliance Context
This policy supports SOC2 Common Criteria (CC) 2.1 and CC 2.2, ensuring that information security policies are established, communicated, and periodically reviewed and updated.
{% endif %}

{{ company }} implements policies and procedures to maintain compliance and integrity of data. The Security Officer and Privacy Officer are responsible for maintaining policies and procedures and assuring all {{ company }} workforce members, business associates, customers, and partners are adherent to all applicable policies. Previous versions of polices are retained to assure ease of finding policies at specific historic dates in time.

## Applicable Standards from the HITRUST Common Security Framework

* 12.c - Developing and Implementing Continuity Plans Including Information Security

## Applicable Standards from the HIPAA Security Rule

* 164.316(a) - Policies and Procedures
* 164.316(b)(1)(i) - Documentation

## Maintenance of Policies

1. All policies are stored and up to date to maintain {{ company }} compliance with HIPAA, HITRUST, NIST, and other relevant standards. Updates and version control is done similar to source code control.
2. Policy update requests can be made by any workforce member at any time. Furthermore, all policies are reviewed annually by both the Security and Privacy Officer to ensure that they are accurate and up-to-date.
3. Edits and updates made by appropriate and authorized workforce members are done on their own versions, or branches. These changes are only merged back into final, or master, versions by the Privacy or Security Officer, similarly to a pull request. All changes are linked to workforce personnel who made them and the Officer who accepted them.
4. All policies are made accessible to all {{ company }} workforce members. The current master policies are published at {{ policy_website }}.
	* Changes can be requested to policies using the change request form at {{ change_request_form_link }}. 
5. All policies, and associated documentation, are retained for 6 years from the date of its creation or the date when it last was in effect, whichever is later
	1. Version history of all {{ company }} policies is done via Github.
	2. Backup storage of all policies is done with Box.
6. The policies and information security policies are reviewed and audited annually. Issues that come up as part of this process are reviewed by {{ company }} management to assure all risks and potential gaps are mitigated and/or fully addressed. 

{% if hitRUST %}
7. {{ company }} utilizes the HITRUST MyCSF framework to track compliance with the HITRUST CSF on an annual basis. 
{% endif %}

{% if hipaa %}
8. {{ company }} tracks HIPAA compliance and publishes results at {{ hipaa_website }}.
{% endif %}

Additional documentation related to maintenance of policies is outlined in the Security Officer's responsibilities.