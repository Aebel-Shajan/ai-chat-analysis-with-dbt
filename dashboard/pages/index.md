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

---
title: Usage Heatmap
---

```sql available_years
select distinct extract(year from created_at)::int as year
from ai_chat.claude_messages
union
select distinct extract(year from created_at)::int
from ai_chat.cc_messages
order by 1 desc
```

<Dropdown
    name=year
    data={available_years}
    value=year
    title="Year"
    defaultValue="2024"
    noDefault=true
/>

```sql chat_daily
select
    created_at::date as date,
    count(*) as messages
from ai_chat.claude_messages
where sender = 'human'
  and created_at >= '${inputs.dates.start}'
  and created_at <= '${inputs.dates.end}'
  and extract(year from created_at) = ${inputs.year.value}
group by 1
order by 1
```

```sql cc_daily
select
    created_at::date as date,
    count(*) as messages
from ai_chat.cc_messages
where role = 'user'
  and created_at >= '${inputs.dates.start}'
  and created_at <= '${inputs.dates.end}'
  and extract(year from created_at) = ${inputs.year.value}
group by 1
order by 1
```

## Claude Chat

<CalendarHeatmap
    data={chat_daily}
    date=date
    value=messages
    title="Daily Claude Chat Messages"
/>

## Claude Code

<CalendarHeatmap
    data={cc_daily}
    date=date
    value=messages
    title="Daily Claude Code Messages"
/>

## Messages Over Time

<BarChart
    data={messages_by_month}
    x=month
    y={["user_messages", "assistant_messages"]}
    type=stacked
/>

## Activity by Hour of Day

<BarChart
    data={activity_by_hour}
    x=hour
    y=messages
/>

## Most Active Conversations

<DataTable data={top_conversations} />