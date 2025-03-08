import token
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


User=get_user_model()

class JWTAuthMiddlewareStack(BaseMiddleware):
    
    async def __call__(self, scope, receive, send):
    
        token = self.get_token_from_scope(scope)
        print(f'token:{token}')
        
                
        if token != None:
            user_id = await self.get_user_from_token(token)
            if user_id:
                scope['user_id']=user_id
                            

            else:
                scope['error'] = 'Invalid token'

        if token == None:
            scope['error'] = 'provide an auth token'    
    
                
        return await super().__call__(scope, receive, send)

    def get_token_from_scope(self, scope):
        query = scope.get('query_string', b'').decode('utf-8')
        token=query.split('token=')[-1] if 'token=' in query else None
        # token=token.split('%')[-1]
        print(token)
        if token :
            return token
        else:
            return None
        
    @database_sync_to_async
    def get_user_from_token(self, token):
            try:
                print('--------')
                access_token = AccessToken(token)
                print(f'access_token: {access_token['user_id']}')
                return access_token['user_id']
            except InvalidToken:
                print("Invalid token")
                return None
            except Exception as e:
                print(f"Error decoding token: {e}")
                return None
