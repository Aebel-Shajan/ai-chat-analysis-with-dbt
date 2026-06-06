{{ config(materialized='view') }}

select *
from read_json_auto('data/extracted/conversations.json')
