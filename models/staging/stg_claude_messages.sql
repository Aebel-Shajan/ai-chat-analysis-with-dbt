with unnested as (
    select
        uuid                                        as conversation_id,
        unnest(chat_messages)                       as msg
    from {{ ref('raw_claude_chat') }}
)

select
    msg.uuid                                        as message_id,
    conversation_id,
    msg.sender,
    msg.text,
    msg.created_at::timestamptz                     as created_at,
    msg.updated_at::timestamptz                     as updated_at,
    msg.parent_message_uuid                         as parent_message_id,
    len(msg.attachments) > 0                        as has_attachments,
    len(msg.files) > 0                              as has_files,
    len(msg.text)                                   as text_length
from unnested
