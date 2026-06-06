{{ config(materialized='incremental', unique_key='session_id') }}

select
    session_id,
    project,
    min(created_at)                                 as started_at,
    max(created_at)                                 as ended_at,
    datediff('minute', min(created_at), max(created_at)) as duration_minutes,
    count(*)                                        as total_messages,
    count(*) filter (where role = 'user')           as user_messages,
    count(*) filter (where role = 'assistant')      as assistant_messages,
    sum(input_tokens)                               as total_input_tokens,
    sum(output_tokens)                              as total_output_tokens,
    sum(cache_read_tokens)                          as total_cache_read_tokens,
    max(model)                                      as model,
    max(cwd)                                        as cwd,
    max(git_branch)                                 as git_branch,
    max(version)                                    as version
from {{ ref('stg_cc_messages') }}
group by session_id, project
