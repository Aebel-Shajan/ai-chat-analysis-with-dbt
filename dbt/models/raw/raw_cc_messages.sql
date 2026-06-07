{{ config(materialized='view') }}

select *
from read_json_auto('s3://{{ env_var("R2_BUCKET") }}/claude_code/messages.jsonl')
