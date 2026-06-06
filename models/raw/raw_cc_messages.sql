{{ config(materialized='view') }}

select *
from read_json_auto('data/extracted/claude_code/messages.jsonl')
