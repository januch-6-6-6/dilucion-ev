-- Etapa 1 — Task 4: propuestas.
-- Las llamadas con clave de servicio (auth.uid() nulo) no se sobrescriben: sirven para sembrar datos y para el administrador de infraestructura.

create function public.propuestas_antes_de_insertar() returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  yo uuid := auth.uid();
  p public.personas;
begin
  if yo is null then
    return new;
  end if;
  select * into p from public.personas where id = yo;
  if not found or p.estado <> 'activa' then
    raise exception 'Tu acceso está suspendido';
  end if;
  if p.establecimiento is null then
    raise exception 'Las prácticas locales se proponen desde hospitales chilenos';
  end if;
  new.autora := yo;
  new.establecimiento := p.establecimiento;
  new.estado := 'en_votacion';
  new.texto_publicado := null;
  new.comentario_admin := null;
  new.resuelta_el := null;
  new.creada_el := now();
  return new;
end $$;

create trigger propuestas_antes_insertar before insert on public.propuestas
  for each row execute function public.propuestas_antes_de_insertar();

create function public.propuestas_despues_de_insertar() returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  perform public.registrar('propuso', new.id::text, jsonb_build_object('medicamento', new.medicamento, 'establecimiento', new.establecimiento));
  return new;
end $$;

create trigger propuestas_despues_insertar after insert on public.propuestas
  for each row execute function public.propuestas_despues_de_insertar();

create function public.retirar_propuesta(p uuid) returns void
language plpgsql security definer set search_path = public
as $$
declare v public.propuestas;
begin
  select * into v from public.propuestas where id = p for update;
  if not found or v.autora is distinct from auth.uid() or v.estado <> 'en_votacion' or not public.persona_activa() then
    raise exception 'No puedes retirar esta propuesta';
  end if;
  update public.propuestas set estado = 'retirada', resuelta_el = now() where id = p;
  perform public.registrar('retiro', p::text, jsonb_build_object('motivo', 'retirada por la autora'));
end $$;

revoke all on function public.retirar_propuesta(uuid) from public, anon;
grant execute on function public.retirar_propuesta(uuid) to authenticated;

-- Lo que ve la comunidad: sin autora, y solo con sesión de una persona activa.
-- Cuenta únicamente los votos de personas activas (una persona suspendida deja de contar).
create view public.propuestas_comunidad as
select
  p.id,
  p.medicamento,
  p.establecimiento,
  e.nombre as nombre_establecimiento,
  p.texto,
  p.estado,
  p.creada_el,
  (select count(*) from public.votos v join public.personas pe on pe.id = v.persona and pe.estado = 'activa'
     where v.propuesta = p.id and v.a_favor)::int as a_favor,
  (select count(*) from public.votos v join public.personas pe on pe.id = v.persona and pe.estado = 'activa'
     where v.propuesta = p.id and not v.a_favor)::int as en_contra,
  (p.autora = auth.uid()) as es_mia,
  (select v.a_favor from public.votos v where v.propuesta = p.id and v.persona = auth.uid()) as mi_voto
from public.propuestas p
join public.establecimientos e on e.codigo = p.establecimiento
where public.persona_activa() and (p.estado in ('en_votacion', 'en_bandeja') or p.autora = auth.uid());

revoke all on public.propuestas_comunidad from public, anon, authenticated;
grant select on public.propuestas_comunidad to authenticated;

-- Permisos de la tabla: se puede crear y leer lo propio; nada de editar ni borrar desde la app.
revoke all on public.propuestas from anon, authenticated;
grant select, insert on public.propuestas to authenticated;

create policy propuestas_crear on public.propuestas for insert to authenticated
  with check (public.persona_activa());
create policy propuestas_ver_propias on public.propuestas for select to authenticated
  using (autora = auth.uid());
create policy propuestas_ver_admin on public.propuestas for select to authenticated
  using (public.es_admin());
