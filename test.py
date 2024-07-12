import logging

import aiomysql
import asyncio

from service.user_login_service import LoginService
print(LoginService.get_password_hash("welcome"))
print(LoginService.verify_password("welcome", b'$2b$12$L2TmBVD0xLmxhnxw.JHI0OA4Wknah74fTXJ1iiDvDXlJp.YkF4v7y'))
