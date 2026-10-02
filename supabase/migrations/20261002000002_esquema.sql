-- Comunidad de prácticas locales, Etapa 1 — Task 2: esquema (spec §5.1).
-- RLS queda activado en todas las tablas; las políticas y grants llegan con cada task siguiente.

create type public.estado_propuesta as enum ('en_votacion', 'en_bandeja', 'aprobada', 'rechazada', 'retirada');
create type public.estado_persona as enum ('activa', 'suspendida');

-- Catálogo DEIS (lo carga un script; nadie lo edita a mano).
create table public.establecimientos (
  codigo text primary key,
  nombre text not null,
  tipo text not null default '',
  comuna text not null default '',
  region text not null default '',
  vigente boolean not null default true
);

-- Ids de las fichas publicadas por la app (los carga el mismo script).
create table public.medicamentos (
  id text primary key check (id ~ '^[a-z0-9-]+$')
);

create table public.personas (
  id uuid primary key references auth.users (id) on delete restrict,
  correo text not null unique,
  nombre text not null,
  profesion text not null default '',
  establecimiento text references public.establecimientos (codigo) on delete restrict,
  pais_extranjero text check (pais_extranjero is null or btrim(pais_extranjero) <> ''),
  estado public.estado_persona not null default 'activa',
  invitada_el timestamptz not null default now(),
  -- Trabaja en un hospital chileno O fuera de Chile, nunca ambos.
  constraint personas_hospital_o_pais check (establecimiento is null or pais_extranjero is null)
);

create table public.administradores (
  persona uuid primary key references public.personas (id) on delete restrict
);

create table public.historial_hospital (
  id uuid primary key default gen_random_uuid(),
  persona uuid not null references public.personas (id) on delete restrict,
  desde text,
  hacia text not null,
  fecha timestamptz not null default now()
);
create index historial_hospital_persona on public.historial_hospital (persona);

create table public.propuestas (
  id uuid primary key default gen_random_uuid(),
  medicamento text not null references public.medicamentos (id) on delete restrict,
  establecimiento text not null references public.establecimientos (codigo) on delete restrict,
  texto text not null check (char_length(btrim(texto)) between 1 and 500),
  autora uuid not null references public.personas (id) on delete restrict,
  creada_el timestamptz not null default now(),
  estado public.estado_propuesta not null default 'en_votacion',
  texto_publicado text check (texto_publicado is null or char_length(btrim(texto_publicado)) between 1 and 500),
  comentario_admin text check (comentario_admin is null or char_length(comentario_admin) <= 500),
  resuelta_el timestamptz
);
create index propuestas_estado on public.propuestas (estado);
create index propuestas_medicamento on public.propuestas (medicamento);

create table public.votos (
  propuesta uuid not null references public.propuestas (id) on delete restrict,
  persona uuid not null references public.personas (id) on delete restrict,
  a_favor boolean not null,
  establecimiento_al_votar text references public.establecimientos (codigo) on delete restrict,
  pais_al_votar text,
  fecha timestamptz not null default now(),
  primary key (propuesta, persona)
);
create index votos_propuesta on public.votos (propuesta);

create table public.bitacora (
  id bigint generated always as identity primary key,
  fecha timestamptz not null default now(),
  actor uuid references public.personas (id) on delete restrict,
  accion text not null,
  objeto text,
  detalle jsonb not null default '{}'::jsonb
);
create index bitacora_fecha on public.bitacora (fecha);

alter table public.establecimientos enable row level security;
alter table public.medicamentos enable row level security;
alter table public.personas enable row level security;
alter table public.administradores enable row level security;
alter table public.historial_hospital enable row level security;
alter table public.propuestas enable row level security;
alter table public.votos enable row level security;
alter table public.bitacora enable row level security;
