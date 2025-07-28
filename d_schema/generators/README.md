## Schema Formats Explained

This section provides examples of the different schema formats that D-Schema aims to support. When run with the `--profile` flag, schemas will be enriched with statistical data.

### 1. DDL Schema

Standard SQL Data Definition Language (DDL) statements. When profiling is enabled, key statistics are added as comments.

**Example (`--profile` enabled):**
```sql
# Table: hero
CREATE TABLE hero (
    id INTEGER NOT NULL,  -- Profile: 100.0% non-null, 1 distinct
    name VARCHAR(100) NOT NULL,  -- Profile: 100.0% non-null, 1 distinct
    PRIMARY KEY (id)
);
```

### 2. MAC-SQL Schema

A more descriptive format that includes table and column details. It natively integrates profiling data when available.

**Example (`--profile` enabled):**
```
# Table: hero (1 rows)
[
(id, the id of the hero. Value examples: ['1']. (Profile: 100.0% non-null, 1 distinct, min='1', max='1'))
(name, the name of the hero. Value examples: ['Superman']. (Profile: 100.0% non-null, 1 distinct, min='Superman', max='Superman', avg_len=8.0))
]
```

### 3. M-Schema

A minimal, clean representation. Profiling data is added as an extra element in the column's descriptive tuple.

**Example (`--profile` enabled):**
```
# Table: hero
(id:INTEGER, Primary Key, the id of the hero, Examples:[1], Profile: 100.0% non-null, 1 distinct values)
(name:TEXT, the name of the hero, Examples:[Superman], Profile: 100.0% non-null, 1 distinct values)
```

### 4. Profile Report

A detailed, human-readable report in Markdown format, designed specifically to display all collected profiling statistics. This format is only available when using the `--profile` flag.

**Example (`--schema-type profile-report --profile`):**
```markdown
### Table: `hero`
*Record Count: 1*

| Column Name | Data Type | Profile Details |
|-------------|-----------|-----------------|
| id | INTEGER | **Non-Null**: 100.0%<br>**Distinct**: 1<br>**Min**: 1<br>**Max**: 1<br>**Top Values**: '1' (1) |
| name | TEXT | **Non-Null**: 100.0%<br>**Distinct**: 1<br>**Min**: Superman<br>**Max**: Superman<br>**Avg. Len**: 8.00<br>**Top Values**: 'Superman' (1) |
```
