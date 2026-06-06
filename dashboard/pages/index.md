---
title: AI Chat Analysis
---

```sql messages_by_month
select
    date_trunc('month', created_at)::date as month,
    count(*) filter (where sender = 'human') as user_messages,
    count(*) filter (where sender = 'assistant') as assistant_messages
from ai_chat.claude_messages
group by 1
order by 1
```

```sql top_conversations
select
    conversation_name,
    count(*) as messages,
    min(created_at)::date as date
from ai_chat.claude_messages
group by conversation_name
order by messages desc
limit 10
```

```sql activity_by_hour
select
    extract(hour from created_at)::int as hour,
    count(*) as messages
from ai_chat.claude_messages
where sender = 'human'
group by 1
order by 1
```

## Messages Over Time

<BarChart
    data={messages_by_month}
    x=month
    y={["user_messages", "assistant_messages"]}
    type=stacked
/>

## Most Active Conversations

<DataTable data={top_conversations} />

## Activity by Hour of Day

<BarChart
    data={activity_by_hour}
    x=hour
    y=messages
/>
