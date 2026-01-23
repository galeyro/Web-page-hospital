from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Usuario

class CustomOIDCBackend(OIDCAuthenticationBackend):
    def filter_users_by_claims(self, claims):
        """Match users by email"""
        email = claims.get('email')
        if not email:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(email=email)

    def verify_claims(self, claims):
        """
        Verify the claims.
        Allow login if email is present.
        We DO NOT check for existing Usuario in DB here anymore, to allow 'register' flow.
        """
        verified = super(CustomOIDCBackend, self).verify_claims(claims)
        email = claims.get('email')
        # Only check if email exists in claims, don't block if Usuario missing
        return verified and email is not None

    def create_user(self, claims):
        """
        Create a standard Django user if needed.
        """
        return super(CustomOIDCBackend, self).create_user(claims)

    def update_user(self, user, claims):
        return super(CustomOIDCBackend, self).update_user(user, claims)

@receiver(user_logged_in)
def sync_custom_session(sender, user, request, **kwargs):
    """
    Signal handler: When OIDC logs in a standard Django user,
    find the corresponding internal 'Usuario' and populate the session.
    """
    print(f"DEBUG: OIDC Login successful for {user.email}, syncing session...")
    try:
        # Find the custom app user by email
        app_user = Usuario.objects.get(email=user.email)
        
        # Populate the session exactly as the manual login does
        request.session['usuario_id'] = app_user.id
        request.session['usuario_nombre'] = app_user.nombres
        request.session['usuario_email'] = app_user.email
        request.session['usuario_rol'] = app_user.rol
        
        print(f"DEBUG: Session synced for Usuario ID {app_user.id} ({app_user.rol})")
        
    except Usuario.DoesNotExist:
        print(f"DEBUG: New SSO user found {user.email} - Auto-creating local user...")
        try:
            # Auto-create the user with default role 'usuario'
            # Note: cedula, telefono, etc. are now optional in models.py
            new_user = Usuario.objects.create(
                nombres=user.first_name or "Usuario",
                apellidos=user.last_name or "Sin Apellido",
                email=user.email,
                rol='usuario',
                password="sso_managed_password", # Not used for SSO
                # Optional fields left empty: cedula, telefono, fecha_nacimiento, genero
            )
            
            # Populate session for the new user
            request.session['usuario_id'] = new_user.id
            request.session['usuario_nombre'] = new_user.nombres
            request.session['usuario_email'] = new_user.email
            request.session['usuario_rol'] = new_user.rol
            
            print(f"DEBUG: Created and synced new user {new_user.email}")
            
        except Exception as e:
            print(f"ERROR: Failed to auto-create user {user.email}: {e}")
