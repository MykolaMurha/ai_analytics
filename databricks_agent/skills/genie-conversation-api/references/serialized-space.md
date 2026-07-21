# `serialized_space` schema & validation (reference)

Source: https://docs.databricks.com/aws/en/genie-agents/conversation-api
(captured 2026-07-21). Used with `POST`/`PUT /api/2.0/genie/spaces` to
programmatically create or update an agent. It is a **JSON string** (serialize
the object below with `json.dumps`).

## Structure

```json
{
  "version": 2,
  "config": {
    "sample_questions": [
      { "id": "<32-char-hex>", "question": ["<question>"] }
    ]
  },
  "data_sources": {
    "tables": [
      {
        "identifier": "catalog.schema.table",
        "description": ["<description>"],
        "column_configs": [
          {
            "column_name": "<name>",
            "synonyms": ["<synonym>"],
            "enable_entity_matching": true,
            "exclude": false
          }
        ]
      }
    ],
    "metric_views": []
  },
  "instructions": {
    "text_instructions": [
      { "id": "<32-char-hex>", "content": ["<instruction>"] }
    ],
    "example_question_sqls": [
      {
        "id": "<32-char-hex>",
        "question": ["<question>"],
        "sql": ["<sql>"],
        "parameters": [],
        "usage_guidance": ["<guidance>"]
      }
    ],
    "sql_functions": [
      { "id": "<32-char-hex>", "identifier": "catalog.schema.function" }
    ],
    "join_specs": [
      {
        "id": "<32-char-hex>",
        "left":  { "identifier": "...", "alias": "..." },
        "right": { "identifier": "...", "alias": "..." },
        "sql":   ["join_condition", "--rt=FROM_RELATIONSHIP_TYPE_MANY_TO_ONE--"],
        "comment": ["<comment>"],
        "instruction": ["<instruction>"]
      }
    ],
    "sql_snippets": {
      "filters": [
        {
          "id": "<32-char-hex>",
          "sql": ["<sql>"],
          "display_name": "<name>",
          "synonyms": ["<synonym>"],
          "comment": ["<comment>"],
          "instruction": ["<instruction>"]
        }
      ],
      "expressions": [],
      "measures": []
    }
  },
  "benchmarks": {
    "questions": [
      {
        "id": "<32-char-hex>",
        "question": ["<question>"],
        "answer": [ { "format": "SQL", "content": ["<sql>"] } ]
      }
    ]
  }
}
```

## Validation rules — get these right or the API rejects the payload

### ID format
- Every `id` is a **32-character lowercase hexadecimal** string, **no hyphens**.
- Valid example: `a1b2c3d4e5f60000000000000000000a`.
- Generate in Python:
  ```python
  import secrets
  new_id = secrets.token_hex(16)   # 16 bytes -> 32 hex chars
  ```

### Sorting (arrays must be pre-sorted)
- `data_sources.tables` — by `identifier` (alphabetical)
- `data_sources.metric_views` — by `identifier`
- `config.sample_questions` — by `id`
- `instructions.text_instructions` — by `id`
- all `sql_snippets` arrays (`filters`, `expressions`, `measures`) — by `id`
- `join_specs` — by `id`

### Uniqueness
- Question `id`s unique **across** `sample_questions` **and**
  `benchmarks.questions`.
- Instruction `id`s unique across **all** instruction types.
- Column configs: `(table_identifier, column_name)` must be unique.

### Size limits
- Any string element: **≤ 25,000 characters**.
- Any array: **≤ 10,000 items**.
- **Exactly one** `text_instructions` entry per agent.
- `join_specs.sql` must have **exactly 2** elements: the join condition **and**
  the relationship-type annotation (`--rt=FROM_RELATIONSHIP_TYPE_*--`).

### Identifiers
- Tables and functions use the **three-level** name `catalog.schema.table`.

## Practical tips

- Round-trip first: `GET .../spaces/{id}?include_serialized_space=true`, tweak,
  then `PUT` back — easier than authoring from scratch.
- Note the many **list-wrapped scalars** (`"question": ["..."]`,
  `"description": ["..."]`) — the schema wraps single values in arrays.
- Validate IDs, sorting, and uniqueness client-side before sending; the API is
  strict and error messages can be terse.
