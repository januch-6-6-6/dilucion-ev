-- Etapa 1 — Task 6: funciones del administrador y vista pública de notas aprobadas.
-- Cada función verifica es_admin() y registra en la bitácora dentro de la misma transacción.

create function public.exigir_admin() returns void
language plpgsql security definer stable set search_path = public
as $$ begin
  if not public.es_admin() then
    raise exception 'Solo el administrador puede hacer esto';
  end if;
end $$;
revoke all on function public.exigir_admin() from public, anon, authenticated;

create function public.aprobar(p uuid, texto_final text default null) returns void
language plpgsql security definer set search_path = public
as $$
declare v public.propuestas;
begin
  perform public.exigir_admin();
  select * into v from public.propuestas where id = p for update;
  if not found or v.estado not in ('en_votacion', 'en_bandeja') then
    raise exception 'Esta propuesta no se puede aprobar';
  end if;
  update public.propuestas
     set estado = 'aprobada', texto_publicado = coalesce(texto_final, v.texto), resuelta_el = now()
   where id = p;
  if texto_final is not null and texto_final is distinct from v.texto then
    perform public.registrar('edito_y_aprobo', p::text, jsonb_build_object('antes', v.texto, 'despues', texto_final));
  else
    perform public.registrar('aprobo', p::text, '{}'::jsonb);
  end if;
end $$;

create function public.rechazar(p uuid, comentario text) returns void
language plpgsql security definer set search_path = public
as $$
declare v public.propuestas;
begin
  perform public.exigir_admin();
  if comentario is null or char_length(btrim(comentario)) not between 1 and 500 then
    raise exception 'El comentario es obligatorio (hasta 500 caracteres)';
  end if;
  select * into v from public.propuestas where id = p for update;
  if not found or v.estado not in ('en_votacion', 'en_bandeja') then
    raise exception 'Esta propuesta no se puede rechazar';
  end if;
  update public.propuestas set estado = 'rechazada', comentario_admin = btrim(comentario), resuelta_el = now() where id = p;
  perform public.registrar('rechazo', p::text, jsonb_build_object('comentario', btrim(comentario)));
end $$;

create function public.retirar_nota(p uuid, motivo text) returns void
language plpgsql security definer set search_path = public
as $$
declare v public.propuestas;
begin
  perform public.exigir_admin();
  if motivo is null or char_length(btrim(motivo)) not between 1 and 500 then
    raise exception 'El motivo es obligatorio (hasta 500 caracteres)';
  end if;
  select * into v from public.propuestas where id = p for update;
  if not found or v.estado <> 'aprobada' then
    raise exception 'Solo se puede retirar una nota aprobada';
  end if;
  update public.propuestas set estado = 'retirada', comentario_admin = btrim(motivo) where id = p;
  perform public.registrar('retiro', p::text, jsonb_build_object('motivo', btrim(motivo), 'por', 'administrador'));
end $$;

create function public.suspender(persona uuid) returns void
language plpgsql security definer set search_path = public
as $$
begin
  perform public.exigir_admin();
  if suspender.persona = auth.uid() then
    raise exception 'No puedes suspenderte a ti mismo';
  end if;
  update public.personas set estado = 'suspendida' where id = suspender.persona;
  if not found then raise exception 'La persona no existe'; end if;
  perform public.registrar('suspendio', suspender.persona::text, '{}'::jsonb);
end $$;

create function public.reactivar(persona uuid) returns void
language plpgsql security definer set search_path = public
as $$
begin
  perform public.exigir_admin();
  update public.personas set estado = 'activa' where id = reactivar.persona;
  if not found then raise exception 'La persona no existe'; end if;
  perform public.registrar('reactivo', reactivar.persona::text, '{}'::jsonb);
end $$;

create function public.cambiar_umbral(n int) returns void
language plpgsql security definer set search_path = public
as $$
declare antes int;
begin
  perform public.exigir_admin();
  if n is null or n not between 1 and 50 then
    raise exception 'El umbral debe estar entre 1 y 50';
  end if;
  select umbral_votos into antes from public.ajustes where id = 1;
  update public.ajustes set umbral_votos = n where id = 1;
  perform public.registrar('cambio_umbral', '1', jsonb_build_object('antes', antes, 'despues', n));
end $$;

-- Quien no es administrador llega a la función y recibe el mensaje; el público ni siquiera puede ejecutarla.
revoke all on function public.aprobar(uuid, text), public.rechazar(uuid, text), public.retirar_nota(uuid, text),
  public.suspender(uuid), public.reactivar(uuid), public.cambiar_umbral(int) from public, anon;
grant execute on function public.aprobar(uuid, text), public.rechazar(uuid, text), public.retirar_nota(uuid, text),
  public.suspender(uuid), public.reactivar(uuid), public.cambiar_umbral(int) to authenticated;

-- Lo único que el público lee de la comunidad: notas aprobadas, sin autora.
create view public.notas_publicadas as
select
  p.id,
  p.medicamento,
  p.establecimiento,
  e.nombre as nombre_establecimiento,
  p.texto_publicado,
  p.resuelta_el,
  (select count(*) from public.votos v join public.personas pe on pe.id = v.persona and pe.estado = 'activa'
     where v.propuesta = p.id and v.a_favor)::int as votos_a_favor
from public.propuestas p
join public.establecimientos e on e.codigo = p.establecimiento
where p.estado = 'aprobada';

revoke all on public.notas_publicadas from public, anon, authenticated;
grant select on public.notas_publicadas to anon, authenticated;
