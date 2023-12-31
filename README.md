# 智慧团建重置密码验证码批量获取器

如果你是共青团管理员，你就会知道使用智慧团建网站帮一些忘掉自己的网站密码的同学获取“重置密码验证码”是一件多么糟心的事情。虽然网站提供了全局搜索功能，可以轻松地输入身份证号来找到对应的账户，但是搜索结果旁边并没有获取验证码的按钮😅，你还得在左下角的团员列表要死要活地翻，找到目标账户，在点击目标账户旁边的小钥匙按钮，才能显示出来验证码。哦，没有一键复制，你还得选择再按ctrl + C。

所以就应运而生出来了这么个工具。通过该项目，你可以输入一大堆身份证号，就能轻松地获取到每个人的重置密码验证码，十分方便。如果你想，你还可以把它部署在服务器上，直接提供给老师使用。

## 使用教程

0. 下载安装 python *(windows的话在安装时一定要勾选上 Add To Path)*
1. 下载 main.py requirements-gui.txt utils.py 三个文件放到一个空文件夹里面
2. 打开终端（命令提示符），如有必要，请使用 cd 指令(change directory)转到刚刚的空文件夹里面
3. 创建一个虚拟环境，如果你下载安装python只是为了使用这个项目的话，那么你可以跳过此步
4. 使用`pip install -r requirements-gui.txt`指令安装项目所需要的依赖项目
5. 使用管理员账号登入[智慧团建](https://zhtj.youth.cn/zhtj/)，获取账号 Token（可以将其理解为通行令牌），填入main.py文件第8行第一个`""`中
   > 你可能注意到有多个`""`，这意味着你可以同时填入多个管理账号的 Token，对于每一个身份证号，程序会先使用填入的第一个Token搜索身份证号对应的账户，当收到`只能查询本级及下级团组织团员`响应时，会自动切换到下一个Token重新搜索。
7. 运行`streamlit run main.py`，此时会自动打开一个浏览器窗口，你就可以在其中执行批量获取重置密码验证码的操作了（默认密码是`ikun`）
8. 如有各种疑问，欢迎来[这里](https://github.com/jexjws/Zhtj-IDNumber-PasswordResetVerificationCode/issues)点击`New Issue`提问。
