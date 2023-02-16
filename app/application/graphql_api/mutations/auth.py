import strawberry
from gqlauth.user import relay
from strawberry_django_plus import gql
from strawberry_django_plus.permissions import IsAuthenticated


@strawberry.type
class AuthMutation:
    update_account = relay.UpdateAccount.field
    archive_account = relay.ArchiveAccount.field
    delete_account = relay.DeleteAccount.field
    password_change = relay.PasswordChange.field


@strawberry.type
class LoginMutation:
    @gql.django.field(directives=[IsAuthenticated])
    def auth_entry(self) -> AuthMutation:
        return AuthMutation()

    token_auth = relay.ObtainJSONWebToken.field
    register = relay.Register.field
    verify_token = relay.VerifyToken.field
    resend_activation_email = relay.ResendActivationEmail.field
    send_password_reset_email = relay.SendPasswordResetEmail.field
    password_reset = relay.PasswordReset.field
    password_set = relay.PasswordSet.field
    refresh_token = relay.RefreshToken.field
    revoke_token = relay.RevokeToken.field
    verify_account = relay.VerifyAccount.field
