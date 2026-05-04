---
name: xml-serialization-security
description: >
  Apply when reviewing or writing code that parses XML, processes
  DTDs, transforms XSLT, or deserializes data from untrusted sources.
  Covers XXE prevention, entity expansion, parser hardening, and
  safe deserialization per language.
license: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
origin: Adapted from CoSAI Project CodeGuard (https://github.com/cosai-oasis/project-codeguard)
category: "secure_development"
subcategory: "web-security"
---

# XML and Serialization Hardening

Secure parsing and processing of XML and serialized data. Prevent XXE, entity expansion, SSRF, DoS, and unsafe deserialization across platforms.

## XML Parser Hardening

- Disable DTDs and external entities by default; reject DOCTYPE declarations.
- Validate strictly against local, trusted XSDs; set explicit limits (size, depth, element counts).
- Sandbox or block resolver access; no network fetches during parsing; monitor for unexpected DNS activity.

### Java

Java parsers have XXE enabled by default. Primary defense -- disallow DTDs completely:

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setXIncludeAware(false);
```

If DTDs cannot be completely disabled, disable external entities individually:

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
String[] featuresToDisable = {
    "http://xml.org/sax/features/external-general-entities",
    "http://xml.org/sax/features/external-parameter-entities",
    "http://apache.org/xml/features/nonvalidating/load-external-dtd"
};
for (String feature : featuresToDisable) {
    dbf.setFeature(feature, false);
}
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
```

### .NET

```csharp
var settings = new XmlReaderSettings {
    DtdProcessing = DtdProcessing.Prohibit,
    XmlResolver = null
};
var reader = XmlReader.Create(stream, settings);
```

### Python

```python
# Option 1: defusedxml (preferred)
from defusedxml import ElementTree as ET
ET.parse('file.xml')

# Option 2: lxml with safe settings
from lxml import etree
parser = etree.XMLParser(resolve_entities=False, no_network=True)
tree = etree.parse('filename.xml', parser)
```

## Secure XSLT / Transformer Usage

- Set `ACCESS_EXTERNAL_DTD` and `ACCESS_EXTERNAL_STYLESHEET` to empty strings.
- Avoid loading remote resources during transformation.

## Deserialization Safety

**General rule**: never deserialize untrusted native objects. Prefer JSON with schema validation. Enforce size/structure limits before parsing. Reject polymorphic types unless strictly allow-listed.

### Per-Language Guidance

| Language | Dangerous | Safe Alternative |
|----------|-----------|-----------------|
| **PHP** | `unserialize()` | `json_decode()` |
| **Python** | `pickle`, `yaml.load()` | `json.loads()`, `yaml.safe_load()` |
| **Java** | Default `ObjectInputStream`, Jackson default typing, XStream without allow-lists | Override `resolveClass` with allow-list; disable default typing; use XStream allow-lists |
| **.NET** | `BinaryFormatter` | `DataContractSerializer`, `System.Text.Json` with `TypeNameHandling=None` |
| **Ruby** | `Marshal.load` from untrusted input | `JSON.parse()` |

### Additional Controls

- Sign and verify serialized payloads where applicable.
- Log and alert on deserialization failures and anomalies.
- Keep all parsing and deserialization libraries up to date.

## Implementation Checklist

- [ ] DTDs disabled; external entities off; strict schema validation; parser limits set
- [ ] No network access during XML parsing; resolvers restricted
- [ ] XSLT transformers block external DTD and stylesheet access
- [ ] No unsafe native deserialization (`pickle`, `unserialize`, `BinaryFormatter`, `Marshal.load`)
- [ ] JSON preferred over native serialization for untrusted data
- [ ] Allow-lists enforced for any remaining native deserialization
- [ ] Regular testing with XXE and deserialization payloads

## Test Plan

- Automated checks for dangerous parser configurations and deserialization calls.
- Test with XXE payloads (external entity, parameter entity, Billion Laughs).
- Verify XSLT resolvers block external resources.
- Fuzz deserialization endpoints with malformed and oversized payloads.
