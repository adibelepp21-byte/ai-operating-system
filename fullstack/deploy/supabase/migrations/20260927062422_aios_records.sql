-- AIOS Full Stack: the StorageFacility backend on Supabase (FS-DP-01 Option A,
-- ratified FS-ARCH-RAT-001, Register §68).
--
-- Every object here is required by the StorageFacility contract
-- (native_core/core/infrastructure/storage.py), and nothing else is created:
--
--   append(partition, record: bytes)  -> one row: partition, record
--   read(partition), in append order   -> seq, a strictly increasing identity
--   partitions()                       -> aios_partitions()
--   no edit, no delete                 -> privileges + triggers refuse both
--
-- Entities keep their own meaning inside `record`; the database models none
-- of them. The record is stored as bytes, unchanged, so a read returns exactly
-- what was appended. It may not hold a raw newline, as in the local backend,
-- so an export to the local store's line format is lossless.

create table public.aios_records (
    seq       bigint generated always as identity primary key,
    partition text   not null
              check (partition <> '' and partition not in ('.', '..')
                     and strpos(partition, '/') = 0 and strpos(partition, E'\\') = 0
                     and length(partition) <= 200),
    record    bytea  not null
              check (position('\x0a'::bytea in record) = 0)
);

comment on table public.aios_records is
    'AIOS StorageFacility backend: append-only partitions of opaque records. '
    'seq is the append order. No update, delete or truncate (INV-5).';

create index aios_records_partition_seq on public.aios_records (partition, seq);

-- Append-only, second barrier: even a role that holds the privilege is refused.
create function public.aios_records_refuse_mutation()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
    raise exception 'aios_records is append-only: % refused', tg_op
        using errcode = 'insufficient_privilege';
end;
$$;

create trigger aios_records_no_update_or_delete
    before update or delete on public.aios_records
    for each row execute function public.aios_records_refuse_mutation();

create trigger aios_records_no_truncate
    before truncate on public.aios_records
    for each statement execute function public.aios_records_refuse_mutation();

-- partitions(): the names of existing partitions, in byte order like the
-- local backend's sorted file names.
create function public.aios_partitions()
returns setof text
language sql
stable
security invoker
set search_path = ''
as $$
    select distinct partition collate "C" from public.aios_records order by 1;
$$;

-- No browser path: Row Level Security on, and no policy for any role. The
-- backend alone reads and appends, with a server-side key (service_role).
alter table public.aios_records enable row level security;

revoke all on table public.aios_records from public, anon, authenticated, service_role;
grant select, insert on table public.aios_records to service_role;

revoke all on function public.aios_partitions() from public, anon, authenticated;
grant execute on function public.aios_partitions() to service_role;
revoke all on function public.aios_records_refuse_mutation() from public, anon, authenticated, service_role;
