{{ config(materialized='incremental', unique_key='message_id') }}

select
    message_id,
    parent_message_id,
    session_id,
    role,
    timestamp::timestamptz                          as created_at,
    text,
    len(text)                                       as text_length,
    project,
    cwd,
    git_branch,
    version,
    model,
    input_tokens,
    output_tokens,
    cache_read_tokens,
    cache_creation_tokens,
    coalesce(input_tokens, 0)
        + coalesce(output_tokens, 0)
        + coalesce(cache_read_tokens, 0)            as total_tokens
from {{ ref('raw_cc_messages') }}

{% if is_incremental() %}
where timestamp::timestamptz > (select max(created_at) from {{ this }})
{% endif %}
