import json
from etk.etk import ETK
from etk.extractors.glossary_extractor import GlossaryExtractor

sample_input = {
    "projects": [
        {
            "name": "etk",
            "description": "version 2 of etk, implemented by Runqi, Dongyu, Sylvia and others."
        }
    ]
}

etk = ETK()
doc = etk.create_document(sample_input)

name_extractor = GlossaryExtractor(etk.load_glossary("./names.txt"))

descriptions_path = etk.parser("projects[*].description")
projects_path = etk.parser("projects[*]")

descriptions = doc.select_segments(descriptions_path)
projects = doc.select_segments(projects_path)

for d, p in zip(descriptions, projects):
    names = doc.invoke_extractor(name_extractor, d)
    p.store_extractions(names, "members")

print(json.dumps(sample_input, indent=2))