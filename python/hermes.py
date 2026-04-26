def hermes_process(content):
prompt = f"""
You are a Hermes Agent.

Transform the following content into structured input for the next AI step.

Tasks:

* Compress
* Normalize
* Preserve intent
* Add constraints

Content:
{content}
"""
return prompt
