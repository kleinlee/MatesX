from fastapi import APIRouter, HTTPException, Body, Depends, Query, status, Form
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
import utils.sqlite_manager as sqlite_manager
import sqlite3
from utils.session_manager import user_session_cache  # 导入全局会话管理器
import httpx
import asyncio
from fastapi import HTTPException, BackgroundTasks

from utils.dashscope import MatesX_key

auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/update_role")
async def update_role(data: dict = Body(...)):
    print("update_role", data)
    try:
        # 参数校验
        avatar_id = data.get("avatar_id")
        unionid = data.get("unionid")
        avatar_name = data.get("avatar_name")
        cosyvoice_id = data.get("cosyvoice_id")
        system_prompt = data.get("system_prompt")

        if not unionid or not avatar_id:
            raise HTTPException(status_code=400, detail="Missing required parameters")

        sqlite_manager.insert_or_update_table(
            table_name="roles",
            avatar_id=avatar_id,
            unionid=unionid,
            avatar_name=avatar_name,
            cosyvoice_id=cosyvoice_id,
            system_prompt=system_prompt
        )

        # 删除对应的会话缓存
        if unionid in user_session_cache:
            sessions = user_session_cache[unionid]
            if avatar_id in sessions:
                del sessions[avatar_id]

        return {
            "code": 0
        }

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.post("/apply_new_role")
async def apply_new_role(data: dict = Body(...)):
    print("apply_new_role", data)
    try:
        # 参数校验
        unionid = data.get("unionid")
        avatar_name = data.get("avatar_name")  # 注意这里改为接收前端字段名

        if not unionid or not avatar_name:
            raise HTTPException(status_code=400, detail="Missing required parameters")

        # 查询当前形象余额
        user = sqlite_manager.get_user_by_unionid(unionid)
        avatar_balance = user.get("avatar_balance")
        if avatar_balance < 1:
            return {
                "code": 1002,
                "message": "已无足够形象创建额度",
                "data": {
                    "unionid": unionid,
                    "avatar_balance": avatar_balance,
                    "check_status": ""
                }
            }

        # 查询现有角色
        roles = sqlite_manager.get_roles_by_unionid(unionid)

        # 检查 pending 状态
        if any(role.get("status") == "pending" for role in roles):
            return {"code": 1001, "message": "您已有任务正在排队，请等待完成后请再申请", "data": {"unionid": unionid}}

        # 生成新 avatar_id
        import uuid
        avatar_id = str(uuid.uuid4())

        return {
            "code": 0,
            "message": "申请已提交",
            "data": {
                "unionid": unionid,
                "avatar_id": avatar_id,
                "avatar_balance": avatar_balance,
                "check_status": "pending"
            }
        }

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.post("/handle_new_role2")
async def handle_new_role2(
        unionid: str = Form(...),
        avatar_id: str = Form(...),
        avatar_name: str = Form(...),
        matting: bool = Form(False),
        keepsize: bool = Form(False),
        reverse: bool = Form(False),
        file: UploadFile = File(...)
):
    print("handle_new_role2", {
        "unionid": unionid,
        "avatar_id": avatar_id,
        "avatar_name": avatar_name,
        "matting": matting,
        "keepsize": keepsize,
        "reverse": reverse,
        "filename": file.filename
    })
    try:
        if not unionid or not avatar_id or not avatar_name:
            raise HTTPException(status_code=400, detail="缺少必要参数")
        
        avatar_url = ""
        
        # 插入新记录
        sqlite_manager.insert_or_update_table(
            table_name="roles",
            avatar_id=avatar_id,
            unionid=unionid,
            status="pending",
            cosyvoice_id="longhua",
            avatar_name=avatar_name,
            avatar_url=avatar_url,
            version=1
        )

        # 1. 构建OSS URL并上传文件
        file_ext = os.path.splitext(file.filename.lower())[1]
        
        # 构建完整的OSS路径
        final_task_id = avatar_id
        if matting:
            final_task_id += "__alpha"
        if keepsize:
            final_task_id += "__keepsize"
        if not reverse:
            final_task_id += "__noreverse"
        final_task_id += "__api"
        
        oss_url = f"https://matesx.oss-cn-beijing.aliyuncs.com/avatar/tasks/{final_task_id}{file_ext}"
        
        try:
            # 读取文件内容
            file_content = await file.read()
            
            # 上传文件到OSS
            async with httpx.AsyncClient(timeout=300.0) as client:
                oss_response = await client.put(
                    oss_url,
                    content=file_content,
                    headers={
                        'Content-Type': file.content_type or 'application/octet-stream'
                    }
                )
                
                if oss_response.status_code != 200:
                    raise Exception(f"OSS上传失败，状态码: {oss_response.status_code}")
                    
        except Exception as oss_error:
            print(f"OSS上传异常: {str(oss_error)}")
            sqlite_manager.insert_or_update_table(
                table_name="roles",
                avatar_id=avatar_id,
                unionid=unionid,
                status="failed",
                avatar_name=avatar_name,
                avatar_url=avatar_url,
                errorMessage=f"OSS上传异常: {str(oss_error)}"
            )
            raise HTTPException(status_code=500, detail=f"OSS上传异常: {str(oss_error)}")

        # 2. 调用上传接口（传入oss_url）
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                data = {
                    "key": MatesX_key,
                    "oss_url": oss_url,
                    "task_id": avatar_id,
                    "callback_url": ""  # 如果需要回调，可以在这里设置
                }

                upload_response = await client.post(
                    "https://www.matesx.com/platform/api/upload",
                    data=data
                )

                upload_response.raise_for_status()

                result = upload_response.json()
                if result.get("code") != 0:
                    raise Exception(f"上传接口返回错误: {result.get('message', '未知错误')}")

        except Exception as upload_error:
            print(f"上传接口调用异常: {str(upload_error)}")
            sqlite_manager.insert_or_update_table(
                table_name="roles",
                avatar_id=avatar_id,
                unionid=unionid,
                status="failed",
                avatar_name=avatar_name,
                avatar_url=avatar_url,
                errorMessage=f"上传接口调用异常: {str(upload_error)}"
            )
            raise HTTPException(status_code=500, detail=f"上传处理异常: {str(upload_error)}")

        # 启动后台任务进行轮询
        asyncio.create_task(poll_task_status(avatar_id, unionid, avatar_name))
        return {
            "code": 0,
            "message": "操作成功",
            "data": {
                "avatar_id": avatar_id,
                "new_status": "processing"
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"处理新角色异常: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def poll_task_status(avatar_id: str, unionid: str, avatar_name: str):
    """
    轮询任务状态的后台任务
    """
    max_retries = 60  # 最大重试次数（20秒*60=20分钟）
    retry_count = 0
    poll_interval = 20  # 20秒轮询一次

    while retry_count < max_retries:
        try:
            # 等待20秒
            await asyncio.sleep(poll_interval)

            async with httpx.AsyncClient(timeout=30.0) as client:
                # 查询任务状态
                response = await client.get(f"https://www.matesx.cn/api/task/{avatar_id}")
                response.raise_for_status()

                task_data = response.json()
                print(f"轮询任务状态 {avatar_id}: {task_data}")

                # 根据任务状态更新数据库
                task_status = task_data.get("status", "")
                avatar_url = task_data.get("avatar_url", "")
                video_url = task_data.get("video_url", "")
                video_asset_url = task_data.get("video_asset_url", "")
                errorMessage = task_data.get("errorMessage", "")

                # 如果任务完成或失败，结束轮询
                if task_status in ["success", "failed"]:
                    # 更新角色状态
                    sqlite_manager.insert_or_update_table(
                        table_name="roles",
                        avatar_id=avatar_id,
                        status=task_status,
                        avatar_url=avatar_url,
                        video_url=video_url,
                        video_asset_url=video_asset_url,
                        errorMessage=errorMessage
                    )
                    print(f"任务 {avatar_id} 完成，最终状态: {task_status}")
                    break

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"任务 {avatar_id} 尚未就绪，继续轮询...")
            else:
                print(f"查询任务状态HTTP错误: {str(e)}")
        except Exception as e:
            print(f"轮询任务状态异常: {str(e)}")

        retry_count += 1

    if retry_count >= max_retries:
        print(f"任务 {avatar_id} 轮询超时，更新为超时状态")
        # 更新为超时状态
        sqlite_manager.insert_or_update_table(
            table_name="roles",
            avatar_id=avatar_id,
            status="failed",
            errorMessage=f"任务 {avatar_id} 轮询超时，更新为超时状态"
        )

@auth_router.post("/remove_role")
async def remove_role(data: dict = Body(...)):
    print("remove_role", data)
    try:
        # 参数校验
        unionid = data.get("unionid")
        avatar_id = data.get("avatar_id")

        if not unionid or not avatar_id:
            raise HTTPException(status_code=400, detail="缺少必要参数")

        success = sqlite_manager.remove_role_from_roles(
            unionid=unionid,
            avatar_id=avatar_id
        )

        if not success:
            raise HTTPException(
                status_code=404,
                detail={"code": 404, "message": "未找到指定的角色或角色不属于该用户"}
            )

        return {
            "code": 0,
            "message": "角色删除成功",
            "data": {
                "avatar_id": avatar_id
            }
        }

    except HTTPException:
        raise  # 直接抛出已有的HTTPException
    except Exception as e:
        print(f"删除角色失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": "服务器内部错误"}
        )


@auth_router.post("/check_role_status")
async def check_role_status(data: dict = Body(...)):
    print("check_role_status", data)
    try:
        # 参数校验
        unionid = data.get("unionid")
        avatar_id = data.get("avatar_id")

        if not unionid or not avatar_id:
            raise HTTPException(status_code=400, detail="缺少必要参数")

        # 查询现有角色
        role = sqlite_manager.get_role_by_avatar_id(avatar_id)
        if role:
            role.pop('key', None)
            return role
        else:
            return {}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
