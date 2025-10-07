# Solución: Dokploy sin memoria suficiente

## Problema
Dokploy se está reiniciando constantemente con error "Killed" (exit code 137) debido a falta de RAM.

## Causa
El Droplet actual tiene 1GB de RAM, pero Dokploy requiere mínimo 2GB para funcionar correctamente.

---

## OPCIÓN 1: Aumentar RAM del Droplet (RECOMENDADO)

### Pasos en DigitalOcean:

1. **Ve a tu Droplet:**
   - https://cloud.digitalocean.com/droplets

2. **Haz clic en "Resize" (Redimensionar):**
   - Botón en la parte derecha del Droplet

3. **Selecciona plan con 2GB RAM:**
   - Basic plan: $12/mes (2GB RAM, 1 CPU, 50GB SSD)
   - O Premium plan: $18/mes (2GB RAM, 1 CPU Intel)

4. **Marca "CPU and RAM only":**
   - Esto permite reducir después si es necesario
   - No marca "Permanent resize" si quieres poder volver

5. **Haz clic en "Resize Droplet":**
   - Tardará 2-3 minutos
   - El Droplet se reiniciará automáticamente

6. **Espera a que termine:**
   - Estado cambiará de "Resizing" a "Active"

7. **Verifica que Dokploy arranque:**
   ```bash
   # Conéctate nuevamente y verifica
   docker service ls
   docker service logs dokploy --tail 20
   
   # Deberías ver que ya NO dice "Killed"
   ```

8. **Accede a Dokploy:**
   - http://147.182.226.170:3000

### Costo:
- **1GB → 2GB:** +$6/mes
- **Con GitHub Student Pack:** Tienes $200 de crédito (16 meses gratis con plan de 2GB)

---

## OPCIÓN 2: Usar alternativa más ligera (NO RECOMENDADO)

Si NO puedes aumentar RAM, tendrías que:

1. **Desinstalar Dokploy:**
   ```bash
   docker stack rm dokploy
   docker swarm leave --force
   ```

2. **Usar despliegue manual con Docker Compose:**
   ```bash
   cd ~
   git clone https://github.com/AbelMoyaCode/recuiva.git
   cd recuiva
   docker-compose up -d
   ```

3. **Configurar Nginx manualmente** para acceder a la app

**PERO PIERDES:**
- ❌ Interfaz web de gestión
- ❌ Despliegues automáticos desde GitHub
- ❌ SSL automático
- ❌ Logs centralizados
- ❌ Rollbacks fáciles

---

## Recomendación Final

✅ **AUMENTA EL DROPLET A 2GB RAM**

**Razones:**
1. ✅ Tienes $200 de crédito gratis (GitHub Student Pack)
2. ✅ Dokploy vale mucho la pena vs. configuración manual
3. ✅ Es la solución profesional para producción
4. ✅ Puedes reducir después si no lo necesitas

**Tiempo total:** 5 minutos para redimensionar
**Inversión:** $0 (cubierto por créditos)
**Beneficio:** Sistema estable y fácil de gestionar

---

## Siguiente Paso

Una vez que hayas redimensionado el Droplet a 2GB:

1. Espera 2-3 minutos a que reinicie
2. Conéctate a la consola nuevamente
3. Ejecuta: `docker service logs dokploy --tail 20`
4. Deberías ver que arranca correctamente
5. Abre http://147.182.226.170:3000

**¿Necesitas ayuda con el redimensionamiento?** Avísame cuando estés en el panel de DigitalOcean.
