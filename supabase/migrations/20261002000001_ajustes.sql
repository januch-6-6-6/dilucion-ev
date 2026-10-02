-- Comunidad de prácticas locales, Etapa 1 — Task 1: ajustes.
-- Una sola fila con el umbral de votos que lleva una propuesta a la bandeja del administrador.

create table public.ajustes (
  id smallint primary key default 1 check (id = 1),
  umbral_votos int not null default 3 check (umbral_votos between 1 and 50)
);

insert into public.ajustes (id, umbral_votos) values (1, 3);

-- RLS activado y sin políticas: nadie con sesión pública o de invitada lee ni escribe.
-- Solo la clave de servicio (que se salta RLS) y las funciones security definer de tasks posteriores.
alter table public.ajustes enable row level security;
