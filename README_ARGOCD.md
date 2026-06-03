# 🚀 Guía de Despliegue y Gestión con ArgoCD y Minikube

Este documento explica de forma clara cómo levantar, detener y reanudar el proyecto **Alfa Hospital** en tu entorno local de Kubernetes (Minikube) utilizando ArgoCD.

---

## 🛠️ Requisitos Previos
Asegúrate de tener instalado:
* [Minikube](https://minikube.sigs.k8s.io/docs/start/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/)
* [git](https://git-scm.com/)

---

## 🏁 Paso 1: Configurar Minikube
Debes asegurarte de tener habilitado el controlador de Ingress en Minikube:
```bash
minikube addons enable ingress
```

---

## 🏗️ Paso 2: Compilar y Cargar la Imagen Docker

### Opción A: Comandos para Windows (PowerShell)
1. **Compilar la imagen localmente**:
   ```powershell
   docker build -t web-page-hospital:v2 .
   ```
2. **Exportar y cargar la imagen en Minikube** (evita conflictos de caché y contextos):
   ```powershell
   docker save web-page-hospital:v2 -o web-page-hospital.tar
   minikube image load web-page-hospital.tar
   Remove-Item web-page-hospital.tar
   ```

### Opción B: Comandos para macOS / Linux (Terminal / Bash / Zsh)
1. **Compilar la imagen localmente**:
   ```bash
   docker build -t web-page-hospital:v2 .
   ```
2. **Exportar y cargar la imagen en Minikube**:
   ```bash
   docker save web-page-hospital:v2 -o web-page-hospital.tar
   minikube image load web-page-hospital.tar
   rm web-page-hospital.tar
   ```

---

## 📡 Paso 3: Subir Cambios y Crear la App en ArgoCD

1. **Subir los cambios a tu rama en GitHub** (ArgoCD necesita leerlos del repositorio remoto):
   ```bash
   git add .
   git commit -m "feat: setup kubernetes and argocd deployment"
   git push
   ```
2. **Aplicar el archivo de ArgoCD** (asegúrate de tener tu servidor ArgoCD corriendo y el port-forward activo):
   ```bash
   kubectl apply -f argocd-app.yaml
   ```
3. Abre tu panel de ArgoCD (`https://localhost:8080`) y haz clic en **Refresh** dentro de la app `hospital` si es necesario para acelerar la sincronización.

---

## 🔌 Paso 4: Acceder a la Aplicación
Para poder ingresar, levanta un canal de comunicación directo al servicio de Kubernetes:
```bash
kubectl port-forward -n hospital svc/hospital-service 9000:80
```
Abre en tu navegador: [http://localhost:9000/](http://localhost:9000/)  
*(Credenciales: `admin@admin.com` / `admin`)*

---
---

## 💤 Cómo Apagar el Proyecto (Al finalizar tu día)
Si vas a apagar tu computadora o quieres liberar recursos de memoria/CPU, tienes dos formas de detener el proyecto:

### Opción 1: Apagar Minikube por completo (Recomendado)
Esto guardará el estado de todo tu clúster (incluyendo la base de datos persistente) y detendrá la máquina virtual de Minikube. **No se perderá ningún dato**.
```bash
minikube stop
```
*(Puedes cerrar Docker Desktop después de esto).*

### Opción 2: Pausar el Pod sin apagar Minikube
Si vas a seguir usando Minikube para otros proyectos pero quieres liberar la memoria del hospital, puedes escalar el despliegue a `0` réplicas:
```bash
kubectl scale deployment -n hospital hospital-deployment --replicas=0
```
> ⚠️ **Nota Importante:** Debido a que ArgoCD tiene activa la opción de *Self-Healing*, es posible que al detectar que cambiaste las réplicas manualmente a `0` intente restaurar el Pod a `1`. Para evitar esto de manera temporal, puedes desactivar la auto-sincronización desde la UI de ArgoCD antes de escalar, o simplemente usar la **Opción 1** (apagar Minikube), que es más limpia y directa.

---

## ☀️ Cómo Volver a Encender el Proyecto (Otro día)

Cuando vuelvas a trabajar, el flujo para tener todo corriendo es sumamente rápido:

### 1. Iniciar Minikube
```bash
minikube start
```
*(Espera un minuto a que todos los componentes internos inicien. ArgoCD y el hospital se encenderán solos automáticamente recuperando su estado previo).*

### 2. Levantar el Port-Forward de ArgoCD (Si necesitas entrar al panel)
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### 3. Levantar el Port-Forward del Hospital
```bash
kubectl port-forward -n hospital svc/hospital-service 9000:80
```
¡Listo! Entra a [http://localhost:9000/](http://localhost:9000/) y la aplicación estará funcionando con los mismos datos que guardaste el día anterior.
