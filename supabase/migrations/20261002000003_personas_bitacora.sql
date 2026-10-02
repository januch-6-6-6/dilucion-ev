-- Etapa 1 — Task 3: administrador, personas activas, historial de hospital y bitácora inmutable.

-- ===== Funciones de identidad =====
create function public.es_admin() returns boolean
language sql security definer stable set search_path = public
as $$ select exists (select 1 from public.administradores where persona = auth.uid()) $$;

create function public.persona_activa() returns boolean
language sql security definer stable set search_path = public
as $$ select exists (select 1 from public.personas where id = auth.uid() and estado = 'activa') $$;

revoke all on function public.es_admin() from public, anon;
revoke all on function public.persona_activa() from public, anon;
grant execute on function public.es_admin() to authenticated;
grant execute on function public.persona_activa() to authenticated;

-- ===== Bitácora: solo se agregan filas =====
create function public.registrar(accion text, objeto text, detalle jsonb default '{}'::jsonb) returns void
language sql security definer set search_path = public
as $$ insert into public.bitacora (actor, accion, objeto, detalle) values (auth.uid(), accion, objeto, coalesce(detalle, '{}'::jsonb)) $$;

-- Solo la usan los disparadores y funciones del servidor, nunca la app directamente.
revoke all on function public.registrar(text, text, jsonb) from public, anon, authenticated;

create function public.bitacora_inmutable() returns trigger
language plpgsql set search_path = public
as $$ begin raise exception 'La bitácora no se puede modificar'; end $$;

create trigger bitacora_no_modificar before update or delete on public.bitacora
  for each row execute function public.bitacora_inmutable();
create trigger bitacora_no_vaciar before truncate on public.bitacora
  for each statement execute function public.bitacora_inmutable();

-- Desde la app solo se lee (y solo el administrador, ver políticas abajo).
revoke all on public.bitacora from anon, authenticated;
grant select on public.bitacora to authenticated;

-- ===== Historial de cambios de hospital =====
create function public.personas_historial() returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  desde text := coalesce(old.establecimiento, case when old.pais_extranjero is not null then 'extranjero: ' || old.pais_extranjero end);
  hacia text := coalesce(new.establecimiento, case when new.pais_extranjero is not null then 'extranjero: ' || new.pais_extranjero end, 'sin definir');
begin
  insert into public.historial_hospital (persona, desde, hacia) values (new.id, desde, hacia);
  perform public.registrar('cambio_hospital', new.id::text, jsonb_build_object('desde', desde, 'hacia', hacia));
  return new;
end $$;

create trigger personas_cambio_hospital after update of establecimiento, pais_extranjero on public.personas
  for each row
  when (old.establecimiento is distinct from new.establecimiento or old.pais_extranjero is distinct from new.pais_extranjero)
  execute function public.personas_historial();

-- ===== Permisos =====
-- Una persona solo puede cambiar su hospital o su país; el resto de las columnas no se toca desde la app.
revoke update on public.personas from anon, authenticated;
grant update (establecimiento, pais_extranjero) on public.personas to authenticated;

create policy personas_ver on public.personas for select to authenticated
  using (id = auth.uid() or public.es_admin());
create policy personas_cambiar_hospital on public.personas for update to authenticated
  using (id = auth.uid() and public.persona_activa())
  with check (id = auth.uid());

create policy historial_ver on public.historial_hospital for select to authenticated
  using (persona = auth.uid() or public.es_admin());

create policy administradores_ver on public.administradores for select to authenticated
  using (public.es_admin());

create policy bitacora_ver on public.bitacora for select to authenticated
  using (public.es_admin());

-- Catálogos: los lee cualquiera.
create policy establecimientos_ver on public.establecimientos for select to anon, authenticated using (true);
create policy medicamentos_ver on public.medicamentos for select to anon, authenticated using (true);
