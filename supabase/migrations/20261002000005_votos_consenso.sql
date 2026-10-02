-- Etapa 1 — Task 5: votos y regla del consenso.

create function public.votos_antes_de_escribir() returns trigger
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
  select * into pr from public.propuestas where id = new.propuesta;
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

create trigger votos_antes_escribir before insert or update on public.votos
  for each row execute function public.votos_antes_de_escribir();

-- Cuenta solo votos de personas activas. Pasa a la bandeja con >= umbral votos a favor del mismo hospital
-- y más votos a favor que en contra (todos los hospitales y países). Nunca retrocede.
create function public.evaluar_umbral(p uuid) returns void
language plpgsql security definer set search_path = public
as $$
declare
  pr public.propuestas;
  umbral int;
  local_ int;
  favor int;
  contra int;
begin
  select * into pr from public.propuestas where id = p for update;
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

revoke all on function public.evaluar_umbral(uuid) from public, anon, authenticated;

create function public.votos_despues_de_escribir() returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  perform public.registrar(case tg_op when 'INSERT' then 'voto' else 'cambio_voto' end, new.propuesta::text,
                           jsonb_build_object('a_favor', new.a_favor));
  perform public.evaluar_umbral(new.propuesta);
  return new;
end $$;

create trigger votos_despues_escribir after insert or update on public.votos
  for each row execute function public.votos_despues_de_escribir();

-- Permisos: votar y cambiar solo el sentido del voto propio; leer solo lo propio (el administrador lee todo).
revoke all on public.votos from anon, authenticated;
grant select, insert on public.votos to authenticated;
grant update (a_favor) on public.votos to authenticated;

create policy votos_votar on public.votos for insert to authenticated
  with check (public.persona_activa());
create policy votos_cambiar on public.votos for update to authenticated
  using (persona = auth.uid())
  with check (persona = auth.uid());
create policy votos_ver on public.votos for select to authenticated
  using (persona = auth.uid() or public.es_admin());
