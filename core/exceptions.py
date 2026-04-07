from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    """自定义HTTP异常"""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


# 常见异常定义
def create_not_found_exception(resource: str) -> CustomHTTPException:
    """创建资源未找到异常"""
    return CustomHTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found"
    )


def create_bad_request_exception(detail: str) -> CustomHTTPException:
    """创建请求错误异常"""
    return CustomHTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )


def create_unauthorized_exception() -> CustomHTTPException:
    """创建未授权异常"""
    return CustomHTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_forbidden_exception() -> CustomHTTPException:
    """创建禁止访问异常"""
    return CustomHTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions"
    )


def create_conflict_exception(resource: str) -> CustomHTTPException:
    """创建资源冲突异常"""
    return CustomHTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{resource} already exists"
    )
