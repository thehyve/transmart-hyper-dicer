import os

keycloak_config = dict(
    oidc_server_url='{}/auth/realms/{}'.format(os.environ.get('KEYCLOAK_SERVER_URL'), os.environ.get('KEYCLOAK_REALM')),
    client_id=os.environ.get('KEYCLOAK_CLIENT_ID', 'transmart-client'),
    offline_token=os.environ.get('OFFLINE_TOKEN')
)

transmart_config = dict(
    host=os.environ.get('TRANSMART_URL'),
    verify_cert=True,
)

logging_config = dict(
    path=os.environ.get('LOG_CFG', 'dicer/logging.yaml')
)
