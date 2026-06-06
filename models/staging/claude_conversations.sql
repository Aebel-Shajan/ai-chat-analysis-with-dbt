{{ config(materialized='view') }}

select
    uuid                                            as conversation_id,
    name                                            as conversation_name,
    summary,
    created_at::timestamptz                         as created_at,
    updated_at::timestamptz                         as updated_at,
    account.uuid                                    as account_id
from {{ ref('raw_conversations') }}
