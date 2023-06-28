import requests
import time
import re
import streamlit as st

password = 'ikun'

tokens = [
    "",
    "",
    "",
    "",
]


def zhtjGet(headers, url, data) -> requests.models.Response:
    req = None
    for _ in range(3):
        try:
            req = requests.post(
                url=url,
                data=data,
                headers=headers,
                timeout=10
            )
            break
        except requests.exceptions.RequestException:
            pass
    if req is not None:
        return req
    else:
        raise requests.exceptions.RequestException


def gogo(i: str) -> dict[str, str]:
    """
    ok
    cookieError
    """
    SFZnumber = i
    req = None
    headers = None
    status = 0
    for idx, token in enumerate(tokens):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Cookie": token,
        }
        req = zhtjGet(
            url="https://zhtj.youth.cn/v1/center/fullSearchUser",
            data={"identityCardNo": SFZnumber},
            headers=headers
        )
        print(req.text)

        if req.text == "您的登录已超时，请重新登录":
            return {'status': 'cookieError', 'data': '您的登录已超时，请重新登录'}
        if req.json()["retCode"] == 1009:
            return {'status': 'cookieError', 'data': req.json()["retMsg"]}

        if req.json()["retMsg"] == "只能查询本级及下级团组织团员":
            print(f"{idx} 号cookie无权限,开始切换到下一个cookie.")
        elif req.json()["retCode"] == 1001:
            status = "成员错误"
            break
        else:
            status = "OK"
            break
        time.sleep(0)

    if req is None:
        raise EOFError

    if status == "成员错误" or status == 0:
        return {'status': 'ok', 'data': (SFZnumber + "：" + req.json()["retMsg"] + "\n")}

    uid = req.json()["results"]["userList"][0]["userId"]
    leagueId = req.json()["results"]["userList"][0]["leagueId"]
    if len(req.json()["results"]["userList"]) > 1:
        raise EOFError

    print("获取到的UID：" + uid)
    print("获取到的leagueId：" + leagueId)

    result = zhtjGet(
        url="https://zhtj.youth.cn/v1/center/tuanyuan/logincode",
        data={"userId": uid, "leagueId": leagueId},
        headers=headers,
    ).json()["results"]

    return {
        'status': 'ok',
        'data': f"{result.get('name')}：{result.get('loginCode')}\n"
    }


# st.session_state

st.title('智慧团建验证码批量获取器')
st.write(
    "欢迎使用验证码批量获取器（beta version），本工具为团管理员量身定做。使用本工具，可以轻松获取重置密码验证码，省时省心。")


def showPasswordInputPanel():
    st.text_input("使用密码：", key="password", placeholder="", autocomplete="etfcsdxx")
    st.button("验证", use_container_width=True, type="primary")


if 'password' in st.session_state:
    if st.session_state['password'] != password:
        showPasswordInputPanel()
        st.error('密码错误')
        exit()
else:
    showPasswordInputPanel()
    exit()

inputBox = st.text_area("在此处粘贴包含待获取验证码的身份证号的文段：", key="input", placeholder="点击按钮开始处理")

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
    state = {'status': 'ok'}

    for i in range(len(identity)):
        identityWidget.text(f'正在处理第 {i + 1} 个  共 {len(identity)} 个')
        g = gogo(identity[i])

        if not g['status'] == 'ok':
            state = g
            break
        output += g['data']
        time.sleep(0.2)
        outputArea.code(output, language=None)

    if state["status"] == 'ok':
        identityWidget.success("完毕", icon='✅')
    elif state["status"] == 'cookieError':
        output += state["data"]
        outputArea.code(output, language=None)
        identityWidget.error('有登陆凭据已过期。请联系工具维护者更新登陆凭据。', icon="🚨")
    else:
        identityWidget.error('出现未知错误：' + state['data'], icon="❌")
