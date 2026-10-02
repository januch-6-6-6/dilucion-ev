-- Etapa 1 — arreglo de la revisión final: votos simultáneos.
-- El INSERT en `votos` toma KEY SHARE sobre la propuesta (clave foránea) y luego evaluar_umbral pedía FOR UPDATE:
-- dos votos a la vez se esperaban mutuamente (deadlock), y un voto podía leer el estado antes de que `aprobar`
-- lo cambiara. Ahora el voto toma FOR NO KEY UPDATE desde el primer momento: los votos de una propuesta se
-- serializan, releen el estado vigente y no chocan con la clave foránea.

create or replace function public.votos_antes_de_escribir() returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  yo uuid := auth.uid();
  p public.personas;
  pr public.propuestas;
begin
  if yo is null then -- clave de servicio: se siembran datos tal cual
    return new;
  end if;
  select * into p from public.personas where id = yo;
  if not found or p.estado <> 'activa' then
    raise exception 'Tu acceso está suspendido';
  end if;
  if p.establecimiento is null and p.pais_extranjero is null then
    raise exception 'Elige tu hospital antes de votar';
  end if;
  select * into pr from public.propuestas where id = new.propuesta for no key update;
  if not found then
    raise exception 'La propuesta no existe';
  end if;
  if pr.autora = yo then
    raise exception 'No puedes votar tu propia propuesta';
  end if;
  if pr.estado <> 'en_votacion' then
    raise exception 'La votación de esta propuesta está cerrada';
  end if;
  if tg_op = 'UPDATE' then
    new.propuesta := old.propuesta;
  end if;
  new.persona := yo;
  new.establecimiento_al_votar := p.establecimiento;
  new.pais_al_votar := p.pais_extranjero;
  new.fecha := now();
  return new;
end $$;

create or replace function public.evaluar_umbral(p uuid) returns void
language plpgsql security definer set search_path = public
as $$
declare
  pr public.propuestas;
  umbral int;
  local_ int;
  favor int;
  contra int;
begin
  select * into pr from public.propuestas where id = p for no key update;
  if not found or pr.estado <> 'en_votacion' then
    return;
  end if;
  select umbral_votos into umbral from public.ajustes where id = 1;
  select
    count(*) filter (where v.a_favor and v.establecimiento_al_votar = pr.establecimiento),
    count(*) filter (where v.a_favor),
    count(*) filter (where not v.a_favor)
  into local_, favor, contra
  from public.votos v join public.personas pe on pe.id = v.persona and pe.estado = 'activa'
  where v.propuesta = p;
  if local_ >= umbral and favor > contra then
    update public.propuestas set estado = 'en_bandeja' where id = p;
    insert into public.bitacora (actor, accion, objeto, detalle)
      values (null, 'paso_a_bandeja', p::text, jsonb_build_object('a_favor_local', local_, 'a_favor', favor, 'en_contra', contra));
  end if;
end $$;
