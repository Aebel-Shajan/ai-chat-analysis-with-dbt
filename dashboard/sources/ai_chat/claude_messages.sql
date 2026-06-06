select
    m.*,
    c.conversation_name
from main_staging.stg_claude_messages m
join main_staging.stg_claude_conversations c using (conversation_id)
