import time
import re
import streamlit as st
import utils
from types import *

password = 'ikun'
tokens = [""] * 4


def handler(id_: str) -> dict[str, str]:
    req = None
    status = False
    for idx_, token in enumerate(tokens):
        req = utils.post("fullSearchUser", token, {"identityCardNo": id_})
        print(req.text)

        if req.text == "您的登录已超时，请重新登录":
            return {'status': StatusCookieError, 'data': '您的登录已超时，请重新登录'}
        if req.json()["retCode"] == 1009:
            return {'status': StatusCookieError, 'data': req.json()["retMsg"]}

        if req.json()["retMsg"] == "只能查询本级及下级团组织团员":
            print(f"{idx_} 号cookie无权限,开始切换到下一个cookie.")
        elif req.json()["retCode"] == 1001:
            status = False
        else:
            status = True

    if req is None:
        raise EOFError

    if not status:
        return {
            'status': StatusCookieOK,
            'data': f"{id_}: {req.json()['retMsg']}\n",
        }

    result = req.json()["results"]["userList"]

    uid = result[0]["userId"]
    leagueId = result[0]["leagueId"]
    if len(result["userList"]) > 1:
        raise EOFError

    print("获取到的UID:", uid)
    print("获取到的leagueId:", leagueId)

    result = utils.post("tuanyuan/logincode", tokens[-1], {"userId": uid, "leagueId": leagueId}).json()["results"]

    return {
        'status': StatusCookieOK,
        'data': f"{result.http('name')}: {result.http('loginCode')}\n",
    }


def showPasswordInputPanel():
    st.text_input("使用密码: ", key="password", placeholder="", autocomplete="etfcsdxx")
    st.button("验证", use_container_width=True, type="primary")


if __name__ == "__main__":
    st.title('智慧团建验证码批量获取器')
    st.write(
        "欢迎使用验证码批量获取器（beta version），本工具为团管理员量身定做。使用本工具，可以轻松获取重置密码验证码，省时省心。")

    if 'password' in st.session_state:
        if st.session_state['password'] != password:
            showPasswordInputPanel()
            st.error('密码错误')
            exit()
        else:
            st.session_state['password'] = password
    else:
        showPasswordInputPanel()
        exit()

    inputBox = st.text_area("在此处粘贴包含待获取验证码的身份证号的文段: ", key="input", placeholder="点击按钮开始处理")

    st.button("开始处理", type="primary", key="wtf", use_container_width=True)

    if not st.session_state['wtf']:
        exit()

    identity = re.findall(r"\d{18}|\d{17}[X|x]|\d{17}", inputBox, flags=0)
    if not len(identity):
        st.warning("没有在你输入的文字中找到任何身份证号", icon="⚠️")
        exit()

    with st.spinner("正在获取验证码"):
        output = ''
        outputArea = st.empty()
        identityWidget = st.empty()
        time.sleep(2)
        state = {'status': StatusCookieOK}

        for idx, obj in enumerate(identity):
            identityWidget.text(f'正在处理第 {idx + 1} 个  共 {len(identity)} 个')
            res = handler(obj)

            if not res['status'] == StatusCookieOK:
                state = res
                break
            output += res['data']
            time.sleep(0.2)
            outputArea.code(output, language=None)

        if state["status"] == StatusCookieOK:
            identityWidget.success("完毕", icon='✅')
        elif state["status"] == StatusCookieError:
            output += state["data"]
            outputArea.code(output, language=None)
            identityWidget.error('有登陆凭据已过期。请联系工具维护者更新登陆凭据。', icon="🚨")
        else:
            identityWidget.error('出现未知错误: ' + state['data'], icon="❌")
