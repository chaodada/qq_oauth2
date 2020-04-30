import requests
import re
# 计算发送说说的防御CSRF的Token
def getACSRFToken(p_skey):
    hash_v = 5381
    if p_skey:
        for i in range(len(p_skey)):
            hash_v += (hash_v << 5) + ord(p_skey[i])
        return hash_v & 2147483647
    return None
# 想要发送的说说



Message = "接口创建说说"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
    "Referer": "https://i.qq.com/"
}


# 从QQ服务器获取请求本地服务器的Cookie
get_local_token_url = "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html&pt_no_auth=1"



# Header头Referer字段必须为qq.com
login_session = requests.Session()
res = login_session.get(get_local_token_url, headers=header)

# 获取关键参数pt_local_token
pt_local_token = res.cookies.get("pt_local_token")
# 带着刚才的Cookie以及从Cookie中拿到的pt_local_tk对本地服务器进行请求

print(pt_local_token)


# # 获取已登录的账号信息
port = 4301
local_qq_server_url = "https://localhost.ptlogin2.qq.com"  # 建立在本地的QQ服务器地址，等待应用与其交互
# # 传参获取本地已登录账号信息
get_QQ_num_url = local_qq_server_url +  ":{}/pt_get_uins?callback=ptui_getuins_CB&r=0.7068102287925351&pt_local_tk={}".format(port, pt_local_token)

print(get_QQ_num_url)
header={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
    "Referer": "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=https%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=https%3A//z.qzone.com/download.html&pt_no_auth=0"
}
res = login_session.get(get_QQ_num_url, headers=header)




# # 返回的账号信息是一段js的数组
dic_str = None
try:
    dic_str = re.findall("var var_sso_uin_list=(\[[\s\S]*?\])", res.text)[0]
except IndexError:
    print("Fail to get local account info. ")
    exit(0)

print(dic_str)
# # ====================================== 显示本地登录账号信息 ===========================================
account_list = eval(dic_str)
print("Detect {} account login locally".format(len(account_list)))

print("=====================================================")
account_num_list = []
for i in range(len(account_list)):
    print("NO.{}".format(i + 1))
    print("account:{}\nnickname:{}".format(account_list[i].get("account"), account_list[i].get("nickname")))
    account_num_list.append(account_list[i].get("account"))
print("=====================================================")
# # # ====================================== 对每个账号进行快捷登录 ===========================================
# # # ===================================== 以登录QQ空间发个说说为例 ==========================================
# # # 对于已登录的账号
for account in account_num_list:
    # 发送QQ号码及pt_local_token参数到本地服务器获取必要的Cookie，以便获取远程服务器登录许可
    get_QQ_cookie_url = local_qq_server_url + \
                        ":{}/pt_get_st?callback=ptui_getst_CB&" \
                        "r=0.7068102287925351&" \
                        "pt_local_tk={}&" \
                        "clientuin={}".format(port,
                                              pt_local_token,
                                              account)
                                              
    print("========================get_QQ_cookie_url=============================\n\n")
    print(get_QQ_cookie_url)
    print("\n\n========================get_QQ_cookie_url=============================")

    res = login_session.get(get_QQ_cookie_url, headers=header)
    # 获取远程登录凭证
    # 其中u1为QQ空间地址（抓包可获得）
    login_url = "https://ssl.ptlogin2.qq.com/jump?clientuin={}&" \
                "keyindex=19&" \
                "pt_aid=549000912&" \
                "daid=5&" \
                "u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&" \
                "pt_local_tk={}&" \
                "pt_3rd_aid=0&" \
                "ptopt=1&style=40".format(account, pt_local_token)

    print("=========================login_url============================\n\n")
    print(login_url)
    print("\n\n=========================login_url============================")

    # 按照抓包获得的请求照样地设置了一下Referer 免得有检测
    login_session.headers['Referer'] = get_local_token_url
    res = login_session.get(login_url)
    clientkey=res.cookies.get("clientkey")
    print(clientkey)

    print(res.text)
    # 至此获取凭证(clientkey)成功,下面获取p_skey
    # 到此处会有个check操作，需要GET去请求验证一下上一个请求响应内容给的地址
    # ============================================ 获取p_skey ===================================================
    zone_login_check_url = None
    try:
        # 获取认证地址及参数
        zone_login_check_url = re.findall("'(http.*?)'", res.text)[0]
    except IndexError:
        print('Fail to get login token .')
        exit(0)
    # 发起认证请求
    print("******")
    print(zone_login_check_url)



    res = login_session.get(zone_login_check_url)
    # 一样的补一下Referer和UA
    login_session.headers['Referer'] = "https://qzs.qzone.qq.com/qzone/v5/loginsucc.html?para=izone"
    login_session.headers[
        'User-Agent'] =    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"

    # 请求对应账号的空间，获取发送说说必要参数——qzone_token(响应的JS里面获取)以及p_skey(cookie中获取)
    res = login_session.get("https://user.qzone.qq.com/{}".format(account))
    # 获取必要参数p_skey用来计算CSRFToken
    p_skey = login_session.cookies.get("p_skey")
    print("=========================p_skey============================\n\n")
    print(p_skey)
    print("\n\n=========================p_skey============================")


    g_tk = getACSRFToken(p_skey) # 计算CSRFToken
    print("=========================g_tk============================\n\n")
    print(g_tk)
    print("\n\n=========================g_tk============================")

    # 从响应的页面JS中获取qzone_token
    res.encoding = 'utf-8'
    qzone_token = re.findall('window.g_qzonetoken = \(function\(\){ try\{return "([0-9a-fA-F]+?)";\}', res.text)[0]
    # 发送说说的地址（抓包可得），并传入刚才获取的qzone_token以及g_tk
    post_comment_url = "https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6?" \
                       "qzonetoken={}&g_tk={}".format(qzone_token, g_tk)
    # 补一下Content-Type
    login_session.headers["Content-Type"] = "application/x-www-form-urlencoded"
    # 发送说说的必要参数（抓包可得），其中con字段及说说内容
    param = {"syn_tweet_verson": "1", "paramstr": "1", "pic_template": "", "richtype": "", "richval": "",
             "special_url": "", "subrichtype": "", "who": "1", "con": Message, "feedversion": "1",
             "ver": "1", "ugc_right": "1", "to_sign": "0", "hostuin": "2167162990", "code_version": "1", "format": "fs",
             "qzreferrer": "https%3A%2F%2Fuser.qzone.qq.com%2F2167162990"}
    # 发送说说
    res = login_session.post(post_comment_url, data=param)
    if res.status_code == 200:
        print("[+] Account {} send message successfully.".format(account))
    # ================================================= 获取好友列表 =====================================================
    # 接口地址
    # get_friends_url = "https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_show_qqfriends.cgi?" \
    #                   "uin={}&follow_flag=1&" \
    #                   "groupface_flag=0&fupdate=1&" \
    #                   "g_tk={}".format(account, g_tk)
    # res = login_session.get(get_friends_url)
    # print("QQ friends info.")
    # print(res.text)